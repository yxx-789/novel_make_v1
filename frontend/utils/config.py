"""
配置管理模块
"""
import os


class Config:
    """全局配置"""
    
    # API 配置 - 从环境变量读取，如果没有则使用默认值
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
    
    # 默认模型
    DEFAULT_MODEL = "glm-5.1"
    
    # 页面配置
    PAGE_TITLE = "AI 小说创作平台"
    PAGE_ICON = "📖"
    
    # 主题配置
    PRIMARY_COLOR = "#667eea"
    SECONDARY_COLOR = "#764ba2"
    
    # 功能开关
    ENABLE_CHAT = True
    ENABLE_DRAMA = True
    
    @classmethod
    def update_api_url(cls, url: str):
        """更新 API 地址"""
        cls.API_BASE_URL = url
