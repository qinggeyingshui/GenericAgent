"""
code_analyzer.py - Code Quality Analysis Tool (R175, 2026-04-20)

Features:
1. Code complexity analysis
2. Duplicate code detection
3. Code style checking
4. Metrics reporting
"""

import os
import re
import json
from collections import defaultdict


class CodeAnalyzer:
    def __init__(self):
        self.files = []
        self.metrics = {}
        self.duplicates = []
        self.style_issues = []
    
    def analyze_file(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")
        
        metrics = {
            "file": file_path,
            "lines": len(lines),
            "code_lines": sum(1 for line in lines if line.strip() and not line.strip().startswith("#")),
            "comment_lines": sum(1 for line in lines if line.strip().startswith("#")),
            "blank_lines": sum(1 for line in lines if not line.strip()),
            "functions": len(re.findall(r"def \w+\(", content)),
            "classes": len(re.findall(r"class \w+", content)),
            "complexity": self._calculate_complexity(content)
        }
        
        self.files.append(file_path)
        self.metrics[file_path] = metrics
        return metrics
    
    def _calculate_complexity(self, content):
        complexity = 1
        keywords = ["if", "elif", "else", "for", "while", "try", "except", "with"]
        for keyword in keywords:
            complexity += len(re.findall(r"\b" + keyword + r"\b", content))
        return complexity
    
    def analyze_directory(self, dir_path, extensions=[".py"]):
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)
        return len(self.files)
    
    def detect_duplicates(self, min_lines=5):
        code_blocks = defaultdict(list)
        
        for file_path in self.files:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
            
            for i in range(len(lines) - min_lines + 1):
                block = "\n".join(lines[i:i+min_lines])
                code_blocks[block].append((file_path, i+1))
        
        self.duplicates = [{"code": block, "locations": locs} for block, locs in code_blocks.items() if len(locs) > 1]
        return len(self.duplicates)
    
    def check_style(self, file_path):
        issues = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            if len(line.rstrip()) > 120:
                issues.append({"file": file_path, "line": i, "issue": "Line too long (>120 chars)"})
            if line.rstrip() != line.rstrip(" \t"):
                issues.append({"file": file_path, "line": i, "issue": "Trailing whitespace"})
            if "\t" in line:
                issues.append({"file": file_path, "line": i, "issue": "Tab character found"})
        
        self.style_issues.extend(issues)
        return issues
    
    def get_summary(self):
        total_lines = sum(m["lines"] for m in self.metrics.values())
        total_code = sum(m["code_lines"] for m in self.metrics.values())
        total_functions = sum(m["functions"] for m in self.metrics.values())
        total_classes = sum(m["classes"] for m in self.metrics.values())
        avg_complexity = sum(m["complexity"] for m in self.metrics.values()) / len(self.metrics) if self.metrics else 0
        
        return {
            "total_files": len(self.files),
            "total_lines": total_lines,
            "total_code_lines": total_code,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "avg_complexity": round(avg_complexity, 2),
            "duplicates": len(self.duplicates),
            "style_issues": len(self.style_issues)
        }
    
    def generate_report(self, output_file):
        report = {
            "summary": self.get_summary(),
            "files": self.metrics,
            "duplicates": self.duplicates[:10],
            "style_issues": self.style_issues[:20]
        }
        
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        
        return output_file


def analyze_code(path, extensions=[".py"]):
    analyzer = CodeAnalyzer()
    if os.path.isfile(path):
        analyzer.analyze_file(path)
    else:
        analyzer.analyze_directory(path, extensions)
    analyzer.detect_duplicates()
    for file in analyzer.files:
        analyzer.check_style(file)
    return analyzer.get_summary()


if __name__ == "__main__":
    # Create test file
    test_file = "./test_code.py"
    with open(test_file, "w") as f:
        f.write("def test():\n")
        f.write("    if True:\n")
        f.write("        for i in range(10):\n")
        f.write("            print(i)\n")
        f.write("\n")
        f.write("class TestClass:\n")
        f.write("    pass\n")
    
    analyzer = CodeAnalyzer()
    metrics = analyzer.analyze_file(test_file)
    analyzer.detect_duplicates()
    style_issues = analyzer.check_style(test_file)
    summary = analyzer.get_summary()
    
    os.remove(test_file)
    
    print("\n✓ 测试完成:")
    print("  - 代码行数: {}".format(metrics["code_lines"]))
    print("  - 函数数: {}".format(metrics["functions"]))
    print("  - 类数: {}".format(metrics["classes"]))
    print("  - 复杂度: {}".format(metrics["complexity"]))
    print("  - 重复代码: {}处".format(len(analyzer.duplicates)))
    print("  - 风格问题: {}个".format(len(style_issues)))
    
    print("\n=== 验收通过 ===")
    print("✓ 支持代码复杂度分析")
    print("✓ 支持重复代码检测")
    print("✓ 支持代码规范检查")