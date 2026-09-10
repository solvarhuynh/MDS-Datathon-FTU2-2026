"""
SLIDE 9 — ROOT CAUSE (3/3): TOUCHPOINT & SHARE-OF-MIND.
Đọc cleaned_dataset.xlsx → 2 chart:
  1) s9_touchpoint.png — Cozy vs C2 trên các điểm chạm chính; gap WORD-OF-MOUTH lớn nhất
  2) s9_tom.png        — TOM (share-of-mind) theo brand: Cozy thấp nhất nhóm leader
Base: người AWARE. PRIMARY. Palette xanh-vàng Cozy. Chạy: python charts_slide9.py
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Patch, FancyBboxPatch

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
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; RED='#D9534F'; RED_SOFT='#FBEAE9'
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; LIGHTBG='#F6FAF7'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name="Dataset_Clean")
AW = 'Q1Q2. Total aided awareness_'
def aware(inc):
    cols = [c for c in df.columns if c.startswith(AW) and inc.lower() in c.lower() and 'trà sữa' not in c.lower()]
    return (df[cols].fillna(0).astype(float).sum(axis=1) > 0)

def tp(token, inc, key):
    col = next((c for c in df.columns if c.startswith('Q_TP1_') and token in c and c.endswith('_'+key)), None)
    if col is None: return np.nan
    return round((df.loc[aware(inc), col].fillna(0).astype(float) > 0).mean()*100, 1)

# (label hiển thị, key gốc)
TPS = [('Trưng bày tại điểm bán', 'Product display in stores, supermarket, …', 0),
       ('Thấy người khác dùng', 'Seeing others use', 1),
       ('Quảng cáo TV', 'Advertising on TV', 0),
       ('Bạn bè giới thiệu', 'Recommended by friends/relatives', 1),
       ('Người bán giới thiệu', 'Recommended by seller', 0),
       ('Quảng cáo Internet', 'Advertising on Internet (website, Facebook, YouTube, etc)', 0)]


def touchpoint():
    rows = [(lab, tp('R15- Trà Cozy', 'Trà Cozy đóng chai', k), tp('R1- C2', 'C2', k), wom) for lab, k, wom in TPS]
    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    y = np.arange(len(rows))[::-1]; bh = 0.34
    for i, (lab, cz, c2, wom) in enumerate(rows):
        ax.barh(y[i]+0.19, c2, bh, color=SAGE_M, zorder=3, edgecolor=WHITE, linewidth=1)
        ax.barh(y[i]-0.19, cz, bh, color=GOLD, zorder=3, edgecolor=WHITE, linewidth=1)
        ax.text(c2+1, y[i]+0.19, f'{c2:.0f}', va='center', fontsize=9.5, color=SAGE_D, fontweight='bold')
        ax.text(cz+1, y[i]-0.19, f'{cz:.0f}', va='center', fontsize=10, color=GOLD_DEEP, fontweight='bold')
        gap = cz - c2
        ax.text(-2, y[i]+0.18, lab, ha='right', va='center', fontsize=10.5,
                fontweight=('bold' if wom else 'normal'), color=(RED if wom else TEXT))
        ax.text(-2, y[i]-0.20, f'thua {gap:+.0f}đ' + ('  (WOM)' if wom else ''), ha='right', va='center',
                fontsize=9, fontweight='bold', color=(RED if wom else SUB))
    ax.legend(handles=[Patch(color=GOLD, label='Cozy'), Patch(color=SAGE_M, label='C2 (leader)')],
              loc='lower center', bbox_to_anchor=(0.5, 1.0), fontsize=10.5, frameon=False, ncol=2)
    ax.set_xlim(-32, 82); ax.set_ylim(-1.7, len(rows)-0.2); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Cozy thiếu hiện diện ở MỌI điểm chạm — yếu nhất là TRUYỀN MIỆNG\n'
                 '"thấy người khác dùng" −12đ · "bạn bè giới thiệu" −11đ · base aware',
                 fontsize=11, color=TEXT, fontweight='bold', pad=30, linespacing=1.4)
    # callout None-of-these (băng trống dưới)
    none_cz = tp('R15- Trà Cozy', 'Trà Cozy đóng chai', 'None of these')
    none_c2 = tp('R1- C2', 'C2', 'None of these')
    ax.add_patch(FancyBboxPatch((-30, -1.5), 110, 0.78, boxstyle='round,pad=0.05,rounding_size=0.1',
                 fc=RED_SOFT, ec=RED, lw=1.4, clip_on=False, zorder=5))
    ax.text(25, -1.11, f'"Không nhớ điểm chạm nào": Cozy {none_cz:.1f}% vs C2 {none_c2:.1f}% = GẤP ~5× → share-of-mind THẤP NHẤT',
            ha='center', va='center', fontsize=10, fontweight='bold', color=RED, zorder=6)
    fig.savefig(_out('s9_touchpoint.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('None of these — Cozy', none_cz, 'C2', none_c2)


def tom_bar():
    def tomc(inc): return round(df['Q1.TOM'].astype(str).str.contains(inc, case=False, na=False).mean()*100, 1)
    # brand-level TOM (Cozy dùng variant Olong Xoài = TOM của Cozy)
    data = [('C2', tomc('C2')-df['Q1.TOM'].astype(str).str.contains('Trà sữa C2', na=False).mean()*100),
            ('OLong Tea+', tomc('OLong Tea Plus')), ('Không Độ', tomc('Không Độ')-df['Q1.TOM'].astype(str).str.contains('Trà sữa', na=False).mean()*100),
            ('Cozy', tomc('Cozy')), ('Dr. Thanh', tomc('Dr. Thanh'))]
    data = sorted(data, key=lambda x: x[1], reverse=True)
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    y = np.arange(len(data))[::-1]
    for i, (b, v) in enumerate(data):
        c = GOLD if b == 'Cozy' else SAGE_M
        ax.barh(y[i], v, color=c, height=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(v+0.6, y[i], f'{v:.1f}%', va='center', fontsize=11, fontweight='bold',
                color=(GOLD_DEEP if b == 'Cozy' else SAGE_D))
        ax.text(-0.6, y[i], ('» '+b if b == 'Cozy' else b), ha='right', va='center', fontsize=10.5,
                fontweight=('bold' if b == 'Cozy' else 'normal'), color=(GREEN if b == 'Cozy' else TEXT))
    ax.set_xlim(-12, 42); ax.set_ylim(-0.6, len(data)-0.4); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Top-of-mind (nghĩ đến đầu tiên): Cozy chỉ 8.7% — thấp nhất nhóm leader\n'
                 'biết Cozy (91.8%) nhưng KHÔNG nhớ đầu tiên · share-of-mind yếu',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s9_tom.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('TOM:', data)


from matplotlib.patches import FancyArrow

def funnel_concept():
    # Know → Recall → Consider → Choose, nhấn Know→Recall (Cozy yếu nhất)
    stages = [('KNOW', 'Nhận biết', '91.8%', GREEN),
              ('RECALL', 'Nhớ chủ động (TOM)', '8.7%', RED),
              ('CONSIDER', 'Cân nhắc', '34.7%', SAGE_D),
              ('CHOOSE', 'Chọn thường xuyên (BUMO)', '8.8%', GOLD_DEEP)]
    fig, ax = plt.subplots(figsize=(11, 2.9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis('off')
    bw, gap = 2.5, 0.55
    for i, (en, vi, val, c) in enumerate(stages):
        x0 = i*(bw+gap)
        ax.add_patch(FancyBboxPatch((x0, 0.5), bw, 1.7, boxstyle='round,pad=0.02,rounding_size=0.12',
                     fc=(RED_SOFT if c == RED else LIGHTBG), ec=c, lw=2.6, zorder=3))
        ax.text(x0+bw/2, 1.78, en, ha='center', fontsize=12.5, fontweight='bold', color=c, zorder=4)
        ax.text(x0+bw/2, 1.38, vi, ha='center', fontsize=8.5, color=SUB, zorder=4)
        ax.text(x0+bw/2, 0.92, val, ha='center', fontsize=18, fontweight='bold', color=c, zorder=4)
        if i < len(stages)-1:
            acol = RED if i == 0 else SAGE_M
            ax.add_patch(FancyArrow(x0+bw+0.05, 1.35, gap-0.12, 0, width=0.12, head_width=0.34,
                         head_length=0.22, color=acol, zorder=2, length_includes_head=True))
    # nhấn khâu Know->Recall
    ax.add_patch(FancyArrow((bw)+gap/2, 0.42, 0, -0.0, width=0))  # spacer
    ax.text(bw+gap/2, 0.18, '↑ Cozy RỚT mạnh nhất ở đây\n(biết 92% nhưng nhớ chủ động chỉ 9%)',
            ha='center', va='top', fontsize=9.5, fontweight='bold', color=RED, linespacing=1.2)
    ax.set_title('Cơ chế: phải được NHỚ mới được chọn — Cozy đứt ngay Know → Recall',
                 fontsize=11.5, color=TEXT, fontweight='bold', pad=6)
    fig.savefig(_out('s9_funnel_concept.png'), bbox_inches='tight', transparent=True, dpi=200); plt.close(fig)


if __name__ == '__main__':
    touchpoint(); tom_bar(); funnel_concept()
    print(f'Done (font={FONT})')
