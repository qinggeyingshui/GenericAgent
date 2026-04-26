#!/usr/bin/env python3
"""quality_scorer_v2.py - v2: batch折线图+预警+建议"""
import re,html as H,json
from datetime import datetime
HIST=r"E:\2026\x-fudan\new\GenericAgent\temp\autonomous_reports\history.txt"
OUT=r"E:\2026\x-fudan\new\GenericAgent\temp\autonomous_reports\quality_report_v2.html"
TS={"产出":3,"探测+分析":2.5,"分析":2.5,"探测":2,"规划":2,"自身演进":3,
    "机制":2.5,"知识库填充":2.5,"环境":1.5,"案例":1.5,"冲浪":1,"设计":2,
    "维护":2,"知识库维护":2.5}
def parse(path):
    raw=open(path,encoding="utf-8").read()
    raw=re.sub(r"(?<!\n)(R\d{1,3}\s*[|])",r"\n\1",raw)
    raw=re.sub(r"(?<!\n)(\[R\d{1,3}\])",r"\n\1",raw)
    es=[]
    for line in raw.splitlines():
        m=re.match(r"\[?R(\d{1,3})\]?\s*[|]\s*(.+)",line.strip())
        if not m: continue
        p=[x.strip() for x in m.group(2).split("|")]; i=0; e={"num":int(m.group(1))}
        dm=re.match(r"(\d{4}-\d{2}-\d{2})",p[i]) if p else None
        if dm: e["date"]=dm.group(1);i+=1
        else: e["date"]=""
        e["type"]=p[i] if i<len(p) else "";i+=1
        e["title"]=p[i] if i<len(p) else "";i+=1
        e["desc"]=p[i] if i<len(p) else "";i+=1
        e["artifact"]=p[i] if i<len(p) else ""
        es.append(e)
    return es
def score(e):
    ps=TS.get(e["type"].strip(),1.5); d=e["desc"]+e["title"]; df=1.0
    if any(k in d for k in ["脚本","工具","自动","生成","分析","解析","HTML","JSON"]): df+=0.8
    if any(k in d for k in ["可视化","全量","批量","实测","多维"]): df+=0.7
    df=min(df,3.0); a=e["artifact"].strip()
    en=3.0 if len(a)>20 else(2.0 if len(a)>5 else(1.0 if a else 0.5))
    vf=2.5 if any(k in d for k in ["验收","实测","验证","通过","完成"]) else 1.0
    return {"ps":round(ps,1),"df":round(df,1),"en":round(en,1),"vf":round(vf,1),
            "total":min(round((ps+df+en+vf)/4*10/3,1),10.0)}
def batches(entries):
    bd={}
    for e in entries:
        bn=(e["num"]-1)//10+1; bk=f"B{bn}"
        if bk not in bd: bd[bk]={"es":[],"s":(bn-1)*10+1,"end":bn*10}
        bd[bk]["es"].append(e)
    res=[]
    for k in sorted(bd,key=lambda x:int(x[1:])):
        v=bd[k]; avgs=[e["sc"]["total"] for e in v["es"]]
        avg=round(sum(avgs)/len(avgs),2) if avgs else 0
        res.append({"k":k,"avg":avg,"n":len(v["es"]),
                    "low":sum(1 for s in avgs if s<5),
                    "high":sum(1 for s in avgs if s>=7),
                    "rng":f"R{v['s']:02d}-R{v['end']:02d}"})
    return res
def warns(bs):
    w=[]
    for b in bs[-3:]:
        if b["avg"]<5: w.append(f"[RED] {b['k']}({b['rng']}) 均分{b['avg']}低于5分警戒，低分{b['low']}条")
        elif b["avg"]<6: w.append(f"[WARN] {b['k']}({b['rng']}) 均分{b['avg']}偏低")
        if b["n"]>0 and b["low"]>=b["n"]*0.5:
            w.append(f"[RED] {b['k']} 超50%低分({b['low']}/{b['n']})")
    return w or ["最近3批无低分预警"]
