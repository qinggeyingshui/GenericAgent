import json
import os

target_files = [
    "adb_ui.py", "autonomous_operation_sop.md", "github_contribution_sop.md",
    "keychain.py", "ljqCtrl.py", "ljqCtrl_sop.md", "memory_cleanup_sop.md",
    "memory_management_sop.md", "ocr_utils.py", "plan_sop.md", "procmem_scanner.py",
    "procmem_scanner_sop.md", "scheduled_task_sop.md", "subagent.md", "tmwebdriver_sop.md",
    "ui_detect.py", "verify_sop.md", "vision_api.template.py", "vision_sop.md", "web_setup_sop.md"
]

with open("e:/2026/x-fudan/new/GenericAgent/temp/skill_tree/skill_tree.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Find any skill that uses any of these target_files and move it to meta_capability
meta_cap = data["skill_categories"].setdefault("meta_capability", {})

# Strategy:
# For each file, we want to ensure it is in meta_capability. 
# We'll create logic to group files into skills safely.
# If a file is an SOP, we create/find a skill and set it.
# Let's map target files to logical subcategory names inside meta_capability

mapping = {
    "adb_ui.py": "device_control",
    "autonomous_operation_sop.md": "autonomous_operation",
    "github_contribution_sop.md": "github_contribution",
    "keychain.py": "credential_management",
    "ljqCtrl.py": "keyboard_mouse_control",
    "ljqCtrl_sop.md": "keyboard_mouse_control",
    "memory_cleanup_sop.md": "memory_cleanup",
    "memory_management_sop.md": "memory_management",
    "ocr_utils.py": "ocr_capability",
    "plan_sop.md": "planning",
    "procmem_scanner.py": "process_memory_scanner",
    "procmem_scanner_sop.md": "process_memory_scanner",
    "scheduled_task_sop.md": "scheduled_task",
    "subagent.md": "subagent_management",
    "tmwebdriver_sop.md": "browser_control",
    "ui_detect.py": "ui_detection",
    "verify_sop.md": "verification",
    "vision_api.template.py": "vision_api",
    "vision_sop.md": "vision_capability",
    "web_setup_sop.md": "web_setup",
}

# Create missing skills under meta_capability
for f, skill_name in mapping.items():
    if skill_name not in meta_cap:
        meta_cap[skill_name] = {
            "sop": "",
            "tools": [],
            "functions": [],
            "usage_count": 0,
            "last_used": "2026-04-20"
        }
    
    # Assign the file
    if f.endswith(".md"):
        meta_cap[skill_name]["sop"] = f
    else:
        if f not in meta_cap[skill_name]["tools"]:
            meta_cap[skill_name]["tools"].append(f)

# Now, we also need to remove these files / skills from OTHER categories
for cat_name, cat_data in list(data["skill_categories"].items()):
    if cat_name == "meta_capability":
        continue
    
    for skill_name, skill_data in list(cat_data.items()):
        # Check if the sop is in target_files
        if skill_data.get("sop") in target_files:
            skill_data["sop"] = ""
            
        # Check if tools have target files
        skill_data["tools"] = [t for t in skill_data.get("tools", []) if t not in target_files]
        
        # If both SOP and Tools are empty and we just stripped them, maybe delete the skill? Or just leave it.

with open("e:/2026/x-fudan/new/GenericAgent/temp/skill_tree/skill_tree.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("done")
