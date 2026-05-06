# -*- coding: utf-8 -*-
"""
FastAPI 路由定义
提供小说创作和剧本转换的 RESTful API
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import asyncio
from datetime import datetime

# 导入核心引擎
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.novel_engine import NovelEngine
from core.drama_engine import DramaEngine
from models.schemas import (
    CreateNovelRequest, GenerateChapterRequest, CreateDramaRequest,
    ConvertToDramaRequest, APIResponse, NovelListResponse, DramaListResponse,
    NovelProject, DramaProject, NovelGenre, DramaFormat
)

# 创建 FastAPI 应用
app = FastAPI(
    title="Novel Creation API",
    description="AI 小说创作 + 短剧剧本转换 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化引擎（需要配置）
novel_engine: Optional[NovelEngine] = None
drama_engine: Optional[DramaEngine] = None


def init_engines(llm_config: Dict = None, embedding_config: Dict = None):
    """初始化引擎"""
    global novel_engine, drama_engine
    
    config = llm_config or {
        "api_key": "sk-xxx",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini"
    }
    
    novel_engine = NovelEngine(config, embedding_config)
    drama_engine = DramaEngine(config)


# ==================== 健康检查 ====================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engines": {
            "novel": novel_engine is not None,
            "drama": drama_engine is not None
        }
    }


# ==================== 小说创作 API ====================

@app.post("/api/v1/novels", response_model=APIResponse)
async def create_novel(request: CreateNovelRequest):
    """
    创建小说项目
    
    - **title**: 小说标题
    - **genre**: 小说类型
    - **topic**: 主题/故事梗概
    - **total_chapters**: 总章节数
    - **target_word_count**: 每章目标字数
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        project = await novel_engine.create_project(request.dict())
        return APIResponse(
            success=True,
            message="小说项目创建成功",
            data=project.dict()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="创建失败",
            error=str(e)
        )


@app.get("/api/v1/novels", response_model=NovelListResponse)
async def list_novels(page: int = 1, page_size: int = 10):
    """列出所有小说项目"""
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    novels = await novel_engine.list_projects(page, page_size)
    return NovelListResponse(
        novels=novels,
        total=len(novels),
        page=page,
        page_size=page_size
    )


@app.get("/api/v1/novels/{novel_id}", response_model=APIResponse)
async def get_novel(novel_id: str):
    """获取小说项目详情"""
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    project = await novel_engine.get_project(novel_id)
    if not project:
        raise HTTPException(status_code=404, detail="Novel not found")
    
    return APIResponse(
        success=True,
        message="获取成功",
        data=project.dict()
    )


@app.post("/api/v1/novels/{novel_id}/blueprint", response_model=APIResponse)
async def generate_blueprint(novel_id: str):
    """
    生成小说蓝图
    
    包括：世界观设定、角色设定、情节大纲
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        blueprint = await novel_engine.generate_blueprint(novel_id)
        return APIResponse(
            success=True,
            message="蓝图生成成功",
            data=blueprint.dict()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="生成失败",
            error=str(e)
        )


@app.get("/api/v1/novels/{novel_id}/blueprint/stream")
async def generate_blueprint_stream(novel_id: str):
    """
    流式生成小说蓝图（SSE）
    
    实时显示生成进度和结果
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    async def generate():
        """流式生成器"""
        try:
            # 发送开始事件
            yield f"data: {json.dumps({'type': 'start', 'message': '开始生成蓝图...'}, ensure_ascii=False)}\n\n"
            
            # 生成蓝图
            yield f"data: {json.dumps({'type': 'progress', 'message': '正在生成世界观设定...'}, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0.1)
            
            blueprint = await novel_engine.generate_blueprint(novel_id)
            
            # 发送完成事件
            yield f"data: {json.dumps({'type': 'complete', 'message': '蓝图生成完成', 'data': blueprint.dict()}, ensure_ascii=False)}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'生成失败: {str(e)}'}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/v1/novels/{novel_id}/outline", response_model=APIResponse)
async def generate_chapter_outline(novel_id: str):
    """生成章节大纲"""
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        outlines = await novel_engine.generate_chapter_outline(novel_id)
        return APIResponse(
            success=True,
            message=f"生成 {len(outlines)} 个章节大纲",
            data=[o.dict() for o in outlines]
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="生成失败",
            error=str(e)
        )


