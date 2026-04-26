"""
素材库管理工具
支持分类、标签、检索，基于SQLite
"""
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = Path(__file__).parent.parent / "assets.db"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 素材表
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL UNIQUE,
        category TEXT,
        description TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )''')
    
    # 标签表
    c.execute('''CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    
    # 素材-标签关联表
    c.execute('''CREATE TABLE IF NOT EXISTS asset_tags (
        asset_id INTEGER,
        tag_id INTEGER,
        FOREIGN KEY (asset_id) REFERENCES assets(id),
        FOREIGN KEY (tag_id) REFERENCES tags(id),
        PRIMARY KEY (asset_id, tag_id)
    )''')
    
    conn.commit()
    conn.close()

def add_asset(path: str, category: str = None, description: str = None, tags: List[str] = None) -> int:
    """添加素材"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    try:
        c.execute('''INSERT INTO assets (path, category, description, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)''', (path, category, description, now, now))
        asset_id = c.lastrowid
        
        # 添加标签
        if tags:
            for tag in tags:
                c.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag,))
                c.execute('SELECT id FROM tags WHERE name = ?', (tag,))
                tag_id = c.fetchone()[0]
                c.execute('INSERT INTO asset_tags (asset_id, tag_id) VALUES (?, ?)', (asset_id, tag_id))
        
        conn.commit()
        return asset_id
    except sqlite3.IntegrityError:
        return -1
    finally:
        conn.close()

def update_asset(asset_id: int, category: str = None, description: str = None, tags: List[str] = None):
    """更新素材"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    if category is not None:
        c.execute('UPDATE assets SET category = ?, updated_at = ? WHERE id = ?', (category, now, asset_id))
    if description is not None:
        c.execute('UPDATE assets SET description = ?, updated_at = ? WHERE id = ?', (description, now, asset_id))
    
    if tags is not None:
        # 清除旧标签
        c.execute('DELETE FROM asset_tags WHERE asset_id = ?', (asset_id,))
        # 添加新标签
        for tag in tags:
            c.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag,))
            c.execute('SELECT id FROM tags WHERE name = ?', (tag,))
            tag_id = c.fetchone()[0]
            c.execute('INSERT INTO asset_tags (asset_id, tag_id) VALUES (?, ?)', (asset_id, tag_id))
    
    conn.commit()
    conn.close()

def delete_asset(asset_id: int):
    """删除素材"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('DELETE FROM asset_tags WHERE asset_id = ?', (asset_id,))
    c.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
    
    conn.commit()
    conn.close()

def search_assets(keyword: str = None, category: str = None, tags: List[str] = None) -> List[Dict]:
    """检索素材"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = 'SELECT DISTINCT a.* FROM assets a'
    conditions = []
    params = []
    
    if tags:
        query += ' JOIN asset_tags at ON a.id = at.asset_id JOIN tags t ON at.tag_id = t.id'
        conditions.append(f't.name IN ({",".join(["?"] * len(tags))})')
        params.extend(tags)
    
    if keyword:
        conditions.append('(a.path LIKE ? OR a.description LIKE ?)')
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    
    if category:
        conditions.append('a.category = ?')
        params.append(category)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    c.execute(query, params)
    
    results = []
    for row in c.fetchall():
        asset = {
            'id': row[0],
            'path': row[1],
            'category': row[2],
            'description': row[3],
            'created_at': row[4],
            'updated_at': row[5]
        }
        
        # 获取标签
        c.execute('''SELECT t.name FROM tags t
                    JOIN asset_tags at ON t.id = at.tag_id
                    WHERE at.asset_id = ?''', (asset['id'],))
        asset['tags'] = [r[0] for r in c.fetchall()]
        
        results.append(asset)
    
    conn.close()
    return results

def get_asset(asset_id: int) -> Optional[Dict]:
    """获取单个素材"""
    results = search_assets()
    for asset in results:
        if asset['id'] == asset_id:
            return asset
    return None

def list_categories() -> List[str]:
    """列出所有分类"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT DISTINCT category FROM assets WHERE category IS NOT NULL')
    categories = [r[0] for r in c.fetchall()]
    conn.close()
    return categories

def list_tags() -> List[str]:
    """列出所有标签"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name FROM tags')
    tags = [r[0] for r in c.fetchall()]
    conn.close()
    return tags

def batch_import(directory: str, category: str = None, default_tags: List[str] = None):
    """批量导入目录下的文件"""
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    imported = []
    for file_path in dir_path.rglob('*'):
        if file_path.is_file():
            asset_id = add_asset(str(file_path), category=category, tags=default_tags)
            if asset_id > 0:
                imported.append(str(file_path))
    
    return imported
