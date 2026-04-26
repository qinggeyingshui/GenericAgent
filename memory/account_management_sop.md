# 多平台账号管理与数据同步 (L3 SOP)
工具: temp/tools/account_manager.py

## 核心功能

### 1. 账号管理 (AccountManager)

管理多个平台的账号信息，支持增删改查。

```python
import sys
sys.path.append('./tools')
import account_manager

mgr = account_manager.AccountManager()

# 添加账号
account_id = mgr.add_account(
    platform="wechat",
    username="user1",
    nickname="昵称",
    email="user@example.com"
)

# 列出账号
all_accounts = mgr.list_accounts()
wechat_accounts = mgr.list_accounts("wechat")

# 获取账号
account = mgr.get_account(account_id)

# 更新账号
mgr.update_account(account_id, status="inactive")

# 删除账号
mgr.remove_account(account_id)
```

### 2. 数据同步 (PlatformSync)

同步发布记录和互动数据。

```python
sync = account_manager.PlatformSync()

# 同步发布记录
posts = [
    {"post_id": "p1", "title": "文章标题", "status": "published"},
    {"post_id": "p2", "title": "另一篇", "status": "draft"}
]
sync.sync_posts(account_id, posts)

# 同步互动数据
stats = {
    "views": 1000,
    "likes": 50,
    "comments": 10,
    "shares": 5
}
sync.sync_stats(account_id, stats)

# 获取历史数据
posts = sync.get_posts(account_id)
stats_history = sync.get_stats_history(account_id)
```

### 3. 状态监控 (StatusMonitor)

监控账号登录状态和发布状态。

```python
monitor = account_manager.StatusMonitor(mgr)

# 检查登录状态
login_status = monitor.check_login_status(account_id)
# 返回: {"status": "active", "last_active": "...", "account_id": "..."}

# 检查发布状态
publish_status = monitor.check_publish_status(account_id, post_id)
# 返回: {"status": "published", "post_id": "...", "account_id": "..."}

# 获取账号摘要
summary = monitor.get_account_summary(account_id)
# 返回: {"account_id": "...", "platform": "...", "total_posts": 10, ...}
```

## 快速使用

### 快速添加账号
```python
account_id = account_manager.quick_add_account(
    "wechat", "username", nickname="昵称"
)
```

### 快速同步发布
```python
account_manager.quick_sync_post(
    account_id, "post_123", "文章标题",
    url="https://...", views=100
)
```

## 支持平台

- 微信公众号 (wechat)
- 知乎 (zhihu)
- 小红书 (xiaohongshu)
- 微博 (weibo)
- 抖音 (douyin)
- B站 (bilibili)

## 数据存储

所有数据存储在 `./account_data/` 目录：

- `accounts.json` - 账号信息
- `{account_id}_posts.json` - 发布记录
- `{account_id}_stats.json` - 互动数据历史

## 注意事项

1. **账号安全**：敏感信息（如密码、token）不应直接存储，建议使用引用方式
2. **数据备份**：定期备份 account_data 目录
3. **并发访问**：多进程访问时注意文件锁
4. **平台限制**：遵守各平台API调用频率限制
5. **隐私保护**：妥善处理用户数据，遵守隐私政策

## 典型场景

### 场景1：批量管理多个账号
```python
mgr = account_manager.AccountManager()

# 添加多个平台账号
platforms = ["wechat", "zhihu", "xiaohongshu"]
for platform in platforms:
    mgr.add_account(platform, f"user_{platform}")

# 查看所有账号
for account in mgr.list_accounts():
    print(f"{account['platform']}: {account['username']}")
```

### 场景2：跨平台数据统计
```python
sync = account_manager.PlatformSync()
monitor = account_manager.StatusMonitor(mgr)

total_posts = 0
total_views = 0

for account in mgr.list_accounts():
    account_id = f"{account['platform']}_{account['username']}"
    summary = monitor.get_account_summary(account_id)
    total_posts += summary.get("total_posts", 0)
    
    stats = sync.get_stats_history(account_id)
    if stats:
        total_views += stats[-1].get("views", 0)

print(f"总发布: {total_posts}篇, 总阅读: {total_views}")
```

### 场景3：定期数据同步
```python
# 配合scheduled_task_sop使用
def sync_all_accounts():
    mgr = account_manager.AccountManager()
    sync = account_manager.PlatformSync()
    
    for account in mgr.list_accounts():
        account_id = f"{account['platform']}_{account['username']}"
        # 从平台API获取最新数据
        # posts = fetch_posts_from_platform(account)
        # stats = fetch_stats_from_platform(account)
        # sync.sync_posts(account_id, posts)
        # sync.sync_stats(account_id, stats)
        pass
```

## 扩展开发

### 添加新平台支持
1. 在 add_account 时指定新平台名称
2. 实现平台特定的数据获取逻辑
3. 使用 web_scan/web_execute_js 进行web自动化

### 集成平台API
```python
# 示例：集成知乎API
def sync_zhihu_account(account_id):
    account = mgr.get_account(account_id)
    # 调用知乎API获取数据
    # posts = zhihu_api.get_articles(account['username'])
    # sync.sync_posts(account_id, posts)
    pass
```

---

**最后更新**: 2026-04-21 (R197账号管理)

[skill_mapping]
category: content_creation
skill: account_management
tools: account_manager.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('account_management_sop.md')
```