@app.post("/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate", response_model=APIResponse)
async def generate_chapter(novel_id: str, chapter_num: int, request: GenerateChapterRequest = None):
    """
    生成章节内容
    
    - **chapter_num**: 章节号
    - **additional_guidance**: 额外创作指导
    - **use_memory**: 是否使用记忆系统保持一致性
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        guidance = request.additional_guidance if request else None
        use_memory = request.use_memory if request else True
        
        chapter = await novel_engine.generate_chapter(novel_id, chapter_num, guidance, use_memory)
        return APIResponse(
            success=True,
            message=f"第 {chapter_num} 章生成成功",
            data=chapter.dict()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="生成失败",
            error=str(e)
        )


@app.post("/api/v1/novels/{novel_id}/chapters/{chapter_num}/finalize", response_model=APIResponse)
async def finalize_chapter(novel_id: str, chapter_num: int):
    """
    最终化章节
    
    更新记忆系统、角色状态、情节发展
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        result = await novel_engine.finalize_chapter(novel_id, chapter_num)
        return APIResponse(
            success=True,
            message=f"第 {chapter_num} 章已最终化",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="最终化失败",
            error=str(e)
        )


@app.post("/api/v1/novels/{novel_id}/chapters/{chapter_num}/check", response_model=APIResponse)
async def check_consistency(novel_id: str, chapter_num: int):
    """
    检查章节一致性
    
    检查角色逻辑、情节连贯性、时间线、设定冲突
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        result = await novel_engine.check_consistency(novel_id, chapter_num)
        return APIResponse(
            success=True,
            message="一致性检查完成",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="检查失败",
            error=str(e)
        )


@app.get("/api/v1/novels/{novel_id}/export", response_model=APIResponse)
async def export_novel(novel_id: str, format: str = "markdown"):
    """
    导出小说
    
    支持格式：markdown, txt, word
    """
    if not novel_engine:
        raise HTTPException(status_code=500, detail="Novel engine not initialized")
    
    try:
        content = await novel_engine.export_novel(novel_id, format)
        return APIResponse(
            success=True,
            message="导出成功",
            data={"content": content, "format": format}
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="导出失败",
            error=str(e)
        )


# ==================== 剧本转换 API ====================

@app.post("/api/v1/drama/projects", response_model=APIResponse)
async def create_drama_project(request: CreateDramaRequest):
    """
    创建剧本项目
    
    - **title**: 项目标题
    - **source_novel_id**: 来源小说ID（可选）
    - **source_file**: 来源文件路径（可选）
    - **episode_duration**: 每集时长（秒）
    - **chapters_per_episode**: 每集章节数
    """
    if not drama_engine:
        raise HTTPException(status_code=500, detail="Drama engine not initialized")
    
    try:
        project = await drama_engine.create_project(request.dict())
        return APIResponse(
            success=True,
            message="剧本项目创建成功",
            data=project.dict()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="创建失败",
            error=str(e)
        )


@app.post("/api/v1/drama/convert", response_model=APIResponse)
async def convert_to_drama(request: ConvertToDramaRequest):
    """
    小说转剧本
    
    - **novel_id**: 小说ID
    - **chapter_range**: 章节范围（如 "1-3" 或 "all"）
    - **episode_num**: 集数编号
    - **output_formats**: 输出格式列表
    """
    if not drama_engine or not novel_engine:
        raise HTTPException(status_code=500, detail="Engines not initialized")
    
    try:
        # 获取小说项目
        novel = await novel_engine.get_project(request.novel_id)
        if not novel:
            raise HTTPException(status_code=404, detail="Novel not found")
        
        # 获取章节内容
        if request.chapter_range == "all":
            chapters = novel.generated_chapters
        else:
            start, end = map(int, request.chapter_range.split("-"))
            chapters = [c for c in novel.generated_chapters if start <= c.chapter_num <= end]
        
        if not chapters:
            raise HTTPException(status_code=404, detail="No chapters found")
        
        # 合并章节文本
        combined_text = "\n\n".join([c.content for c in chapters])
        characters = [c.dict() for c in novel.characters]
        
        # 生成大纲
        outline = await drama_engine.map_to_episode_outline(
            combined_text,
            characters,
            request.episode_num or 1,
            request.chapter_range
        )
        
        # 生成剧本
        script = await drama_engine.generate_script(outline, combined_text, characters)
        
        # 导出
        output_files = await drama_engine.export_script(script, request.output_formats)
        
        return APIResponse(
            success=True,
            message="转换成功",
            data={
                "script": script.dict(),
                "output_files": output_files
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="转换失败",
            error=str(e)
        )


@app.post("/api/v1/drama/upload", response_model=APIResponse)
async def upload_novel_and_convert(
    file: UploadFile = File(...),
    episode_duration: float = 90.0,
    chapters_per_episode: int = 3,
    output_formats: List[str] = ["json", "markdown"]
):
    """
    上传小说文件并转换为剧本
    
    支持 .txt, .md, .json 格式
    """
    if not drama_engine:
        raise HTTPException(status_code=500, detail="Drama engine not initialized")
    
    try:
        # 读取文件
        content = await file.read()
        text = content.decode("utf-8")
        
        # 解析小说
        parsed = await drama_engine.parse_novel(text)
        
        # 批量转换
        scripts = await drama_engine.batch_convert(
            text,
            parsed.get("main_characters", []),
            chapters_per_episode,
            [DramaFormat(f) for f in output_formats]
        )
        
        return APIResponse(
            success=True,
            message=f"成功转换为 {len(scripts)} 集剧本",
            data={
                "parsed": parsed,
                "scripts": [s.dict() for s in scripts]
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="转换失败",
            error=str(e)
        )


@app.get("/api/v1/drama/projects/{project_id}", response_model=APIResponse)
async def get_drama_project(project_id: str):
    """获取剧本项目详情"""
    if not drama_engine:
        raise HTTPException(status_code=500, detail="Drama engine not initialized")
    
    project = await drama_engine.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return APIResponse(
        success=True,
        message="获取成功",
        data=project.dict()
    )


# ==================== 启动配置 ====================

def create_app(llm_config: Dict = None, embedding_config: Dict = None) -> FastAPI:
    """创建并配置应用"""
    init_engines(llm_config, embedding_config)
    return app


if __name__ == "__main__":
    import uvicorn
    
    # 默认配置
    default_config = {
        "api_key": "sk-xxx",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini"
    }
    
    app = create_app(default_config)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


# ==================== AI 聊天 API ====================

# 简单的会话存储（生产环境应使用数据库）
chat_sessions: Dict[str, List[Dict[str, str]]] = {}


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    model: Optional[str] = None
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    success: bool
    response: str
    model: str
    conversation_id: str


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    AI 聊天
    
    - **message**: 用户消息
    - **model**: 模型名称（可选）
    - **conversation_id**: 会话ID（可选，用于保持对话上下文）
    """
    if not novel_engine or not novel_engine.llm:
        raise HTTPException(status_code=500, detail="LLM not initialized")
    
    try:
        # 获取或创建会话
        conversation_id = request.conversation_id or datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 获取对话历史
        history = chat_sessions.get(conversation_id, [])
        
        # 构建消息列表
        messages = []
        
        # 添加系统提示
        system_prompt = """你是一个专业的小说创作助手，擅长：
- 提供小说创作建议和灵感
- 帮助塑造角色和构建世界观
- 解答写作技巧和风格问题
- 分析故事情节和结构

请用专业、友好、鼓励的语气回答用户的问题。"""
        
        messages.append({"role": "system", "content": system_prompt})
        
        # 添加历史对话
        for msg in history:
            messages.append(msg)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": request.message})
        
        # 调用 LLM
        response = novel_engine.llm.client.chat.completions.create(
            model=request.model or novel_engine.llm.model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = response.choices[0].message.content
        
        # 保存对话历史
        history.append({"role": "user", "content": request.message})
        history.append({"role": "assistant", "content": ai_response})
        
        # 限制历史长度（保留最近10轮对话）
        if len(history) > 20:
            history = history[-20:]
        
        chat_sessions[conversation_id] = history
        
        return ChatResponse(
            success=True,
            response=ai_response,
            model=request.model or novel_engine.llm.model,
            conversation_id=conversation_id
        )
    
    except Exception as e:
        return ChatResponse(
            success=False,
            response=f"聊天失败: {str(e)}",
            model=request.model or "unknown",
            conversation_id=request.conversation_id or "error"
        )


@app.get("/api/v1/models")
async def get_models():
    """获取可用模型列表"""
    return {
        "models": [
            {"id": "glm-5.1", "name": "GLM-5.1", "provider": "Baidu"},
            {"id": "qwen3.5-397b-a17b", "name": "Qwen 3.5", "provider": "Alibaba"},
            {"id": "deepseek-v3.2", "name": "DeepSeek V3.2", "provider": "DeepSeek"}
        ]
    }
