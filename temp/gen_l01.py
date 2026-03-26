import sys,os
sys.path.insert(0,"E:\\2026\\x-fudan\\new\\GenericAgent\\temp")
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
BASE="E:\\2026\\x-fudan\\new\\GenericAgent\\temp"
SD=os.path.join(BASE,"teaching_kb","courses","图神经网络与大语言模型","lessons","L01_GNN与LLM联合架构导论","slides")
os.makedirs(SD,exist_ok=True)
OUT=os.path.join(SD,"L01_GNN导论.pptx")
BL=RGBColor(0x1F,0x49,0x8B); LB=RGBColor(0x2E,0x75,0xB6); GR=RGBColor(0x59,0x59,0x59)
WH=RGBColor(0xFF,0xFF,0xFF); OR=RGBColor(0xED,0x7D,0x31); LG=RGBColor(0xDA,0xE8,0xFC)
LB2=RGBColor(0xBD,0xD7,0xEE); GN=RGBColor(0x37,0x86,0x44)
C=[BL,LB,RGBColor(0x25,0x6E,0xBF),RGBColor(0x17,0x5A,0x8E)]
prs=Presentation(); prs.slide_width=Inches(13.33); prs.slide_height=Inches(7.5)
blank=prs.slide_layouts[6]
def R(sl,l,t,w,h,fill=None,lc=None):
    sh=sl.shapes.add_shape(1,Inches(l),Inches(t),Inches(w),Inches(h))
    sh.line.fill.background()
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb=fill
    else: sh.fill.background()
    if lc: sh.line.color.rgb=lc; sh.line.width=Pt(1)
    return sh
def T(sl,tx,l,t,w,h,sz=16,bold=False,co=None,al=PP_ALIGN.LEFT):
    tb=sl.shapes.add_textbox(Inches(l),Inches(t),Inches(w),Inches(h))
    tb.word_wrap=True; tf=tb.text_frame; tf.word_wrap=True
    p=tf.paragraphs[0]; p.alignment=al; r=p.add_run(); r.text=tx
    r.font.size=Pt(sz); r.font.bold=bold; r.font.color.rgb=co or GR
    return tb
# S1 封面
s=prs.slides.add_slide(blank)
R(s,0,0,13.33,7.5,fill=BL); R(s,0,4.8,13.33,2.7,fill=LB)
T(s,"图神经网络与大语言模型",0.5,1.0,12.33,1.2,sz=38,bold=True,co=WH,al=PP_ALIGN.CENTER)
T(s,"L01  GNN与LLM联合架构导论",0.5,2.4,12.33,0.9,sz=26,co=LB2,al=PP_ALIGN.CENTER)
T(s,"论文: MASPOB — Bandit Prompt Optimization for MAS with GNN | 2026",0.5,3.4,12.33,0.7,sz=13,co=LB2,al=PP_ALIGN.CENTER)
T(s,"建议学时: 2学时  |  授课对象: 研究生",0.5,5.15,12.33,0.6,sz=16,co=WH,al=PP_ALIGN.CENTER)
print("S1")
# S2 教学目标
s=prs.slides.add_slide(blank)
R(s,0,0,13.33,1.1,fill=BL)
T(s,"教学目标",0.3,0.15,12,0.8,sz=26,bold=True,co=WH)
OB=["1  理解GNN基本概念与消息传播机制","2  了解LLM在多智能体MAS中的角色","3  掌握GNN+LLM结合核心动机：结构化关系+语言理解","4  描述MASPOB框架工作流程"]
[( R(s,0.5,1.3+i*1.45,12.33,1.2,fill=C[i]), T(s,OB[i],0.8,1.45+i*1.45,11.8,0.9,sz=17,co=WH) ) for i in range(4)]
print("S2")
# S3 大纲
s=prs.slides.add_slide(blank)
R(s,0,0,13.33,1.1,fill=LB)
T(s,"课程大纲",0.3,0.15,12,0.8,sz=26,bold=True,co=WH)
TP=[("01","图神经网络基础","节点/边/消息传递/GCN/GAT"),("02","LLM在多智能体中","Agent=LLM+Prompt;工作流固定"),("03","MASPOB框架","Bandit+GNN三步闭环"),("04","实验结果","性能提升与样本效率"),("05","架构展望","三种GNN+LLM范式"),("06","练习与总结","思考题与要点")]
for i,(n,ti,su) in enumerate(TP):
    x=0.35+(i%3)*4.3; y=1.35 if i<3 else 4.2
    R(s,x,y,4.0,2.7,fill=C[min(i,3)])
    T(s,n,x+0.15,y+0.12,0.7,0.55,sz=22,bold=True,co=WH)
    T(s,ti,x+0.15,y+0.72,3.7,0.6,sz=14,bold=True,co=WH)
    T(s,su,x+0.15,y+1.4,3.7,1.0,sz=11,co=LB2)
