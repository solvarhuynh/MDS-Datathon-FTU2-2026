"""
SLIDE 10 — AVAILABILITY & TRIAL GAP. 3 chart tách + 1 chart repeat (habit gap).
  s10_barrier.png     — rào cản phân phối 18.8% (2 thành phần)
  s10_instore.png     — in-store Cozy vs đối thủ (nền tảng bán lẻ)
  s10_trialhabit.png  — P4W 25.8 → BUMO 8.8 (−17pp)
  s10_repeat.png      — TỶ LỆ giữ chân trier (BUMO/P4W): Cozy 34% vs leaders ~55% (HABIT GAP)  ← thêm
Đọc cleaned_dataset.xlsx. PRIMARY. Palette xanh-vàng Cozy.
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrow, Patch

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

# barrier
q = [c for c in df.columns if c.startswith('QME2 - Trà Cozy đóng chai')]
sub = df[q].apply(pd.to_numeric, errors='coerce'); base = sub.notna().any(axis=1)
pct = (sub[base].fillna(0) > 0).mean().mul(100)
def bget(k): return round(pct[next(c for c in q if k in c)], 1)
B_STORE, B_COOL = bget('Asked but the store'), bget('Not preserved in cool')

# in-store
def instore(token, inc):
    col = next((c for c in df.columns if c.startswith('Q_TP1_') and token in c and c.endswith('Product display in stores, supermarket, …')), None)
    return round((df.loc[aware(inc), col].fillna(0).astype(float) > 0).mean()*100, 1)
INS = {'Cozy': instore('R15- Trà Cozy', 'Trà Cozy đóng chai'), 'C2': instore('R1- C2', 'C2'),
       'OLong Tea+': instore('R7- OLong Tea Plus', 'OLong Tea Plus'), 'Không Độ': instore('R11- Không Độ', 'Không Độ')}

# P4W & BUMO per brand
def p4w(inc):
    cols = [c for c in df.columns if c.startswith('Q4. P4W_') and inc.lower() in c.lower() and 'trà sữa' not in c.lower()]
    return round((df[cols].fillna(0).astype(float).sum(axis=1) > 0).mean()*100, 1)
def bumo(inc): return round(df['Q5.Bumo'].astype(str).str.contains(inc, case=False, na=False).mean()*100, 1)
BR = {'Cozy': 'Trà Cozy', 'C2': 'C2', 'OLong Tea+': 'OLong Tea Plus', 'Không Độ': 'Không Độ'}
P4W = {b: p4w(inc) for b, inc in BR.items()}
BUMOv = {b: bumo(inc) for b, inc in BR.items()}


def barrier():
    fig, ax = plt.subplots(figsize=(5.4, 3.0)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    tot = B_STORE + B_COOL
    ax.text(0, 88, 'Rào cản PHÂN PHỐI', fontsize=13, fontweight='bold', color=TEXT)
    ax.text(0, 50, f'{tot:.1f}%', fontsize=46, fontweight='bold', color=AMBER, va='center')
    ax.text(42, 60, 'người KHÔNG chọn Cozy', fontsize=10.5, color=TEXT)
    ax.text(42, 46, f'• Cửa hàng không bán: {B_STORE:.1f}%', fontsize=9.5, color=SUB)
    ax.text(42, 36, f'• Không bảo quản lạnh: {B_COOL:.1f}%', fontsize=9.5, color=SUB)
    ax.text(0, 8, 'khó THẤY / khó MUA → chặn ngay từ điểm bán', fontsize=9.5, color=AMBER, fontweight='bold', style='italic')
    fig.savefig(_out('s10_barrier.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def instore_chart():
    order = ['Cozy', 'C2', 'OLong Tea+', 'Không Độ']
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    y = np.arange(len(order))[::-1]
    for i, b in enumerate(order):
        c = GOLD if b == 'Cozy' else SAGE_M
        ax.barh(y[i], INS[b], color=c, height=0.6, zorder=3, edgecolor=WHITE, linewidth=1.5)
        ax.text(INS[b]+1, y[i], f'{INS[b]:.0f}%', va='center', fontsize=11, fontweight='bold',
                color=(GOLD_DEEP if b == 'Cozy' else SAGE_D))
        ax.text(-1, y[i], ('» '+b if b == 'Cozy' else b), ha='right', va='center', fontsize=10,
                fontweight=('bold' if b == 'Cozy' else 'normal'), color=(GREEN if b == 'Cozy' else TEXT))
    ax.set_xlim(-22, 88); ax.set_ylim(-0.6, len(order)-0.4); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Điểm chạm IN-STORE (trưng bày) — Cozy 68% ≈ leaders\n'
                 'kênh bán lẻ ĐÃ có nền tảng để khai thác · base aware',
                 fontsize=10.5, color=TEXT, fontweight='bold', pad=8, linespacing=1.4)
    fig.savefig(_out('s10_instore.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def trialhabit():
    fig, ax = plt.subplots(figsize=(6.0, 3.0)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    for i, (lab, v) in enumerate([('Dùng thử (P4W)', P4W['Cozy']), ('Thói quen (BUMO)', BUMOv['Cozy'])]):
        x0 = 4 + i*52
        ax.add_patch(FancyBboxPatch((x0, 25), 40, 50, boxstyle='round,pad=0,rounding_size=4',
                     fc=(GOLD if i == 0 else '#F6D98A'), ec=GOLD_DEEP, lw=1.6))
        ax.text(x0+20, 56, f'{v:.1f}%', ha='center', fontsize=26, fontweight='bold', color=GOLD_DEEP)
        ax.text(x0+20, 34, lab, ha='center', fontsize=9.5, color=TEXT)
    ax.add_patch(FancyArrow(45, 50, 10, 0, width=2.5, head_width=8, head_length=4, color=RED, length_includes_head=True))
    ax.text(50, 66, '−17pp', ha='center', fontsize=11, fontweight='bold', color=RED)
    ax.text(0, 90, 'TRIAL → HABIT GAP', fontsize=13, fontweight='bold', color=TEXT)
    ax.text(0, 10, 'thử ít, lặp lại càng ít → chưa thành thói quen', fontsize=9.5, color=SUB, style='italic')
    fig.savefig(_out('s10_trialhabit.png'), bbox_inches='tight', transparent=True); plt.close(fig)


def repeat():
    # tỷ lệ giữ chân trier = BUMO / P4W
    order = ['C2', 'Không Độ', 'OLong Tea+', 'Cozy']
    conv = {b: round(BUMOv[b]/P4W[b]*100, 0) for b in order}
    srt = sorted(order, key=lambda b: conv[b], reverse=True)
    lead = np.mean([conv[b] for b in ['C2', 'OLong Tea+', 'Không Độ']])
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    y = np.arange(len(srt))[::-1]
    for i, b in enumerate(srt):
        c = GOLD if b == 'Cozy' else SAGE_M
        ax.barh(y[i], conv[b], color=c, height=0.6, zorder=3, edgecolor=WHITE, linewidth=1.5)
        # nhãn giá trị: trong thanh (trắng) cho leaders để không đụng đường TB; ngoài cho Cozy
        if b == 'Cozy':
            ax.text(conv[b]+1.5, y[i], f'{conv[b]:.0f}%', va='center', fontsize=12, fontweight='bold', color=GOLD_DEEP)
        else:
            ax.text(conv[b]-1.5, y[i], f'{conv[b]:.0f}%', ha='right', va='center', fontsize=11, fontweight='bold', color=WHITE)
        ax.text(-1, y[i], ('» '+b if b == 'Cozy' else b), ha='right', va='center', fontsize=10,
                fontweight=('bold' if b == 'Cozy' else 'normal'), color=(GREEN if b == 'Cozy' else TEXT))
    ax.axvline(lead, ls='--', lw=1.3, color=GREEN, zorder=4)
    ax.text(lead, y[0]+0.55, f'TB leaders {lead:.0f}%', ha='center', fontsize=8.5, color=GREEN, fontweight='bold')
    ax.set_xlim(-18, 66); ax.set_ylim(-0.6, len(srt)+0.1); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('Giữ chân người THỬ → DÙNG CHÍNH (BUMO÷P4W): Cozy 34% — chỉ ~⅗ leaders\n'
                 'không chỉ trial thấp, mà REPEAT cũng yếu → khó thành thói quen',
                 fontsize=10, color=TEXT, fontweight='bold', pad=8, linespacing=1.4)
    fig.savefig(_out('s10_repeat.png'), bbox_inches='tight', transparent=True); plt.close(fig)
    print('Repeat conv:', conv)


if __name__ == '__main__':
    barrier(); instore_chart(); trialhabit(); repeat()
    print(f'Done (font={FONT}) · P4W {P4W} · BUMO {BUMOv}')
