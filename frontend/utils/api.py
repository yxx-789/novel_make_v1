"""
API 调用封装模块 - 完全适配后端 API
"""
import requests
import os
from typing import Dict, List, Optional, Any


class Config:
    """配置类"""
    # 自动检测环境
    if os.environ.get('STREAMLIT_SERVER_HEADLESS') == 'true':
        # 生产环境 - Railway
        API_BASE_URL = os.environ.get('API_BASE_URL', 'https://novelmakev1-production.up.railway.app')
    else:
        # 开发环境
        API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
    
    DEFAULT_MODEL = os.environ.get('LLM_MODEL', 'glm-5.1')


class APIClient:
    """API 客户端类"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.timeout = 600  # 10分钟超时，因为 AI 生成长内容需要时间
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """发送 HTTP 请求"""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {"error": "请求超时，AI 正在生成中，请稍后重试", "success": False}
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "success": False}
        except Exception as e:
            return {"error": f"未知错误: {str(e)}", "success": False}
    
    # ==================== 系统相关 API ====================
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return self._request("GET", "/health")
    
    def get_models(self) -> Dict[str, Any]:
        """获取可用模型列表"""
        # 后端暂未实现此 API，返回默认模型列表
        return {
            "success": True,
            "models": [
                {"id": "glm-5.1", "name": "GLM-5.1", "provider": "Baidu"},
                {"id": "qwen3.5-397b-a17b", "name": "Qwen 3.5", "provider": "Alibaba"},
                {"id": "deepseek-v3.2", "name": "DeepSeek V3.2", "provider": "DeepSeek"}
            ]
        }
    
    # ==================== 小说相关 API ====================
    
    def create_novel(
        self, 
        title: str, 
        genre: str,  # 后端使用枚举值
        topic: str,  # 后端参数名是 topic
        theme: Optional[str] = None,
        style_guide: Optional[str] = None,
        total_chapters: int = 10,
        target_word_count: int = 3000
    ) -> Dict[str, Any]:
        """创建小说
        
        参数说明：
        - title: 小说标题
        - genre: 小说类型（后端枚举值：玄幻、都市、言情、科幻、历史、悬疑、武侠、仙侠、其他）
        - topic: 主题/故事梗概
        - theme: 核心主题（可选）
        - style_guide: 风格指南（可选）
        - total_chapters: 总章节数
        - target_word_count: 每章目标字数
        """
        data = {
            "title": title,
            "genre": genre,
            "topic": topic,
            "total_chapters": total_chapters,
            "target_word_count": target_word_count
        }
        
        if theme:
            data["theme"] = theme
        if style_guide:
            data["style_guide"] = style_guide
        
        return self._request("POST", "/api/v1/novels", json=data)
    
    def get_novels(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """获取小说列表
        
        返回格式：
        {
            "novels": [NovelProject, ...],
            "total": 10,
            "page": 1,
            "page_size": 100
        }
        """
        return self._request("GET", "/api/v1/novels", params={"page": page, "page_size": page_size})
    
    def get_novel(self, novel_id: str) -> Dict[str, Any]:
        """获取小说详情
        
        返回格式：
        {
            "success": true,
            "message": "获取成功",
            "data": NovelProject
        }
        """
        return self._request("GET", f"/api/v1/novels/{novel_id}")
    
    def delete_novel(self, novel_id: str) -> Dict[str, Any]:
        """删除小说
        
        注意：需要检查后端是否实现了此 API
        """
        return self._request("DELETE", f"/api/v1/novels/{novel_id}")
    
    # ==================== 小说生成 API ====================
    
    def generate_blueprint(self, novel_id: str) -> Dict[str, Any]:
        """生成小说蓝图
        
        包括：世界观设定、角色设定、情节大纲
        
        返回格式：
        {
            "success": true,
            "message": "蓝图生成成功",
            "data": PlotBlueprint
        }
        """
        return self._request("POST", f"/api/v1/novels/{novel_id}/blueprint")
    
    def generate_outline(self, novel_id: str) -> Dict[str, Any]:
        """生成章节大纲
        
        返回格式：
        {
            "success": true,
            "message": "生成 X 个章节大纲",
            "data": [ChapterOutline, ...]
        }
        """
        return self._request("POST", f"/api/v1/novels/{novel_id}/outline")
    
    def generate_chapter(
        self, 
        novel_id: str,
        chapter_num: int,
        additional_guidance: Optional[str] = None,
        use_memory: bool = True
    ) -> Dict[str, Any]:
        """生成章节内容
        
        参数说明：
        - novel_id: 小说ID
        - chapter_num: 章节号
        - additional_guidance: 额外创作指导
        - use_memory: 是否使用记忆系统保持一致性
        
        返回格式：
        {
            "success": true,
            "message": "第 X 章生成成功",
            "data": ChapterContent
        }
        """
        data = {}
        if additional_guidance:
            data["additional_guidance"] = additional_guidance
        if use_memory is not None:
            data["use_memory"] = use_memory
        
        return self._request(
            "POST", 
            f"/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate",
            json=data if data else None
        )
    
    def finalize_chapter(self, novel_id: str, chapter_num: int) -> Dict[str, Any]:
        """最终化章节
        
        更新记忆系统、角色状态、情节发展
        """
        return self._request(
            "POST", 
            f"/api/v1/novels/{novel_id}/chapters/{chapter_num}/finalize"
        )
    
    def check_consistency(self, novel_id: str, chapter_num: int) -> Dict[str, Any]:
        """检查章节一致性
        
        检查角色逻辑、情节连贯性、时间线、设定冲突
        """
        return self._request(
            "POST", 
            f"/api/v1/novels/{novel_id}/chapters/{chapter_num}/check"
        )
    
    def export_novel(self, novel_id: str, format: str = "markdown") -> Dict[str, Any]:
        """导出小说
        
        支持格式：markdown, txt, word
        """
        return self._request(
            "GET", 
            f"/api/v1/novels/{novel_id}/export",
            params={"format": format}
        )
    
    # ==================== 剧本转换 API ====================
    
    def create_drama_project(
        self,
        title: str,
        source_novel_id: Optional[str] = None,
        episode_duration: float = 90.0,
        chapters_per_episode: int = 3
    ) -> Dict[str, Any]:
        """创建剧本项目
        
        参数说明：
        - title: 项目标题
        - source_novel_id: 来源小说ID
        - episode_duration: 每集时长（秒）
        - chapters_per_episode: 每集章节数
        """
        data = {
            "title": title,
            "episode_duration": episode_duration,
            "chapters_per_episode": chapters_per_episode
        }
        
        if source_novel_id:
            data["source_novel_id"] = source_novel_id
        
        return self._request("POST", "/api/v1/drama/projects", json=data)
    
    def convert_to_drama(
        self, 
        novel_id: str,
        chapter_range: Optional[str] = None,  # 如 "1-3" 或 "all"
        episode_num: Optional[int] = None,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """将小说转换为剧本
        
        参数说明：
        - novel_id: 小说ID
        - chapter_range: 章节范围（如 "1-3" 或 "all"）
        - episode_num: 剧集编号
        - output_format: 输出格式（json/markdown/csv/fdx）
        
        返回格式：
        {
            "success": true,
            "message": "转换成功",
            "data": DramaScript
        }
        """
        data = {
            "novel_id": novel_id,
            "output_formats": [output_format]
        }
        
        if chapter_range:
            data["chapter_range"] = chapter_range
        if episode_num:
            data["episode_num"] = episode_num
        
        return self._request("POST", "/api/v1/drama/convert", json=data)
    
    def get_drama_project(self, project_id: str) -> Dict[str, Any]:
        """获取剧本项目详情"""
        return self._request("GET", f"/api/v1/drama/projects/{project_id}")
    
    # ==================== AI 聊天 API ====================
    
    def chat(
        self, 
        message: str,
        model: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """AI 聊天
        
        参数说明：
        - message: 用户消息
        - model: 模型名称（可选）
        - conversation_id: 会话ID（可选，用于保持对话上下文）
        """
        data = {
            "message": message
        }
        
        if model:
            data["model"] = model
        if conversation_id:
            data["conversation_id"] = conversation_id
        
        return self._request("POST", "/api/v1/chat", json=data)


# 创建全局 API 客户端实例
api_client = APIClient()