print("S3")
# S4 GNN基础
s=prs.slides.add_slide(blank)
R(s,0,0,13.33,1.1,fill=BL)
T(s,"01  图神经网络基础回顾",0.3,0.15,12,0.8,sz=24,bold=True,co=WH)
T(s,"图的基本元素",0.4,1.2,6,0.5,sz=17,bold=True,co=BL)
EL=[("节点 V","Agents/概念/实体；特征向量h_v"),("边 E","依赖/交互；可加权有向"),("图 G","G=(V,E,X)；结构+特征联合表示")]
for i,(nm,de) in enumerate(EL): R(s,0.4,1.75+i*1.0,6.0,0.85,fill=LG,lc=LB); T(s,nm,0.6,1.82+i*1.0,1.6,0.65,sz=14,bold=True,co=BL); T(s,de,2.3,1.82+i*1.0,3.9,0.65,sz=13)
T(s,"消息传递机制",6.7,1.2,6,0.5,sz=17,bold=True,co=BL)
R(s,6.7,1.75,6.3,1.35,fill=RGBColor(0xF0,0xF4,0xFF),lc=LB)
T(s,"h_v^(l+1)=UPDATE(h_v^(l), AGG({h_u^(l):u in N(v)}))",6.9,1.85,5.9,0.75,sz=13,bold=True,co=BL)
T(s,"AGG:Mean/Max/Sum/Attn | UPDATE:MLP/GRU | l层=l跳感受野",6.9,3.1,5.9,0.65,sz=12)
AR=[("GCN","谱域均值聚合,简单高效"),("GAT","注意力权重,可解释"),("GraphSAGE","归纳式,支持未见节点")]
for i,(nm,de) in enumerate(AR): R(s,0.4+i*4.25,5.0,4.0,2.2,fill=C[i]); T(s,nm,0.6+i*4.25,5.1,3.6,0.55,sz=17,bold=True,co=WH); T(s,de,0.6+i*4.25,5.75,3.6,1.2,sz=13,co=LB2)
print("S4")
s=prs.slides.add_slide(blank);R(s,0,0,13.33,1.1,fill=LB);T(s,'02  LLM在多智能体系统中的角色',0.3,0.15,12,0.8,sz=24,bold=True,co=WH)
for i,(ro,de) in enumerate([('Planner','规划'),('Researcher','检索'),('Writer','生成'),('Reviewer','审核')]):
    R(s,0.6+i*3.1,1.3,2.8,3.8,fill=[BL,RGBColor(0x25,0x60,0x5E),RGBColor(0x7B,0x3F,0x00),RGBColor(0x4A,0x00,0x30)][i])
    T(s,ro,0.7+i*3.1,1.4,2.6,0.65,sz=18,bold=True,co=WH,al=PP_ALIGN.CENTER)
    T(s,de,0.7+i*3.1,2.75,2.6,0.8,sz=12,co=WH,al=PP_ALIGN.CENTER)
