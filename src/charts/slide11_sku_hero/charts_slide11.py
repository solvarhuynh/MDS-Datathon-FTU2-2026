"""
SLIDE 11 — SKU & HERO PRODUCTS.
  s11_bumo.png    — BUMO theo variant (top 10): vị CHANH thống trị, Cozy Vải = hero fruit duy nhất
  s11_switch.png  — người TỪNG chọn Cozy giờ chuyển đi đâu (rò rỉ về lemon leaders) · n=60
Đọc cleaned_dataset.xlsx (Q5.Bumo, Q7). PRIMARY. Palette xanh-vàng Cozy.
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Patch, FancyArrow

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
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; RED='#D9534F'
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; LIGHTBG='#F6FAF7'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name="Dataset_Clean")
N = len(df)
vc = df['Q5.Bumo'].value_counts()


def bumo_variant():
    top = vc.head(10)
    pct = (top / N * 100).round(1)
    labels = list(top.index)
    short = {'OLong Tea Plus vị chanh': 'Tea+ Chanh', 'C2 - Vị chanh': 'C2 Chanh',
             'Không Độ - Không xác định': 'Không Độ (xanh)', 'Trà Cozy Vải': 'Cozy Vải',
             'C2 - Vị đào': 'C2 Đào', 'Không Độ - Vị chanh': 'Không Độ Chanh',
             'C2 - Vị táo': 'C2 Táo', 'Trà mật ong Boncha vị chanh': 'Boncha Chanh',
             'Dr. Thanh - Không đường': 'Dr.Thanh', 'TH True Tea - Trà Olong Tự Nhiên': 'TH Olong'}
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    y = np.arange(len(labels))[::-1]
    for i, lab in enumerate(labels):
        v = pct[lab]; sl = short.get(lab, lab)
        cozy = 'Cozy' in lab; lemon = 'chanh' in lab.lower()
        c = GOLD if cozy else (AMBER if lemon else SAGE_M)
        ax.barh(y[i], v, color=c, height=0.66, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(v+0.4, y[i], f'{v:.1f}%', va='center', fontsize=10, fontweight='bold',
                color=(GOLD_DEEP if cozy else (GOLD_DEEP if lemon else SAGE_D)))
        ax.text(-0.5, y[i], sl, ha='right', va='center', fontsize=10,
                fontweight=('bold' if cozy else 'normal'), color=(GREEN if cozy else TEXT))
    ax.legend(handles=[Patch(color=AMBER, label='Vị chanh (động cơ volume)'),
                       Patch(color=GOLD, label='Cozy Vải (hero)'), Patch(color=SAGE_M, label='Vị khác')],
              loc='lower right', fontsize=9.5, frameon=False)
    lemon_sum = pct['OLong Tea Plus vị chanh'] + pct['C2 - Vị chanh']
    ax.set_xlim(-13, 34); ax.set_ylim(-0.6, len(labels)-0.2); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(f'Vị CHANH là động cơ volume ngành — Top 2 BUMO đều chanh (~{lemon_sum:.0f}% thị trường)\n'
                 'Cozy Vải = hero TRÁI CÂY duy nhất lọt top (8.4%) → đánh niche khác biệt, không đối đầu chanh',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s11_bumo.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('BUMO top:', dict(pct))


def switching():
    q7 = 'Q7. Previous BUMO'
    prev = df[df[q7].astype(str).str.contains('Cozy', case=False, na=False)]
    n = len(prev)
    dest = prev['Q5.Bumo'].astype(str)
    def share(inc): return round(dest.str.contains(inc, case=False, na=False).mean()*100, 0)
    rows = [('C2', share('C2')), ('Không Độ', share('Không Độ')), ('Tea+ (OLong)', share('OLong')),
            ('Khác', 0)]
    used = sum(r[1] for r in rows[:3]); rows[-1] = ('Khác', round(100-used, 0))
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    y = np.arange(len(rows))[::-1]
    for i, (b, v) in enumerate(rows):
        lemon = b in ('C2', 'Tea+ (OLong)')
        c = AMBER if lemon else SAGE_M
        ax.barh(y[i], v, color=c, height=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(v+0.8, y[i], f'{v:.0f}%', va='center', fontsize=11, fontweight='bold', color=(GOLD_DEEP if lemon else SAGE_D))
        ax.text(-0.8, y[i], b, ha='right', va='center', fontsize=10.5, color=TEXT)
    ax.set_xlim(-16, 40); ax.set_ylim(-0.6, len(rows)-0.4); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.legend(handles=[Patch(color=AMBER, label='đối thủ vị chanh')], loc='lower right', fontsize=9.5, frameon=False)
    ax.set_title(f'Người TỪNG chọn Cozy giờ chuyển sang đâu? → rò rỉ về 3 leader (chủ yếu vị CHANH)\n'
                 f'(base nhỏ n={n} — chỉ minh hoạ HƯỚNG rò rỉ, không phải con số chắc)',
                 fontsize=10, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s11_switch.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Switch dest:', rows, 'n', n)


if __name__ == '__main__':
    bumo_variant(); switching()
    print(f'Done (font={FONT})')
