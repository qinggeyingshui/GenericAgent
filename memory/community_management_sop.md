# 评论区互动管理 SOP

## 功能
评论抓取、情感分析、智能回复、粉丝分层

## 工具
- `temp/tools/comment_assistant.py`

## 使用流程

### 1. 加载评论数据
```python
import sys
sys.path.append('./tools')
import comment_assistant as ca

# 从JSON文件加载
comments = ca.load_comments('./comments.json')
```

### 2. 情感分析
```python
# 单条分析
sentiment = ca.analyze_sentiment('内容很棒！')
print(sentiment)  # positive/negative/neutral

# 批量分析
results = ca.analyze_comments(comments)
```

### 3. 智能回复
```python
# 自动生成回复
reply = ca.generate_reply('内容很棒！')
print(reply)  # 感谢支持！会继续努力的💪

# 指定情感生成
reply = ca.generate_reply('内容很棒！', sentiment='positive')
```

### 4. 粉丝分层
```python
# 生成粉丝报告
fan_report = ca.generate_fan_report(comments)

# 查看分层结果
for user_id, info in fan_report.items():
    print(f"{info['name']}: {info['tier']}")
```

### 5. 保存分析结果
```python
ca.save_analysis(results, './analysis.json')
```

## 完整工作流示例
```python
import sys
sys.path.append('./tools')
import comment_assistant as ca

# 1. 加载评论
comments = ca.load_comments('./comments.json')

# 2. 批量分析
results = ca.analyze_comments(comments)

# 3. 生成粉丝报告
fan_report = ca.generate_fan_report(comments)

# 4. 保存结果
ca.save_analysis(results, './analysis.json')

# 5. 输出统计
sentiments = [r['sentiment'] for r in results]
print(f'正面: {sentiments.count("positive")}条')
print(f'负面: {sentiments.count("negative")}条')
print(f'中性: {sentiments.count("neutral")}条')
```

## 数据格式

### 输入格式（JSON）
```json
[
  {
    "user_id": "u001",
    "user_name": "小明",
    "text": "内容很棒！",
    "timestamp": "2026-04-21 10:00"
  }
]
```

### 输出格式
```json
{
  "user_id": "u001",
  "user_name": "小明",
  "text": "内容很棒！",
  "sentiment": "positive",
  "suggested_reply": "感谢支持！",
  "timestamp": "2026-04-21 10:00"
}
```

## 粉丝分层规则
- **核心粉丝**: 评论≥10次 且 正面率>70%
- **活跃粉丝**: 评论≥5次
- **普通粉丝**: 评论≥2次
- **新粉丝**: 评论<2次

## 情感词典
- **正面词**: 好/棒/赞/喜欢/支持/优秀/精彩/厉害/感谢/有用
- **负面词**: 差/烂/垃圾/失望/不好/无聊/浪费/骗人/退款

## 注意事项
1. 情感分析基于关键词匹配，可扩展词典
2. 回复模板可自定义
3. 粉丝分层规则可调整
4. 支持JSON和CSV格式

---

[skill_mapping]
category: content_creation
tools: temp/tools/comment_assistant.py
[/skill_mapping]
