from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from visualize_cozy_brandhealth import BRANDS, normalize_numeric, read_sheet


BARRIER_GROUPS = {
    "Taste / flavor": [
        "Do not like the flavor/The flavor do not taste good",
        "Does not have enough flavour that I want to choose",
    ],
    "Availability": [
        "Asked but the store does not sell it",
        "Not preserved in cool place",
    ],
    "Brand relevance": [
        "Do not want other people see when I drink/buy this brand",
        "Do not like recent packaging designs",
        "Does not elegant, premium",
    ],
    "Health / trust": [
        "Unhealthy",
        "Do not trust in product quality",
    ],
    "Promotion": [
        "Usually do not have sale promotion while other brands have",
    ],
}

BRANDS_TO_SHOW = [
    "Cozy",
    "C2",
    "OLong Tea Plus",
    "Không Độ",
    "Dr. Thanh",
    "TH True Tea",
]


def find_barrier_columns(columns: list[str], source_brand: str, item: str) -> list[str]:
    exact = f"QME2 - {source_brand}_{item}"
    matches = [column for column in columns if column == exact]
    if matches:
        return matches

    prefix = f"QME2 - {source_brand}_"
    return [
        column
        for column in columns
        if column.startswith(prefix) and item.lower() in column.lower()
    ]


def respondent_share_any(dataset: pd.DataFrame, columns: list[str]) -> float:
    if not columns:
        return np.nan
    flags = pd.DataFrame({column: normalize_numeric(dataset[column]) for column in columns})
    return flags.gt(0).any(axis=1).mean() * 100


def calculate_barriers(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset.columns = [str(column) for column in dataset.columns]
    columns = list(dataset.columns)

    rows = []
    for display_brand in BRANDS_TO_SHOW:
        source_brand = BRANDS[display_brand]
        row = {"Brand": display_brand}

        for group, items in BARRIER_GROUPS.items():
            group_columns = []
            for item in items:
                group_columns.extend(find_barrier_columns(columns, source_brand, item))
            row[group] = respondent_share_any(dataset, group_columns)

        rows.append(row)

    return pd.DataFrame(rows).set_index("Brand")


def draw_heatmap(barriers: pd.DataFrame, output_path: Path) -> None:
    plot_data = barriers.copy()
    max_value = np.nanmax(plot_data.to_numpy())

    fig, ax = plt.subplots(figsize=(12.8, 6.8), dpi=180)
    masked = np.ma.masked_invalid(plot_data.to_numpy())
    image = ax.imshow(masked, cmap="YlOrBr", aspect="auto", vmin=0, vmax=max_value)

    ax.set_xticks(np.arange(len(plot_data.columns)))
    ax.set_xticklabels(plot_data.columns, fontsize=10)
    ax.set_yticks(np.arange(len(plot_data.index)))
    ax.set_yticklabels(plot_data.index, fontsize=10)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    for row_idx in range(plot_data.shape[0]):
        for col_idx in range(plot_data.shape[1]):
            value = plot_data.iloc[row_idx, col_idx]
            if pd.isna(value):
                label = "n/a"
                color = "#6b7280"
            else:
                label = f"{value:.1f}%"
                color = "white" if value >= max_value * 0.55 else "#1f2937"
            ax.text(
                col_idx,
                row_idx,
                label,
                ha="center",
                va="center",
                color=color,
                fontsize=9,
                fontweight="bold",
            )

    ax.set_title(
        "Conversion Blockers: Cozy Is Most Exposed on Taste and Availability",
        fontsize=15,
        fontweight="bold",
        loc="left",
        pad=26,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(-0.5, len(plot_data.columns), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(plot_data.index), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(image, ax=ax, fraction=0.026, pad=0.02)
    cbar.ax.set_ylabel("Higher barrier", rotation=270, labelpad=14)

    cozy = plot_data.loc["Cozy"].sort_values(ascending=False)
    insight = (
        f"Key insight: Cozy's top blockers are {cozy.index[0]} ({cozy.iloc[0]:.1f}%) "
        f"and {cozy.index[1]} ({cozy.iloc[1]:.1f}%). Promotion is a secondary issue."
    )
    fig.text(0.07, 0.045, insight, fontsize=9.5, color="#374151", weight="bold")
    fig.tight_layout(rect=[0.04, 0.08, 0.98, 0.92])
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def draw_priority_bar(barriers: pd.DataFrame, output_path: Path) -> None:
    cozy = barriers.loc["Cozy"].sort_values(ascending=True)
    colors = ["#f5d76e", "#eab84b", "#d98c28", "#b96118", "#7f3b08"]

    fig, ax = plt.subplots(figsize=(9, 5.4), dpi=180)
    ax.barh(cozy.index, cozy.values, color=colors[: len(cozy)])

    for idx, value in enumerate(cozy.values):
        ax.text(value + 0.5, idx, f"{value:.1f}%", va="center", fontsize=10, color="#1f2937")

    ax.set_title("Cozy Priority Barriers to Fix", fontsize=15, fontweight="bold", loc="left", pad=14)
    ax.set_xlabel("% respondents citing barrier")
    ax.set_xlim(0, max(cozy.values) * 1.22)
    ax.grid(axis="x", color="#e5e7eb", linewidth=0.8)
    ax.set_axisbelow(True)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def write_notes(barriers: pd.DataFrame, output_path: Path) -> None:
    cozy = barriers.loc["Cozy"].sort_values(ascending=False)
    text = f"""Slide 10 - Key Driver Analysis / Barriers & Conversion Blockers

Main message:
Cozy's conversion problem is mainly driven by product experience and availability, not promotion.

Key insight:
- Taste / flavor is the largest blocker for Cozy at {cozy['Taste / flavor']:.1f}%.
- Availability is the second blocker at {cozy['Availability']:.1f}%.
- Promotion is low at {cozy['Promotion']:.1f}%, so discounting alone is unlikely to fix conversion.

Priority drivers:
1. Taste / flavor: refresh taste profile, hero the most appealing variants, support with sampling.
2. Availability: improve cold-channel presence and focus on office, school, lunch, and after-meal occasions.
3. Brand relevance: modernize pack/communication and anchor Cozy in a daily tea routine.

Slide design:
- Left: heatmap by brand x barrier group.
- Right: priority box with three actions: Fix taste, increase availability, activate trial-to-repeat.
- Use warm barrier colors: light yellow for low barrier, brown/dark orange for high barrier.
"""
    output_path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize Cozy conversion blockers from cleaned_dataset.xlsx")
    parser.add_argument("--input", default="cleaned_dataset.xlsx", help="Path to cleaned_dataset.xlsx")
    parser.add_argument("--outdir", default="outputs", help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    dataset = read_sheet(input_path, "Dataset_Clean")
    barriers = calculate_barriers(dataset)

    csv_path = outdir / "cozy_barriers_summary.csv"
    heatmap_path = outdir / "cozy_barriers_heatmap.png"
    priority_path = outdir / "cozy_priority_barriers.png"
    notes_path = outdir / "cozy_barriers_strategy_notes.txt"

    barriers.round(2).to_csv(csv_path, encoding="utf-8-sig")
    draw_heatmap(barriers, heatmap_path)
    draw_priority_bar(barriers, priority_path)
    write_notes(barriers, notes_path)

    print(f"Saved: {csv_path}")
    print(f"Saved: {heatmap_path}")
    print(f"Saved: {priority_path}")
    print(f"Saved: {notes_path}")


if __name__ == "__main__":
    main()
