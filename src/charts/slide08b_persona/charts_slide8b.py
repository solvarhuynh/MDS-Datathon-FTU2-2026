"""
SLIDE 8b — TARGET CONSUMER PERSONA (capstone sau Consumer Profile).
  s8b_persona.png — 2 the persona: PRIMARY (Nu 30-40, giu & upsell) vs RECLAIM (GenZ 25-29, tai chiem).
So lien tu cleaned_dataset.xlsx (PRIMARY n=764, RECLAIM n=484). Palette: xanh (giu) / cam (tai chiem).
"""
import os, textwrap
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Circle

_HERE = os.path.dirname(os.path.abspath(__file__))
def _out(n): return os.path.join(_HERE, n)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; AMBER='#E0902E'; TEAL='#2E7D8A'
SAGE_D='#5E8268'; SAGE_M='#86A892'; RED='#C0413D'
TEXT='#15321F'; SUB='#5A6B60'; WHITE='#FFFFFF'
GREEN_BG='#EAF3EC'; AMBER_BG='#FBF1E2'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

P1 = dict(
    head=GREEN, bg=GREEN_BG, tag='PRIMARY · GIỮ & UPSELL  (ưu tiên #1)',
    name='"Chị Hằng" — Nữ 30–40, trung lưu', n='n=764 · ~29% mẫu',
    essence='Đã TIN Cozy — chỉ cần dễ mua hơn, ngon hơn, có lý do trả thêm',
    demo=['Nữ', '30–40 tuổi', 'Thu nhập 15–30tr (51% ≥15tr)', 'Lõi: Bắc · upsell: Nam'],
    funnel=[('Aware','88%'),('Consider','37%'),('P4W','27%'),('BUMO','8%')],
    rows=[
        ('TẦN SUẤT', '80% uống RTD tea ≥2–3 lần/tuần — đậm nhất'),
        ('UỐNG CÙNG', 'Sữa đậu nành · trà pha/túi lọc · nước khoáng · nước ép → "health + tại nhà"'),
        ('GẶP COZY Ở', 'Trưng bày điểm bán 65% · bạn bè giới thiệu 24% · người bán 16%'),
        ('RÀO CẢN', 'VỊ 37% + không sẵn ở cửa hàng / không để lạnh ~18%  (giá KHÔNG phải rào cản)'),
        ('HÌNH ẢNH', 'ĐÃ TIN: nguyên liệu tự nhiên 57% · đáng tin 57% · sức khỏe 52%'),
    ],
    win='Fix VỊ + cold-chain/độ phủ → UPSELL premium (Vải/Olong). Kênh: in-store + truyền miệng.',
    pillar='→ Trụ PRODUCT & IMAGE + DISTRIBUTION',
)
P2 = dict(
    head=AMBER, bg=AMBER_BG, tag='RECLAIM · TÁI CHIẾM  (phòng thủ tương lai)',
    name='"Linh" — GenZ 25–29, mới đi làm', n='n=484 · rơi −2.9đ YoY',
    essence='Biết Cozy qua người khác — kén vị, nhạy giá & hình ảnh',
    demo=['64% Nữ', '25–29 tuổi', 'Thu nhập khá (54% ≥15tr)', 'Đô thị · digital-native'],
    funnel=[('Aware','90%'),('Consider','34%'),('P4W','26%'),('BUMO','7%')],
    rows=[
        ('TẦN SUẤT', '74% uống ≥2–3 lần/tuần (≈ trung bình)'),
        ('UỐNG CÙNG', 'Cà phê & RTD coffee · energy · nước có ga (46%) · RTD juice → "on-the-go"'),
        ('GẶP COZY Ở', '"Thấy người khác dùng" 45% · Internet 14% · billboard 8% · PG 7%'),
        ('RÀO CẢN', 'Thiếu đa dạng vị 23% + "đắt hơn mong đợi" 8.8% (gấp 2) + "không phổ biến/sang"'),
        ('NGHẼN', 'Aware 90% nhưng BUMO chỉ 7% → biết mà KHÔNG chọn (thiếu lý do + bằng chứng XH)'),
    ],
    win='Social proof (UGC · KOC · sampling) + vị mới/limited + ưu đãi. Digital/social-first.',
    pillar='→ Trụ ACTIVATION & DIGITAL',
)


