-- =====================================================
-- Novel Creation Platform - 数据库 Schema
-- 支持小说创作和剧本转换的数据存储
-- =====================================================

-- ==================== 1. 小说项目表 ====================

CREATE TABLE IF NOT EXISTS novels (
    novel_id VARCHAR(32) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) DEFAULT 'AI',
    genre VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    topic TEXT NOT NULL,
    theme TEXT,
    style_guide TEXT,
    total_chapters INTEGER DEFAULT 0,
    target_word_count INTEGER DEFAULT 3000,
    current_word_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_novels_genre ON novels(genre);
CREATE INDEX idx_novels_status ON novels(status);

-- ==================== 2. 角色表 ====================

CREATE TABLE IF NOT EXISTS characters (
    character_id VARCHAR(32) PRIMARY KEY,
    novel_id VARCHAR(32) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    age INTEGER,
    gender VARCHAR(20),
    personality JSON,
    background TEXT,
    abilities JSON,
    current_location VARCHAR(255),
    last_ap