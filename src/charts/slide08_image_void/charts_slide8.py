"""
SLIDE 8 — ROOT CAUSE (2/3): BRAND IMAGE VOID (WOW slide).
Base: người AWARE, Wave 2025 (khớp deck 100%). Đọc thẳng cleaned_dataset.xlsx → 2 chart:
  1) s8_dumbbell.png   — Cozy vs đối-thủ-max trên 18/18 thuộc tính (thua tất) + 4 key nhấn
  2) s8_perceptmap.png — perceptual map Health/Natural × Modern; Cozy gold cô lập + white space
PRIMARY. Palette xanh-vàng Cozy. Chạy: python charts_slide8.py
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Circle, FancyArrowPatch

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

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; GREEN_DEEP='#0E5C2F'; GOLD_SOFT='#FBE9C7'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; RED='#D9534F'
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; LIGHTBG='#F6FAF7'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name="Dataset_Clean")
W25 = df['Wave'] == 2025
AW = 'Q1Q2. Total aided awareness_'
QI = {'Cozy': 'QI - Trà Cozy đóng chai', 'C2': 'QI - C2', 'OLong Tea+': 'QI - OLong Tea Plus',
      'Không Độ': 'QI - Không Độ', 'Dr. Thanh': 'QI - Dr. Thanh'}
INC = {'Cozy': 'Trà Cozy đóng chai', 'C2': 'C2', 'OLong Tea+': 'OLong Tea Plus',
       'Không Độ': 'Không Độ', 'Dr. Thanh': 'Dr. Thanh'}

def amask(inc):
    cols = [c for c in df.columns if c.startswith(AW) and inc.lower() in c.lower() and 'trà sữa' not in c.lower()]
    return (df[cols].fillna(0).astype(float).sum(axis=1) > 0) & W25
AM = {b: amask(INC[b]) for b in QI}

attrs = [c.split('_', 1)[1] for c in df.columns if c.startswith('QI - Trà Cozy đóng chai_') and 'DK/NA' not in c]

def score(b, attr):
    col = next((c for c in df.columns if c.startswith(QI[b]) and c.endswith('_'+attr)), None)
    if col is None: return np.nan
    return round((df.loc[AM[b], col].fillna(0).astype(float) > 0).mean()*100, 1)

IMG = pd.DataFrame({b: [score(b, a) for a in attrs] for b in QI}, index=attrs)
IMG['max'] = IMG[['C2', 'OLong Tea+', 'Không Độ', 'Dr. Thanh']].max(axis=1)
IMG['gap'] = (IMG['Cozy'] - IMG['max']).round(1)

SHORT = {'Có nhiều vị để lựa chọn': 'Có nhiều vị', 'Thương hiệu mang tính hiện đại, trẻ trung': 'Hiện đại, trẻ trung',
         'Vị ngon mà tôi yêu thích': 'Vị ngon yêu thích', 'Những thương hiệu được ưa chuộng và phổ biến': 'Phổ biến, ưa chuộng',
         'Mang đến sự vui tươi và lạc quan': 'Vui tươi, lạc quan', 'Phù hợp để thưởng thức hàng ngày': 'Uống hàng ngày',
         'Tạo cảm giác sảng khoái': 'Sảng khoái', 'Làm dịu cơn khát': 'Dịu cơn khát',
         'Giúp giảm căng thẳng và mệt mỏi': 'Giảm căng thẳng', 'Mang lại cảm giác thư giãn': 'Thư giãn',
         'Tái tạo năng lượng': 'Tái tạo năng lượng', 'Giá cả hợp lý với chất lượng mang lại': 'Giá hợp lý',
         'Mang đến cảm giác tươi mát': 'Tươi mát', 'Sản xuất từ nguyên liệu tự nhiên': 'Nguyên liệu tự nhiên',
         'Bao bì có thiết kế thu hút': 'Bao bì thu hút', 'Giải nhiệt cuộc sống': 'Giải nhiệt',
         'Nhãn hiệu đáng tin cậy': 'Đáng tin cậy', 'Có lợi cho sức khỏe': 'Có lợi sức khỏe'}
KEY = ['Có lợi cho sức khỏe', 'Vị ngon mà tôi yêu thích', 'Thương hiệu mang tính hiện đại, trẻ trung', 'Có nhiều vị để lựa chọn']


# ===== 1) GROUPED BAR — Cozy vs đối thủ (dễ hiểu: Cozy luôn thấp hơn) =====
def dumbbell():
    K6 = ['Có nhiều vị để lựa chọn', 'Thương hiệu mang tính hiện đại, trẻ trung',
          'Vị ngon mà tôi yêu thích', 'Nhãn hiệu đáng tin cậy',
          'Sản xuất từ nguyên liệu tự nhiên', 'Có lợi cho sức khỏe']  # worst trên → foothold dưới
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    y = np.arange(len(K6))[::-1]; bh = 0.34
    for i, attr in enumerate(K6):
        cz, mx, gap = IMG.loc[attr, 'Cozy'], IMG.loc[attr, 'max'], IMG.loc[attr, 'gap']
        health = attr == 'Có lợi cho sức khỏe'; worst = attr == 'Có nhiều vị để lựa chọn'
        # bar đối thủ (trên, sage) + Cozy (dưới, gold)
        ax.barh(y[i]+0.19, mx, bh, color=SAGE_M, zorder=3, edgecolor=WHITE, linewidth=1)
        ax.barh(y[i]-0.19, cz, bh, color=GOLD, zorder=3, edgecolor=WHITE, linewidth=1)
        ax.text(mx+1.5, y[i]+0.19, f'{mx:.0f}', va='center', fontsize=10, color=SAGE_D, fontweight='bold')
        ax.text(cz+1.5, y[i]-0.19, f'{cz:.0f}', va='center', fontsize=10.5, color=GOLD_DEEP, fontweight='bold')
        # tên + gap (trái)
        nm = SHORT.get(attr, attr)
        if health: nm += '  (điểm bám)'
        if worst: nm += '  (xa nhất)'
        ax.text(-2, y[i]+0.19, nm, ha='right', va='center', fontsize=10.5, fontweight='bold',
                color=(GREEN if health else RED if worst else TEXT))
        ax.text(-2, y[i]-0.19, f'thua {gap:+.0f}đ', ha='right', va='center', fontsize=9.5,
                fontweight='bold', color=(GREEN if health else RED if worst else SUB))
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=GOLD, label='Cozy'), Patch(color=SAGE_M, label='Đối thủ cao nhất')],
              loc='lower center', bbox_to_anchor=(0.5, -0.13), fontsize=10.5, frameon=False, ncol=2)
    ax.set_xlim(-30, 92); ax.set_ylim(-0.6, len(K6)-0.2); ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Cozy (vàng) LUÔN thấp hơn đối thủ (xám) ở mọi thuộc tính\n'
                 'gần nhất "có lợi sức khỏe" (thua 19đ) · xa nhất "nhiều vị" (thua 57đ) · base aware 2025',
                 fontsize=11, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s8_dumbbell.png'), bbox_inches='tight', transparent=True); plt.close(fig)


# ===== 2) PERCEPTUAL MAP Health/Natural × Modern =====
def perceptmap():
    def comp(b): return (score(b, 'Có lợi cho sức khỏe') + score(b, 'Sản xuất từ nguyên liệu tự nhiên')) / 2
    pts = {b: (round(comp(b), 1), score(b, 'Thương hiệu mang tính hiện đại, trẻ trung')) for b in QI}
    fig, ax = plt.subplots(figsize=(8.4, 6.6))
    cx, cy = 55, 48
    ax.axhline(cy, color=BORDER, lw=1, zorder=1); ax.axvline(cx, color=BORDER, lw=1, zorder=1)
    # vùng đối thủ sở hữu (shade góc trên-phải)
    ax.add_patch(plt.Rectangle((cx, cy), 96-cx, 100-cy, color='#EEF3EF', zorder=0))
    ax.text(76, 92, 'VÙNG ĐỐI THỦ SỞ HỮU', ha='center', fontsize=9, color=SAGE_D, fontweight='bold', zorder=1)
    lbloff = {'Cozy': (0, -6, 'center'), 'C2': (0, 6, 'center'), 'Không Độ': (-7, -1, 'right'),
              'OLong Tea+': (8, -1, 'left'), 'Dr. Thanh': (0, -6, 'center')}
    for b, (x, yv) in pts.items():
        cozy = b == 'Cozy'
        col = GOLD if cozy else (SAGE_D if b != 'Dr. Thanh' else SAGE_L)
        ax.scatter(x, yv, s=520 if cozy else 380, color=col, alpha=0.95, edgecolors=WHITE, linewidths=2, zorder=4)
        dx, dy, ha = lbloff[b]
        ax.text(x+dx, yv+dy, b, ha=ha, va='center', fontsize=10.5 if cozy else 9.5,
                fontweight='bold', color=(GOLD_DEEP if cozy else TEXT), zorder=5)
    # white space
    ax.add_patch(Circle((82, 34), 8.5, fill=True, fc=GOLD_SOFT, ec=GOLD_DEEP, ls=(0,(5,4)), lw=2.5, zorder=2))
    ax.text(82, 37.5, 'WHITE SPACE', ha='center', fontsize=10.5, fontweight='bold', color=GOLD_DEEP, zorder=3)
    ax.text(82, 31.5, '"trà Việt thật"\nnatural + bản địa', ha='center', fontsize=8, color=GOLD_DEEP, zorder=3, linespacing=1.1)
    czx, czy = pts['Cozy']
    ax.add_patch(FancyArrowPatch((czx+4, czy), (74.5, 33), arrowstyle='-|>', mutation_scale=18,
                 lw=2.4, color=GREEN, connectionstyle='arc3,rad=-0.2', zorder=3))
    ax.text(64, 26, 'Cozy đang TRỐNG hình ảnh\n→ leo lên & đóng dấu Việt', ha='center', fontsize=8.5,
            fontweight='bold', color=GREEN, zorder=3, linespacing=1.2)
    ax.text(95, 16.5, 'HEALTH / NATURAL →', ha='right', fontsize=9.5, color=SUB, fontweight='bold')
    ax.text(cx+1, 99, 'MODERN / TRẺ ↑', ha='left', fontsize=9.5, color=SUB, fontweight='bold')
    ax.set_xlim(20, 96); ax.set_ylim(14, 102); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(BORDER)
    ax.set_title('Perceptual map: đối thủ chiếm vùng "mạnh" (góc trên-phải),\n'
                 'Cozy CÔ LẬP ở vùng yếu — phải mở lãnh thổ health/natural + Việt · base aware 2025',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s8_perceptmap.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Map pts:', pts)


from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle, FancyBboxPatch

# ===== A) ATTRIBUTE × BRAND HEATMAP =====
def attr_heatmap():
    rows = [('Vị ngon mà tôi yêu thích', 'Ngon / dễ uống'),
            ('Giải nhiệt cuộc sống', 'Giải nhiệt / thanh mát'),
            ('Thương hiệu mang tính hiện đại, trẻ trung', 'Trẻ trung'),
            ('Sản xuất từ nguyên liệu tự nhiên', 'Tự nhiên'),
            ('Có lợi cho sức khỏe', 'Healthy / ít đường'),
            ('Nhãn hiệu đáng tin cậy', 'Đáng tin cậy')]
    cols = ['C2', 'Không Độ', 'OLong Tea+', 'Cozy']
    M = np.array([[IMG.loc[a, c] for c in cols] for a, _ in rows])
    cmap = LinearSegmentedColormap.from_list('g', ['#FFFFFF', '#BfD9C7', GREEN, GREEN_DEEP])
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.imshow(M, cmap=cmap, aspect='auto', vmin=0, vmax=90)
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = M[i, j]
            ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=12,
                    fontweight='bold', color=(WHITE if v > 50 else TEXT))
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([('» '+c if c == 'Cozy' else c) for c in cols], fontsize=11, fontweight='bold')
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([s for _, s in rows], fontsize=10.5)
    ax.xaxis.tick_top(); ax.tick_params(length=0)
    ci = cols.index('Cozy')
    ax.add_patch(Rectangle((ci-0.5, -0.5), 1, len(rows), fill=False, ec=GOLD, lw=3.5, zorder=5))
    ax.set_title('Cozy NHẠT nhất mọi thuộc tính — không sở hữu vùng nào\n'
                 '(% liên tưởng · base aware Wave 2025 · ô càng xanh = càng sở hữu)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=28, linespacing=1.4)
    for s in ax.spines.values(): s.set_visible(False)
    fig.savefig(_out('s8_attr_heatmap.png'), bbox_inches='tight', transparent=True); plt.close(fig)


# ===== B) "NO OWNED TERRITORY" — reason-to-choose mỗi brand =====
def territory():
    cards = [
        ('C2', 'Giải khát hằng ngày,\nvị quen — "nhiều vị"', 'sở hữu "nhiều vị" 82', SAGE_D, False),
        ('Không Độ', 'Thanh nhiệt /\ngiải nhiệt', 'giải nhiệt 71', SAGE_M, False),
        ('OLong Tea+', 'Trà thật, tự nhiên,\nhơi premium', 'tự nhiên 80', SAGE_M, False),
        ('Cozy', '?', 'chưa sở hữu lý do chọn', GOLD, True),
    ]
    fig, ax = plt.subplots(figsize=(10.6, 3.6))
    ax.set_xlim(0, 4); ax.set_ylim(0, 1); ax.axis('off')
    ax.text(2, 1.06, 'Người tiêu dùng chọn mỗi brand VÌ điều gì?', ha='center', fontsize=13,
            fontweight='bold', color=TEXT)
    W = 0.92
    for i, (b, reason, hook, c, cozy) in enumerate(cards):
        x0 = i + (1-W)/2
        bg = GOLD_SOFT if cozy else LIGHTBG
        ax.add_patch(FancyBboxPatch((x0, 0.06), W, 0.84, boxstyle='round,pad=0.01,rounding_size=0.05',
                     fc=bg, ec=c, lw=(3.5 if cozy else 1.6), transform=ax.transData, clip_on=False))
        ax.add_patch(FancyBboxPatch((x0+0.04, 0.74), W-0.08, 0.14, boxstyle='round,pad=0.005,rounding_size=0.04',
                     fc=c, ec='none', transform=ax.transData, clip_on=False))
        ax.text(x0+W/2, 0.81, b, ha='center', va='center', fontsize=12.5, fontweight='bold', color=WHITE)
        if cozy:
            ax.text(x0+W/2, 0.48, '?', ha='center', va='center', fontsize=46, fontweight='bold', color=GOLD_DEEP)
            ax.text(x0+W/2, 0.20, 'Weakly defined\nreason-to-choose', ha='center', va='center',
                    fontsize=10, fontweight='bold', color=GOLD_DEEP, linespacing=1.15)
        else:
            ax.text(x0+W/2, 0.48, reason, ha='center', va='center', fontsize=11, color=TEXT, linespacing=1.2)
            ax.text(x0+W/2, 0.18, hook, ha='center', va='center', fontsize=8.5, style='italic', color=SUB)
    fig.savefig(_out('s8_territory.png'), bbox_inches='tight', transparent=True, dpi=200); plt.close(fig)


if __name__ == '__main__':
    dumbbell(); perceptmap(); attr_heatmap(); territory()
    print(f'Done (font={FONT})')
    print(IMG[['Cozy', 'max', 'gap']].sort_values('gap').to_string())