print('S5')
s=prs.slides.add_slide(blank);R(s,0,0,13.33,1.1,fill=BL);T(s,'03  MASPOB框架精读',0.3,0.15,12,0.8,sz=24,bold=True,co=WH)
for i,(ti,de) in enumerate([('Step1 GNN编码','对MAS图编码生成节点向量'),('Step2 Bandit选择','UCB/Thompson平衡探索利用'),('Step3 评估执行','运行候选Prompt获取反馈'),('Step4 迭代更新','更新参数收敛最优Prompt')]):
    R(s,0.3+i*3.25,1.3,3.0,3.5,fill=C[i]);T(s,ti,0.45+i*3.25,1.45,2.7,0.85,sz=14,bold=True,co=WH,al=PP_ALIGN.CENTER);T(s,de,0.45+i*3.25,2.5,2.7,1.8,sz=12,co=LB2,al=PP_ALIGN.CENTER)
print('S6')
s=prs.slides.add_slide(blank);R(s,0,0,13.33,1.1,fill=LB);T(s,'04  实验结果',0.3,0.15,12,0.8,sz=24,bold=True,co=WH)
cd=ChartData();cd.categories=['HotpotQA','GSM8K','MMLU','ALFWorld']
cd.add_series('固定Prompt',(62.3,55.1,70.2,48.6));cd.add_series('随机搜索',(65.8,58.4,72.1,52.3));cd.add_series('MASPOB',(74.1,68.9,79.3,63.2))
ch=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.5),Inches(1.3),Inches(12),Inches(5.8),cd).chart
ch.has_title=True;ch.chart_title.text_frame.text='各基准任务准确率对比(%)';ch.series[2].format.fill.solid();ch.series[2].format.fill.fore_color.rgb=OR
print('S7')
s=prs.slides.add_slide(blank);R(s,0,0,13.33,1.1,fill=BL);T(s,'05  GNN+LLM联合架构展望',0.3,0.15,12,0.8,sz=24,bold=True,co=WH)
for i,(ti,de,fc) in enumerate([('范式一 GNN辅助LLM','结构化检索+知识图谱+RAG',BL),('范式二 LLM辅助GNN','自然语言特征生成冷启动',LB),('范式三 深度融合','联合训练端到端MASPOB',RGBColor(0x17,0x37,0x5E))]):
    R(s,0.4+i*4.25,1.3,4.0,4.5,fill=fc);T(s,ti,0.55+i*4.25,1.45,3.7,0.85,sz=16,bold=True,co=WH,al=PP_ALIGN.CENTER);T(s,de,0.55+i*4.25,2.5,3.7,3.0,sz=13,co=LB2,al=PP_ALIGN.CENTER)
print('S8')
s=prs.slides.add_slide(blank);R(s,0,0,13.33,1.1,fill=LB);T(s,'06  课堂练习与总结',0.3,0.15,12,0.8,sz=24,bold=True,co=WH)
for i,q in enumerate(['Q1 为什么随机搜索优化MAS Prompt效果差？GNN如何解决？','Q2 Bandit算法解决什么问题？UCB与Thompson各有何优缺点？','Q3 举例GNN辅助LLM与LLM辅助GNN范式应用场景区别。']):
    R(s,0.4,1.75+i*1.55,12,1.35,fill=LG,lc=LB);T(s,q,0.6,1.85+i*1.55,11.6,1.1,sz=14)
print('S9')
s=prs.slides.add_slide(blank);R(s,0,0,13.33,7.5,fill=BL);R(s,0,3.5,13.33,0.08,fill=LB)
T(s,'感谢聆听',0.5,1.2,12.33,1.2,sz=42,bold=True,co=WH,al=PP_ALIGN.CENTER)
T(s,'GNN + LLM = 结构感知 x 语言理解',0.5,2.6,12.33,0.8,sz=22,co=LB2,al=PP_ALIGN.CENTER)
T(s,'MASPOB | arXiv:2603.02630v1 | Zhi Hong et al. (2026)',0.5,3.8,12.33,0.6,sz=13,co=LB2,al=PP_ALIGN.CENTER)
T(s,'下次课: GNN变体深度解析 GCN/GAT/GraphSAGE代码实现',0.5,5.0,12.33,0.7,sz=16,co=WH,al=PP_ALIGN.CENTER)
print('S10')
prs.save(OUT)
print(f'SAVED {OUT} | {os.path.getsize(OUT)} bytes | {len(prs.slides)} slides')
