
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontends.wechatapp import WxBotClient
import json

# 初始化客户端
client = WxBotClient()

print("=== 微信Bot消息结构探测 ===\n")
print(f"Bot ID: {client.bot_id}")
print(f"Token存在: {bool(client.token)}\n")

# 获取最近的消息
print("正在获取消息...")
msgs = client.get_updates(timeout=5)

print(f"\n收到 {len(msgs)} 条消息\n")

if msgs:
    for i, msg in enumerate(msgs[:3], 1):  # 只分析前3条
        print(f"--- 消息 {i} ---")
        print(f"完整结构: {json.dumps(msg, ensure_ascii=False, indent=2)}\n")
        
        # 分析关键字段
        print("关键字段:")
        for key in ['from_user_id', 'to_user_id', 'chat_type', 'group_id', 
                    'room_id', 'conversation_id', 'message_type']:
            if key in msg:
                print(f"  {key}: {msg[key]}")
        
        # 检查是否有群聊相关字段
        group_indicators = []
        for key in msg.keys():
            if any(kw in key.lower() for kw in ['group', 'room', 'chat', 'conversation']):
                group_indicators.append(f"{key}: {msg[key]}")
        
        if group_indicators:
            print("\n可能的群聊标识:")
            for ind in group_indicators:
                print(f"  {ind}")
        
        print()
else:
    print("未收到消息。建议:")
    print("1. 向Bot发送一条单聊消息")
    print("2. 如果有群聊，在群里@Bot或发送消息")
    print("3. 再次运行此脚本对比消息结构差异")
