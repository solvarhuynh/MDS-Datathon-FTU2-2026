# -*- coding: utf-8 -*-
"""
SCALE OPPORTUNITY — NORTH.
Present miền Bắc như cơ hội scale lớn nhất, bằng "bể khách ấm" (aware-but-not-using)
và headroom chuyển đổi. Số liệu đọc thẳng từ cleaned_dataset.xlsx (n=2.600).
Xuất: s5_scale_opportunity_north.png  (cùng tông xanh-vàng Cozy với slide 5)
"""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch

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
SAGE_M='#86A892'; SAGE_L='#B6CDBE'; SAGE_XL='#D8E3DC'
TEXT='#15321F'; SUB='#5A6B60'; BORDER='#DCE6DF'; WHITE='#FFFFFF'; GREEN_SOFT='#E4F1E9'
_av={f.name for f in fm.fontManager.ttflist}
FONT=next((f for f in ['Segoe UI','Calibri','Arial'] if f in _av),'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'font.size':11,'text.color':TEXT,'savefig.dpi':200})

df = pd.read_excel(_DATA, sheet_name='Dataset_Clean')
order = ['North', 'South', 'Mekong', 'Central']          # sắp theo size pool
aware = df['Q1Q2. Total aided awareness_Trà Cozy đóng chai'].fillna(0).astype(float) > 0
p4wc  = [c for c in df.columns if c.startswith('Q4. P4W_Trà Cozy')]
p4w   = df[p4wc].fillna(0).astype(float).sum(axis=1) > 0
g = df['Region']

users = p4w.groupby(g).sum().reindex(order).astype(int)               # đang dùng
pool  = ((aware) & (~p4w)).astype(int).groupby(g).sum().reindex(order).astype(int)  # biết-chưa-dùng
N     = g.value_counts().reindex(order).astype(int)
pool_rate = (pool / N * 100).round(1)
p4w_rate  = (users / N * 100).round(1)
best_rate = p4w_rate.max() / 100
north_head = int(round(N['North'] * best_rate - users['North']))
north_pct  = round(north_head / users['North'] * 100)
pool_share = round(pool['North'] / pool.sum() * 100)

fig, ax = plt.subplots(figsize=(8.2, 4.8))
y = np.arange(len(order))[::-1]
for i, r in enumerate(order):
    hi = (r == 'North')
    ax.barh(y[i], users[r], color=GOLD if hi else '#EBD38A', zorder=3)
    ax.barh(y[i], pool[r], left=users[r], color=GREEN if hi else SAGE_L, zorder=3)
    ax.text(users[r]/2, y[i], f'{users[r]}', ha='center', va='center',
            color=WHITE, fontsize=9, fontweight='bold', zorder=4)
    ax.text(users[r]+pool[r]+12, y[i], f'{pool[r]} người · {pool_rate[r]:.0f}% biết-chưa-dùng',
            va='center', fontsize=9.5, color=(GREEN_DEEP if hi else SUB),
            fontweight=('bold' if hi else 'normal'))

ax.set_yticks(y); ax.set_yticklabels([f'{r}\n(n={N[r]})' for r in order], fontsize=10.5)
for lbl, r in zip(ax.get_yticklabels(), order):
    if r == 'North': lbl.set_color(GREEN_DEEP); lbl.set_fontweight('bold')
ax.set_xlim(0, max(users+pool)*1.32); ax.set_xticks([])
for s in ['top','right','bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(BORDER)

from matplotlib.patches import Patch
ax.legend([Patch(color=GOLD), Patch(color=GREEN)],
          ['Đang dùng (P4W)', 'Biết nhưng CHƯA dùng = bể chuyển đổi'],
          loc='lower right', fontsize=9, frameon=False, bbox_to_anchor=(1.0, -0.02))

ax.set_title('MIỀN BẮC = CƠ HỘI SCALE LỚN NHẤT\n'
             f'{pool["North"]} người biết-chưa-dùng ({pool_rate["North"]:.0f}% dân vùng · '
             f'{pool_share}% bể chuyển đổi cả nước) — đạt mức Mekong (37%) → +{north_pct}% người dùng',
             fontsize=11, color=TEXT, fontweight='bold', pad=14, linespacing=1.5, loc='left')

fig.text(0.012, -0.02,
         'Awareness Bắc đã 94% → dư địa KHÔNG ở việc cho biết thêm, mà ở gỡ rào cản chọn–nhớ–mua.  '
         'Nguồn: khảo sát FUU, n=2.600.', fontsize=8, color=SUB)

fig.savefig(_out('s5_scale_opportunity_north.png'), bbox_inches='tight', transparent=True)
plt.close(fig)
print('saved s5_scale_opportunity_north.png')
print(pd.DataFrame({'N':N,'users':users,'pool':pool,'pool%':pool_rate,'P4W%':p4w_rate}).to_string())
print(f'North headroom to {best_rate*100:.0f}%: +{north_head} users (+{north_pct}%) · pool share {pool_share}%')
