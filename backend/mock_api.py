#!/usr/bin/env python3
"""
模拟AI后端服务 - 用于测试前端功能
不需要真实的API Key，返回模拟数据
"""
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ==================== 数据模型 ====================

class CreateNovelRequest(BaseModel):
    """创建小说请求"""
    title: str
    genre: str
    topic: str
    theme: Optional[str] = None
    style_guide: Optional[str] = None
    total_chapters: int = 10
    target_word_count: int = 3000

class GenerateChapterRequest(BaseModel):
    """生成章节请求"""
    additional_guidance: Optional[str] = None
    use_memory: bool = True

class ConvertDramaRequest(BaseModel):
    """剧本转换请求"""
    novel_id: str
    chapter_range: Optional[str] = None
    episode_num: Optional[int] = 1
    output_formats: List[str] = ["json"]

# ==================== 模拟数据存储 ====================

NOVELS_DB: Dict[str, Dict] = {}

# ==================== FastAPI 应用 ====================

app = FastAPI(
    title="Novel Creation API - Mock",
    description="模拟AI后端，用于测试前端功能",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 工具函数 ====================

def generate_mock_blueprint(genre: str, topic: str) -> Dict:
    """生成模拟蓝图"""
    return {
        "world_setting": {
            "era": "架空古代" if genre in ["玄幻", "仙侠", "武侠"] else "现代",
            "location": "神秘的修仙界" if genre in ["玄幻", "仙侠"] else "繁华都市",
            "power_system": "灵气修炼体系" if genre in ["玄幻", "仙侠"] else "现代科技"
        },
        "characters": [
            {
                "name": "林逸风",
                "role": "主角",
                "age": 18,
                "personality": ["坚韧", "聪明", "善良"],
                "background": "出身平凡，却拥有不凡天赋的少年"
            },
            {
                "name": "苏晴雪",
                "role": "女主角",
                "age": 17,
                "personality": ["温柔", "聪慧", "独立"],
                "background": "世家千金，却向往自由的少女"
            },
            {
                "name": "秦无极",
                "role": "反派",
                "age": 35,
                "personality": ["阴险", "野心勃勃", "手段狠辣"],
                "background": "权倾一方的霸主，渴望更大的力量"
            }
        ],
        "plot_blueprint": {
            "main_conflict": f"主角在{topic}的过程中，与强大势力产生冲突",
            "climax": "最终决战，主角突破极限，击败强敌",
            "resolution": "主角成长蜕变，开始新的征程"
        }
    }

def generate_mock_outline(total_chapters: int) -> List[Dict]:
    """生成模拟章节大纲"""
    outlines = []
    for i in range(1, total_chapters + 1):
        outlines.append({
            "chapter_num": i,
            "title": f"第{i}章：{'初入江湖' if i == 1 else '风云际会' if i == 2 else '暗中较劲' if i == 3 else '渐入佳境'}",
            "summary": f"主角在这一章经历了{'初次冒险' if i == 1 else '重要转折' if i % 5 == 0 else '日常成长'}，剧情逐步推进。",
            "key_events": [f"事件{i}-1", f"事件{i}-2"],
            "estimated_words": 3000
        })
    return outlines

def generate_mock_chapter(chapter_num: int, title: str) -> Dict:
    """生成模拟章节内容"""
    content = f"""
# 第{chapter_num}章：{title}

清晨的阳光洒落，林逸风站在山巅，眺望远方。

"这就是修仙之路吗..."他喃喃自语。

身后传来轻柔的脚步声，苏晴雪走到他身边："你在想什么？"

林逸风转身，眼中闪烁着坚定的光芒："我在想，无论前方有多少艰难险阻，我都要走下去。"

{"=" * 50}

【模拟章节内容】

这是第{chapter_num}章的模拟内容，用于测试前端显示效果。

实际部署时，这里会由AI生成真实的小说内容，包括：
- 详细的环境描写
- 人物对话和动作
- 情节推进和冲突
- 情感渲染和氛围营造

每章大约3000字左右，符合网络小说的阅读节奏。

{"=" * 50}

"我相信你。"苏晴雪轻声说道。

林逸风握紧拳头，感受着体内流转的灵气。经过这段时间的修炼，他明显感觉到自己的进步。

"走吧，新的征程开始了。"

两人并肩走向远方，身后留下淡淡的晨雾...

---

**【本章完】**
"""
    
    return {
        "chapter_num": chapter_num,
        "title": title,
        "content": content,
        "word_count": len(content),
        "created_at": datetime.now().isoformat()
    }

def generate_mock_drama() -> Dict:
    """生成模拟剧本"""
    return {
        "script_id": str(uuid.uuid4()),
        "episode_num": 1,
        "total_duration": 90,
        "total_shots": 15,
        "scenes": [
            {
                "scene_num": 1,
                "location": "山巅",
                "time_of_day": "清晨",
                "shots": [
                    {
                        "shot_num": 1,
                        "shot_type": "远景",
                        "duration": 5,
                        "visual": "镜头缓缓推进，展现壮丽的山景和晨曦中的云海",
                        "audio": "轻柔的背景音乐渐起"
                    },
                    {
                        "shot_num": 2,
                        "shot_type": "中景",
                        "duration": 4,
                        "visual": "主角站在山巅，背影挺拔，衣袂飘动",
                        "audio": "风声呼啸"
                    },
                    {
                        "shot_num": 3,
                        "shot_type": "特写",
                        "duration": 3,
                        "visual": "主角坚定的眼神，望向远方",
                        "audio": "主角内心独白"
                    }
                ]
            },
            {
                "scene_num": 2,
                "location": "练功房",
                "time_of_day": "日",
                "shots": [
                    {
                        "shot_num": 4,
                        "shot_type": "中景",
                        "duration": 6,
                        "visual": "主角在练功房中修炼，灵气环绕周身",
                        "audio": "能量聚集的音效"
                    }
                ]
            }
        ]
    }

# ==================== API 端点 ====================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engines": {
            "novel": True,
            "drama": True
        },
        "mode": "mock"
    }

