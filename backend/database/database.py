# -*- coding: utf-8 -*-
"""
数据库连接和会话管理
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from .models import Base

# 数据库 URL
# Railway 会自动设置 DATABASE_URL，如果没有则使用本地 SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./novels.db"
)

# SQLite 需要特殊配置
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False  # 设置为 True 可以看到 SQL 日志
    )
else:
    # PostgreSQL 或其他数据库
    engine = create_engine(DATABASE_URL, echo=False)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """初始化数据库（创建所有表）"""
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库初始化完成")


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话（用于 FastAPI 依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """获取数据库会话（用于上下文管理器）"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
