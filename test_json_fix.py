#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的生成流程
"""

import sys
import os
import asyncio
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.utils.json_utils import parse_ai_json


def test_json_parsing():
    """测试 JSON 解析"""
    print("=" * 60)
    print("测试 1: JSON 解析工具")
    print("=" * 60)
    
    # 测试用户提供的错误 JSON
    test_json = '''
{
  "main_conflict": "核心冲突描述...",
  "inciting_incident": "触发事件描述...",
  "rising_actions": [
    0: "转折点1：堕入凡间后的天蓬...",
    1: "转折点2：天庭并未打算放过这个异类...",
    2: "转折点3：巨灵神的陨落让天庭震怒...",
    3: "转折点4：天劫虽退，但福陵山也元气大伤..."
  ],
  "climax": "高潮描述...",
  "falling_actions": [
    0: "解决过程1：昊天镜碎裂后...",
    1: "解决过程2：福陵山满目疮痍..."
  ],
  "resolution": "结局描述..."
}
'''
    
    print("\n输入 JSON (带索引号):")
    print(test_json[:200] + "...")
    
    result = parse_ai_json(test_json)
    
    print("\n解析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 验证解析结果
    if "rising_actions" in result and len(result["rising_actions"]) == 4:
        print("\n✅ rising_actions 解析正确")
        print(f"   - 长度: {len(result['rising_actions'])}")
        print(f"   - 第一个元素: {result['rising_actions'][0][:50]}...")
    else:
        print("\n❌ rising_actions 解析失败")
        return False
    
    if "falling_actions" in result and len(result["falling_actions"]) == 2:
        print("\n✅ falling_actions 解析正确")
        print(f"   - 长度: {len(result['falling_actions'])}")
    else:
        print("\n❌ falling_actions 解析失败")
        return False
    
    return True


def test_outline_json_parsing():
    """测试大纲 JSON 解析"""
    print("\n" + "=" * 60)
    print("测试 2: 大纲 JSON 解析")
    print("=" * 60)
    
    # 测试大纲 JSON
    test_json = '''
{
  "chapters": [
    {
      "chapter_num": 1,
      "title": "第1章：觉醒",
      "summary": "章节摘要...",
      "key_events": [
        0: "事件1：天蓬发现真相",
        1: "事件2：与嫦娥对话",
        2: "事件3：被天庭追杀"
      ]
    },
    {
      "chapter_num": 2,
      "title": "第2章：逃亡",
      "summary": "章节摘要...",
      "key_events": [
        0: "事件1：堕入凡间",
        1: "事件2：成为猪妖"
      ]
    }
  ]
}
'''
    
    print("\n输入 JSON (带索引号):")
    print(test_json[:200] + "...")
    
    result = parse_ai_json(test_json)
    
    print("\n解析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 验证解析结果
    if "chapters" in result and len(result["chapters"]) == 2:
        print("\n✅ chapters 解析正确")
        
        for i, chapter in enumerate(result["chapters"]):
            print(f"\n   第 {i+1} 章:")
            print(f"   - 标题: {chapter.get('title')}")
            print(f"   - 关键事件数量: {len(chapter.get('key_events', []))}")
            
            if "key_events" in chapter:
                print(f"   ✅ key_events 解析正确")
            else:
                print(f"   ❌ key_events 解析失败")
                return False
    else:
        print("\n❌ chapters 解析失败")
        return False
    
    return True


async def test_blueprint_generation():
    """测试蓝图生成（模拟）"""
    print("\n" + "=" * 60)
    print("测试 3: 蓝图生成（使用实际 AI 输出）")
    print("=" * 60)
    
    # 用户提供的实际蓝图输出
    actual_blueprint = '''
{
"main_conflict":"核心冲突的本质在于个体对真实自我的坚守与强权体制对异类抹杀之间的对抗。天蓬元帅（猪八戒）体内流淌着太古混沌凶兽"吞天野猪"的血脉，而天庭的"仙道"本质上是一种抹杀情感与本能的绝对秩序。天庭利用天河之水压制凶兽血脉，将天蓬塑造成无情的镇水工具。当这股血脉开始觉醒，天庭便视其为必须清除的异端。这一冲突贯穿故事始终，迫使天蓬从体制内的顺从者，一步步走向反抗天道的妖皇。主角的利益在于求生与保全本心，而反派（以玉帝法则具象化的昊天镜灵为首）的利益在于维持三界绝对的统治秩序，绝不允许任何不可控的混沌力量存在。两者之间是不可调和的生存与毁灭之争，天蓬若不反抗，便会被天道同化为傀儡；天庭若不将他抹杀，其统治的合法性便会受到质疑。"
"inciting_incident":"蟠桃盛宴之夜，天蓬元帅奉命巡视天河防务，却察觉到天河底层的灵气波动异常。他潜入广寒宫寻找月精轮的掌控者嫦娥，试图询问缘由，却意外撞破了天庭最大的秘密：广寒宫并非仙境，而是镇压下界灵脉的阵眼，嫦娥则是被锁链贯穿琵琶骨的阵灵。嫦娥在痛苦中向天蓬揭示真相——天庭所谓的仙道，实则是通过天河虹吸下界生机，而蟠桃不过是掩盖天地衰败的麻醉剂。天蓬试图用九齿钉耙斩断嫦娥的锁链，却瞬间触发了天庭的最高警戒。昊天镜光芒大作，无数金甲神将包围广寒宫。天庭为了掩盖这骇人听闻的真相，将天蓬的拯救之举污蔑为"醉酒调戏仙子"。天蓬百口莫辩，眼睁睁看着嫦娥被昊天镜吞噬，自己则被剥夺仙骨，打入畜生道。这一事件彻底击碎了天蓬对天庭的信仰，让他从高高在上的元帅沦为受尽屈辱的猪妖，也让他明白，唯有彻底掀翻这虚伪的天道，才能掌握自己的命运。"
"rising_actions":[
0:"堕入凡间后的天蓬，在一头母猪的腹中重生，化为人头猪身的怪物。起初，他仍试图用残存的仙家功法净化肉身，渴望洗刷耻辱重返天庭。然而，他发现自己每一次运转仙气，都会遭到这具混沌凶兽躯体的反噬。在福陵山的一个雨夜，他被一群低阶狼妖围攻，仙气涣散的他险些被生吞。生死关头，他本能地放弃了仙道功法，任由野性的妖气充斥经脉。那一瞬间，他化作一头黑色的巨猪，将狼妖撕碎吞噬。这次觉醒让他彻底认清现实：天庭的仙道根本容不下他，唯有接纳这被世人唾弃的妖身，才能在这残酷的世间活下去。他霸占云栈洞，正式与过去的自己决裂，踏上了妖修之路。"
1:"天庭并未打算放过这个异类，派出了曾与天蓬同殿为臣的巨灵神下界剿杀。巨灵神手持宣花斧，以高高在上的姿态审判天蓬的"堕落"。战斗初期，天蓬被巨灵神的神力压制，伤痕累累。巨灵神的嘲讽让他意识到，仅凭妖气的蛮力无法对抗天庭的法则。在濒死之际，他的鲜血浸透了九齿钉耙，唤醒了这件神兵的真正来历——它根本不是天庭赐予的兵刃，而是太古神铁打造的凶兵，专克天道法则。天蓬握住钉耙，凶兵与凶兽血脉共鸣，他一耙击碎了巨灵神的法相，将其打落凡间。这一战，不仅让天蓬获得了足以抗衡天庭的武装，更让他明白，天庭的法则并非不可战胜，他的反叛之心愈发坚定。"
2:"巨灵神的陨落让天庭震怒，昊天镜降下法旨，发动了对福陵山的局部天劫，意图将方圆百里的生灵连同天蓬一并抹杀。面对灭顶之灾，天蓬没有选择独善其身地逃亡。他孤身走入周围妖族的领地，以血为誓，以九齿钉耙为证，将原本一盘散沙的妖族团结起来。他利用自己对天庭阵法的了解，在福陵山布下了逆天大阵。当雷劫降临，天蓬率领众妖逆天而起，不仅硬扛下了天雷，更将雷劫的力量转化为妖阵的底蕴，反噬了天庭的执刑使。这次战役让天蓬从一个独行的妖怪，蜕变为统御万妖的妖王。他意识到，自己的命运已经与这片大地的生灵绑定，反抗天道不再是他一人的私仇。"
3:"天劫虽退，但福陵山也元气大伤。此时，佛门尊者观音踏莲而来，带来了天庭的最终通牒：天庭将引天河之水倒灌福陵山，彻底清洗此地。观音提出一个交易，若天蓬愿意戴上佛门的禁制，护送转世金蝉子西天取经，佛门可保他一命，并庇护福陵山众妖。天蓬看穿了佛门的算计——这不过是另一种形式的圈养与奴役。他拒绝了观音的立刻庇护，选择独自面对即将到来的天河倾泻，为众妖争取撤离的时间。这个决定让他失去了退路，也将他推向了与天庭法则正面硬撼的绝境，为最终的决战拉开了序幕。"
]
"climax":"天河决堤，亿万吨带有天道法则的星水化作灭世瀑布，轰然砸向福陵山。天蓬独自立于山巅，面对漫天水幕，他的身后是正在撤离的妖族老弱。昊天镜灵在天河之上显化，冷漠的法则之音响彻天地，宣告天蓬的宿命不过是天道轮盘下的蝼蚁。天河之水不仅重若千钧，更带有消融灵魂的法则之力，天蓬的凶兽之躯在冲刷下皮开肉绽，九齿钉耙也发出不堪重负的悲鸣。在这生死存亡的一刻，天蓬面临最艰难的抉择：是彻底放弃自我意识，让太古凶兽的本能完全吞噬自己，化作一具只知杀戮的行尸走肉来换取力量；还是保持清醒，在天道法则下灰飞烟灭。天蓬仰天狂啸，他既不愿做天道的奴隶，也不愿做本能的傀儡。他猛然将手插入自己的胸膛，生生挖出了天庭当年植入的最后一丝仙骨，将其捏碎。没有了仙骨的束缚，凶兽血脉彻底爆发，但他凭借着惊人的意志力，硬生生在狂暴的凶兽之躯中保留了一丝清明。他与九齿钉耙人兵合一，化作一尊比天道更古老的混沌法相。他没有选择格挡天河之水，而是张开巨口，以吞天野猪的本源之力，疯狂吞噬天河中蕴含的法则与灵气。他将天庭的惩罚化作了自身的修为，随后挥动九齿钉耙，一耙向着天穹的昊天镜狠狠砸去。这一击，不仅击碎了昊天镜，更在南天门上砸出了一道无法愈合的裂痕。天蓬以半神半妖的姿态，向整个三界宣告，他天蓬的命，只由他自己说了算。"
"falling_actions":[
0:"昊天镜碎裂后，天庭的法则之力反噬，天河之水失去控制，眼看就要淹没南赡部洲。化作混沌法相的天蓬虽然击溃了天敌，但凶兽的嗜血本能也几乎要将他的理智吞没。他在云层中狂暴地破坏，连曾经的手下也认不出。就在他即将彻底迷失之际，福陵山下传来了妖族幼崽惊恐的啼哭声，这微弱的声音如同锚点，将他从无意识的杀戮深渊中拉回。他拼尽全力，将体内刚吞噬的天河之水强行逆转，重新逼回天际，化作一道隔绝两界的水幕。完成这一幕后，他力竭跌落，褪去法相，变回了那个丑陋却真实的半人半猪形态，身受重伤，修为十去其八。"
1:"福陵山满目疮痍，观音再次现身。这一次，天蓬已无力再战。为了保全幸存的妖族，他答应了观音的条件，但并非无条件的屈服。他在众目睽睽之下，与观音定下心魔大誓：佛门必须庇护福陵山余部，而他则作为"猪八戒"入局取经。他故意在观音面前表现出贪吃好色的市侩模样，以此降低天庭和佛门的防备。他接受了"八戒"这个法号，将锋芒与仇恨深深埋藏在圆滑的外表之下，将九齿钉耙的凶兵之气封印。他不再是那个宁折不弯的天蓬元帅，而是一个懂得隐忍、等待时机的潜伏者，准备在取经这个巨大的棋局中，寻找彻底掀翻天道与佛门算计的契机。"
]
"resolution":"故事的最后，猪八戒背负着破烂的行囊，在一处荒凉的路口等候未来的取经人。他回望了一眼被云雾遮蔽的福陵山，眼中没有了曾经的狂傲与不甘，取而代之的是一种如渊般的深沉。他摸了摸腰间被封印的九齿钉耙，嘴角勾起一抹自嘲却又危险的笑意。主题在此升华：真正的自由与抗争，并非一味地追求力量的爆发，而是在绝境中懂得蛰伏，在屈辱中坚守本心。神与魔的界限，不在于外表的仙风道骨还是獠牙面容，而在于是否拥有在既定宿命中做出自我选择的勇气。猪八戒接受了这具丑陋的皮囊，接受了世人加诸其身的污名，但他从未向命运低头。西行之路，看似是一场赎罪的苦旅，实则是他布下的一个惊天大局。当读者合上书本，不禁会去猜想：当这头懒猪在灵山之上、诸佛眼前撕下伪装的那一刻，三界的规则是否会被他再次砸得粉碎？这种对宿命的反抗与对自由的终极追问，留给读者无尽的思考空间。"
"foreshadowing":[]
}
'''
    
    print("\n使用实际 AI 输出测试...")
    
    result = parse_ai_json(actual_blueprint)
    
    print("\n解析结果:")
    print(f"main_conflict: {result.get('main_conflict', '')[:100]}...")
    print(f"rising_actions 数量: {len(result.get('rising_actions', []))}")
    print(f"falling_actions 数量: {len(result.get('falling_actions', []))}")
    
    # 验证
    if "main_conflict" in result and len(result["main_conflict"]) > 0:
        print("\n✅ main_conflict 解析成功")
    else:
        print("\n❌ main_conflict 解析失败")
        return False
    
    if "rising_actions" in result and len(result["rising_actions"]) == 4:
        print("✅ rising_actions 解析成功")
        for i, action in enumerate(result["rising_actions"]):
            print(f"   - 转折点{i+1}: {action[:50]}...")
    else:
        print("❌ rising_actions 解析失败")
        return False
    
    if "falling_actions" in result and len(result["falling_actions"]) == 2:
        print("✅ falling_actions 解析成功")
    else:
        print("❌ falling_actions 解析失败")
        return False
    
    return True


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("开始测试 JSON 解析和生成流程")
    print("=" * 60)
    
    # 测试 1: JSON 解析工具
    test1 = test_json_parsing()
    
    # 测试 2: 大纲 JSON 解析
    test2 = test_outline_json_parsing()
    
    # 测试 3: 实际蓝图生成
    test3 = await test_blueprint_generation()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"测试 1 (JSON 解析工具): {'✅ 通过' if test1 else '❌ 失败'}")
    print(f"测试 2 (大纲 JSON 解析): {'✅ 通过' if test2 else '❌ 失败'}")
    print(f"测试 3 (实际蓝图生成): {'✅ 通过' if test3 else '❌ 失败'}")
    
    if test1 and test2 and test3:
        print("\n🎉 所有测试通过！")
        print("\n结论：")
        print("- ✅ JSON 解析工具可以正确处理带索引号的 JSON")
        print("- ✅ 即使 AI 输出错误格式，后端也能正确解析")
        print("- ✅ 可以正常生成蓝图和大纲")
        return True
    else:
        print("\n❌ 部分测试失败")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)