def suggests(entries,bs):
    sg=[]; tc={}
    for e in entries: t=e["type"] or "未知"; tc[t]=tc.get(t,0)+1
    lv=sum(tc.get(t,0) for t in ["规划","冲浪","环境"])
    if lv>len(entries)*0.3: sg.append(f"低价值类型占{lv/len(entries)*100:.0f}%>30%，建议升级为复合任务")
    nv=sum(1 for e in entries if e["sc"]["vf"]<2)
    if nv>len(entries)*0.4: sg.append(f"{nv}条缺验收描述，建议补充'实测通过'关键词")
    na=sum(1 for e in entries if e["sc"]["en"]<1.5)
    if na>len(entries)*0.3: sg.append(f"{na}条缺产出文件，建议每任务交付可验证文件")
    if len(bs)>=2:
        tr=bs[-1]["avg"]-bs[-2]["avg"]
        if tr>0.5: sg.append(f"近两批质量上升+{tr:.1f}分，策略有效")
        elif tr<-0.5: sg.append(f"近两批质量下降{tr:.1f}分，审查TODO设计")
    ta={}
    for e in entries:
        t=e["type"] or "未知"
        if t not in ta: ta[t]=[]
        ta[t].append(e["sc"]["total"])
    if ta:
        best=max(ta,key=lambda t:sum(ta[t])/len(ta[t]))
        sg.append(f"最高价值类型：{best}(均{sum(ta[best])/len(ta[best]):.1f}分)，优先选择")
    return sg or ["暂无改进建议"]
def sb(v,mx=3,c="#4E79A7"):
    p=v/mx*100
    return(f'<span style="display:inline-block;background:#ddd;border-radius:2px;'
           f'width:80px;height:11px;vertical-align:middle">'
           f'<span style="display:block;background:{c};width:{p:.0f}%;height:100%;border-radius:2px"></span></span>')
