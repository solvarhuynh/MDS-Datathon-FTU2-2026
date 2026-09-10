# -*- coding: utf-8 -*-
"""
Slide 18 — SKU & HERO PRODUCTS. Render 3 PNG (full-base, weighted N=2600).
  1) sku_redocean.png   — BUMO ladder mọi variant: chanh = red ocean (top2=50.1%), Cozy Vải là fruit SKU duy nhất lọt top
  2) sku_herovai.png     — Fruit-only BUMO: Cozy Vải #1 fruit (8.5%) + convert P4W->BUMO 33% > fruit C2 29%
  3) sku_dao.png         — SKU#2 Đào: cầu thật & convert được (C2 Đào) vs Cozy Đào Sả còn ngủ -> headroom, gate CLT
Nguồn số: tính từ cleaned_dataset.xlsx (Q5.Bumo, Q4.P4W) — xem _sharpen_out*.txt
Palette đồng bộ charts_competitive.py.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GOLD_SOFT='#FBE9C7'
GREEN='#1B7A3D'; GREEN_DEEP='#0E5C2F'; GREEN_SOFT='#E4F1E9'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'
RED='#C2503A'; RED_SOFT='#F0D6CE'          # "red ocean" = chanh
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; WHITE='#FFFFFF'

_avail={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _avail),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,
                     'axes.edgecolor':BORDER,'savefig.dpi':220})

def _clean(ax):
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.tick_params(length=0)

# ============ 1) RED OCEAN — BUMO ladder mọi variant ============
def chart_redocean():
    # (label, BUMO%, bucket)  bucket: 'lemon' | 'hero' | 'fruit' | 'plain'
    data=[('OLong Tea+ Chanh',29.0,'lemon'),('C2 Chanh',21.2,'lemon'),
          ('Không Độ (plain)',17.3,'plain'),('Cozy Vải  ‹HERO›',8.5,'hero'),
          ('C2 Đào',5.2,'fruit'),('Không Độ Chanh',4.4,'lemon'),
          ('C2 Táo',3.1,'fruit'),('Boncha Chanh',1.4,'lemon'),
          ('Dr. Thanh',1.2,'plain'),('TH Olong',1.2,'fruit')]
    cmap={'lemon':RED,'hero':GOLD,'fruit':SAGE_M,'plain':SAGE_L}
    data=data[::-1]
    labels=[d[0] for d in data]; vals=[d[1] for d in data]; cols=[cmap[d[2]] for d in data]
    fig,ax=plt.subplots(figsize=(7.6,4.7))
    y=np.arange(len(data))
    ax.barh(y,vals,color=cols,height=0.64,zorder=3,
            edgecolor=[GOLD_DEEP if d[2]=='hero' else 'none' for d in data],
            linewidth=[2.2 if d[2]=='hero' else 0 for d in data])
    for yi,v,d in zip(y,vals,data):
        fw='bold' if d[2]=='hero' else 'normal'
        ax.text(v+0.5,yi,f'{v:.1f}%',va='center',fontsize=10,fontweight=fw,
                color=GOLD_DEEP if d[2]=='hero' else TEXT)
    ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=9.5)
    for t,d in zip(ax.get_yticklabels(),data):
        if d[2]=='hero': t.set_color(GOLD_DEEP); t.set_fontweight('bold')
        elif d[2]=='lemon': t.set_color(RED)
    ax.set_xlim(0,37); ax.set_xticks([]); _clean(ax)
    # bracket top-2 lemon = 50.1%
    i1=labels.index('OLong Tea+ Chanh'); i2=labels.index('C2 Chanh')
    ax.annotate('',xy=(32.5,i1),xytext=(32.5,i2),
                arrowprops=dict(arrowstyle='-',color=RED,lw=1.4))
    ax.text(33.2,(i1+i2)/2,'Top-2 BUMO\nđều là chanh\n= 50.1%',va='center',ha='left',
            fontsize=9,color=RED,fontweight='bold')
    leg=[Line2D([0],[0],marker='s',color='none',markerfacecolor=RED,markersize=11,label='Vị chanh (red ocean) · 56.9% BUMO'),
         Line2D([0],[0],marker='s',color='none',markerfacecolor=GOLD,markersize=11,label='Cozy Vải — fruit hero'),
         Line2D([0],[0],marker='s',color='none',markerfacecolor=SAGE_M,markersize=11,label='Fruit khác'),
         Line2D([0],[0],marker='s',color='none',markerfacecolor=SAGE_L,markersize=11,label='Plain/khác')]
    ax.legend(handles=leg,loc='lower right',fontsize=8.3,frameon=False,handletextpad=0.3,bbox_to_anchor=(1.0,-0.02))
    ax.set_title('Chanh là red ocean — Cozy Vải là vị trái cây DUY NHẤT lọt top BUMO',
                 fontsize=11.5,fontweight='bold',color=TEXT,loc='left',pad=10)
    fig.text(0.01,-0.02,'BUMO (Q5, weighted, N=2.600). Top-2 SKU chanh nắm nửa thị trường → Cozy không nên đối đầu chanh.',
             fontsize=8,color=SUB)
    fig.savefig('sku_redocean.png',bbox_inches='tight',transparent=True); plt.close(fig)

# ============ 2) HERO VẢI — fruit-only BUMO + conversion ============
def chart_herovai():
    fruit=[('Cozy Vải',8.5,True),('C2 Đào',5.2,False),('C2 Táo',3.1,False),
           ('C2 Hồng Trà Vải',0.6,False),('Cozy Đào Sả',0.4,'cozy2')]
    fruit=fruit[::-1]
    labels=[f[0] for f in fruit]; vals=[f[1] for f in fruit]
    cols=[GOLD if f[2]==True else (GOLD_SOFT if f[2]=='cozy2' else SAGE_M) for f in fruit]
    fig,(ax,ax2)=plt.subplots(1,2,figsize=(8.8,3.9),gridspec_kw={'width_ratios':[1.7,1]})
    y=np.arange(len(fruit))
    ax.barh(y,vals,color=cols,height=0.6,zorder=3,
            edgecolor=[GOLD_DEEP if f[2]==True else 'none' for f in fruit],
            linewidth=[2.2 if f[2]==True else 0 for f in fruit])
    for yi,v,f in zip(y,vals,fruit):
        ax.text(v+0.12,yi,f'{v:.1f}%',va='center',fontsize=10,
                fontweight='bold' if f[2]==True else 'normal',
                color=GOLD_DEEP if f[2]==True else TEXT)
    ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=9.5)
    ax.get_yticklabels()[labels.index('Cozy Vải')].set_color(GOLD_DEEP)
    ax.get_yticklabels()[labels.index('Cozy Vải')].set_fontweight('bold')
    ax.set_xlim(0,10); ax.set_xticks([]); _clean(ax)
    ax.set_title('#1 fruit BUMO toàn thị trường',fontsize=11,fontweight='bold',loc='left',pad=8)
    ax.text(0,-1.15,'Vị trái cây bán chạy nhất thị trường là của Cozy —\ncao hơn fruit mạnh nhất của C2 (Đào) 1,6 lần.',
            fontsize=8,color=SUB)
    # right: conversion efficiency BUMO/P4W
    conv=[('Tea+ Chanh',55,RED),('C2 Chanh',51,RED),('Cozy Vải',33,GOLD),('C2 Đào',29,SAGE_M),('C2 Táo',29,SAGE_M)]
    conv=conv[::-1]
    yl=[c[0] for c in conv]; cv=[c[1] for c in conv]; cc=[c[2] for c in conv]
    y2=np.arange(len(conv))
    ax2.barh(y2,cv,color=cc,height=0.6,zorder=3,
             edgecolor=[GOLD_DEEP if c[0]=='Cozy Vải' else 'none' for c in conv],
             linewidth=[2.2 if c[0]=='Cozy Vải' else 0 for c in conv])
    for yi,v,c in zip(y2,cv,conv):
        ax2.text(v+1,yi,f'{v}%',va='center',fontsize=9,
                 fontweight='bold' if c[0]=='Cozy Vải' else 'normal',
                 color=GOLD_DEEP if c[0]=='Cozy Vải' else TEXT)
    ax2.set_yticks(y2); ax2.set_yticklabels(yl,fontsize=9)
    ax2.get_yticklabels()[yl.index('Cozy Vải')].set_color(GOLD_DEEP)
    ax2.get_yticklabels()[yl.index('Cozy Vải')].set_fontweight('bold')
    ax2.set_xlim(0,68); ax2.set_xticks([]); _clean(ax2)
    ax2.set_title('Convert P4W → BUMO',fontsize=11,fontweight='bold',loc='left',pad=8)
    ax2.text(0,-1.15,'Vải convert tốt hơn mọi fruit của C2\n(33% > 29%), chỉ thua 2 mega-brand chanh.',
             fontsize=8,color=SUB)
    fig.suptitle('Hero Vải: vị trái cây mạnh & hiệu quả nhất — gánh 95% BUMO của Cozy',
                 fontsize=11.8,fontweight='bold',x=0.01,ha='left',y=1.04)
    fig.savefig('sku_herovai.png',bbox_inches='tight',transparent=True); plt.close(fig)

# ============ 3) SKU #2 ĐÀO — cầu thật, convert được, headroom ============
def chart_dao():
    fig,(axL,axR)=plt.subplots(1,2,figsize=(8.8,3.8),gridspec_kw={'width_ratios':[1,1.25]})
    # Left: demand cầu đào theo vùng
    regs=['Toàn quốc','South','Mekong','North','Central']
    dem=[22.8,32.2,17.8,22.7,14.0]
    colsd=[SAGE_M,GOLD,SAGE_L,SAGE_L,SAGE_L]
    x=np.arange(len(regs))
    axL.bar(x,dem,color=colsd,width=0.62,zorder=3)
    for xi,v in zip(x,dem):
        axL.text(xi,v+0.7,f'{v:.1f}%',ha='center',fontsize=9,fontweight='bold' if v==32.2 else 'normal',
                 color=GOLD_DEEP if v==32.2 else TEXT)
    axL.set_xticks(x); axL.set_xticklabels(regs,fontsize=8.6,rotation=0)
    axL.set_ylim(0,38); axL.set_yticks([]); _clean(axL)
    axL.set_title('Cầu vị Đào — fruit demand #2 sau Vải',fontsize=10.5,fontweight='bold',loc='left',pad=8)
    axL.text(0,-6.0,'Mạnh nhất ở South (32.2%) = đúng vùng pilot.',fontsize=8,color=SUB)
    # Right: proven-convertible (C2 Đào) vs Cozy Đào Sả còn ngủ
    cats=['P4W','BUMO']
    c2=[18.0,5.2]; cozy=[1.3,0.4]
    xx=np.arange(len(cats)); wd=0.34
    axR.bar(xx-wd/2,c2,width=wd,color=SAGE_D,zorder=3,label='C2 Đào (cầu đã convert)')
    axR.bar(xx+wd/2,cozy,width=wd,color=GOLD,zorder=3,label='Cozy Đào Sả (đang ngủ)')
    for xi,v in zip(xx-wd/2,c2): axR.text(xi,v+0.4,f'{v:.1f}%',ha='center',fontsize=9,color=SAGE_D,fontweight='bold')
    for xi,v in zip(xx+wd/2,cozy): axR.text(xi,v+0.4,f'{v:.1f}%',ha='center',fontsize=9,color=GOLD_DEEP,fontweight='bold')
    axR.set_xticks(xx); axR.set_xticklabels(cats,fontsize=9.5)
    axR.set_ylim(0,21); axR.set_yticks([]); _clean(axR)
    axR.legend(fontsize=8.2,frameon=False,loc='upper right')
    axR.set_title('Cầu đào convert ĐƯỢC — Cozy chưa khai thác',fontsize=10.5,fontweight='bold',loc='left',pad=8)
    # arrow headroom
    axR.annotate('',xy=(0+wd/2,17.0),xytext=(0+wd/2,2.2),
                 arrowprops=dict(arrowstyle='-|>',color=GOLD_DEEP,lw=1.8))
    axR.text(0+wd/2+0.07,9.5,'headroom\nrelaunch',fontsize=8.2,color=GOLD_DEEP,fontweight='bold',va='center')
    fig.suptitle('SKU #2 = Đào Sả: cầu thật & đã chứng minh convert (C2 Đào) — Cozy relaunch, gate CLT ≥70%',
                 fontsize=11,fontweight='bold',x=0.01,ha='left',y=1.04)
    fig.savefig('sku_dao.png',bbox_inches='tight',transparent=True); plt.close(fig)

if __name__=='__main__':
    chart_redocean(); chart_herovai(); chart_dao()
    print('saved: sku_redocean.png, sku_herovai.png, sku_dao.png')
