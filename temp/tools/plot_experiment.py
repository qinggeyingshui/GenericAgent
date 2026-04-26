"""
plot_experiment.py - 实验数据可视化

读取experiment_log.jsonl，生成趋势图：
1. 技能/工具数量变化
2. 类别覆盖率变化
3. 基尼系数变化（usage_count分布均匀度）
"""
import json
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

log_path = Path(__file__).parent / "experiment_log.jsonl"

if not log_path.exists():
    print(f"未找到实验日志: {log_path}")
    exit(1)

# 读取数据
data = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))

print(f"共 {len(data)} 条记录")

# 提取字段
r_numbers = [d["r_number"] for d in data]
total_skills = [d["total_skills"] for d in data]
total_tools = [d["total_tools"] for d in data]
category_coverage = [d["category_coverage"] for d in data]
gini = [d["gini_coefficient"] for d in data]

# 绘图
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Skill Tree实验数据趋势", fontsize=16)

# 1. 技能数量
axes[0, 0].plot(r_numbers, total_skills, marker="o", label="Skills")
axes[0, 0].set_xlabel("R Number")
axes[0, 0].set_ylabel("Count")
axes[0, 0].set_title("技能数量变化")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. 工具数量
axes[0, 1].plot(r_numbers, total_tools, marker="s", color="orange", label="Tools")
axes[0, 1].set_xlabel("R Number")
axes[0, 1].set_ylabel("Count")
axes[0, 1].set_title("工具数量变化")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. 类别覆盖率
axes[1, 0].plot(r_numbers, category_coverage, marker="^", color="green", label="Categories")
axes[1, 0].set_xlabel("R Number")
axes[1, 0].set_ylabel("Count")
axes[1, 0].set_title("类别覆盖率")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. 基尼系数
axes[1, 1].plot(r_numbers, gini, marker="d", color="red", label="Gini")
axes[1, 1].set_xlabel("R Number")
axes[1, 1].set_ylabel("Coefficient")
axes[1, 1].set_title("基尼系数（越低越均匀）")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("experiment_trends.png", dpi=150)
print("\n✓ 图表已保存: experiment_trends.png")
plt.show()