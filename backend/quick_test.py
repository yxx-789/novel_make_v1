# -*- coding: utf-8 -*-
"""
快速测试脚本 - 用于本地测试
运行: python quick_test.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """测试所有 API 端点"""
    
    print("=" * 60)
    print("🔍 小说创作平台 - 本地测试")
    print("=" * 60)
    
    # 测试1: 健康检查
    print("\n1️⃣ 测试健康检查")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ 状态: {data.get('status')}")
            print(f"✅ 时间: {data.get('timestamp')}")
        else:
            print(f"❌ 失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return
    
    # 测试2: 创建小说项目
    print("\n2️⃣ 创建小说项目")
    novel_data = {
        "title": "测试小说",
        "genre": "玄幻",
        "topic": "一个少年修仙的故事",
        "total_chapters": 3,
        "target_word_count": 800
    }
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/novels",
            json=novel_data,
            headers={"Content-Type": "application/json"}
        )
        
        if resp.status_code == 200:
            novel = resp.json()
            novel_id = novel.get("novel_id")
            print(f"✅ 创建成功!")
            print(f"   ID: {novel_id}")
            print(f"   标题: {novel.get('title')}")
            print(f"   类型: {novel.get('genre')}")
        else:
            print(f"❌ 创建失败: {resp.status_code}")
            print(f"   响应: {resp.text}")
            return
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return
    
    # 测试3: 获取项目列表
    print("\n3️⃣ 获取项目列表")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/novels")
        if resp.status_code == 200:
            novels = resp.json()
            print(f"✅ 项目数量: {len(novels)}")
            for n in novels:
                print(f"   - {n.get('title')} ({n.get('novel_id')})")
        else:
            print(f"❌ 获取失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试4: 生成小说蓝图
    print(f"\n4️⃣ 生成小说蓝图 (项目ID: {novel_id})")
    try:
        resp = requests.post(f"{BASE_URL}/api/v1/novels/{novel_id}/blueprint")
        if resp.status_code == 200:
            blueprint = resp.json()
            print(f"✅ 蓝图生成成功!")
            print(f"   核心冲突: {blueprint.get('main_conflict', 'N/A')[:80]}...")
        else:
            print(f"⚠️ 蓝图生成可能耗时较长: {resp.status_code}")
            print(f"   响应: {resp.text[:200]}")
    except Exception as e:
        print(f"⚠️ 蓝图生成跳过: {e}")
    
    # 测试5: 剧本转换测试
    print("\n5️⃣ 剧本转换测试")
    drama_data = {
        "title": "短剧测试",
        "content": "少年林风在山上采药时，发现一个发光的洞穴。洞穴中有一块神秘玉佩，"
                  "当他触摸玉佩时，获得了一段古老的修炼记忆。他决定开始修炼，改变自己的命运。",
        "characters": [
            {"name": "林风", "role": "主角", "age": 16, "personality": ["好奇", "勇敢"]}
        ]
    }
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/drama/convert",
            json=drama_data,
            headers={"Content-Type": "application/json"}
        )
        
        if resp.status_code == 200:
            drama = resp.json()
            print(f"✅ 剧本转换成功!")
            print(f"   标题: {drama.get('title', 'N/A')}")
            print(f"   格式: {drama.get('format', 'N/A')}")
            print(f"   总时长: {drama.get('total_duration', 'N/A')}秒")
        else:
            print(f"❌ 剧本转换失败: {resp.status_code}")
            print(f"   响应: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ 剧本转换失败: {e}")
    
    # 测试6: 查看API文档
    print("\n6️⃣ API文档状态")
    print(f"   文档地址: {BASE_URL}/docs")
    print(f"   OpenAPI地址: {BASE_URL}/openapi.json")
    
    # 测试7: 测试导出功能
    print(f"\n7️⃣ 测试导出功能 (项目ID: {novel_id})")
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/novels/{novel_id}/export?format=markdown")
        if resp.status_code == 200:
            content = resp.text
            print(f"✅ 导出成功!")
            print(f"   长度: {len(content)} 字符")
            print(f"   预览:")
            print(f"   {content[:200]}...")
        else:
            print(f"❌ 导出失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 导出测试失败: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    print("🎯 下一步:")
    print("1. 访问文档: http://localhost:8000/docs")
    print("2. 交互测试: 在浏览器中点击 'Try it out'")
    print("3. 测试所有功能: 使用 /docs 界面")
    print("4. 检查日志: 查看服务控制台输出")
    
    print("\n🛠️ 如果遇到问题:")
    print("1. 确保服务正在运行: python main.py")
    print("2. 检查端口占用: netstat -an | grep 8000")
    print("3. 检查依赖: pip install -r requirements.txt")
    print("4. 检查网络连接: 能否访问千帆API")
    
    print("\n🎉 祝你测试愉快!")

if __name__ == "__main__":
    test_api()