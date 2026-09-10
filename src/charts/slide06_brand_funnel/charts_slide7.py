"""
SLIDE 7 (deck Slide 6) — BRAND FUNNEL + HEALTH SCORECARD.
Đọc thẳng cleaned_dataset.xlsx → 3 chart:
  1) s7_funnel.png      — funnel Cozy + % chuyển đổi mỗi bậc + benchmark C2 · bottleneck Consideration
  2) s7_scorecard.png   — heatmap 7 brand × 5 metric (leaders convert, Cozy rớt sau awareness)
  3) s7_conversion.png  — HIỆU SUẤT chuyển đổi Aware→P4W theo brand (chart "đắt" slide đang thiếu)

PRIMARY (n=2.600). Palette xanh-vàng Cozy. Chạy: python charts_slide7.py
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap

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

GOLD='#F2B705'; GOLD_DEEP='#D89A04'; GREEN='#1B7A3D'; GREEN_DEEP='#0E5C2F'
SAGE_D='#5E8268'; SAGE_M='#86A892'; SAGE_L='#B6CDBE'; SAGE_XL='#DCE7DF'
RED='#D9534F'; RED_SOFT='#FBEAE9'; TEXT='#15321F'; SUB='#5A6B60'
BORDER='#DCE6DF'; LIGHTBG='#F6FAF7'; WHITE='#FFFFFF'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name="Dataset_Clean")
BRANDS = {  # name: (include, exclude)
    'C2': ('C2', 'Trà sữa C2'), 'OLong Tea+': ('OLong Tea Plus', None),
    'Không Độ': ('Không Độ', 'Trà sữa'), 'Cozy': ('Cozy', None),
    'Boncha': ('Boncha', None), 'TH True Tea': ('TH True Tea', None), 'Dr. Thanh': ('Dr. Thanh', None),
}
BLOCKS = {'Aware': 'Q1Q2. Total aided awareness_', 'Consid': 'Q4Q8.BRAND CONSIDERATION SET_',
          'P3M': 'Q3. P3M _', 'P4W': 'Q4. P4W_', 'Spont': 'Q1.Total Spontaneous_'}

def metric(pre, inc, exc):
    cols = [c for c in df.columns if c.startswith(pre) and inc.lower() in c.lower()
            and (exc is None or exc.lower() not in c.lower())]
    if not cols: return np.nan
    return round((df[cols].fillna(0).astype(float).sum(axis=1) > 0).mean()*100, 1)

SC = {}
for b, (inc, exc) in BRANDS.items():
    r = {m: metric(pre, inc, exc) for m, pre in BLOCKS.items()}
    r['TOM'] = round(df['Q1.TOM'].astype(str).str.contains(inc, case=False, na=False).mean()*100, 1)
    r['BUMO'] = round(df['Q5.Bumo'].astype(str).str.contains(inc, case=False, na=False).mean()*100, 1)
    SC[b] = r


# ===== 1) COZY FUNNEL + conversion + benchmark C2 =====
def funnel():
    steps = ['Aware', 'Spont', 'Consid', 'P3M', 'P4W', 'BUMO']
    labs = ['Awareness', 'Spontaneous', 'Consideration', 'P3M', 'P4W', 'BUMO']
    cz = [SC['Cozy'][s] for s in steps]
    c2 = [SC['C2'][s] for s in steps]
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    y = np.arange(len(steps))[::-1]
    for i, s in enumerate(steps):
        yi = y[i]
        col = RED if labs[i] == 'Consideration' else GOLD
        ax.add_patch(FancyBboxPatch((0, yi-0.34), cz[i], 0.68, boxstyle='round,pad=0,rounding_size=0.1',
                     fc=col, ec='none', zorder=3))
        ax.text(cz[i]+1.5, yi, f'{cz[i]:.1f}%', va='center', fontsize=11, fontweight='bold',
                color=(RED if col == RED else GOLD_DEEP), zorder=4)
        ax.text(-1.5, yi, labs[i], va='center', ha='right', fontsize=10.5,
                fontweight=('bold' if col == RED else 'normal'), color=TEXT, zorder=4)
        ax.text(101, yi, f'vs C2 {c2[i]:.0f}', va='center', ha='left', fontsize=8.5, color=SAGE_M, zorder=4)
        if i > 0:  # % chuyển đổi từ bậc trước
            conv = cz[i]/cz[i-1]*100
            ax.text(cz[i-1]+10, (y[i-1]+yi)/2, f'↓ {conv:.0f}%', va='center', ha='center',
                    fontsize=8.5, color=(RED if conv < 50 else SUB), fontweight='bold', zorder=4)
    # callout bottleneck Aware->Consid
    drop = SC['Cozy']['Consid']/SC['Cozy']['Aware']*100
    ax.annotate(f'Aware→Consid chỉ giữ {drop:.0f}%\n= mất ~⅔ (C2 giữ 78%)',
                xy=(SC['Cozy']['Consid']+1, y[2]+0.28), xytext=(60, y[2]+0.78),
                fontsize=9.5, fontweight='bold', color=RED, va='center', ha='left',
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.6))
    ax.set_xlim(-22, 116); ax.set_ylim(-0.7, len(steps)-0.3); ax.axis('off')
    ax.set_title('Funnel Cozy: rơi mạnh nhất ngay Awareness→Consideration (bottleneck)\n'
                 'TOM chỉ 8.7% vs C2 35.8% · % = tỷ lệ giữ từ bậc trước',
                 fontsize=11, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s7_funnel.png'), bbox_inches='tight', transparent=True); plt.close(fig)


# ===== 2) SCORECARD HEATMAP =====
def scorecard():
    order = ['C2', 'OLong Tea+', 'Không Độ', 'Cozy', 'Boncha', 'TH True Tea', 'Dr. Thanh']
    metrics = ['Aware', 'Consid', 'P3M', 'P4W', 'BUMO']
    mlab = ['Awareness', 'Consideration', 'P3M', 'P4W', 'BUMO']
    M = np.array([[SC[b][m] for m in metrics] for b in order])
    cmap = LinearSegmentedColormap.from_list('g', ['#FFFFFF', '#BfD9C7', GREEN, GREEN_DEEP])
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.imshow(M, cmap=cmap, aspect='auto', vmin=0, vmax=100)
    for i in range(len(order)):
        for j in range(len(metrics)):
            v = M[i, j]
            ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=10,
                    fontweight='bold', color=(WHITE if v > 55 else TEXT))
    ax.set_xticks(range(len(metrics))); ax.set_xticklabels(mlab, fontsize=10, fontweight='bold')
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([('» '+b if b == 'Cozy' else b) for b in order], fontsize=10.5,
                       fontweight='bold')
    ax.xaxis.tick_top(); ax.tick_params(length=0)
    # viền Cozy
    ci = order.index('Cozy')
    ax.add_patch(Rectangle((-0.5, ci-0.5), len(metrics), 1, fill=False, ec=GOLD, lw=3, zorder=5))
    ax.set_title('Brand Health Scorecard — leaders đậm đều, Cozy SÁNG dần sau Awareness\n'
                 '(% người dùng · n=2.600 · ô càng xanh = càng cao)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=30, linespacing=1.4)
    for s in ax.spines.values(): s.set_visible(False)
    fig.savefig(_out('s7_scorecard.png'), bbox_inches='tight', transparent=True); plt.close(fig)


# ===== 3) AWARE→P4W CONVERSION EFFICIENCY (chart đắt) =====
def conversion():
    order = ['C2', 'OLong Tea+', 'Không Độ', 'Cozy', 'Boncha', 'TH True Tea', 'Dr. Thanh']
    conv = {b: SC[b]['P4W']/SC[b]['Aware']*100 for b in order}
    srt = sorted(order, key=lambda b: conv[b], reverse=True)
    leaders_avg = np.mean([conv[b] for b in ['C2', 'OLong Tea+', 'Không Độ']])
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    y = np.arange(len(srt))[::-1]
    for i, b in enumerate(srt):
        c = GOLD if b == 'Cozy' else SAGE_M if b in ('C2', 'OLong Tea+', 'Không Độ') else SAGE_L
        ax.barh(y[i], conv[b], color=c, height=0.62, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(conv[b]+1, y[i], f'{conv[b]:.0f}%', va='center', fontsize=10.5, fontweight='bold',
                color=(GOLD_DEEP if b == 'Cozy' else SAGE_D), zorder=4)
        ax.text(-1.5, y[i], ('» '+b if b == 'Cozy' else b), va='center', ha='right',
                fontsize=10, fontweight=('bold' if b == 'Cozy' else 'normal'),
                color=(GREEN if b == 'Cozy' else TEXT), zorder=4)
    ax.axvline(leaders_avg, ls='--', lw=1.4, color=GREEN, zorder=2)
    ax.text(leaders_avg+0.5, y[0]+0.5, f'TB 3 leaders {leaders_avg:.0f}%', fontsize=8.5, color=GREEN)
    ax.set_xlim(-20, 70); ax.set_ylim(-0.7, len(srt)-0.3); ax.set_xticks([]); ax.axis('off')
    ax.set_title('HIỆU SUẤT chuyển đổi Awareness→P4W: Cozy 28% — chỉ ~½ leaders\n'
                 '(P4W ÷ Awareness · biết nhiều ≠ dùng nhiều)',
                 fontsize=11, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s7_conversion.png'), bbox_inches='tight', transparent=True); plt.close(fig)


# ===== 4) FUNNEL CHUẨN HOÁ (Awareness=100) — prove "leaders convert tốt hơn" =====
def funnel_compare():
    steps = ['Aware', 'Consid', 'P3M', 'P4W', 'BUMO']
    xlab = ['Awareness', 'Consideration', 'P3M', 'P4W', 'BUMO']
    show = [('Cozy', GOLD, 3.2, 'o'), ('C2', SAGE_D, 2, 's'),
            ('OLong Tea+', SAGE_M, 2, '^'), ('Không Độ', SAGE_L, 2, 'D')]
    x = np.arange(len(steps))
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    for b, c, lw, mk in show:
        base = SC[b]['Aware']
        ret = [SC[b][s]/base*100 for s in steps]
        ax.plot(x, ret, color=c, lw=lw, marker=mk, markersize=8 if b == 'Cozy' else 6,
                zorder=(5 if b == 'Cozy' else 3), label=b)
        ax.text(x[-1]+0.12, ret[-1], f'{b} {ret[-1]:.0f}', va='center', fontsize=9,
                fontweight=('bold' if b == 'Cozy' else 'normal'),
                color=(GOLD_DEEP if b == 'Cozy' else SUB))
        if b == 'Cozy':
            for xi, r in zip(x, ret):
                ax.text(xi, r-6, f'{r:.0f}%', ha='center', fontsize=9, fontweight='bold', color=GOLD_DEEP)
    # khoanh điểm rơi tại Consideration
    cz_c = SC['Cozy']['Consid']/SC['Cozy']['Aware']*100
    ax.annotate('Cozy giữ 38% ở Consideration\nvs leaders 66–78% → rớt NGAY', xy=(1, cz_c),
                xytext=(1.35, 60), fontsize=9.5, fontweight='bold', color=RED, va='center',
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.6))
    ax.set_xticks(x); ax.set_xticklabels(xlab, fontsize=10.5)
    ax.set_ylim(0, 108); ax.set_yticks([]); ax.set_xlim(-0.3, len(steps)+0.4)
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)
    ax.legend(loc='upper right', fontsize=9, frameon=False, ncol=2)
    ax.set_title('Cùng xuất phát Awareness=100 — Cozy RỚT nhanh nhất\n'
                 '(% giữ lại từ awareness · leaders convert tốt hơn, không chỉ aware nhiều hơn)',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=10, linespacing=1.4)
    fig.savefig(_out('s7_funnel_compare.png'), bbox_inches='tight', transparent=True); plt.close(fig)


if __name__ == '__main__':
    funnel(); scorecard(); conversion(); funnel_compare()
    print(f'Done (font={FONT}): funnel + scorecard + conversion')
    for b in ['Cozy', 'C2', 'OLong Tea+', 'Không Độ']:
        cv = SC[b]['P4W']/SC[b]['Aware']*100
        print(f"{b}: Aware {SC[b]['Aware']} P4W {SC[b]['P4W']} conv {cv:.0f}%")
