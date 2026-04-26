# knowledge_graph.py
"""
GNN论文概念知识图谱生成器

用法:
  python knowledge_graph.py                    # 生成完整图谱
  python knowledge_graph.py --year 2024        # 按年份过滤
  python knowledge_graph.py --venue NeurIPS    # 按会议过滤
  python knowledge_graph.py --keyword GNN      # 按关键词过滤
  python knowledge_graph.py --output my.html   # 自定义输出路径

输出: gnn_knowledge_graph.html (可在浏览器直接打开)
"""
import re, os, sys, argparse
from collections import Counter, defaultdict
import networkx as nx
from pyvis.network import Network

# ─── 路径配置 ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))  # GenericAgent/
PAPERS_MD = os.path.join(ROOT_DIR, "gnn_papers", "PAPERS.md")
OUTPUT_HTML = os.path.join(BASE_DIR, "gnn_knowledge_graph.html")

# ─── 颜色配置（节点类型） ────────────────────────────────────────────
COLOR = {
    "paper":   "#4A90D9",  # 蓝色 - 论文
    "keyword": "#E8A838",  # 橙色 - 关键词/概念
    "year":    "#5CB85C",  # 绿色 - 年份
    "venue":   "#9B59B6",  # 紫色 - 会议/来源
}
SIZE = {"paper": 25, "keyword": 15, "year": 20, "venue": 18}

# ─── PAPERS.md 解析器 ───────────────────────────────────────────────
def parse_block(block):
    paper = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^(summary|applications|relevance):\s*>\s*$", line):
            key = line.split(":")[0].strip()
            val_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                val_lines.append(lines[i].strip())
                i += 1
            paper[key] = " ".join(v for v in val_lines if v)
            continue
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            if val.startswith("["):
                items = re.findall(r'"([^"]+)"', val)
                paper[key] = items
            else:
                paper[key] = val
        i += 1
    return paper


def load_papers(path=PAPERS_MD):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"\n---\n", content)
    papers = []
    for block in blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        p = parse_block(block)
        if p.get("id") and p.get("title") and "QUICK_START" not in p.get("id", ""):
            # 过滤明显错误年份
            yr = str(p.get("year", ""))
            if yr.isdigit() and 2000 <= int(yr) <= 2030:
                papers.append(p)
            elif not yr.isdigit():
                papers.append(p)
    return papers


# ─── 图构建 ──────────────────────────────────────────────────────────
def build_graph(papers, filter_year=None, filter_venue=None, filter_keyword=None):
    """构建论文-关键词-年份-会议多类型知识图谱"""
    # 应用过滤
    if filter_year:
        papers = [p for p in papers if str(p.get("year","")) == str(filter_year)]
    if filter_venue:
        papers = [p for p in papers if filter_venue.lower() in p.get("venue","").lower()]
    if filter_keyword:
        fk = filter_keyword.lower()
        papers = [p for p in papers if any(fk in k.lower() for k in p.get("keywords",[]))]

    G = nx.Graph()

    # 统计关键词共现
    kw_cooccur = defaultdict(int)
    kw_paper_count = Counter()

    for p in papers:
        pid = p["id"]
        title = p.get("title", pid)
        year = str(p.get("year", ""))
        venue = p.get("venue", "")
        kws = p.get("keywords", [])
        if not isinstance(kws, list):
            kws = []

        # 论文节点
        G.add_node(pid, label=pid, title=f"{title}\n年份:{year}\n会议:{venue}",
                   group="paper", color=COLOR["paper"], size=SIZE["paper"],
                   node_type="paper", year=year, venue=venue)

        # 年份节点
        if year:
            ynode = f"Y:{year}"
            if not G.has_node(ynode):
                G.add_node(ynode, label=year, title=f"年份: {year}",
                           group="year", color=COLOR["year"], size=SIZE["year"],
                           node_type="year")
            G.add_edge(pid, ynode, weight=1, title="发表于")

        # 会议节点（简化名称）
        if venue:
            vshort = venue.split(" ")[0] if len(venue) > 15 else venue
            vnode = f"V:{vshort}"
            if not G.has_node(vnode):
                G.add_node(vnode, label=vshort, title=f"会议: {venue}",
                           group="venue", color=COLOR["venue"], size=SIZE["venue"],
                           node_type="venue")
            G.add_edge(pid, vnode, weight=1, title="发表于")

        # 关键词节点 + 论文-关键词边
        for kw in kws:
            knode = f"K:{kw}"
            kw_paper_count[kw] += 1
            if not G.has_node(knode):
                G.add_node(knode, label=kw, title=f"关键词: {kw}",
                           group="keyword", color=COLOR["keyword"],
                           size=SIZE["keyword"], node_type="keyword")
            G.add_edge(pid, knode, weight=1, title=f"论文包含关键词: {kw}")

        # 关键词共现边
        for i in range(len(kws)):
            for j in range(i+1, len(kws)):
                k1, k2 = f"K:{kws[i]}", f"K:{kws[j]}"
                if G.has_edge(k1, k2):
                    G[k1][k2]["weight"] += 1
                else:
                    G.add_edge(k1, k2, weight=1, title=f"共现于同一论文")

    # 根据出现频次调整关键词节点大小
    for kw, cnt in kw_paper_count.items():
        knode = f"K:{kw}"
        if G.has_node(knode):
            G.nodes[knode]["size"] = 10 + cnt * 5
            G.nodes[knode]["title"] += f"\n出现次数: {cnt}"

    return G