def run(hist=HIST,out=OUT):
    es=parse(hist)
    for e in es: e["sc"]=score(e)
    es.sort(key=lambda x:x["num"]); n=len(es)
    avg=round(sum(e["sc"]["total"] for e in es)/n,2)
    low=[e for e in es if e["sc"]["total"]<5]
    hi=[e for e in es if e["sc"]["total"]>=7]
    top5=sorted(es,key=lambda x:x["sc"]["total"],reverse=True)[:5]
    bs=batches(es); ws=warns(bs); sgs=suggests(es,bs)
    bls=json.dumps([b["k"] for b in bs],ensure_ascii=False)
    bas=json.dumps([b["avg"] for b in bs])
    blos=json.dumps([b["low"] for b in bs])
    bhis=json.dumps([b["high"] for b in bs])
    def row(e):
        s=e["sc"]; tc="#59A14F" if s["total"]>=7 else("#EDC948" if s["total"]>=5 else"#E15759")
        return(f'<tr><td>R{e["num"]:02d}</td><td>{H.escape(e["type"])}</td>'
               f'<td>{H.escape(e["title"][:40])}</td>'
               f'<td>{sb(s["ps"])} {s["ps"]}</td><td>{sb(s["df"],c="#F28E2B")} {s["df"]}</td>'
               f'<td>{sb(s["en"],c="#76B7B2")} {s["en"]}</td><td>{sb(s["vf"],c="#59A14F")} {s["vf"]}</td>'
               f'<td style="font-weight:bold;color:{tc}">{s["total"]}</td></tr>')
    rows="".join(row(e) for e in es)
    top_li="".join(f'<li>R{e["num"]:02d}[{H.escape(e["type"])}] {H.escape(e["title"][:40])} — {e["sc"]["total"]}分</li>' for e in top5)
    low_li="".join(f'<li>R{e["num"]:02d}[{H.escape(e["type"])}] {H.escape(e["title"][:40])} — {e["sc"]["total"]}分</li>' for e in low[:10])
    warn_li="".join(f'<li style="color:{"#c0392b" if b.startswith("[") else "#27ae60"}">{H.escape(b)}</li>' for b in ws)
    sugg_li="".join(f'<li>{H.escape(s)}</li>' for s in sgs)
    rlbls={b["k"] for b in bs[-3:]}
    btbl=""
    for b in bs:
        ac="#59A14F" if b["avg"]>=7 else("#EDC948" if b["avg"]>=5 else"#E15759")
        bg=' style="background:#fffde7"' if b["k"] in rlbls else ""
        btbl+=(f'<tr{bg}><td>{b["k"]}</td><td>{b["rng"]}</td><td>{b["n"]}</td>'
               f'<td style="color:{ac};font-weight:bold">{b["avg"]}</td>'
               f'<td>{b["low"]}</td><td>{b["high"]}</td></tr>')
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    CSS=("body{font-family:'Microsoft YaHei',sans-serif;margin:20px;background:#f8f9fa;color:#333}"
         "h1{color:#2c3e50}h2{color:#34495e;border-left:4px solid #3498db;padding-left:8px;margin-top:26px}"
         "table{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:14px}"
         "th{background:#34495e;color:#fff;padding:7px 9px;font-size:13px;text-align:left}"
         "td{padding:5px 9px;border-bottom:1px solid #eee;font-size:12px}tr:hover{background:#eef5ff}"
         ".stat{display:inline-block;background:#fff;border-radius:8px;padding:12px 18px;margin:5px;"
         "box-shadow:0 1px 3px rgba(0,0,0,.1);text-align:center}"
         ".val{font-size:24px;font-weight:bold;color:#2c3e50}.lbl{font-size:11px;color:#888;margin-top:3px}"
         ".cw{background:#fff;border-radius:8px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:18px}"
         "ul{line-height:2}")
    html=(f'<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>质量报告v2</title>'
          f'<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'
          f'<style>{CSS}</style></head><body>'
          f'<h1>自主任务质量评分报告 v2</h1>'
          f'<p style="color:#888">生成:{now} | 共{n}条 | {len(bs)}批次</p>'
          f'<div>'
          f'<div class="stat"><div class="val">{n}</div><div class="lbl">总条目</div></div>'
          f'<div class="stat"><div class="val">{avg}</div><div class="lbl">平均分</div></div>'
          f'<div class="stat"><div class="val" style="color:#E15759">{len(low)}</div><div class="lbl">低分(&lt;5)</div></div>'
          f'<div class="stat"><div class="val" style="color:#59A14F">{len(hi)}</div><div class="lbl">高分(≥7)</div></div>'
          f'<div class="stat"><div class="val">{len(bs)}</div><div class="lbl">批次数</div></div>'
          f'</div>'
          f'<h2>批次趋势折线图</h2><div class="cw"><canvas id="bc" height="80"></canvas></div>'
          f'<script>new Chart(document.getElementById("bc").getContext("2d"),{{type:"line",'
          f'data:{{labels:{bls},datasets:['
          f'{{label:"批次均分",data:{bas},borderColor:"#3498db",backgroundColor:"rgba(52,152,219,0.07)",tension:0.3,pointRadius:5,fill:true}},'
          f'{{label:"低分数",data:{blos},borderColor:"#e74c3c",tension:0.3,pointRadius:4,yAxisID:"y2",fill:false}},'
          f'{{label:"高分数",data:{bhis},borderColor:"#27ae60",tension:0.3,pointRadius:4,yAxisID:"y2",fill:false}}'
          f']}},'
          f'options:{{responsive:true,plugins:{{legend:{{position:"top"}}}},'
          f'scales:{{y:{{min:0,max:10,title:{{display:true,text:"均分"}}}},y2:{{position:"right",min:0,title:{{display:true,text:"条目数"}},grid:{{drawOnChartArea:false}}}}}}}}}});</script>'
          f'<h2>最近3批预警</h2><ul>{warn_li}</ul>'
          f'<h2>批次统计（黄底=最近3批）</h2>'
          f'<table><thead><tr><th>批次</th><th>范围</th><th>条目</th><th>均分</th><th>低分</th><th>高分</th></tr></thead>'
          f'<tbody>{btbl}</tbody></table>'
          f'<h2>改进建议</h2><ul>{sugg_li}</ul>'
          f'<h2>Top5高分</h2><ul>{top_li}</ul>'
          f'<h2>低分条目(&lt;5分, 前10)</h2><ul>{low_li}</ul>'
          f'<h2>全部评分明细</h2>'
          f'<p style="font-size:11px;color:#888">个性化(类型)|难度(技术)|产出实体(artifact)|验收</p>'
          f'<table><thead><tr><th>编号</th><th>类型</th><th>标题</th><th>个性化</th><th>难度</th><th>实体</th><th>验收</th><th>总分</th></tr></thead>'
          f'<tbody>{rows}</tbody></table>'
          f'</body></html>')
    open(out,'w',encoding='utf-8').write(html)
    print(f"解析{n}条 | 平均{avg} | 低分{len(low)} | 高分{len(hi)}")
    print(f"报告: {out}")
if __name__=="__main__":
    run()
