"""
SLIDE 13 — POSITIONING + BRAND IMAGE TARGET  (slide WOW).
  s13_house.png   — Positioning House: Purpose -> Statement -> 3 tru -> RTB (nen tang).
  s13_target.png  — Muc tieu hinh anh 12 thang: before -> after 3 thuoc tinh (score 0-100).
Slide dinh tinh + so image tu Slide 8 (base aware Wave 2025, da verify). Palette xanh-vang Cozy.
"""
import os, textwrap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

_HERE = os.path.dirname(os.path.abspath(__file__))
def _out(n): return os.path.join(_HERE, n)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; AMBER='#E0902E'; TEAL='#2E7D8A'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; RED='#D9534F'
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; LIGHTBG='#F6FAF7'; WHITE='#FFFFFF'
GREEN_BG='#EAF3EC'; AMBER_BG='#FBF1E2'; TEAL_BG='#E4F0F2'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

# 3 tru dinh vi (3 mau design-system -> noi sang Slide tiep theo 3 PILLARS)
PILLARS = [
    dict(name='TRÀ VIỆT THẬT', head=GREEN, bg=GREEN_BG,
         lines=['Di sản 20+ năm · vùng nguyên', 'liệu thật, kiểm soát chất lượng']),
    dict(name='ÍT ĐƯỜNG · HEALTHY', head=AMBER, bg=AMBER_BG,
         lines=['Đón xu hướng #1 của ngành', '(ít đường/zero sugar 85%)']),
    dict(name='VỊ TRÁI CÂY BẢN ĐỊA', head=TEAL, bg=TEAL_BG,
         lines=['Hero Cozy Vải làm signature Việt', 'khác biệt — không đua vị chanh']),
]