def card(ax, x0, w, P):
    y0, y1 = 3, 97
    ax.add_patch(FancyBboxPatch((x0, y0), w, y1-y0, boxstyle='round,pad=0,rounding_size=1.4',
                 facecolor=P['bg'], edgecolor=P['head'], linewidth=1.8, zorder=2))
    cx = x0 + w/2
    # header
    hh = 13
    ax.add_patch(FancyBboxPatch((x0, y1-hh), w, hh, boxstyle='round,pad=0,rounding_size=1.4',
                 facecolor=P['head'], edgecolor='none', zorder=3))
    ax.scatter([x0+5.2], [y1-hh/2], s=560, c=WHITE, edgecolors=GOLD, linewidths=1.6, zorder=4)
    ax.text(x0+5.2, y1-hh/2, P['name'][1], ha='center', va='center', fontsize=13, fontweight='bold', color=P['head'], zorder=5)
    ax.text(x0+9.8, y1-5.0, P['name'], ha='left', va='center', fontsize=11, fontweight='bold', color=WHITE, zorder=5)
    ax.text(x0+9.4, y1-9.4, P['tag']+'   ·   '+P['n'], ha='left', va='center', fontsize=8, color=GOLD, fontweight='bold', zorder=5)
    # essence
    yy = y1-hh-3.5
    ax.text(cx, yy, P['essence'], ha='center', va='center', fontsize=8.8, style='italic',
            color=P['head'], fontweight='bold', zorder=4)
    # demo chips
    yy -= 4.2
    chips=P['demo']; cw=(w-6)/len(chips)
    for i,ch in enumerate(chips):
        chx=x0+3+i*cw
        ax.add_patch(FancyBboxPatch((chx+0.4, yy-1.9), cw-0.8, 3.8, boxstyle='round,pad=0,rounding_size=1.0',
                     facecolor=WHITE, edgecolor=P['head'], linewidth=1.0, zorder=4))
        ax.text(chx+cw/2, yy, ch, ha='center', va='center', fontsize=7.2, color=TEXT, zorder=5)
    # funnel mini
    yy -= 6.5
    fw=(w-6)/4
    for i,(lab,val) in enumerate(P['funnel']):
        fx=x0+3+i*fw
        ax.text(fx+fw/2, yy+1.0, val, ha='center', va='center', fontsize=12.5, fontweight='bold', color=P['head'], zorder=4)
        ax.text(fx+fw/2, yy-2.6, lab, ha='center', va='center', fontsize=7.4, color=SUB, zorder=4)
        if i<3: ax.text(fx+fw, yy+0.2, '›', ha='center', va='center', fontsize=11, color=SAGE_M, zorder=4)
    # divider
    yy -= 5.2
    ax.plot([x0+3, x0+w-3],[yy,yy], color=P['head'], lw=0.8, alpha=.35, zorder=3)
    # behavior rows
    yy -= 1.0
    rowh = (yy - 17) / len(P['rows'])
    for lab, val in P['rows']:
        ry = yy - rowh/2
        ax.add_patch(FancyBboxPatch((x0+3, ry-1.7), 15.5, 3.4, boxstyle='round,pad=0,rounding_size=0.9',
                     facecolor=P['head'], edgecolor='none', zorder=4))
        ax.text(x0+3+7.75, ry, lab, ha='center', va='center', fontsize=7.0, fontweight='bold', color=WHITE, zorder=5)
        ax.text(x0+19.5, ry, textwrap.fill(val, 50), ha='left', va='center', fontsize=7.7,
                color=TEXT, zorder=4, linespacing=1.15)
        yy -= rowh
    # win footer
    ax.add_patch(FancyBboxPatch((x0+2.5, y0+2.0), w-5, 11, boxstyle='round,pad=0,rounding_size=1.1',
                 facecolor=GOLD, edgecolor=P['head'], linewidth=1.4, zorder=4))
    ax.text(cx, y0+10.0, 'ĐÒN ĐÁNH', ha='center', va='center', fontsize=7.6, fontweight='bold', color=GOLD_DEEP, zorder=5)
    ax.text(cx, y0+6.4, textwrap.fill(P['win'], 60), ha='center', va='center', fontsize=8.0,
            fontweight='bold', color=TEXT, zorder=5, linespacing=1.2)
    ax.text(cx, y0+2.6, P['pillar'], ha='center', va='center', fontsize=8.2, fontweight='bold', color=P['head'], zorder=5)


def persona():
    fig, ax = plt.subplots(figsize=(14.0, 7.8))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    card(ax, 1.0, 48.0, P1)
    card(ax, 51.0, 48.0, P2)
    fig.savefig(_out('s8b_persona.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('saved s8b_persona.png')


if __name__ == '__main__':
    persona()
    print(f'Done (font={FONT})')
