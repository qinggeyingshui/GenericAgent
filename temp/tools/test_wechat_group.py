"""
微信Bot群聊功能单元测试

测试群聊消息识别、发送等功能
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from wechat_group_toolkit import WxGroupHelper


def test_group_message_detection():
    """测试群聊消息识别"""
    print("=== 测试1: 群聊消息识别 ===")
    
    helper = WxGroupHelper()
    
    # 测试用例1: 明确的群聊消息(有group_id)
    msg1 = {
        'message_id': '123',
        'from_user_id': 'user_001',
        'to_user_id': 'group_abc',
        'group_id': 'group_abc',
        'item_list': [{'type': 1, 'text_item': {'text': '测试消息'}}]
    }
    result1 = helper.is_group_message(msg1)
    print(f"  用例1 (有group_id): {result1} {'✓' if result1 else '✗'}")
    
    # 测试用例2: 群聊消息(to_user_id包含@chatroom)
    msg2 = {
        'message_id': '124',
        'from_user_id': 'user_002',
        'to_user_id': 'xxx@chatroom',
        'item_list': [{'type': 1, 'text_item': {'text': '群聊测试'}}]
    }
    result2 = helper.is_group_message(msg2)
    print(f"  用例2 (@chatroom): {result2} {'✓' if result2 else '✗'}")
    
    # 测试用例3: 单聊消息
    msg3 = {
        'message_id': '125',
        'from_user_id': 'user_003',
        'to_user_id': 'user_004',
        'item_list': [{'type': 1, 'text_item': {'text': '单聊消息'}}]
    }
    result3 = helper.is_group_message(msg3)
    print(f"  用例3 (单聊): {not result3} {'✓' if not result3 else '✗'}")
    
    # 测试用例4: 有chat_type字段
    msg4 = {
        'message_id': '126',
        'from_user_id': 'user_005',
        'to_user_id': 'conv_123',
        'chat_type': 'group',
        'item_list': [{'type': 1, 'text_item': {'text': 'chat_type测试'}}]
    }
    result4 = helper.is_group_message(msg4)
    print(f"  用例4 (chat_type=group): {result4} {'✓' if result4 else '✗'}")
    
    return all([result1, result2, not result3, result4])


def test_group_info_extraction():
    """测试群聊信息提取"""
    print("\n=== 测试2: 群聊信息提取 ===")
    
    helper = WxGroupHelper()
    
    msg = {
        'message_id': '127',
        'from_user_id': 'user_006',
        'to_user_id': 'group_xyz',
        'group_id': 'group_xyz',
        'group_sender': 'user_006',
        'context_token': 'ctx_abc',
        'item_list': [{'type': 1, 'text_item': {'text': '提取测试'}}]
    }
    
    info = helper.extract_group_info(msg)
    
    print(f"  是否群聊: {info['is_group']} {'✓' if info['is_group'] else '✗'}")
    print(f"  群聊ID: {info['group_id']} {'✓' if info['group_id'] == 'group_xyz' else '✗'}")
    print(f"  发送者: {info['sender_id']} {'✓' if info['sender_id'] == 'user_006' else '✗'}")
    print(f"  消息文本: {info['text']}")
    print(f"  上下文token: {info['context_token']} {'✓' if info['context_token'] == 'ctx_abc' else '✗'}")
    
    return (info['is_group'] and 
            info['group_id'] == 'group_xyz' and 
            info['sender_id'] == 'user_006' and
            info['context_token'] == 'ctx_abc')


def test_mention_detection():
    """测试@提及检测"""
    print("\n=== 测试3: @提及检测 ===")
    
    helper = WxGroupHelper()
    
    # 测试用例1: 有at_item
    msg1 = {
        'message_id': '128',
        'from_user_id': 'user_007',
        'to_user_id': 'group_test',
        'item_list': [
            {'type': 1, 'text_item': {'text': '测试'}},
            {'type': 5, 'at_item': {'user_id': helper.bot.bot_id}}
        ]
    }
    result1 = helper.is_mentioned(msg1)
    print(f"  用例1 (有at_item): {result1} {'✓' if result1 else '✗'}")
    
    # 测试用例2: 文本中包含@
    msg2 = {
        'message_id': '129',
        'from_user_id': 'user_008',
        'to_user_id': 'group_test',
        'item_list': [{'type': 1, 'text_item': {'text': f'@{helper.bot.bot_id} 你好'}}]
    }
    result2 = helper.is_mentioned(msg2)
    print(f"  用例2 (文本@): {result2} {'✓' if result2 else '✗'}")
    
    # 测试用例3: 无@提及
    msg3 = {
        'message_id': '130',
        'from_user_id': 'user_009',
        'to_user_id': 'group_test',
        'item_list': [{'type': 1, 'text_item': {'text': '普通消息'}}]
    }
    result3 = helper.is_mentioned(msg3)
    print(f"  用例3 (无@): {not result3} {'✓' if not result3 else '✗'}")
    
    return result1 and result2 and not result3


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("微信Bot群聊功能单元测试")
    print("=" * 50 + "\n")
    
    results = []
    
    try:
        results.append(("群聊消息识别", test_group_message_detection()))
    except Exception as e:
        print(f"  测试失败: {e}")
        results.append(("群聊消息识别", False))
    
    try:
        results.append(("群聊信息提取", test_group_info_extraction()))
    except Exception as e:
        print(f"  测试失败: {e}")
        results.append(("群聊信息提取", False))
    
    try:
        results.append(("@提及检测", test_mention_detection()))
    except Exception as e:
        print(f"  测试失败: {e}")
        results.append(("@提及检测", False))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
