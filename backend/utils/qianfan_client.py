# -*- coding: utf-8 -*-
"""
百度千帆平台 API 客户端
封装所有 API 调用逻辑
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional, Any, Generator
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class QianfanMessage:
    """千帆消息格式"""
    role: str
    content: str
    name: Optional[str] = None


@dataclass
class QianfanResponse:
    """千帆响应格式"""
    success: bool
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str
    raw_response: Dict


class QianfanClient:
    """
    百度千帆平台 API 客户端
    
    支持功能：
    - 聊天补全
    - 流式响应
    - 多模型切换
    - 自动重试
    """
    
    # 可用模型
    MODELS = {
        "glm-5.1": {"name": "智谱 GLM-5.1", "context": 128000},
        "qwen3.5-397b-a17b": {"name": "阿里 Qwen3.5-397B", "context": 32000},
        "deepseek-v3.2": {"name": "DeepSeek-V3.2", "context": 128000}
    }
    
    DEFAULT_MODEL = "glm-5.1"
    
    def __init__(
        self,
        api_key: str = None,
        api_url: str = None,
        model: str = None,
        timeout: int = 600,  # 10分钟超时
        max_retries: int = 3
    ):
        """初始化客户端
        
        Args:
            api_key: 千帆 API Key（如未提供则从环境变量读取）
            api_url: API URL（如未提供则使用默认值）
            model: 默认模型
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        # 从环境变量读取 API Key
        env_api_key = os.getenv("QIANFAN_API_KEY", "")
        env_api_url = os.getenv("QIANFAN_API_URL", "https://qianfan.baidubce.com/v2/chat/completions")
        
        self.api_key = api_key or env_api_key
        self.api_url = api_url or env_api_url
        self.model = model or self.DEFAULT_MODEL
        self.timeout = timeout
        self.max_retries = max_retries
        
        if not self.api_key:
            raise ValueError("QIANFAN_API_KEY not found. Please set it in environment variables or pass it as argument.")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 100000,  # 增加到100000
        stream: bool = False,
        **kwargs
    ) -> QianfanResponse:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否流式响应
            **kwargs: 其他参数
        
        Returns:
            QianfanResponse: 响应对象
        """
        model = model or self.model
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 重试机制
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=self.timeout,
                    stream=stream
                )
                response.raise_for_status()
                
                if stream:
                    return self._handle_stream_response(response, model)
                else:
                    return self._parse_response(response.json(), model)
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    return QianfanResponse(
                        success=False,
                        content=f"API 调用失败: {str(e)}",
                        model=model,
                        usage={},
                        finish_reason="error",
                        raw_response={"error": str(e)}
                    )
                time.sleep(1)
        
        return QianfanResponse(
            success=False,
            content="超过最大重试次数",
            model=model,
            usage={},
            finish_reason="error",
            raw_response={}
        )
    
    def _parse_response(self, response: Dict, model: str) -> QianfanResponse:
        """解析响应"""
        try:
            choices = response.get("choices", [])
            if not choices:
                return QianfanResponse(
                    success=False,
                    content="响应中没有内容",
                    model=model,
                    usage=response.get("usage", {}),
                    finish_reason="empty",
                    raw_response=response
                )
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            finish_reason = choices[0].get("finish_reason", "unknown")
            
            return QianfanResponse(
                success=True,
                content=content,
                model=model,
                usage=response.get("usage", {}),
                finish_reason=finish_reason,
                raw_response=response
            )
        
        except Exception as e:
            logger.error(f"解析响应失败: {e}")
            return QianfanResponse(
                success=False,
                content=f"解析响应失败: {str(e)}",
                model=model,
                usage={},
                finish_reason="parse_error",
                raw_response=response
            )
    
    def _handle_stream_response(self, response, model: str) -> Generator:
        """处理流式响应"""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8').replace('data: ', ''))
                    if 'choices' in data and data['choices']:
                        delta = data['choices'][0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            yield content
                except:
                    continue
    
    def generate(self, prompt: str, model: str = None, temperature: float = None, max_tokens: int = None) -> QianfanResponse:
        """
        便捷方法：将单个 prompt 转换为 messages 并调用 chat
        
        Args:
            prompt: 用户提示
            model: 模型ID
            temperature: 温度参数
            max_tokens: 最大 token 数
        
        Returns:
            QianfanResponse 对象
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model, temperature, max_tokens)
    
    async def async_generate(self, prompt: str, model: str = None, temperature: float = None, max_tokens: int = None) -> str:
        """
        异步便捷方法：将单个 prompt 转换为 messages 并调用 chat
        
        Args:
            prompt: 用户提示
            model: 模型ID
            temperature: 温度参数
            max_tokens: 最大 token 数
        
        Returns:
            生成的内容字符串
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, model, temperature, max_tokens)
        return response.content if response.success else ""
    
    def test_connection(self, model: str = None) -> bool:
        """测试 API 连接"""
        test_message = [{"role": "user", "content": "你好，这是一条测试消息"}]
        response = self.chat(test_message, model=model or self.model)
        return response.success
    
    def list_models(self) -> List[Dict[str, Any]]:
        """列出可用模型"""
        return [
            {"id": model_id, **info}
            for model_id, info in self.MODELS.items()
        ]


# ==================== 测试代码 ====================

def main():
    """测试千帆 API"""
    print("=" * 60)
    print("测试百度千帆平台 API")
    print("=" * 60)
    
    # 创建客户端
    client = QianfanClient()
    
    # 测试1：连接测试
    print("\n测试1：API 连接测试")
    if client.test_connection():
        print("✅ API 连接成功")
    else:
        print("❌ API 连接失败")
        return
    
    # 测试2：基础聊天
    print("\n测试2：基础聊天功能")
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "请用一句话介绍你自己。"}
    ]
    
    response = client.chat(messages, model="glm-5.1")
    
    if response.success:
        print(f"✅ 模型: {response.model}")
        print(f"✅ 响应: {response.content}")
        print(f"✅ Token使用: {response.usage}")
    else:
        print(f"❌ 失败: {response.content}")
    
    # 测试3：测试不同模型
    print("\n测试3：测试不同模型")
    for model_id in client.MODELS.keys():
        print(f"\n测试模型: {model_id}")
        test_msg = [{"role": "user", "content": "说一个数字"}]
        resp = client.chat(test_msg, model=model_id)
        
        if resp.success:
            print(f"  ✅ 响应: {resp.content[:50]}...")
        else:
            print(f"  ❌ 失败: {resp.content}")
    
    # 测试4：列出模型
    print("\n测试4：可用模型列表")
    models = client.list_models()
    for m in models:
        print(f"  - {m['id']}: {m['name']} (上下文: {m['context']} tokens)")


if __name__ == "__main__":
    main()
