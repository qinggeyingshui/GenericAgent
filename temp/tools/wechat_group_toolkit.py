"""
微信Bot群聊功能扩展工具包

基于ilink bot API的群聊消息处理能力扩展。

功能:
1. 群聊消息识别 - 通过消息结构判断是否为群聊消息
2. 群聊消息发送 - 支持向群聊发送文本和文件
3. 群聊消息接收 - 解析群聊消息的发送者和内容
4. @提及检测 - 识别消息中是否@了Bot

使用示例:
    from wechat_group_toolkit import WxGroupHelper
    
    helper = WxGroupHelper(bot_client)
    
    # 检测是否为群聊消息
    if helper.is_group_message(msg):
        group_id = helper.get_group_id(msg)
        sender = helper.get_sender_in_group(msg)
        
        # 回复群聊
        helper.send_group_text(group_id, "收到消息", context_token=msg.get('context_token'))
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontends.wechatapp import WxBotClient


class WxGroupHelper:
    """微信Bot群聊功能辅助类"""
    
    def __init__(self, bot_client=None):
        """
        初始化群聊助手
        
        Args:
            bot_client: WxBotClient实例，如果为None则自动创建
        """
        self.bot = bot_client or WxBotClient()
    
    def is_group_message(self, msg):
        """
        判断消息是否来自群聊
        
        根据微信Bot API的常见模式，群聊消息可能有以下特征:
        1. to_user_id 以特定前缀开头(如 'group_' 或特殊格式)
        2. 存在 chat_type 字段且值为群聊类型
        3. 存在 group_id 或 room_id 字段
        4. from_user_id 和 to_user_id 不同(群聊中发送者和接收者不同)
        
        Args:
            msg: 消息字典
            
        Returns:
            bool: 是否为群聊消息
        """
        # 方法1: 检查是否有明确的群聊标识字段
        if msg.get('chat_type') == 'group':
            return True
        if 'group_id' in msg or 'room_id' in msg:
            return True
        
        # 方法2: 检查to_user_id格式(群聊ID通常有特殊格式)
        to_user_id = msg.get('to_user_id', '')
        if to_user_id.startswith('group_') or '@chatroom' in to_user_id:
            return True
        
        # 方法3: 检查消息结构中的群聊相关字段
        # 某些实现中，群聊消息会有额外的sender信息
        if 'group_sender' in msg or 'room_sender' in msg:
            return True
        
        return False
    
    def get_group_id(self, msg):
        """
        获取群聊ID
        
        Args:
            msg: 消息字典
            
        Returns:
            str: 群聊ID，如果不是群聊消息则返回None
        """
        # 尝试多种可能的字段名
        for field in ['group_id', 'room_id', 'chat_id', 'conversation_id']:
            if field in msg:
                return msg[field]
        
        # 如果没有专门的群聊ID字段，to_user_id可能就是群聊ID
        if self.is_group_message(msg):
            return msg.get('to_user_id')
        
        return None
    
    def get_sender_in_group(self, msg):
        """
        获取群聊消息的实际发送者ID
        
        在群聊中，from_user_id可能是群聊ID，实际发送者在其他字段
        
        Args:
            msg: 消息字典
            
        Returns:
            str: 发送者ID
        """
        # 尝试获取群聊中的实际发送者
        for field in ['group_sender', 'room_sender', 'sender_id', 'actual_sender']:
            if field in msg:
                return msg[field]
        
        # 如果没有专门字段，返回from_user_id
        return msg.get('from_user_id', '')
    
    def is_mentioned(self, msg):
        """
        检测Bot是否被@提及
        
        Args:
            msg: 消息字典
            
        Returns:
            bool: 是否被@
        """
        # 方法1: 检查是否有@标识字段
        if msg.get('is_mentioned') or msg.get('at_bot'):
            return True
        
        # 方法2: 检查消息文本中是否包含@Bot的标记
        text = self.bot.extract_text(msg)
        bot_name = self.bot.bot_id  # 或其他Bot标识
        if f'@{bot_name}' in text or '@所有人' in text:
            return True
        
        # 方法3: 检查item_list中是否有at_item
        for item in msg.get('item_list', []):
            if 'at_item' in item:
                return True
        
        return False
    
    def send_group_text(self, group_id, text, context_token=''):
        """
        向群聊发送文本消息
        
        Args:
            group_id: 群聊ID
            text: 消息文本
            context_token: 上下文token(用于回复特定消息)
            
        Returns:
            dict: API响应
        """
        return self.bot.send_text(group_id, text, context_token)
    
    def send_group_file(self, group_id, file_path, context_token=''):
        """
        向群聊发送文件
        
        Args:
            group_id: 群聊ID
            file_path: 文件路径
            context_token: 上下文token
            
        Returns:
            dict: API响应
        """
        return self.bot.send_file(group_id, file_path, context_token)
    
    def extract_group_info(self, msg):
        """
        提取群聊消息的完整信息
        
        Args:
            msg: 消息字典
            
        Returns:
            dict: 包含群聊相关信息的字典
        """
        return {
            'is_group': self.is_group_message(msg),
            'group_id': self.get_group_id(msg),
            'sender_id': self.get_sender_in_group(msg),
            'is_mentioned': self.is_mentioned(msg),
            'text': self.bot.extract_text(msg),
            'context_token': msg.get('context_token', ''),
            'message_id': msg.get('message_id', ''),
            'raw_msg': msg  # 保留原始消息以便调试
        }


def demo_usage():
    """演示用法"""
    print("=== 微信Bot群聊功能演示 ===\n")
    
    # 创建助手
    helper = WxGroupHelper()
    
    print("1. 监听消息并识别群聊")
    print("   msgs = helper.bot.get_updates()")
    print("   for msg in msgs:")
    print("       if helper.is_group_message(msg):")
    print("           info = helper.extract_group_info(msg)")
    print("           print(f'群聊消息: {info}')\n")
    
    print("2. 向群聊发送消息")
    print("   group_id = 'group_xxx'  # 从消息中获取")
    print("   helper.send_group_text(group_id, '你好，群聊!')\n")
    
    print("3. 检测@提及")
    print("   if helper.is_mentioned(msg):")
    print("       # Bot被@了，进行响应")
    print("       helper.send_group_text(group_id, '收到!', msg['context_token'])\n")


if __name__ == '__main__':
    demo_usage()