# ─── 研究簇分析 ──────────────────────────────────────────────────────
def detect_clusters(G):
    """用greedy_modularity社区检测识别核心研究簇"""
    from networkx.algorithms import community as nx_comm
    # 只在关键词子图上做社区检测
    kw_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "keyword"]
    kw_subgraph = G.subgraph(kw_nodes).copy()
    # 按度排序找核心关键词
    degrees = dict(kw_subgraph.degree())
    top_kws = set(sorted(degrees, key=degrees.get, reverse=True)[:15])
    # 用greedy_modularity社区检测
    try:
        comms = list(nx_comm.greedy_modularity_communities(kw_subgraph))
    except Exception:
        comms = list(nx.connected_components(kw_subgraph))
    clusters = []
    for comp in sorted(comms, key=len, reverse=True)[:6]:
        comp_set = set(comp)
        core = [n for n in comp_set if n in top_kws]
        core = sorted(core, key=lambda n: degrees.get(n,0), reverse=True)[:3]
        if len(comp_set) >= 2:
            clusters.append({"size": len(comp_set), "core": core,
                             "members": list(comp_set)[:8]})
    return clusters


# ─── pyvis 可视化 ────────────────────────────────────────────────────
def generate_html(G, output_path=OUTPUT_HTML, title="GNN论文概念知识图谱"):
    """生成交互式HTML知识图谱"""
    net = Network(
        height="800px", width="100%",
        bgcolor="#1a1a2e", font_color="#ffffff",
        notebook=False
    )
    net.barnes_hut(gravity=-8000, central_gravity=0.3,
                   spring_length=150, spring_strength=0.05)

    # 添加节点
    for node, attrs in G.nodes(data=True):
        net.add_node(
            node,
            label=attrs.get("label", node),
            title=attrs.get("title", node),
            color=attrs.get("color", "#888888"),
            size=attrs.get("size", 15),
            group=attrs.get("group", "default")
        )

    # 添加边
    for u, v, attrs in G.edges(data=True):
        w = attrs.get("weight", 1)
        net.add_edge(u, v, title=attrs.get("title",""),
                     width=min(w * 1.5, 8), color="#555577")

    # 注入图例和过滤控件HTML
    legend_html = """
    <div style="position:fixed;top:10px;left:10px;background:#2a2a4e;
         padding:12px;border-radius:8px;color:#fff;font-size:13px;z-index:999;">
      <b>GNN论文知识图谱</b><br>
      <span style="color:#4A90D9">&#9679;</span> 论文 &nbsp;
      <span style="color:#E8A838">&#9679;</span> 关键词<br>
      <span style="color:#5CB85C">&#9679;</span> 年份 &nbsp;
      <span style="color:#9B59B6">&#9679;</span> 会议<br>
      <small>节点可拖拽 | 滚轮缩放 | 悬停查看详情</small>
    </div>"""

    net.set_options("""
    var options = {
      "nodes": {"borderWidth": 2, "shadow": true},
      "edges": {"smooth": {"type": "continuous"}, "shadow": false},
      "interaction": {"hover": true, "tooltipDelay": 100,
                      "navigationButtons": true, "keyboard": true},
      "physics": {"stabilization": {"iterations": 200}}
    }""")

    net.save_graph(output_path)

    # 注入图例到HTML
    with open(output_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("<body>", "<body>" + legend_html)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


# ─── CLI 主函数 ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="GNN论文概念知识图谱生成器")
    parser.add_argument("--year", help="按年份过滤, 如 2024")
    parser.add_argument("--venue", help="按会议过滤, 如 NeurIPS")
    parser.add_argument("--keyword", help="按关键词过滤, 如 GNN")
    parser.add_argument("--output", default=OUTPUT_HTML, help="输出HTML路径")
    parser.add_argument("--stats", action="store_true", help="只显示统计信息")
    args = parser.parse_args()

    print("加载论文库...")
    papers = load_papers()
    print(f"  共 {len(papers)} 篇论文")

    print("构建知识图谱...")
    G = build_graph(papers, filter_year=args.year,
                    filter_venue=args.venue, filter_keyword=args.keyword)

    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()
    print(f"  节点数: {n_nodes}")
    print(f"  边数:   {n_edges}")

    # 研究簇分析
    print("\n识别研究簇...")
    clusters = detect_clusters(G)
    for i, c in enumerate(clusters, 1):
        core_labels = [n.replace("K:","") for n in c["core"]]
        sz = c["size"]
        print(f"  簇{i}: {sz}个关键词节点, 核心: {core_labels}")

    if args.stats:
        return

    print(f"\n生成HTML可视化...")
    out = generate_html(G, output_path=args.output)
    print(f"  已保存: {out}")
    print(f"  请用浏览器打开上述文件查看交互式图谱")


if __name__ == "__main__":
    main()
