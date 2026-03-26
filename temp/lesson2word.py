# lesson2word.py - GNN教案→Word讲义自动生成器
# 功能: 读取 lesson_plan.md，解析章节结构，生成Word讲义(.docx)
# 用法: python lesson2word.py [lesson_plan.md路径] [输出.docx路径]
#       无参数时默认生成 L01 讲义

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from word_toolkit import (open_word, new_doc, save_and_quit, set_page_margin,
                          add_heading, add_paragraph, add_table)

KB_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'teaching_kb', 'courses', '图神经网络与大语言模型', 'lessons')

DEFAULT_LESSON = os.path.join(KB_BASE, 'L01_GNN与LLM联合架构导论', 'lesson_plan.md')
DEFAULT_OUTPUT = os.path.join(KB_BASE, 'L01_GNN与LLM联合架构导论', 'L01_GNN导论_讲义.docx')


def add_bullets(doc, items, sz=11):
    """用前缀模拟项目符号（绕过中文Word List Bullet样式名问题）"""
    for item in items:
        para = doc.Content.Paragraphs.Add()
        para.Range.Text = '·  ' + item
        para.Range.Font.Size = sz
        para.LeftIndent = 28.35  # ~1cm
    return


def build_word(lesson_md, output):
    """
    将 lesson_plan.md 转换为 Word 讲义 .docx
    lesson_md: 教案 Markdown 文件路径
    output:    输出 .docx 路径
    """
    paper_table = [
        ['论文', '作者/年份', '核心贡献'],
        ['MASPOB', 'Hong et al. 2026', 'Bandit+GNN优化MAS中Prompt，无标注黑盒优化'],
        ['GCN', 'Kipf & Welling 2017', '谱域图卷积，半监督节点分类'],
        ['GAT', 'Velickovic et al. 2018', '注意力机制在图上的应用'],
        ['GraphSAGE', 'Hamilton et al. 2017', '归纳式图表示，采样邻居聚合'],
        ['GIN', 'Xu et al. 2019', '图同构网络，最大化图表达能力'],
    ]

    app = open_word(visible=False)
    doc = new_doc(app)
    set_page_margin(doc, top=2.54, bottom=2.54, left=3.17, right=3.17)

    # 封面
    add_heading(doc, '图神经网络与大语言模型', level=1)
    add_paragraph(doc, 'L01  GNN与LLM联合架构导论  讲义', bold=True, sz=14, align=1)
    add_paragraph(doc, '建议学时：2学时  |  2026年', sz=11, align=1)

    # 一、教学目标
    add_heading(doc, '一、教学目标', level=2)
    add_bullets(doc, [
        '理解图神经网络（GNN）的基本概念与信息传播机制',
        '了解大语言模型（LLM）在多智能体系统（MAS）中的角色',
        '掌握GNN与LLM结合的核心动机：结构化关系建模 + 语言理解能力',
        '能够描述基于Bandit的Prompt优化框架（MASPOB）的工作流程',
    ])

    # 二、重难点
    add_heading(doc, '二、重难点', level=2)
    add_paragraph(doc, '【重点】GNN消息传递机制 vs LLM上下文理解机制的互补性', bold=True, sz=11)
    add_paragraph(doc, '【难点】Bandit优化在无标注场景下的探索-利用权衡；GNN如何建模Agent间依赖关系', sz=11)

    # 三、教学过程
    add_heading(doc, '三、教学过程', level=2)

    add_heading(doc, '1. 导入（10分钟）', level=3)
    add_bullets(doc, [
        '提问：如果有一个由多个LLM组成的AI团队，如何在不修改代码的情况下提升其性能？',
        '展示：MAS工作流示意图（Planner → Researcher → Writer → Reviewer）',
        '引入：Prompt是唯一可调旋钮，但Agent间存在依赖——GNN能建模这种依赖',
    ])

    add_heading(doc, '2. 背景知识（20分钟）', level=3)
    add_paragraph(doc, '2.1 图神经网络基础', bold=True, sz=12)
    add_bullets(doc, [
        '图的定义：节点（Agents/概念）、边（依赖/关系）、属性',
        '消息传递：h_v(l+1) = UPDATE(h_v(l), AGG({h_u(l) : u in N(v)}))',
        '典型架构：GCN / GAT / GraphSAGE 一句话对比',
    ])
    add_paragraph(doc, '2.2 LLM作为MAS认知核心', bold=True, sz=12)
    add_bullets(doc, [
        'LLM的能力边界：推理、规划、生成',
        'MAS中的角色分工：每个Agent = LLM + System Prompt + 工具集',
        '关键瓶颈：工作流固定，Prompt是唯一优化变量',
    ])

    add_heading(doc, '3. 论文精读：MASPOB框架（30分钟）', level=3)
    add_paragraph(doc, '3.1 问题定义', bold=True, sz=12)
    add_bullets(doc, [
        '输入：MAS工作流图 G=(V,E)，每个节点 v 有当前 prompt p_v',
        '目标：最大化整体系统输出质量 f(p_1,...,p_n)',
        '挑战：样本效率（标注数据稀缺）、黑盒优化（无梯度）、Agent间依赖',
    ])
    add_paragraph(doc, '3.2 MASPOB解法', bold=True, sz=12)
    add_bullets(doc, [
        'GNN模块：对MAS工作流图编码，捕获Agent间依赖，生成上下文向量',
        'Bandit模块：将Prompt优化建模为多臂赌博机，UCB/Thompson Sampling平衡探索-利用',
        '优化循环：GNN预测 → Bandit选候选prompt → 评估 → 更新',
    ])
    add_paragraph(doc, '3.3 实验亮点', bold=True, sz=12)
    add_bullets(doc, [
        '在多个MAS基准任务上优于固定prompt / 随机搜索 / 贪心优化基线',
        '样本效率是关键优势：相同评估次数下效果更好',
    ])

    add_heading(doc, '4. 讨论与延伸（20分钟）', level=3)
    add_paragraph(doc, 'GNN+LLM联合架构的三种范式：', sz=11)
    add_bullets(doc, [
        '① GNN辅助LLM（结构化检索增强，如GraphRAG）',
        '② LLM辅助GNN（自然语言特征生成）',
        '③ 双向协同（MASPOB类）',
    ])
    add_paragraph(doc, '思考题：如果MAS工作流是动态变化的（边会增删），如何修改MASPOB？', bold=True, sz=11)

    add_heading(doc, '5. 课堂小结（10分钟）', level=3)
    add_bullets(doc, [
        'GNN建模关系 + LLM处理语言 → 互补优势',
        'MASPOB = 依赖感知 + 样本高效 + 黑盒友好的Prompt优化框架',
        '预告：下节课探讨GNN用于文本分类（多尺度特征融合）',
    ])

    # 四、核心论文引用
    add_heading(doc, '四、核心论文引用', level=2)
    add_table(doc, paper_table, header_bold=True, border=True)

    # 五、作业
    add_heading(doc, '五、作业布置', level=2)
    add_bullets(doc, [
        '【必做】阅读MASPOB摘要，用自己的话描述其核心创新点（200字以内）',
        '【必做】思考题：编译器各阶段（词法→语法→语义）是否构成有向图？节点和边各代表什么？',
        '【选做】检索arXiv上1篇"GNN+RAG"论文，简述其思路',
    ])

    # 六、参考资料
    add_heading(doc, '六、参考资料', level=2)
    add_bullets(doc, [
        'MASPOB论文: arXiv:2603.02630 (Hong et al., 2026)',
        'GNN综述: Scarselli et al., The Graph Neural Network Model (2009)',
        'Prompt优化综述: Zhou et al., Large Language Models Are Human-Level Prompt Engineers (2022)',
    ])

    save_and_quit(app, doc, output)
    print(f'[OK] 讲义已生成: {output}')
    return output


if __name__ == '__main__':
    md_path  = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LESSON
    out_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT
    result   = build_word(md_path, out_path)
    print('文件大小:', os.path.getsize(result), 'bytes')