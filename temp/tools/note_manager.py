"""
note_manager.py - Note Management & Knowledge Graph Tool (R168, 2026-04-20)

Features:
1. Markdown note management
2. Tag-based classification
3. Knowledge graph visualization
4. Search and link
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path


class NoteManager:
    def __init__(self, notes_dir="./notes"):
        self.notes_dir = notes_dir
        os.makedirs(notes_dir, exist_ok=True)
        self.index_file = os.path.join(notes_dir, ".index.json")
        self.index = self._load_index()
    
    def _load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"notes": {}, "tags": {}}
    
    def _save_index(self):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def create_note(self, title, content, tags=None):
        note_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "{}_{}".format(note_id, title) + ".md"
        filepath = os.path.join(self.notes_dir, filename)
        
        tags = tags or []
        tags_str = ", ".join(["#" + tag for tag in tags])
        
        note_lines = [
            "# {}\n\n".format(title),
            "Created: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "Tags: {}\n\n".format(tags_str),
            "---\n\n",
            content
        ]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(note_lines)
        
        self.index["notes"][note_id] = {
            "title": title,
            "filename": filename,
            "tags": tags,
            "created": datetime.now().isoformat()
        }
        
        for tag in tags:
            if tag not in self.index["tags"]:
                self.index["tags"][tag] = []
            self.index["tags"][tag].append(note_id)
        
        self._save_index()
        return note_id
    
    def search_by_tag(self, tag):
        note_ids = self.index["tags"].get(tag, [])
        return [self.index["notes"][nid] for nid in note_ids if nid in self.index["notes"]]
    
    def search_by_keyword(self, keyword):
        results = []
        for note_id, note_info in self.index["notes"].items():
            if keyword.lower() in note_info["title"].lower():
                results.append(note_info)
        return results
    
    def get_all_tags(self):
        return list(self.index["tags"].keys())
    
    def generate_graph(self, output_path="knowledge_graph.md"):
        lines = [
            "# Knowledge Graph\n\n",
            "Generated: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "## Tags\n\n"
        ]
        
        for tag, note_ids in self.index["tags"].items():
            lines.append("### #{} ({} notes)\n\n".format(tag, len(note_ids)))
            for note_id in note_ids:
                if note_id in self.index["notes"]:
                    note = self.index["notes"][note_id]
                    lines.append("- [{}]({})\n".format(note["title"], note["filename"]))
            lines.append("\n")
        
        graph_path = os.path.join(self.notes_dir, output_path)
        with open(graph_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        return graph_path


if __name__ == "__main__":
    import shutil
    nm = NoteManager("./test_notes")
    
    id1 = nm.create_note("视频创作灵感", "使用快节奏剪辑+热门BGM", ["创作", "视频"])
    id2 = nm.create_note("文案模板", "标题：数字+痛点+解决方案", ["创作", "文案"])
    id3 = nm.create_note("数据分析", "关注粉丝增长率和互动率", ["数据", "分析"])
    
    print("Created notes: {}, {}, {}".format(id1, id2, id3))
    
    results = nm.search_by_tag("创作")
    print("Tag search results: {}".format(len(results)))
    
    keyword_results = nm.search_by_keyword("视频")
    print("Keyword search results: {}".format(len(keyword_results)))
    
    graph = nm.generate_graph()
    print("Knowledge graph: {}".format(graph))
    
    shutil.rmtree("./test_notes")