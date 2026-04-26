"""
batch_processor.py - Batch File Processing Workflow Tool (R167, 2026-04-20)

Features:
1. Batch rename
2. Format conversion
3. File organization
4. Custom rules and templates
"""

import os
import shutil
import re
from pathlib import Path


def batch_rename(directory, pattern, replacement, preview=True):
    """
    Batch rename files
    
    Args:
        directory: Target directory
        pattern: Regex pattern to match
        replacement: Replacement string
        preview: Preview mode (no actual changes)
    
    Returns:
        List of rename operations
    """
    operations = []
    
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_name = re.sub(pattern, replacement, filename)
            if new_name != filename:
                operations.append({
                    "old": filename,
                    "new": new_name,
                    "path": directory
                })
    
    if not preview:
        for op in operations:
            old_path = os.path.join(op["path"], op["old"])
            new_path = os.path.join(op["path"], op["new"])
            os.rename(old_path, new_path)
    
    return operations


def organize_by_extension(directory, target_dir=None, preview=True):
    """
    Organize files by extension
    
    Args:
        directory: Source directory
        target_dir: Target directory (default: same as source)
        preview: Preview mode
    
    Returns:
        Organization plan
    """
    if target_dir is None:
        target_dir = directory
    
    operations = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = Path(filename).suffix.lower().replace(".", "") or "no_extension"
            target_folder = os.path.join(target_dir, ext)
            
            operations.append({
                "file": filename,
                "from": directory,
                "to": target_folder
            })
    
    if not preview:
        for op in operations:
            os.makedirs(op["to"], exist_ok=True)
            src = os.path.join(op["from"], op["file"])
            dst = os.path.join(op["to"], op["file"])
            shutil.move(src, dst)
    
    return operations


def apply_template(template, variables):
    """
    Apply template with variables
    
    Args:
        template: Template string with {var} placeholders
        variables: Dict of variable values
    
    Returns:
        Processed string
    """
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result


def batch_process(directory, rules, preview=True):
    """
    Batch process files with custom rules
    
    Args:
        directory: Target directory
        rules: List of rule dicts
        preview: Preview mode
    
    Returns:
        Processing results
    """
    results = {
        "rename": [],
        "organize": [],
        "total": 0
    }
    
    for rule in rules:
        rule_type = rule.get("type")
        
        if rule_type == "rename":
            ops = batch_rename(
                directory,
                rule.get("pattern", ""),
                rule.get("replacement", ""),
                preview
            )
            results["rename"].extend(ops)
            results["total"] += len(ops)
        
        elif rule_type == "organize":
            ops = organize_by_extension(
                directory,
                rule.get("target_dir"),
                preview
            )
            results["organize"].extend(ops)
            results["total"] += len(ops)
    
    return results


if __name__ == "__main__":
    # Test
    test_dir = "./test_batch"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test files
    for i in range(3):
        open(os.path.join(test_dir, f"file_{i}.txt"), "w").close()
        open(os.path.join(test_dir, f"image_{i}.jpg"), "w").close()
    
    # Test rename
    rename_ops = batch_rename(test_dir, r"file_", "doc_", preview=True)
    print(f"Rename operations: {len(rename_ops)}")
    
    # Test organize
    organize_ops = organize_by_extension(test_dir, preview=True)
    print(f"Organize operations: {len(organize_ops)}")
    
    # Test batch process
    rules = [
        {"type": "rename", "pattern": r"file_", "replacement": "doc_"}
    ]
    results = batch_process(test_dir, rules, preview=True)
    print(f"Total operations: {results['total']}")
    
    # Cleanup
    shutil.rmtree(test_dir)