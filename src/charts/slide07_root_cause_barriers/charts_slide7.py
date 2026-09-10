"""
SLIDE 7 — ROOT CAUSE / CONVERSION BARRIER.
Flow: (1) mini funnel — điểm rơi ở conversion → (2) vì sao không chọn = BARRIER.
Đọc thẳng cleaned_dataset.xlsx → 2 chart:
  1) s7_minifunnel.png  — Aware 91.8 → Consid 34.7 → P4W 25.8 → BUMO 8.8 + leakage Aware→Consid
  2) s7_barriers.png    — top 5 lý do KHÔNG chọn Cozy, gom nhóm (≈55% là VỊ)
PRIMARY. Palette xanh-vàng Cozy. Chạy: python charts_slide7.py
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

_HERE = os.path.dirname(os.path.abspath(__file__))
def _get_data_path():
    for c in [
        os.path.join(_HERE, '..', '..', '..', 'data', 'processed', 'cleaned_dataset.xlsx'),
        os.path.join(_HERE, '..', 'cleaned_dataset.xlsx'),
        os.path.join(os.getcwd(), 'data', 'processed', 'cleaned_dataset.xlsx'),
        os.path.join(os.getcwd(), 'cleaned_dataset.xlsx')
    ]:
        if os.path.exists(c):
            return os.path.abspath(c)
    return os.path.abspath(os.path.join(_HERE, '..', '..', '..', 'data', 'processed', 'cleaned_dataset.xlsx'))

_DATA = _get_data_path()
def _out(n): return os.path.join(_HERE, n)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; AMBER='#E0902E'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'
RED='#D9534F'; TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name="Dataset_Clean")

def cozy_metric(prefix):
    cols = [c for c in df.columns if c.startswith(prefix) and 'cozy' in c.lower()]
    return round((df[cols].fillna(0).astype(float).sum(axis=1) > 0).mean()*100, 1)

FUNNEL = {
    'Awareness': cozy_metric('Q1Q2. Total aided awareness_'),
    'Consideration': cozy_metric('Q4Q8.BRAND CONSIDERATION SET_'),
    'P4W Usage': cozy_metric('Q4. P4W_'),
    'BUMO': round(df['Q5.Bumo'].astype(str).str.contains('Cozy', case=False, na=False).mean()*100, 1),
}


def mini_funnel():
    steps = list(FUNNEL.items())
    fig, ax = plt.subplots(figsize=(8.6, 3.7))
    y = np.arange(len(steps))[::-1]
    for i, (lab, v) in enumerate(steps):
        col = RED if lab == 'Consideration' else GOLD
        ax.add_patch(FancyBboxPatch((0, y[i]-0.36), v, 0.72, boxstyle='round,pad=0,rounding_size=0.12',
                     fc=col, ec='none', zorder=3))
        ax.text(v+1.5, y[i], f'{v:.1f}%', va='center', fontsize=13, fontweight='bold',
                color=(RED if col == RED else GOLD_DEEP), zorder=4)
        ax.text(-1.5, y[i], lab, va='center', ha='right', fontsize=11.5,
                fontweight=('bold' if col == RED else 'normal'), color=TEXT, zorder=4)
        if i > 0:
            drop = steps[i-1][1] - v
            ax.text(v+9.5, (y[i-1]+y[i])/2, f'−{drop:.0f}pp', va='center', ha='left',
                    fontsize=9, color=(RED if i == 1 else SUB), fontweight='bold', zorder=4)
    ax.text(60, y[1], 'BIGGEST LEAKAGE\nAwareness → Consideration\nbiết Cozy nhưng không cân nhắc (mất ~⅔)',
            fontsize=10, fontweight='bold', color=RED, va='center', ha='left', linespacing=1.35)
    ax.set_xlim(-22, 118); ax.set_ylim(-0.6, len(steps)-0.4); ax.axis('off')
    ax.set_title('Điểm rơi nằm ở CHUYỂN ĐỔI, không ở nhận biết · n=2.600',
                 fontsize=11, color=TEXT, fontweight='bold', pad=8)
    fig.savefig(_out('s7_minifunnel.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def barriers():
    qcols = [c for c in df.columns if c.startswith('QME2 - Trà Cozy đóng chai')]
    sub = df[qcols].apply(pd.to_numeric, errors='coerce')
    base = sub.notna().any(axis=1)
    pct = (sub[base].fillna(0) > 0).mean().mul(100)
    pick = {  # label hiển thị: (cột gốc chứa, nhóm)
        'Không thích vị / vị không ngon': ('Do not like the flavor', 'appeal'),
        'Không có đủ vị muốn chọn': ('Does not have enough flavour', 'appeal'),
        'Không có lý do cụ thể (None)': ('None', 'weak'),
        'Hỏi mua nhưng cửa hàng không bán': ('Asked but the store', 'avail'),
        'Không được bảo quản lạnh': ('Not preserved in cool', 'avail'),
    }
    rows = []
    for lab, (key, g) in pick.items():
        col = next((c for c in qcols if key.lower() in c.lower()), None)
        rows.append((lab, round(pct.get(col, 0), 1), g))
    cmap = {'appeal': AMBER, 'avail': SAGE_D, 'weak': SAGE_L}
    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    y = np.arange(len(rows))[::-1]
    for i, (lab, v, g) in enumerate(rows):
        ax.barh(y[i], v, color=cmap[g], height=0.66, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(v+0.6, y[i], f'{v:.1f}%', va='center', fontsize=11, fontweight='bold',
                color=(GOLD_DEEP if g == 'appeal' else SAGE_D), zorder=4)
        ax.text(-0.6, y[i], lab, va='center', ha='right', fontsize=10, color=TEXT, zorder=4)
    appeal = sum(v for _, v, g in rows if g == 'appeal')
    avail = sum(v for _, v, g in rows if g == 'avail')
    ax.annotate('', xy=(38, y[0]+0.42), xytext=(38, y[1]-0.42), arrowprops=dict(arrowstyle='-', color=AMBER, lw=2.2))
    ax.text(39.5, (y[0]+y[1])/2, f'RÀO CẢN SẢN PHẨM (vị)\n≈ {appeal:.0f}%', va='center',
            fontsize=10.5, fontweight='bold', color=GOLD_DEEP)
    ax.annotate('', xy=(38, y[3]+0.42), xytext=(38, y[4]-0.42), arrowprops=dict(arrowstyle='-', color=SAGE_D, lw=2.2))
    ax.text(39.5, (y[3]+y[4])/2, f'Phân phối ≈ {avail:.0f}%', va='center',
            fontsize=9.5, fontweight='bold', color=SAGE_D)
    ax.set_xlim(-1, 58); ax.set_ylim(-0.6, len(rows)-0.4); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Vì sao KHÔNG chọn Cozy — quá nửa rào cản là VỊ & lựa chọn vị\n'
                 '(base: người không chọn Cozy, n=1.485)',
                 fontsize=11, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s7_barriers.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Barriers:', rows, '| appeal', appeal, 'avail', avail)


GREEN_SOFT='#E4F1E9'; GOLD_SOFT='#FBE9C7'; RED_SOFT='#FBEAE9'

def statcards():
    cards = [
        ('91.8%', 'AWARENESS', 'gần bằng top brands\n(C2 97 · Không Độ 92)', GREEN, GREEN_SOFT),
        ('25.8%', 'P4W USAGE', 'chỉ ~45% mức C2\n(C2 57.6%)', GOLD_DEEP, GOLD_SOFT),
        ('8.8%', 'BUMO', 'chưa thành brand chính\n(thấp nhất nhóm leader)', RED, RED_SOFT),
    ]
    fig, ax = plt.subplots(figsize=(10.4, 2.7))
    ax.set_xlim(0, 3); ax.set_ylim(0, 1); ax.axis('off')
    W, gap = 0.93, 0.07
    for i, (num, lab, sub, c, bg) in enumerate(cards):
        x0 = i + gap/2
        ax.add_patch(FancyBboxPatch((x0, 0.08), W, 0.84, boxstyle='round,pad=0.01,rounding_size=0.06',
                     fc=bg, ec=c, lw=1.6, transform=ax.transData, clip_on=False))
        # accent dot
        ax.add_patch(plt.Circle((x0+0.13, 0.74), 0.045, color=c, transform=ax.transData, clip_on=False))
        ax.text(x0+0.50, 0.62, num, ha='center', va='center', fontsize=30, fontweight='bold', color=c)
        ax.text(x0+0.50, 0.36, lab, ha='center', va='center', fontsize=13, fontweight='bold', color=TEXT)
        ax.text(x0+0.50, 0.19, sub, ha='center', va='center', fontsize=9, color=SUB, linespacing=1.2)
        # mũi tên rơi giữa các card
        if i < len(cards)-1:
            ax.annotate('', xy=(i+1+gap/2-0.01, 0.5), xytext=(i+W+gap/2-0.02, 0.5),
                        arrowprops=dict(arrowstyle='-|>', color=SAGE_M, lw=2))
    ax.set_title('Funnel Cozy: mạnh ở Awareness → yếu dần ở Usage & BUMO',
                 fontsize=12, fontweight='bold', color=TEXT, pad=6)
    fig.savefig(_out('s7_statcards.png'), bbox_inches='tight', transparent=True, dpi=200); plt.close(fig)


def barriers_cluster():
    qcols = [c for c in df.columns if c.startswith('QME2 - Trà Cozy đóng chai')]
    sub = df[qcols].apply(pd.to_numeric, errors='coerce')
    base = sub.notna().any(axis=1)
    pct = (sub[base].fillna(0) > 0).mean().mul(100)
    def grp(keys): return round(sum(pct[c] for c in qcols if any(k.lower() in c.lower() for k in keys)), 1)
    clusters = [
        ('VỊ / sản phẩm', grp(['Do not like the flavor', 'enough flavour']), AMBER, 'Rào cản #1'),
        ('Phân phối', grp(['Asked but the store', 'cool place']), SAGE_D, ''),
        ('Không rõ lý do (None)', grp(['None']), SAGE_M, 'low salience'),
        ('Hình ảnh / tin tưởng', grp(['trust', 'Unpopular', 'packaging', 'elegant', 'see when']), SAGE_M, 'image void'),
        ('Giá', grp(['Expensive', 'Too cheap']), SAGE_L, 'lẫn lộn → không phải vấn đề'),
        ('Sức khỏe / đường', grp(['higher sugar', 'Unhealthy']), RED, 'NGHỊCH LÝ với định vị health'),
    ]
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    y = np.arange(len(clusters))[::-1]
    for i, (lab, v, c, note) in enumerate(clusters):
        ax.barh(y[i], v, color=c, height=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(v+0.7, y[i], f'{v:.1f}%', va='center', fontsize=11, fontweight='bold',
                color=(GOLD_DEEP if c == AMBER else RED if c == RED else SAGE_D), zorder=4)
        ax.text(-0.7, y[i], lab, va='center', ha='right', fontsize=10.5,
                fontweight=('bold' if c in (AMBER, RED) else 'normal'),
                color=(RED if c == RED else TEXT), zorder=4)
        if note:
            ax.text(v+7.5, y[i], f'← {note}', va='center', ha='left', fontsize=8.5,
                    style='italic', color=(RED if c == RED else SUB),
                    fontweight=('bold' if c in (AMBER, RED) else 'normal'), zorder=4)
    ax.set_xlim(-1, 72); ax.set_ylim(-0.6, len(clusters)-0.4); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Vì sao KHÔNG chọn Cozy — không chỉ VỊ: còn thiếu lý do, hình ảnh & nghịch lý health\n'
                 '(% nhắc · base người không chọn Cozy, n=1.485 · 1 người nêu nhiều lý do)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s7_barriers_cluster.png'), bbox_inches='tight', transparent=True); plt.close(fig)


if __name__ == '__main__':
    mini_funnel(); barriers(); statcards(); barriers_cluster()
    print(f'Done (font={FONT}): minifunnel + barriers | funnel={FUNNEL}')
