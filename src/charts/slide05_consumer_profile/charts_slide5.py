"""
SLIDE 5 — CONSUMER PROFILE. Đọc thẳng cleaned_dataset.xlsx → 2 chart:
  1) s5_gender_region.png  — 2 donut (giới tính + vùng) xếp dọc
  2) s5_age_yoy.png        — grouped bar tuổi 2024 vs 2025 + mũi tên YoY + zone at-risk/growth

Số liệu PRIMARY (khảo sát FUU, n=2.600, 2 wave 2024/2025). Palette xanh-vàng Cozy.
Chạy: python charts_slide5.py
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

# Đường dẫn theo vị trí script: data ở thư mục cha, ảnh xuất trong folder này
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
def _out(name): return os.path.join(_HERE, name)

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; GREEN_DEEP='#0E5C2F'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; SAGE_XL='#D8E3DC'
RED='#D9534F'; RED_SOFT='#FBEAE9'; GREEN_SOFT='#E4F1E9'
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; LIGHTBG='#F6FAF7'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name='Dataset_Clean')
GENDER = df['D2.Gender'].value_counts(normalize=True).mul(100).round(1)
REGION = df['Region'].value_counts(normalize=True).mul(100).round(1)
AGE_ORDER = ['14 - 18 y.o.','19 - 24 y.o.','25 - 29 y.o.','30 - 34 y.o.','35 - 40 y.o.']
agp = (df.groupby('Wave')['D3.Age'].value_counts(normalize=True).mul(100).round(1)
       .unstack(0).reindex(AGE_ORDER))


def gender_donut():
    gv = [GENDER.get('Female', 0), GENDER.get('Male', 0)]
    fig, ax = plt.subplots(figsize=(4.2, 4.6))
    ax.pie(gv, colors=[GOLD, SAGE_M], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.40, edgecolor=WHITE, linewidth=2.5),
           autopct=lambda p: f'{p:.0f}%', pctdistance=0.80,
           textprops=dict(color=WHITE, fontsize=12, fontweight='bold'))
    ax.text(0, 0.14, 'NỮ', ha='center', fontsize=13, color=SUB, fontweight='bold')
    ax.text(0, -0.20, f'{gv[0]:.0f}%', ha='center', fontsize=28, fontweight='bold', color=GOLD_DEEP)
    ax.set_title('GIỚI TÍNH', fontsize=13, fontweight='bold', color=TEXT, pad=8)
    ax.legend([f'Nữ · {gv[0]:.1f}%', f'Nam · {gv[1]:.1f}%'], loc='upper center',
              bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=9.5, frameon=False)
    ax.set(aspect='equal')
    fig.savefig(_out('s5_gender_donut.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def region_donut():
    rorder = ['North', 'South', 'Mekong', 'Central']
    rv = [REGION.get(k, 0) for k in rorder]
    rc = [GREEN, SAGE_M, SAGE_L, SAGE_XL]
    fig, ax = plt.subplots(figsize=(4.2, 4.8))
    ax.pie(rv, colors=rc, startangle=90, counterclock=False,
           wedgeprops=dict(width=0.40, edgecolor=WHITE, linewidth=2.5),
           autopct=lambda p: f'{p:.0f}%', pctdistance=0.80,
           textprops=dict(color=WHITE, fontsize=11, fontweight='bold'))
    ax.text(0, 0.14, 'MIỀN BẮC', ha='center', fontsize=12, color=SUB, fontweight='bold')
    ax.text(0, -0.20, f'{rv[0]:.0f}%', ha='center', fontsize=26, fontweight='bold', color=GREEN)
    ax.set_title('VÙNG MIỀN', fontsize=13, fontweight='bold', color=TEXT, pad=8)
    ax.legend([f'{k} · {v:.1f}%' for k, v in zip(rorder, rv)], loc='upper center',
              bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=9, frameon=False)
    ax.set(aspect='equal')
    fig.savefig(_out('s5_region_donut.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def income_bar():
    # gộp 6 band → 3 tầng
    tier_map = {'3,000,001 – 4,500,000 VND': 'Thấp', '4,500,001 – 7,500,000 VND': 'Thấp',
                '7,500,001 – 15,000,000 VND': 'Trung lưu', '15,000,001 – 30,000,000 VND': 'Trung lưu',
                '30,000,001 – 45,000,000 VND': 'Cao', 'Above 45,000,001': 'Cao'}
    t = df['D4.Income'].map(tier_map).value_counts(normalize=True).mul(100).round(1)
    low, mid, high = t.get('Thấp', 0), t.get('Trung lưu', 0), t.get('Cao', 0)
    segs = [('Thấp\n<7.5tr', low, SAGE_L), ('Trung lưu  7.5–30tr', mid, GOLD), ('Cao\n>30tr', high, GREEN)]
    fig, ax = plt.subplots(figsize=(7.4, 1.9))
    left = 0
    for name, v, c in segs:
        ax.barh(0, v, left=left, height=0.55, color=c, edgecolor=WHITE, linewidth=2.5, zorder=2)
        tc = TEXT if c == GOLD else WHITE
        if v > 4:
            ax.text(left+v/2, 0, f'{v:.0f}%', ha='center', va='center', fontsize=12, fontweight='bold', color=tc, zorder=3)
        ax.text(left+v/2, -0.52, name, ha='center', va='top', fontsize=8.5,
                color=(GOLD_DEEP if c == GOLD else SUB), fontweight=('bold' if c == GOLD else 'normal'), zorder=3)
        left += v
    ax.text(0, 0.78, '≈88% TRUNG LƯU (7.5–30tr VND/tháng) — định giá premium nhẹ khả thi, không quá cao',
            ha='left', va='center', fontsize=10, fontweight='bold', color=GREEN)
    ax.set_xlim(0, 100); ax.set_ylim(-1.1, 1.2); ax.axis('off')
    ax.set_title('Thu nhập hộ · n=2.600', fontsize=10, color=SUB, loc='right', pad=2)
    fig.savefig(_out('s5_income.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def olong_income():
    # RTD Olong penetration theo tầng thu nhập (premium skew)
    tier_map = {'3,000,001 – 4,500,000 VND': '≤7.5tr', '4,500,001 – 7,500,000 VND': '≤7.5tr',
                '7,500,001 – 15,000,000 VND': '7.5–15tr', '15,000,001 – 30,000,000 VND': '15–30tr',
                '30,000,001 – 45,000,000 VND': '>30tr', 'Above 45,000,001': '>30tr'}
    tt = df['D4.Income'].map(tier_map)
    ol = df['S2.Category used in P4W_RTD Olong Tea'].fillna(0).astype(float)
    order = ['≤7.5tr', '7.5–15tr', '15–30tr', '>30tr']
    pen = ol.groupby(tt).mean().mul(100).round(1).reindex(order)
    cols = [SAGE_L, SAGE_M, SAGE_D, GOLD]
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    bars = ax.bar(order, pen.values, color=cols, width=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
    for x, v in zip(order, pen.values):
        ax.text(x, v+1.3, f'{v:.0f}%', ha='center', fontsize=13, fontweight='bold',
                color=(GOLD_DEEP if x == '>30tr' else SAGE_D))
    ax.annotate('', xy=(3, pen.values[-1]+8), xytext=(0, pen.values[0]+8),
                arrowprops=dict(arrowstyle='-|>', color=GREEN, lw=2.2))
    ax.text(1.5, max(pen.values)+11, 'càng giàu càng uống Olong  →  phân khúc PREMIUM',
            ha='center', fontsize=10.5, fontweight='bold', color=GREEN)
    ax.set_ylim(0, max(pen.values)+16); ax.set_yticks([])
    ax.set_xlabel('Thu nhập hộ / tháng', fontsize=10, color=SUB)
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.set_title('% uống RTD Olong (P4W) theo thu nhập · n=2.600',
                 fontsize=10.5, color=SUB, pad=8)
    fig.savefig(_out('s5_olong_income.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def cozy_reach_region():
    # Cozy aware vs P4W theo vùng — lộ gap "biết nhiều, dùng ít" ở Bắc
    aware = df['Q1Q2. Total aided awareness_Trà Cozy đóng chai'].fillna(0).astype(float)
    czc = [c for c in df.columns if c.startswith('Q4. P4W_Trà Cozy')]
    p4w = (df[czc].fillna(0).astype(float).sum(axis=1) > 0).astype(float)
    order = ['North', 'Central', 'South', 'Mekong']
    aw = aware.groupby(df['Region']).mean().mul(100).round(1).reindex(order)
    pw = p4w.groupby(df['Region']).mean().mul(100).round(1).reindex(order)
    x = np.arange(len(order)); bw = 0.38
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.bar(x-bw/2, aw.values, bw, color=SAGE_L, label='Awareness', zorder=3)
    ax.bar(x+bw/2, pw.values, bw, color=GOLD, label='P4W (dùng thật)', zorder=3)
    for i in range(len(order)):
        ax.text(x[i]-bw/2, aw.values[i]+2, f'{aw.values[i]:.0f}', ha='center', fontsize=9, color=SUB)
        ax.text(x[i]+bw/2, pw.values[i]+2, f'{pw.values[i]:.0f}%', ha='center', fontsize=11, fontweight='bold', color=GOLD_DEEP)
    ax.set_xticks(x); ax.set_xticklabels(order, fontsize=11)
    ax.set_ylim(0, 122); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.005), ncol=2, fontsize=9.5, frameon=False)
    ax.set_title('Cozy: BIẾT nhiều khắp nơi — nhưng DÙNG lệch\n(Bắc untapped: aware 94 / P4W 22 · Nam–Mekong mạnh nhất)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=34, linespacing=1.4)
    fig.savefig(_out('s5_cozy_reach_region.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def cozy_p4w_age_yoy():
    czc = [c for c in df.columns if c.startswith('Q4. P4W_Trà Cozy')]
    cp = (df[czc].fillna(0).astype(float).sum(axis=1) > 0).astype(float)
    piv = cp.groupby([df['Wave'], df['D3.Age']]).mean().mul(100).round(1).unstack(0).reindex(
        ['14 - 18 y.o.', '19 - 24 y.o.', '25 - 29 y.o.', '30 - 34 y.o.', '35 - 40 y.o.'])
    wcols = list(piv.columns)
    w24 = piv[wcols[0]].values; w25 = piv[wcols[1]].values
    delta = (w25 - w24).round(1)
    labels = ['14–18', '19–24', '25–29', '30–34', '35–40']
    x = np.arange(len(labels)); bw = 0.38
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.axvspan(0.5, 2.5, color=RED_SOFT, zorder=0)
    ax.axvspan(2.5, 4.5, color=GREEN_SOFT, zorder=0)
    top = max(w24.max(), w25.max())
    ax.text(1.5, top*1.16, 'AT-RISK · GenZ 19–29', ha='center', fontsize=9.5, fontweight='bold', color=RED)
    ax.text(3.5, top*1.16, 'GROWTH POCKET · 30+', ha='center', fontsize=9.5, fontweight='bold', color=GREEN)
    ax.bar(x-bw/2, w24, bw, color=SAGE_L, label='2024', zorder=3)
    ax.bar(x+bw/2, w25, bw, color=GOLD, label='2025', zorder=3)
    for i in range(len(labels)):
        ax.text(x[i]-bw/2, w24[i]+0.4, f'{w24[i]:.1f}', ha='center', fontsize=8, color=SUB, zorder=4)
        ax.text(x[i]+bw/2, w25[i]+0.4, f'{w25[i]:.1f}', ha='center', fontsize=8.5, color=GOLD_DEEP, fontweight='bold', zorder=4)
        d = delta[i]; up = d >= 0
        ax.text(x[i], max(w24[i], w25[i])+1.8, f'{"▲" if up else "▼"} {d:+.1f}đ',
                ha='center', fontsize=9.5, fontweight='bold', color=(GREEN if up else RED), zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, top*1.34); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.legend(loc='upper left', fontsize=9, frameon=False)
    ax.set_title('Cozy P4W usage theo tuổi · 2024 vs 2025  ·  % (n=1.300/wave)',
                 fontsize=11, color=SUB, pad=10)
    fig.savefig(_out('s5_cozy_p4w_age_yoy.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Cozy P4W by age x wave:\n', piv.to_string())


def cozy_olong_by_region():
    aware_cz = [c for c in df.columns if c.startswith('Q4. P4W_Trà Cozy')]
    cozy = (df[aware_cz].fillna(0).astype(float).sum(axis=1) > 0).astype(float)
    olong = df['S2.Category used in P4W_RTD Olong Tea'].fillna(0).astype(float)
    order = ['North', 'Central', 'South', 'Mekong']
    cz = cozy.groupby(df['Region']).mean().mul(100).round(1).reindex(order)
    ol = olong.groupby(df['Region']).mean().mul(100).round(1).reindex(order)
    pop = (df['Region'].value_counts(normalize=True).mul(100).round(1)).reindex(order)
    cz_avg, ol_avg = cozy.mean()*100, olong.mean()*100
    x = np.arange(len(order)); bw = 0.38
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.axvspan(1.5, 3.5, color=GREEN_SOFT, zorder=0)   # vùng fit cao = South+Mekong
    ax.text(2.5, 80, 'ĐỘ PHÙ HỢP CAO với Cozy + Olong', ha='center', fontsize=10,
            fontweight='bold', color=GREEN)
    ax.text(0.5, 80, 'QUY MÔ (dân số lớn)', ha='center', fontsize=10, fontweight='bold', color=SUB)
    b1 = ax.bar(x-bw/2, cz.values, bw, color=GOLD, label='Cozy P4W usage', zorder=3)
    b2 = ax.bar(x+bw/2, ol.values, bw, color=SAGE_D, label='RTD Olong usage', zorder=3)
    ax.axhline(cz_avg, ls='--', lw=1.3, color=GOLD_DEEP, zorder=2)
    ax.axhline(ol_avg, ls='--', lw=1.3, color=SAGE_D, zorder=2)
    ax.text(3.6, cz_avg, f'TB Cozy {cz_avg:.0f}', va='center', fontsize=8, color=GOLD_DEEP)
    ax.text(3.6, ol_avg, f'TB Olong {ol_avg:.0f}', va='center', fontsize=8, color=SAGE_D)
    for i in range(len(order)):
        ax.text(x[i]-bw/2, cz.values[i]+1.3, f'{cz.values[i]:.0f}', ha='center', fontsize=9.5, fontweight='bold', color=GOLD_DEEP, zorder=4)
        ax.text(x[i]+bw/2, ol.values[i]+1.3, f'{ol.values[i]:.0f}', ha='center', fontsize=9.5, fontweight='bold', color=SAGE_D, zorder=4)
        ax.text(x[i], -8, f'dân số {pop.values[i]:.0f}%', ha='center', fontsize=8.5,
                color=(TEXT if order[i] == 'North' else SUB), fontweight=('bold' if order[i] == 'North' else 'normal'))
    ax.set_xticks(x); ax.set_xticklabels(order, fontsize=11)
    ax.set_ylim(-12, 84); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_position(('data', 0)); ax.spines['bottom'].set_color(BORDER)
    ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.74), fontsize=9.5, frameon=False, ncol=1)
    ax.set_title('Bắc tạo QUY MÔ — nhưng Nam & Mekong PHÙ HỢP hơn (Cozy P4W & Olong cao hơn TB)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=12)
    fig.savefig(_out('s5_cozy_olong_region.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Region — Cozy P4W:', dict(cz), '| Olong:', dict(ol), '| Pop:', dict(pop))


def income_region():
    tmap = {'3,000,001 – 4,500,000 VND': '≤7.5tr', '4,500,001 – 7,500,000 VND': '≤7.5tr',
            '7,500,001 – 15,000,000 VND': '7.5–15tr', '15,000,001 – 30,000,000 VND': '15–30tr',
            '30,000,001 – 45,000,000 VND': '>30tr', 'Above 45,000,001': '>30tr'}
    d2 = df.assign(_t=df['D4.Income'].map(tmap))
    ct = pd.crosstab(d2['Region'], d2['_t'], normalize='index').mul(100)
    tiers = ['≤7.5tr', '7.5–15tr', '15–30tr', '>30tr']
    ct = ct.reindex(columns=tiers)
    ct['aff'] = ct['15–30tr'] + ct['>30tr']
    ct = ct.sort_values('aff', ascending=True)        # giàu nhất lên trên cùng (barh)
    cols = {'≤7.5tr': SAGE_XL, '7.5–15tr': SAGE_L, '15–30tr': SAGE_D, '>30tr': GOLD}
    regions = list(ct.index)
    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    y = np.arange(len(regions))
    for i, r in enumerate(regions):
        left = 0
        for t in tiers:
            v = ct.loc[r, t]
            ax.barh(i, v, left=left, color=cols[t], edgecolor=WHITE, linewidth=1.5, zorder=3)
            if v >= 7:
                ax.text(left+v/2, i, f'{v:.0f}', ha='center', va='center', fontsize=8.5,
                        fontweight='bold', color=(TEXT if t == '>30tr' else WHITE), zorder=4)
            left += v
        ax.text(103, i, f'{ct.loc[r,"aff"]:.0f}% từ 15tr+', va='center', ha='left',
                fontsize=9, fontweight='bold', color=(GREEN if r == 'South' else SUB))
    ax.set_yticks(y); ax.set_yticklabels([('» '+r if r == 'South' else r) for r in regions],
                                         fontsize=11, fontweight='bold')
    ax.set_xlim(0, 102); ax.set_xticks([]); ax.set_ylim(-0.6, len(regions)-0.4)
    for s in ax.spines.values(): s.set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=cols[t]) for t in tiers]
    ax.legend(handles, tiers, loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=4,
              fontsize=9, frameon=False)
    ax.set_title('Miền NAM giàu nhất (76% từ 15tr+) — fit CAO + thu nhập CAO = premium beachhead',
                 fontsize=11, color=TEXT, fontweight='bold', loc='left', pad=42)
    fig.savefig(_out('s5_income_region.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Income x Region affluent% (15tr+):\n', ct['aff'].round(1).to_string())


def cozy_growth_contribution():
    czc = [c for c in df.columns if c.startswith('Q4. P4W_Trà Cozy')]
    cz = (df[czc].fillna(0).astype(float).sum(axis=1) > 0).astype(int)
    order = ['14 - 18 y.o.', '19 - 24 y.o.', '25 - 29 y.o.', '30 - 34 y.o.', '35 - 40 y.o.']
    cnt = cz.groupby([df['D3.Age'], df['Wave']]).sum().unstack().reindex(order)
    net = (cnt.iloc[:, 1] - cnt.iloc[:, 0]).values
    tot = net.sum()
    pct = (net / tot * 100).round(0)
    labels = ['14–18', '19–24', '25–29', '30–34', '35–40']
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    cols = [GREEN if v > 0 else RED for v in net]
    cols[0] = SAGE_M  # 14-18 nhẹ
    ax.bar(x, net, color=cols, width=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
    ax.axhline(0, color=SUB, lw=1)
    for i in range(len(labels)):
        va = 'bottom' if net[i] >= 0 else 'top'
        off = 1.5 if net[i] >= 0 else -1.5
        ax.text(x[i], net[i]+off, f'{net[i]:+.0f} user\n({pct[i]:+.0f}%)', ha='center', va=va,
                fontsize=9.5, fontweight='bold', color=(GREEN if net[i] > 0 else RED) if i != 0 else SAGE_D)
    ax.axvspan(0.5, 2.5, color=RED_SOFT, zorder=0)
    ax.axvspan(2.5, 4.5, color=GREEN_SOFT, zorder=0)
    ax.text(1.5, max(net)*0.62, 'GenZ 19–29\nKÉO LÙI', ha='center', va='center', fontsize=11,
            fontweight='bold', color=RED, linespacing=1.2)
    ax.text(3.5, max(net)+11, 'ĐỘNG CƠ GROWTH', ha='center', fontsize=11, fontweight='bold', color=GREEN)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(min(net)-16, max(net)+20); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_title('30+ tạo ~113% tăng trưởng RÒNG của Cozy — GenZ 19–29 kéo lùi −30%\n'
                 '(net user P4W 2025 vs 2024 · tổng net +53)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=12, linespacing=1.4)
    fig.savefig(_out('s5_growth_contribution.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Net contribution:', dict(zip(labels, net)), 'tot', tot)


def intensity_age():
    # % uống RTD >=2-3 lần/tuần (S3b_ordinal>=5) theo tuổi — đỡ claim "consumption intensity"
    heavy = (df['S3b_ordinal'] >= 5).astype(float)
    order = ['14 - 18 y.o.', '19 - 24 y.o.', '25 - 29 y.o.', '30 - 34 y.o.', '35 - 40 y.o.']
    pen = heavy.groupby(df['D3.Age']).mean().mul(100).round(1).reindex(order)
    labels = ['14–18', '19–24', '25–29', '30–34', '35–40']
    cols = [SAGE_L, SAGE_L, SAGE_M, GOLD, SAGE_D]
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.bar(labels, pen.values, color=cols, width=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
    avg = heavy.mean()*100
    ax.axhline(avg, ls='--', lw=1.2, color=SUB, zorder=2)
    ax.text(4.5, avg, f' TB {avg:.0f}', va='center', fontsize=8.5, color=SUB)
    for i, v in enumerate(pen.values):
        peak = labels[i] == '30–34'
        ax.text(i, v+1.3, f'{v:.0f}%', ha='center', fontsize=12 if peak else 10,
                fontweight='bold', color=GOLD_DEEP if peak else SAGE_D)
    ax.set_ylim(0, max(pen.values)+12); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.set_title('30+ uống ĐẬM hơn: 65% nhóm 30–34 uống RTD ≥2–3 lần/tuần (cao nhất)\n'
                 'vs GenZ 19–24 chỉ 50% · n=2.600',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=12, linespacing=1.4)
    fig.savefig(_out('s5_intensity_age.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Heavy(>=2-3/wk) by age:', dict(pen))


def gender_30plus_donut():
    a30 = df['D3.Age'].isin(['30 - 34 y.o.', '35 - 40 y.o.'])
    g = df.loc[a30, 'D2.Gender'].value_counts(normalize=True).mul(100).round(1)
    gv = [g.get('Female', 0), g.get('Male', 0)]
    fig, ax = plt.subplots(figsize=(4.2, 4.7))
    ax.pie(gv, colors=[GOLD, SAGE_M], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.40, edgecolor=WHITE, linewidth=2.5),
           autopct=lambda p: f'{p:.0f}%', pctdistance=0.80,
           textprops=dict(color=WHITE, fontsize=12, fontweight='bold'))
    ax.text(0, 0.16, 'NỮ', ha='center', fontsize=13, color=SUB, fontweight='bold')
    ax.text(0, -0.20, f'{gv[0]:.0f}%', ha='center', fontsize=30, fontweight='bold', color=GOLD_DEEP)
    ax.set_title('GIỚI TÍNH trong nhóm 30+ (target) — đậm hơn 61% toàn mẫu',
                 fontsize=11.5, fontweight='bold', color=TEXT, pad=8)
    ax.legend([f'Nữ · {gv[0]:.1f}%', f'Nam · {gv[1]:.1f}%'], loc='upper center',
              bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=9.5, frameon=False)
    ax.set(aspect='equal')
    fig.savefig(_out('s5_gender_30plus.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def gender_growth_30plus():
    czc = [c for c in df.columns if c.startswith('Q4. P4W_Trà Cozy')]
    cz = (df[czc].fillna(0).astype(float).sum(axis=1) > 0).astype(int)
    a30 = df['D3.Age'].isin(['30 - 34 y.o.', '35 - 40 y.o.'])
    fem = df['D2.Gender'] == 'Female'
    def rate(mask, wave): return cz[mask & a30 & (df['Wave'] == wave)].mean()*100
    data = [('Nữ 30+', rate(fem, 2024), rate(fem, 2025), GOLD),
            ('Nam 30+', rate(~fem, 2024), rate(~fem, 2025), SAGE_D)]
    femshare = (fem[a30].mean()*100)
    x = np.arange(len(data)); bw = 0.34
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    for i, (name, v24, v25, c) in enumerate(data):
        ax.bar(i-bw/2, v24, bw, color=SAGE_L, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.bar(i+bw/2, v25, bw, color=c, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(i-bw/2, v24+0.6, f'{v24:.1f}', ha='center', fontsize=9, color=SUB, zorder=4)
        ax.text(i+bw/2, v25+0.6, f'{v25:.1f}', ha='center', fontsize=10, fontweight='bold',
                color=(GOLD_DEEP if c == GOLD else SAGE_D), zorder=4)
        d = v25-v24
        ax.text(i, max(v24, v25)+3.4, f'▲ +{d:.1f}đ', ha='center', fontsize=12 if i == 0 else 10.5,
                fontweight='bold', color=GREEN, zorder=4)
    ax.text(0, -4.5, f'(67% nhóm 30+ là Nữ)', ha='center', fontsize=8.5, color=SUB, style='italic')
    from matplotlib.lines import Line2D
    ax.legend([Line2D([0],[0],marker='s',color='none',markerfacecolor=SAGE_L,markersize=10),
               Line2D([0],[0],marker='s',color='none',markerfacecolor=GOLD,markersize=10)],
              ['2024', '2025'], loc='upper left', fontsize=9, frameon=False)
    ax.set_xticks(x); ax.set_xticklabels([d[0] for d in data], fontsize=12, fontweight='bold')
    ax.set_ylim(-6, max(v25 for _, _, v25, _ in data)+10); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.set_title('NỮ 30+ là lõi tăng trưởng — Cozy P4W +9.5đ (nhanh hơn Nam 30+ +6.9đ)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=12)
    fig.savefig(_out('s5_gender_growth_30plus.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Gender growth 30+:', [(d[0], round(d[1],1), round(d[2],1)) for d in data])


def age_yoy():
    labels = ['14–18', '19–24', '25–29', '30–34', '35–40']
    wcols = list(agp.columns)  # [2024, 2025] (int)
    w24 = agp[wcols[0]].values; w25 = agp[wcols[1]].values
    delta = (w25 - w24).round(1)
    x = np.arange(len(labels)); bw = 0.38
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    # zones
    ax.axvspan(0.5, 2.5, color=RED_SOFT, zorder=0)      # at-risk 19–29
    ax.axvspan(2.5, 4.5, color=GREEN_SOFT, zorder=0)    # growth 30+
    ax.text(1.5, max(w25)*1.16, 'AT-RISK · GenZ 19–29', ha='center', fontsize=9.5,
            fontweight='bold', color=RED)
    ax.text(3.5, max(w25)*1.16, 'GROWTH POCKET · 30+', ha='center', fontsize=9.5,
            fontweight='bold', color=GREEN)
    ax.bar(x-bw/2, w24, bw, color=SAGE_L, label='2024', zorder=3)
    ax.bar(x+bw/2, w25, bw, color=SAGE_D, label='2025', zorder=3)
    for i in range(len(labels)):
        ax.text(x[i]-bw/2, w24[i]+0.4, f'{w24[i]:.1f}', ha='center', fontsize=8, color=SUB, zorder=4)
        ax.text(x[i]+bw/2, w25[i]+0.4, f'{w25[i]:.1f}', ha='center', fontsize=8.5, color=TEXT, fontweight='bold', zorder=4)
        d = delta[i]; up = d >= 0
        ax.text(x[i], max(w24[i], w25[i])+2.0, f'{"▲" if up else "▼"} {d:+.1f}đ',
                ha='center', fontsize=9.5, fontweight='bold', color=(GREEN if up else RED), zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, max(w25)*1.34); ax.set_yticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.legend(loc='upper left', fontsize=9, frameon=False)
    ax.set_title('Phân bố tuổi 2024 vs 2025  ·  % theo wave (n=1.300/wave)',
                 fontsize=11, color=SUB, pad=10)
    fig.savefig(_out('s5_age_yoy.png'), bbox_inches='tight', transparent=True); plt.close(fig)


if __name__ == '__main__':
    gender_donut(); region_donut(); income_bar(); age_yoy()
    olong_income(); cozy_reach_region(); cozy_p4w_age_yoy(); cozy_olong_by_region(); income_region()
    cozy_growth_contribution(); intensity_age(); gender_growth_30plus(); gender_30plus_donut()
    print(f'Done (font={FONT}): + gender_30plus_donut')
    print('Gender:', dict(GENDER), '| Region:', dict(REGION))
    print('Age by wave:\n', agp.to_string())
