import json
import os

with open("e:/2026/x-fudan/new/GenericAgent/temp/skill_tree/skill_tree.json", "r", encoding="utf-8") as f:
    old_data = json.load(f)

# Define the new structure based on the table
categories_map = {
    "knowledge_management": [
        "research_paper_kb_sop.md", "paper_comparison_sop.md", "teaching_kb_sop.md", "asset_management_sop.md", "knowledge_tree.md"
    ],
    "document_generation": [
        "ppt_com_sop.md", "ppt_template_manager_sop.md", "word_processing_sop.md", "excel_processing_sop.md", "document_conversion_sop.md"
    ],
    "media_processing": [
        "video_processing_sop.md", "video_effects_advanced_sop.md", "audio_processing_sop.md", "audio_transcription_sop.md", "podcast_production_sop.md", "image_processing_sop.md", "subtitle_proofreading_sop.md"
    ],
    "content_creation": [
        "content_creation_sop.md", "ai_copywriting_sop.md", "platform_adaptation_sop.md", "content_production_workflow_sop.md", "content_publisher_sop.md", "account_management_sop.md", "community_management_sop.md", "live_streaming_sop.md", "trend_tracking_sop.md"
    ],
    "data_analysis": [
        "data_analysis_sop.md", "data_storytelling_sop.md", "media_analytics_sop.md", "media_dashboard_workflow_sop.md"
    ],
    "web_automation": [
        "web_automation_sop.md", "research_search_sop.md", "seo_optimization_sop.md"
    ],
    "system_monitoring": [
        "system_monitoring_sop.md", "log_analysis_sop.md"
    ],
    "meta_capability": [
        "adb_ui.py", "autonomous_operation_sop.md", "github_contribution_sop.md", "keychain.py", "ljqCtrl.py", "ljqCtrl_sop.md", "memory_cleanup_sop.md", "memory_management_sop.md", "ocr_utils.py", "plan_sop.md", "procmem_scanner.py", "procmem_scanner_sop.md", "scheduled_task_sop.md", "subagent.md", "tmwebdriver_sop.md", "ui_detect.py", "verify_sop.md", "vision_api.template.py", "vision_sop.md", "web_setup_sop.md"
    ]
}

new_data = {
    "version": "2.0",
    "last_updated": "2026-04-21",
    "skill_categories": {}
}

# flatten old skills
old_skills_list = []
for cat, skills in old_data.get("skill_categories", {}).items():
    for sk_key, sk_val in skills.items():
        old_skills_list.append((sk_key, sk_val))

def get_skill_name(filename):
    return filename.replace(".md", "").replace(".py", "").replace(".template", "")

for target_cat, items in categories_map.items():
    new_data["skill_categories"][target_cat] = {}
    for item in items:
        sk_name = get_skill_name(item)
        
        merged_tools = set()
        merged_functions = set()
        usage_count = 0
        last_used = "2026-04-20"
        
        # collect matching info from old tree
        for old_sk_key, old_sk_val in old_skills_list:
            match = False
            # exact match by SOP
            if old_sk_val.get("sop") == item:
                match = True
            # exact match by single tool in meta_capability
            if not old_sk_val.get("sop") and item in old_sk_val.get("tools", []):
                match = True
                
            if match:
                merged_tools.update(old_sk_val.get("tools", []))
                merged_functions.update(old_sk_val.get("functions", []))
                usage_count += old_sk_val.get("usage_count", 0)
                if old_sk_val.get("last_used") and old_sk_val.get("last_used") > last_used:
                    last_used = old_sk_val.get("last_used")
        
        # also add the item as sop or tool properly
        sop_val = item if item.endswith(".md") else ""
        if not item.endswith(".md"):
            merged_tools.add(item)
            
        new_data["skill_categories"][target_cat][sk_name] = {
            "sop": sop_val,
            "tools": sorted(list(merged_tools)),
            "functions": sorted(list(merged_functions)),
            "usage_count": usage_count,
            "last_used": last_used
        }

with open("e:/2026/x-fudan/new/GenericAgent/temp/skill_tree/skill_tree.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("skill_tree updated.")