def house():
    fig, ax = plt.subplots(figsize=(7.8, 6.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')

    # ROOF — brand purpose
    ax.add_patch(Polygon([(6, 84), (50, 99), (94, 84)], closed=True,
                 facecolor=GREEN, edgecolor=GOLD, linewidth=2, zorder=3))
    ax.text(50, 88.5, 'BRAND PURPOSE', ha='center', va='center', fontsize=9,
            fontweight='bold', color=GOLD, zorder=4)
    ax.text(50, 85.6, 'Đưa trà Việt thật vào nhịp sống hiện đại', ha='center', va='center',
            fontsize=9.3, color=WHITE, zorder=4)

    # STATEMENT bar
    ax.add_patch(FancyBboxPatch((6, 70.5), 88, 10.5, boxstyle='round,pad=0,rounding_size=1.4',
                 facecolor=GOLD, edgecolor=GOLD_DEEP, linewidth=1.4, zorder=3))
    ax.text(50, 77.6, 'ĐỊNH VỊ', ha='center', va='center', fontsize=8.5,
            fontweight='bold', color=GOLD_DEEP, zorder=4)
    ax.text(50, 74.0, '"Cozy — Trà Việt thật, ít đường, vị trái cây bản địa"',
            ha='center', va='center', fontsize=11.2, fontweight='bold', color=TEXT, zorder=4)

    # 3 PILLARS
    x0, top, bot = 6.0, 66.0, 22.0
    gap = 2.6; pw = (88 - 2*gap)/3
    for i, p in enumerate(PILLARS):
        px = x0 + i*(pw+gap)
        ax.add_patch(FancyBboxPatch((px, bot), pw, top-bot, boxstyle='round,pad=0,rounding_size=1.0',
                     facecolor=p['bg'], edgecolor=p['head'], linewidth=1.4, zorder=2))
        ax.add_patch(FancyBboxPatch((px, top-9), pw, 9, boxstyle='round,pad=0,rounding_size=1.0',
                     facecolor=p['head'], edgecolor='none', zorder=3))
        ax.text(px+pw/2, top-4.5, str(i+1), ha='center', va='center', fontsize=8,
                fontweight='bold', color=WHITE, alpha=.55, zorder=4)
        ax.text(px+pw/2, top-7.0, p['name'], ha='center', va='center', fontsize=9.3,
                fontweight='bold', color=WHITE, zorder=4)
        ty = top-13
        for ln in p['lines']:
            ax.text(px+pw/2, ty, ln, ha='center', va='top', fontsize=8.3, color=TEXT, zorder=4)
            ty -= 4.0

    # FOUNDATION — RTB
    ax.add_patch(FancyBboxPatch((6, 6), 88, 13, boxstyle='round,pad=0,rounding_size=1.2',
                 facecolor=SAGE_D, edgecolor='none', zorder=2))
    ax.text(50, 16.0, 'NỀN TẢNG · REASON TO BELIEVE', ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=GOLD)
    ax.text(50, 10.6, '4.500 ha vùng nguyên liệu · 4 nông trường · 15 nhà máy  ·  Hero Cozy Vải\n'
                      'Top 1 "Hàng Việt được yêu thích 2025"  ·  Xuất khẩu 60+ quốc gia',
            ha='center', va='center', fontsize=8.4, color=WHITE, linespacing=1.4)

    fig.savefig(_out('s13_house.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s13_house.png')


def target():
    # score 0-100; current -> target; ghi gap vs leader cho Health
    rows = [
        dict(attr='Có lợi sức khỏe', cur=50.8, tgt=61.7, note='gap vs leader  −18.9 → −8'),
        dict(attr='Vị ngon yêu thích', cur=34.0, tgt=42.0, note='+8đ'),
        dict(attr='Có nhiều vị', cur=24.8, tgt=40.0, note='24.8% → 40%'),
    ]
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    n = len(rows)
    ax.set_xlim(0, 100); ax.set_ylim(0, n*3.0 + 0.9)
    yc = (np.arange(n)[::-1])*3.0 + 1.5     # row centers
    bh = 0.82; off = 0.55
    for i, r in enumerate(rows):
        c = yc[i]
        ax.text(0, c+1.45, r['attr'], ha='left', va='bottom', fontsize=10.5,
                fontweight='bold', color=TEXT)
        ax.text(99, c+1.45, r['note'], ha='right', va='bottom', fontsize=8.4,
                style='italic', color=GREEN, fontweight='bold')
        # current (muted) on top, target (gold) below
        ax.barh(c+off, r['cur'], color=SAGE_M, height=bh, zorder=3, edgecolor=WHITE, linewidth=1.2)
        ax.text(r['cur']+1.2, c+off, f"{r['cur']:.1f}", va='center', fontsize=9.5,
                color=SAGE_D, fontweight='bold')
        ax.barh(c-off, r['tgt'], color=GOLD, height=bh, zorder=3, edgecolor=WHITE, linewidth=1.2)
        ax.text(r['tgt']+1.2, c-off, f"{r['tgt']:.0f}", va='center', fontsize=9.5,
                color=GOLD_DEEP, fontweight='bold')
        ax.annotate('', xy=(r['tgt'], c), xytext=(r['cur'], c),
                    arrowprops=dict(arrowstyle='-|>', color=GOLD_DEEP, lw=1.8))
    ax.legend(handles=[plt.matplotlib.patches.Patch(color=SAGE_M, label='Hiện tại (Cozy, base aware 2025)'),
                       plt.matplotlib.patches.Patch(color=GOLD, label='Mục tiêu 12 tháng')],
              loc='lower right', fontsize=9, frameon=False)
    ax.set_xlim(0, 100); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Mục tiêu hình ảnh 12 tháng: từ "blank brand" → bám 3 thuộc tính\n'
                 'điểm bám = Sức khỏe (gap nhỏ nhất) → leo & đóng dấu Health + Natural + Việt',
                 fontsize=10, color=TEXT, fontweight='bold', pad=12, linespacing=1.4)
    fig.savefig(_out('s13_target.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s13_target.png')


if __name__ == '__main__':
    house(); target()
    print(f'Done (font={FONT})')
