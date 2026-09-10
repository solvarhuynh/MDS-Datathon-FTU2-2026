"""
SLIDE 15 — 1-YEAR ROADMAP + KPI  (slide WOW).
  s15_roadmap.png — Gantt 3 lane (Image/Distribution/Activation) x 4 quy + dai KPI moi quy + headline BUMO 8.8->14%.
3 lane = 3 mau tru (xanh/cam/teal), giu nguyen tu Positioning/3 Pillars. Slide dinh tinh, KPI tu primary.
"""
import os, textwrap
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

_HERE = os.path.dirname(os.path.abspath(__file__))
def _out(n): return os.path.join(_HERE, n)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; AMBER='#E0902E'; TEAL='#2E7D8A'
SAGE_D='#5E8268'; SAGE_M='#86A892'; RED='#C0413D'
TEXT='#15321F'; SUB='#5A6B60'; WHITE='#FFFFFF'
GREEN_BG='#EAF3EC'; AMBER_BG='#FBF1E2'; TEAL_BG='#E4F0F2'; KPI_BG='#F2F7F3'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

QUARTERS = ['Q1 · FIX & FOCUS', 'Q2 · SHOW UP', 'Q3 · AMPLIFY', 'Q4 · SCALE & LOCK']
LANES = [
    dict(name='PRODUCT\n& IMAGE', head=GREEN, bg=GREEN_BG,
         cells=['Giảm đường hero Vải +\nbao bì "trà thật"', 'Tung SKU bản địa #2\n(đào sả/xoài)',
                'Limited edition\ntheo mùa', 'Chuẩn hoá nhận\ndiện thương hiệu']),
    dict(name='DISTRIB &\nVISIBILITY', head=AMBER, bg=AMBER_BG,
         cells=['Fix cold-chain\nNam / Mekong', 'Trưng bày\nCVS / siêu thị',
                'Mở rộng điểm\nbán lạnh', 'Khóa kệ\nkey accounts']),
    dict(name='ACTIVATION\n& DIGITAL', head=TEAL, bg=TEAL_BG,
         cells=['Sampling\nđiểm bán', 'Digital +\nKOC GenZ',
                'UGC "trà\nViệt thật"', 'Loyalty /\nCRM']),
]
KPIS = [
    'Taste barrier\n29% → <24%',
    'Consideration\n34.7 → 40%\nP4W → 28%',
    'P4W → 32%\nNhiều vị\n25 → 40%',
    'BUMO 8.8 → 14%\nHealth gap\n−18.9 → −8',
]


def roadmap():
    fig, ax = plt.subplots(figsize=(13.4, 6.9))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')

    LG = 13.0           # left gutter for lane names
    x0, x1 = LG, 99.0
    cw = (x1 - x0)/4
    pad = 0.9

    # progression arrow (timeline) at very top
    ax.add_patch(FancyArrowPatch((x0+1, 97.0), (x1-1, 97.0), arrowstyle='-|>', mutation_scale=22,
                 linewidth=2.2, color=GOLD_DEEP, zorder=2))
    # quarter headers
    for q in range(4):
        qx = x0 + q*cw
        ax.add_patch(FancyBboxPatch((qx+pad, 88.0), cw-2*pad, 6.0, boxstyle='round,pad=0,rounding_size=0.8',
                     facecolor=SAGE_D, edgecolor='none', zorder=3))
        ax.text(qx+cw/2, 91.0, QUARTERS[q], ha='center', va='center', fontsize=9.8,
                fontweight='bold', color=WHITE, zorder=4)

    # lanes
    lane_top, lane_bot = 86.0, 44.0
    lh = (lane_top - lane_bot)/3
    for li, lane in enumerate(LANES):
        ly = lane_top - (li+1)*lh
        # lane label
        ax.add_patch(FancyBboxPatch((0.5, ly+1.2), LG-1.6, lh-2.4, boxstyle='round,pad=0,rounding_size=0.8',
                     facecolor=lane['head'], edgecolor='none', zorder=3))
        ax.text((LG-1.1)/2, ly+lh/2, lane['name'], ha='center', va='center', fontsize=9,
                fontweight='bold', color=WHITE, zorder=4, linespacing=1.15)
        # continuity track
        ax.plot([x0+pad, x1-pad], [ly+lh/2, ly+lh/2], color=lane['head'], linewidth=1.0, alpha=.25, zorder=2)
        # cells
        for q in range(4):
            qx = x0 + q*cw
            ax.add_patch(FancyBboxPatch((qx+pad, ly+1.6), cw-2*pad, lh-3.2,
                         boxstyle='round,pad=0,rounding_size=0.8', facecolor=lane['bg'],
                         edgecolor=lane['head'], linewidth=1.2, zorder=3))
            ax.text(qx+cw/2, ly+lh/2, lane['cells'][q], ha='center', va='center', fontsize=8.3,
                    color=TEXT, zorder=4, linespacing=1.2)

    # KPI band
    ax.text(0.5, 39.0, 'KPI', ha='left', va='center', fontsize=10.5, fontweight='bold', color=GOLD_DEEP)
    ax.text(0.5, 35.0, 'đo được', ha='left', va='center', fontsize=8, style='italic', color=SUB)
    kpi_top, kpi_bot = 36.5, 7.0
    for q in range(4):
        qx = x0 + q*cw
        ax.add_patch(FancyBboxPatch((qx+pad, kpi_bot), cw-2*pad, kpi_top-kpi_bot,
                     boxstyle='round,pad=0,rounding_size=0.9', facecolor=KPI_BG,
                     edgecolor=GOLD, linewidth=1.4, zorder=3))
        # mini target dot
        ax.text(qx+cw/2, kpi_top-4.0, '• MỤC TIÊU', ha='center', va='center', fontsize=7.6,
                fontweight='bold', color=GOLD_DEEP, zorder=4)
        ax.text(qx+cw/2, (kpi_top+kpi_bot)/2 - 2.0, KPIS[q], ha='center', va='center', fontsize=9.0,
                fontweight='bold', color=TEXT, zorder=4, linespacing=1.5)
    # headline at far-left under KPI label
    ax.add_patch(FancyBboxPatch((0.5, kpi_bot), LG-1.6, 18.0, boxstyle='round,pad=0,rounding_size=0.9',
                 facecolor=GREEN, edgecolor=GOLD, linewidth=1.6, zorder=3))
    ax.text((LG-1.1)/2, kpi_bot+13.5, 'BẮC ĐÍCH', ha='center', va='center', fontsize=8,
            fontweight='bold', color=GOLD, zorder=4)
    ax.text((LG-1.1)/2, kpi_bot+8.0, 'BUMO\n8.8% → 14%', ha='center', va='center', fontsize=9.5,
            fontweight='bold', color=WHITE, zorder=4, linespacing=1.3)

    fig.savefig(_out('s15_roadmap.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s15_roadmap.png')


if __name__ == '__main__':
    roadmap()
    print(f'Done (font={FONT})')
