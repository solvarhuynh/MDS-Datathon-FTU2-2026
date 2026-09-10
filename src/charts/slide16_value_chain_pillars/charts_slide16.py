"""
SLIDE 16 — NANG LUC PHAT TRIEN & VALUE CHAIN.
  s16_valuechain.png — value chain 5 khau (Vung nguyen lieu->Nha may->San pham->Kenh->Nguoi dung) + loi the tung khau.
  s16_sizing.png      — funnel co hoi TAM->SAM->Target (uoc tinh nhom FUU, macro dong bo Slide 1).
  s16_budget.png      — donut phan bo ngan sach 3 tru (xanh/cam/teal), uu tien in-store + digital.
Slide dinh tinh; macro = Ken Research 2024 + InsightAsia 2025. Sizing/ngan sach = uoc tinh nhom.
"""
import os, textwrap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Polygon, Wedge

_HERE = os.path.dirname(os.path.abspath(__file__))
def _out(n): return os.path.join(_HERE, n)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; AMBER='#E0902E'; TEAL='#2E7D8A'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; RED='#C0413D'
TEXT='#15321F'; SUB='#5A6B60'; WHITE='#FFFFFF'
GREEN_BG='#EAF3EC'; AMBER_BG='#FBF1E2'; TEAL_BG='#E4F0F2'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

CHAIN = [
    ('VÙNG NGUYÊN LIỆU', '4.500 ha · 4 nông trường', 'Kiểm soát chất lượng → RTB "trà thật"'),
    ('15 NHÀ MÁY', 'Năng lực sản xuất & R&D', 'Scale + công thức giảm đường, SKU mới'),
    ('SẢN PHẨM', 'Portfolio + hero Cozy Vải', 'Khác biệt vị bản địa Việt'),
    ('KÊNH PHÂN PHỐI', 'Toàn quốc · XK 60+ quốc gia', 'Đòn bẩy độ phủ + uy tín thương hiệu'),
    ('NGƯỜI DÙNG', '91.8% awareness', 'Nền tảng rộng để chuyển đổi'),
]


