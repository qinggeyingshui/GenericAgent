import json
import os

tree_path = "e:/2026/x-fudan/new/GenericAgent/temp/skill_tree/skill_tree.json"

with open(tree_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cats = data.get("skill_categories", {})

# 1. Merge ppt_creation into presentation
if "document_generation" in cats:
    dg = cats["document_generation"]
    if "ppt_creation" in dg and "presentation" in dg:
        p1 = dg["presentation"]
        p2 = dg["ppt_creation"]
        p1["tools"] = sorted(list(set(p1.get("tools", []) + p2.get("tools", []))))
        p1["functions"] = sorted(list(set(p1.get("functions", []) + p2.get("functions", []))))
        p1["usage_count"] = p1.get("usage_count", 0) + p2.get("usage_count", 0)
        # Update last_used if p2 is newer
        if p2.get("last_used") and (not p1.get("last_used") or p2["last_used"] > p1["last_used"]):
            p1["last_used"] = p2["last_used"]
        del dg["ppt_creation"]
        print("Merged ppt_creation into presentation.")
        
    # Rename content_creation in document_generation to script_generation to avoid confusion
    if "content_creation" in dg:
        dg["script_generation"] = dg.pop("content_creation")
        print("Renamed document_generation.content_creation to script_generation.")

# 2. Merge subtitle into subtitle_proofreading
if "media_processing" in cats:
    mp = cats["media_processing"]
    if "subtitle" in mp and "subtitle_proofreading" in mp:
        s1 = mp["subtitle_proofreading"]
        s2 = mp["subtitle"]
        s1["tools"] = sorted(list(set(s1.get("tools", []) + s2.get("tools", []))))
        s1["functions"] = sorted(list(set(s1.get("functions", []) + s2.get("functions", []))))
        s1["usage_count"] = s1.get("usage_count", 0) + s2.get("usage_count", 0)
        del mp["subtitle"]
        print("Merged subtitle into subtitle_proofreading.")

with open(tree_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
