"""
SLIDE 3 (bo sung) — SEGMENT ATTRACTIVENESS x BRAND FIT.
  s3_segmatrix.png — ma tran 2x2: X = Brand Fit voi Cozy, Y = Segment Growth/Premium potential.
  3 phan khuc: Tra xanh mass · Tra thao moc/thanh nhiet · Tra Olong & Trai cay (PRIORITY, goc tren-phai).
Slide dinh tinh, neo +18% YoY (InsightAsia). Palette xanh-vang Cozy.
"""
import os, textwrap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

_HERE = os.path.dirname(os.path.abspath(__file__))
def _out(n): return os.path.join(_HERE, n)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; AMBER='#E0902E'; TEAL='#2E7D8A'
SAGE_D='#5E8268'; SAGE_M='#86A892'; GREY='#AEB7B0'; RED='#C0413D'
TEXT='#15321F'; SUB='#5A6B60'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

# name, x(fit), y(growth), size, color, sub, label_side
SEGS = [
    ('Trà Olong & Trái cây', 3.15, 3.15, 1300, GOLD,
     '+18% YoY · trà Việt + Vải → FIT cao nhất', 'below'),
    ('Trà xanh (mass)', 2.05, 1.45, 760, SAGE_M,
     'cạnh tranh cao · khác biệt thấp', 'below'),
    ('Trà thảo mộc / thanh nhiệt', 1.25, 2.70, 820, SAGE_M,
     'Không Độ & Dr.Thanh đã sở hữu', 'below'),
]


def segmatrix():
    fig, ax = plt.subplots(figsize=(9.6, 7.7))
    lo, hi, mid = 0.4, 4.0, 2.2
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    # quadrant shading
    ax.add_patch(Rectangle((lo, lo), mid-lo, mid-lo, facecolor='#EFF2F0', zorder=1))           # BL
    ax.add_patch(Rectangle((mid, lo), hi-mid, mid-lo, facecolor='#EAF1EC', zorder=1))          # BR
    ax.add_patch(Rectangle((lo, mid), mid-lo, hi-mid, facecolor='#FBF1E2', zorder=1))          # TL
    ax.add_patch(Rectangle((mid, mid), hi-mid, hi-mid, facecolor='#FCEFC3', zorder=1,          # TR priority
                 edgecolor=GOLD_DEEP, linewidth=2.2, linestyle='--'))
    # divider
    ax.plot([mid, mid], [lo, hi], color=WHITE, lw=2, zorder=2)
    ax.plot([lo, hi], [mid, mid], color=WHITE, lw=2, zorder=2)
    # quadrant micro-labels
    ax.text(lo+0.12, hi-0.12, 'Growth cao · khó thắng', ha='left', va='top', fontsize=13.5, color=SUB, style='italic', zorder=3)
    ax.text(lo+0.12, lo+0.10, 'Ít hấp dẫn', ha='left', va='bottom', fontsize=13.5, color=SUB, style='italic', zorder=3)
    ax.text(hi-0.12, lo+0.10, 'Fit tốt · growth thấp', ha='right', va='bottom', fontsize=13.5, color=SUB, style='italic', zorder=3)
    # PRIORITY banner (TR)
    ax.add_patch(FancyBboxPatch((mid+0.12, hi-0.68), hi-mid-0.24, 0.56, boxstyle='round,pad=0,rounding_size=0.12',
                 facecolor=GOLD_DEEP, edgecolor='none', zorder=4))
    ax.scatter([(mid+hi)/2-1.02], [hi-0.40], marker='*', s=300, c=WHITE, edgecolors='none', zorder=6)
    ax.text((mid+hi)/2+0.10, hi-0.40, 'PRIORITY SEGMENT', ha='center', va='center', fontsize=13.5,
            fontweight='bold', color=WHITE, zorder=5)
    # bubbles
    for nm, x, y, s, c, sub, side in SEGS:
        ax.scatter([x],[y], s=s, c=c, edgecolors=WHITE, linewidths=2.2, zorder=5, alpha=.95)
        prio = (c == GOLD)
        ax.text(x, y, ('Olong\n& Trái cây' if prio else ''), ha='center', va='center',
                fontsize=12, fontweight='bold', color=(TEXT if prio else WHITE), zorder=6, linespacing=1.0)
        # label block below bubble
        r = (s/1300)*0.34 + 0.20
        ax.text(x, y-r-0.05, nm, ha='center', va='top', fontsize=13.5, fontweight='bold',
                color=(GREEN if prio else TEXT), zorder=6)
        ax.text(x, y-r-0.40, textwrap.fill(sub, 26), ha='center', va='top', fontsize=12.5,
                color=(GOLD_DEEP if prio else SUB), zorder=6, linespacing=1.2,
                fontweight=('bold' if prio else 'normal'))
    # axes arrows + titles
    ax.annotate('', xy=(hi, lo), xytext=(lo, lo), arrowprops=dict(arrowstyle='-|>', color=SUB, lw=1.6), zorder=4)
    ax.annotate('', xy=(lo, hi), xytext=(lo, lo), arrowprops=dict(arrowstyle='-|>', color=SUB, lw=1.6), zorder=4)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xlabel('BRAND FIT VỚI COZY  →', fontsize=13.5, fontweight='bold', color=TEXT)
    ax.set_ylabel('SEGMENT GROWTH / PREMIUM POTENTIAL  →', fontsize=12.5, fontweight='bold', color=TEXT)
    ax.text(lo+0.02, lo-0.16, 'Thấp', ha='left', va='top', fontsize=12.5, color=SUB)
    ax.text(hi, lo-0.16, 'Cao', ha='right', va='top', fontsize=12.5, color=SUB)
    ax.set_title('Segment Attractiveness × Brand Fit — Olong & Trái cây là phân khúc ƯU TIÊN',
                 fontsize=15, fontweight='bold', color=TEXT, pad=14)
    fig.savefig(_out('s3_segmatrix.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s3_segmatrix.png')


if __name__ == '__main__':
    segmatrix()
    print(f'Done (font={FONT})')