def valuechain():
    fig, ax = plt.subplots(figsize=(13.4, 2.9))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    n = len(CHAIN); m = 1.0; gap = 1.2
    bw = (100 - 2*m - (n-1)*gap)/n
    cols = [GREEN, GREEN, TEAL, AMBER, SAGE_D]
    for i, (title, cap, adv) in enumerate(CHAIN):
        x = m + i*(bw+gap)
        ax.add_patch(FancyBboxPatch((x, 8), bw, 84, boxstyle='round,pad=0,rounding_size=1.2',
                     facecolor='#F6FAF7', edgecolor=cols[i], linewidth=1.5, zorder=2))
        ax.add_patch(FancyBboxPatch((x, 70), bw, 22, boxstyle='round,pad=0,rounding_size=1.2',
                     facecolor=cols[i], edgecolor='none', zorder=3))
        ax.text(x+bw/2, 81, textwrap.fill(title, 18), ha='center', va='center', fontsize=9.6,
                fontweight='bold', color=WHITE, zorder=4, linespacing=1.1)
        ax.text(x+bw/2, 55, cap, ha='center', va='center', fontsize=8.6, fontweight='bold',
                color=cols[i], zorder=4)
        ax.text(x+bw/2, 30, textwrap.fill(adv, 24), ha='center', va='center', fontsize=8.2,
                color=TEXT, zorder=4, linespacing=1.3)
        if i < n-1:
            ax.annotate('', xy=(x+bw+gap-0.1, 50), xytext=(x+bw+0.1, 50),
                        arrowprops=dict(arrowstyle='-|>', color=GOLD_DEEP, lw=2.0))
    fig.savefig(_out('s16_valuechain.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s16_valuechain.png')


def sizing():
    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    # --- TAM/SAM = 2 dòng "proof" nhỏ phía trên (thị trường đủ lớn) ---
    ax.text(1.5, 96.5, 'THỊ TRƯỜNG ĐỦ LỚN (proof):', ha='left', va='center', fontsize=7.6,
            fontweight='bold', color=SUB)
    proofs = [('TAM', 'RTD Tea VN ~390tr USD · +8–10%/năm', SAGE_M),
              ('SAM', 'Phân khúc health/natural + Olong/trái cây bản địa', SAGE_D)]
    py = 89
    for tag, txt, c in proofs:
        ax.add_patch(FancyBboxPatch((1.5, py-5), 97, 7.0, boxstyle='round,pad=0,rounding_size=0.8',
                     facecolor='#F2F7F3', edgecolor=c, linewidth=1.1, zorder=2))
        ax.add_patch(FancyBboxPatch((2.5, py-4.2), 13, 5.4, boxstyle='round,pad=0,rounding_size=0.7',
                     facecolor=c, edgecolor='none', zorder=3))
        ax.text(9.0, py-1.5, tag, ha='center', va='center', fontsize=8.4, fontweight='bold', color=WHITE, zorder=4)
        ax.text(18, py-1.5, txt, ha='left', va='center', fontsize=8.0, color=TEXT, zorder=4)
        py -= 9.5
    # mũi tên nhỏ "thu hẹp về mục tiêu"
    ax.annotate('', xy=(50, 67.5), xytext=(50, 71.5), arrowprops=dict(arrowstyle='-|>', color=GOLD_DEEP, lw=2), zorder=4)
    # --- HERO TARGET card (lớn) ---
    ax.add_patch(FancyBboxPatch((3, 6), 94, 60, boxstyle='round,pad=0,rounding_size=2.4',
                 facecolor=GREEN, edgecolor=GOLD, linewidth=2.6, zorder=3))
    ax.text(50, 60, 'MỤC TIÊU 12 THÁNG · BUMO (regular usage)', ha='center', va='center',
            fontsize=9, fontweight='bold', color=GOLD, zorder=4)
    # con số hero (3 phần, toạ độ x riêng)
    ax.text(28, 43, '8.8%', ha='center', va='center', fontsize=29, fontweight='bold', color='#BFD8C6', zorder=4)
    ax.text(50, 43.5, '→', ha='center', va='center', fontsize=26, fontweight='bold', color=GOLD, zorder=4)
    ax.text(72, 43, '14%', ha='center', va='center', fontsize=34, fontweight='bold', color=GOLD, zorder=5)
    # badge +5.2pp + insight tương đối
    ax.add_patch(FancyBboxPatch((20, 14), 60, 13, boxstyle='round,pad=0,rounding_size=1.6',
                 facecolor=GOLD, edgecolor='none', zorder=4))
    ax.text(50, 21.0, '+5.2pp  ≈  +60% người dùng thường xuyên', ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=TEXT, zorder=5)
    ax.text(50, 9.5, '→ incremental volume & doanh thu (giả định nhóm FUU)', ha='center', va='center',
            fontsize=7.6, style='italic', color='#D6E8DC', zorder=4)
    ax.set_title('Cơ hội quy ra mục tiêu kinh doanh đo được', fontsize=9.5, fontweight='bold', color=TEXT, pad=8)
    fig.savefig(_out('s16_sizing.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s16_sizing.png')


def budget():
    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    parts = [('Distribution &\nVisibility', 40, AMBER),
             ('Product &\nImage', 30, GREEN),
             ('Activation &\nDigital', 30, TEAL)]
    vals = [p[1] for p in parts]; cols = [p[2] for p in parts]
    wedges, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.40, edgecolor=WHITE, linewidth=2))
    ax.text(0, 0.08, 'NGÂN SÁCH', ha='center', va='center', fontsize=9, fontweight='bold', color=TEXT)
    ax.text(0, -0.16, '12 tháng', ha='center', va='center', fontsize=8, color=SUB)
    # labels — đặt NGOÀI vành, canh lề theo hướng để chữ mọc ra ngoài (tránh đè vành cùng màu)
    import numpy as _np
    ang = 90
    for (lab, v, c) in parts:
        mid = ang - v/100*360/2
        rad = _np.deg2rad(mid)
        cx, cy = _np.cos(rad), _np.sin(rad)
        x = 1.12*cx; y = 1.12*cy
        ha = 'left' if cx > 0.15 else ('right' if cx < -0.15 else 'center')
        ax.text(x, y, f'{lab}\n{v}%', ha=ha, va='center', fontsize=8.8,
                fontweight='bold', color=c, linespacing=1.15)
        ang -= v/100*360
    ax.set_title('Phân bổ ngân sách theo 3 trụ — ưu tiên IN-STORE + DIGITAL\n(touchpoint #1: 66.4% · digital rẻ, đóng gap −7đ) · TV <10% (không đua SOV)',
                 fontsize=8.6, fontweight='bold', color=TEXT, pad=10, linespacing=1.4)
    ax.set(aspect='equal'); ax.set_xlim(-1.95, 1.95); ax.set_ylim(-1.6, 1.6)
    fig.savefig(_out('s16_budget.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s16_budget.png')


if __name__ == '__main__':
    valuechain(); sizing(); budget()
    print(f'Done (font={FONT})')