# ==================== 小说相关 API ====================

@app.post("/api/v1/novels")
async def create_novel(request: CreateNovelRequest):
    """创建小说"""
    novel_id = str(uuid.uuid4())
    
    novel_data = {
        "novel_id": novel_id,
        "title": request.title,
        "genre": request.genre,
        "topic": request.topic,
        "theme": request.theme,
        "style_guide": request.style_guide,
        "total_chapters": request.total_chapters,
        "target_word_count": request.target_word_count,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "chapters": [],
        "generated_chapters": [],
        "world_setting": None,
        "characters": [],
        "plot_blueprint": None
    }
    
    NOVELS_DB[novel_id] = novel_data
    
    return {
        "success": True,
        "message": "小说创建成功",
        "data": novel_data
    }

@app.get("/api/v1/novels")
async def get_novels(page: int = 1, page_size: int = 100):
    """获取小说列表"""
    novels = list(NOVELS_DB.values())
    
    return {
        "novels": novels,
        "total": len(novels),
        "page": page,
        "page_size": page_size
    }

@app.get("/api/v1/novels/{novel_id}")
async def get_novel(novel_id: str):
    """获取小说详情"""
    if novel_id not in NOVELS_DB:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    return {
        "success": True,
        "message": "获取成功",
        "data": NOVELS_DB[novel_id]
    }

@app.post("/api/v1/novels/{novel_id}/blueprint")
async def generate_blueprint(novel_id: str):
    """生成小说蓝图"""
    if novel_id not in NOVELS_DB:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = NOVELS_DB[novel_id]
    blueprint = generate_mock_blueprint(novel["genre"], novel["topic"])
    
    # 更新小说数据
    novel["world_setting"] = blueprint["world_setting"]
    novel["characters"] = blueprint["characters"]
    novel["plot_blueprint"] = blueprint["plot_blueprint"]
    novel["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": "蓝图生成成功",
        "data": blueprint
    }

@app.post("/api/v1/novels/{novel_id}/outline")
async def generate_outline(novel_id: str):
    """生成章节大纲"""
    if novel_id not in NOVELS_DB:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = NOVELS_DB[novel_id]
    outline = generate_mock_outline(novel["total_chapters"])
    
    # 更新小说数据
    novel["chapters"] = outline
    novel["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": f"生成 {len(outline)} 个章节大纲",
        "data": outline
    }

@app.post("/api/v1/novels/{novel_id}/chapters/{chapter_num}/generate")
async def generate_chapter(novel_id: str, chapter_num: int, request: GenerateChapterRequest = None):
    """生成章节内容"""
    if novel_id not in NOVELS_DB:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = NOVELS_DB[novel_id]
    
    # 获取章节标题
    chapters = novel.get("chapters", [])
    chapter_title = f"第{chapter_num}章"
    for ch in chapters:
        if ch.get("chapter_num") == chapter_num:
            chapter_title = ch.get("title", chapter_title)
            break
    
    # 生成模拟内容
    chapter_content = generate_mock_chapter(chapter_num, chapter_title)
    
    # 更新已生成章节
    if "generated_chapters" not in novel:
        novel["generated_chapters"] = []
    novel["generated_chapters"].append(chapter_content)
    novel["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": f"第 {chapter_num} 章生成成功",
        "data": chapter_content
    }

@app.get("/api/v1/novels/{novel_id}/export")
async def export_novel(novel_id: str, format: str = "markdown"):
    """导出小说"""
    if novel_id not in NOVELS_DB:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = NOVELS_DB[novel_id]
    
    # 生成导出内容
    content = f"# {novel['title']}\n\n"
    content += f"类型：{novel['genre']}\n"
    content += f"梗概：{novel['topic']}\n\n"
    
    for ch in novel.get("generated_chapters", []):
        content += ch.get("content", "") + "\n\n"
    
    return {
        "success": True,
        "message": "导出成功",
        "data": {
            "content": content,
            "format": format
        }
    }

# ==================== 剧本转换 API ====================

@app.post("/api/v1/drama/convert")
async def convert_to_drama(request: ConvertDramaRequest):
    """将小说转换为剧本"""
    if request.novel_id not in NOVELS_DB:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    # 生成模拟剧本
    drama = generate_mock_drama()
    
    return {
        "success": True,
        "message": "剧本转换成功",
        "data": drama
    }

# ==================== 启动信息 ====================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Mock Novel Creation API - 模拟后端服务")
    print("="*50)
    print(f"✅ 服务地址: http://localhost:8000")
    print(f"✅ API文档: http://localhost:8000/docs")
    print(f"✅ 模式: 模拟AI（无需API Key）")
    print("="*50 + "\n")
