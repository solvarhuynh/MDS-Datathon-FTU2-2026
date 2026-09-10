import os
from pathlib import Path
import pandas as pd
import numpy as np

# Stable writable cache paths (must be set before importing matplotlib)
os.environ['MPLCONFIGDIR'] = '/private/tmp/mplcache'
os.environ['XDG_CACHE_HOME'] = '/private/tmp/xdg-cache'
Path('/private/tmp/mplcache').mkdir(parents=True, exist_ok=True)
Path('/private/tmp/xdg-cache').mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Ưu tiên chạy tại thư mục hiện tại (vị trí mới), fallback về đường dẫn cũ
BASE = Path.cwd()
EXCEL = BASE / 'cleaned_dataset.xlsx'
if not EXCEL.exists():
    EXCEL = BASE / 'clean_data_analysis' / 'cleaned_dataset.xlsx'
OUT = BASE / 'slide6_charts'
OUT.mkdir(parents=True, exist_ok=True)

# 1) Read data
_df = pd.read_excel(EXCEL)
use_cols = [
    'S2.Category used in P4W_RTD Herbal Tea',
    'S2.Category used in P4W_RTD Green Tea',
    'S2.Category used in P4W_RTD Olong Tea',
]
_df['is_rtd_user'] = (_df[use_cols].fillna(0).max(axis=1) == 1)
df = _df[_df['is_rtd_user']].copy()
df25 = df[df['Wave'] == 2025].copy()

# 2) Aggregate

def composition(series: pd.Series) -> pd.Series:
    return series.value_counts(normalize=True).mul(100).sort_values(ascending=False)

gender = composition(df25['D2.Gender'])
region = composition(df25['Region'])
income = composition(df25['D4.Income'])

age = df.groupby(['Wave', 'D3.Age']).size().reset_index(name='n')
tot = df.groupby('Wave').size().to_dict()
age['share'] = age.apply(lambda r: r['n'] / tot[r['Wave']] * 100, axis=1)
piv = age.pivot(index='D3.Age', columns='Wave', values='share').fillna(0)
order = ['14 - 18 y.o.', '19 - 24 y.o.', '25 - 29 y.o.', '30 - 34 y.o.', '35 - 40 y.o.']
piv = piv.reindex([x for x in order if x in piv.index])

# 3) Plot helpers
plt.rcParams['font.family'] = 'DejaVu Sans'
colors = ['#2E7D32', '#66BB6A', '#26A69A', '#FFA726', '#5C6BC0', '#EF5350', '#8D6E63', '#42A5F5']

def save_pie(series: pd.Series, title: str, filename: str):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=180)
    vals = series.values
    labels = series.index.tolist()
    wedges, _, autotexts = ax.pie(
        vals,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(vals)],
        pctdistance=0.75,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 10},
    )
    for t in autotexts:
        t.set_color('black')
        t.set_fontsize(10)
    ax.set_title(title, fontsize=14, weight='bold')
    ax.legend(
        wedges,
        [f'{l}: {v:.1f}%' for l, v in zip(labels, vals)],
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
        fontsize=10,
    )
    fig.tight_layout()
    out = OUT / filename
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    return out

def save_age(filename: str):
    labels = piv.index.tolist()
    p24 = piv[2024].values
    p25 = piv[2025].values
    yoy = p25 - p24

    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(11, 6), dpi=180)
    ax.bar(x - width / 2, p24, width, label='2024', color='#5C9DED')
    ax.bar(x + width / 2, p25, width, label='2025', color='#2E7D32')

    ax.set_title('Cơ cấu độ tuổi RTD users: 2024 vs 2025', fontsize=14, weight='bold')
    ax.set_ylabel('Tỷ trọng (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.25)
    ax.legend(frameon=False, loc='upper right')

    for i, (a, b, y) in enumerate(zip(p24, p25, yoy)):
        ax.text(i, max(a, b) + 0.5, f'YoY {y:+.1f}đ%', ha='center', va='bottom', fontsize=10)

    ax.set_ylim(0, max(np.max(p24), np.max(p25)) + 4)
    fig.tight_layout()
    out = OUT / filename
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    return out

def save_age_2025_only(filename: str):
    labels = piv.index.tolist()
    p25 = piv[2025].values

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=180)
    bars = ax.bar(x, p25, color='#2E7D32', width=0.55)

    ax.set_title('Cơ cấu độ tuổi RTD users năm 2025', fontsize=14, weight='bold')
    ax.set_ylabel('Tỷ trọng (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.25)

    for bar, val in zip(bars, p25):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.35,
            f'{val:.1f}%',
            ha='center',
            va='bottom',
            fontsize=10,
        )

    ax.set_ylim(0, max(p25) + 4)
    fig.tight_layout()
    out = OUT / filename
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    return out

# 4) Export charts
files = []
files.append(save_pie(gender, 'Cơ cấu giới tính (RTD users 2025)', '01_gender_2025.png'))
files.append(save_pie(region, 'Cơ cấu khu vực (RTD users 2025)', '02_region_2025.png'))
files.append(save_age('04_age_2024_2025_yoy.png'))

print('Excel source:', EXCEL)
for f in files:
    print(f)
