"""多平台账号管理与数据同步"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class AccountManager:
    """账号管理器"""
    def __init__(self, data_dir: str = "./account_data"):
        self.data_dir = data_dir
        self.accounts_file = os.path.join(data_dir, "accounts.json")
        os.makedirs(data_dir, exist_ok=True)
        self._load_accounts()
    
    def _load_accounts(self):
        """加载账号数据"""
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {}
    
    def _save_accounts(self):
        """保存账号数据"""
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, ensure_ascii=False, indent=2)
    
    def add_account(self, platform: str, username: str, **kwargs) -> str:
        """添加账号"""
        account_id = f"{platform}_{username}"
        self.accounts[account_id] = {
            "platform": platform,
            "username": username,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            **kwargs
        }
        self._save_accounts()
        return account_id
    
    def remove_account(self, account_id: str) -> bool:
        """删除账号"""
        if account_id in self.accounts:
            del self.accounts[account_id]
            self._save_accounts()
            return True
        return False
    
    def list_accounts(self, platform: Optional[str] = None) -> List[Dict]:
        """列出账号"""
        accounts = list(self.accounts.values())
        if platform:
            accounts = [a for a in accounts if a["platform"] == platform]
        return accounts
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """获取账号信息"""
        return self.accounts.get(account_id)
    
    def update_account(self, account_id: str, **kwargs) -> bool:
        """更新账号信息"""
        if account_id in self.accounts:
            self.accounts[account_id].update(kwargs)
            self._save_accounts()
            return True
        return False

class PlatformSync:
    """平台数据同步"""
    def __init__(self, data_dir: str = "./account_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def sync_posts(self, account_id: str, posts: List[Dict]) -> str:
        """同步发布记录"""
        sync_file = os.path.join(self.data_dir, f"{account_id}_posts.json")
        
        # 加载现有记录
        existing = []
        if os.path.exists(sync_file):
            with open(sync_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        
        # 合并新记录
        existing_ids = {p.get("post_id") for p in existing}
        for post in posts:
            if post.get("post_id") not in existing_ids:
                existing.append(post)
        
        # 保存
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        
        return sync_file
    
    def sync_stats(self, account_id: str, stats: Dict) -> str:
        """同步互动数据"""
        stats_file = os.path.join(self.data_dir, f"{account_id}_stats.json")
        
        # 加载历史数据
        history = []
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # 添加新数据点
        stats["timestamp"] = datetime.now().isoformat()
        history.append(stats)
        
        # 保存
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        return stats_file
    
    def get_posts(self, account_id: str) -> List[Dict]:
        """获取发布记录"""
        sync_file = os.path.join(self.data_dir, f"{account_id}_posts.json")
        if os.path.exists(sync_file):
            with open(sync_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_stats_history(self, account_id: str) -> List[Dict]:
        """获取数据历史"""
        stats_file = os.path.join(self.data_dir, f"{account_id}_stats.json")
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

class StatusMonitor:
    """状态监控"""
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager
    
    def check_login_status(self, account_id: str) -> Dict:
        """检查登录状态"""
        account = self.account_manager.get_account(account_id)
        if not account:
            return {"status": "not_found"}
        
        # 简化版：基于最后活动时间判断
        last_active = account.get("last_active")
        if last_active:
            # 实际应用中需要调用平台API或web检测
            return {
                "status": "active",
                "last_active": last_active,
                "account_id": account_id
            }
        return {"status": "unknown", "account_id": account_id}
    
    def check_publish_status(self, account_id: str, post_id: str) -> Dict:
        """检查发布状态"""
        sync = PlatformSync(self.account_manager.data_dir)
        posts = sync.get_posts(account_id)
        
        for post in posts:
            if post.get("post_id") == post_id:
                return {
                    "status": post.get("status", "unknown"),
                    "post_id": post_id,
                    "account_id": account_id
                }
        
        return {"status": "not_found", "post_id": post_id}
    
    def get_account_summary(self, account_id: str) -> Dict:
        """获取账号摘要"""
        account = self.account_manager.get_account(account_id)
        if not account:
            return {}
        
        sync = PlatformSync(self.account_manager.data_dir)
        posts = sync.get_posts(account_id)
        stats_history = sync.get_stats_history(account_id)
        
        latest_stats = stats_history[-1] if stats_history else {}
        
        return {
            "account_id": account_id,
            "platform": account["platform"],
            "username": account["username"],
            "total_posts": len(posts),
            "latest_stats": latest_stats,
            "status": account.get("status", "unknown")
        }

def quick_add_account(platform: str, username: str, **kwargs) -> str:
    """快速添加账号"""
    mgr = AccountManager()
    return mgr.add_account(platform, username, **kwargs)

def quick_sync_post(account_id: str, post_id: str, title: str, **kwargs):
    """快速同步发布"""
    sync = PlatformSync()
    post = {
        "post_id": post_id,
        "title": title,
        "published_at": datetime.now().isoformat(),
        "status": "published",
        **kwargs
    }
    return sync.sync_posts(account_id, [post])

if __name__ == "__main__":
    print("账号管理工具")
    print("1. 账号管理: mgr = AccountManager()")
    print("2. 数据同步: sync = PlatformSync()")
    print("3. 状态监控: monitor = StatusMonitor(mgr)")
