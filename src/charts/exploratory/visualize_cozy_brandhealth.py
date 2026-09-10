from __future__ import annotations

import argparse
import re
import textwrap
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BRANDS = {
    "Cozy": "Trà Cozy đóng chai",
    "C2": "C2",
    "OLong Tea Plus": "OLong Tea Plus",
    "Không Độ": "Không Độ",
    "Dr. Thanh": "Dr. Thanh",
    "Boncha": "Trà mật ong Boncha",
    "TH True Tea": "Trà TH True Tea",
}

VARIANT_PREFIXES = {
    "Trà Cozy đóng chai": "Trà Cozy",
    "Trà TH True Tea": "TH True Tea",
}

METRICS = {
    "Awareness": "Q1Q2. Total aided awareness_{brand}",
    "P3M usage": "Q3. P3M _{brand}",
    "P4W usage": "Q4. P4W_{brand}",
    "Consideration": "Q4Q8.BRAND CONSIDERATION SET_{brand}",
}


def _cell_col_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    value = 0
    for ch in letters:
        value = value * 26 + ord(ch.upper()) - 64
    return value - 1


def _xlsx_cell_text(cell: ET.Element, ns: dict[str, str], shared_strings: list[str]) -> str:
    if cell.attrib.get("t") == "inlineStr":
        return "".join(
            text_node.text or ""
            for text_node in cell.iter(f"{{{ns['a']}}}t")
        )

    value_node = cell.find("a:v", ns)
    if value_node is None:
        return ""

    value = value_node.text or ""
    if cell.attrib.get("t") == "s":
        return shared_strings[int(value)]
    return value


def _read_xlsx_sheet_without_openpyxl(path: Path, sheet_name: str) -> pd.DataFrame:
    ns = {
        "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    with zipfile.ZipFile(path) as zf:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for item in root:
                shared_strings.append(
                    "".join(
                        text_node.text or ""
                        for text_node in item.iter(f"{{{ns['a']}}}t")
                    )
                )

        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}

        sheet_target = None
        for sheet in workbook.find("a:sheets", ns):
            if sheet.attrib["name"] == sheet_name:
                rel_id = sheet.attrib[f"{{{ns['r']}}}id"]
                sheet_target = rel_map[rel_id].lstrip("/")
                break

        if sheet_target is None:
            raise ValueError(f"Sheet not found: {sheet_name}")

        if not sheet_target.startswith("xl/"):
            sheet_target = "xl/" + sheet_target

        sheet_root = ET.fromstring(zf.read(sheet_target))
        rows = []
        for row in sheet_root.find("a:sheetData", ns):
            values = []
            for cell in row:
                col_idx = _cell_col_index(cell.attrib["r"])
                while len(values) <= col_idx:
                    values.append("")
                values[col_idx] = _xlsx_cell_text(cell, ns, shared_strings)
            rows.append(values)

    header = rows[0]
    width = len(header)
    records = []
    for row in rows[1:]:
        padded = row + [""] * (width - len(row))
        records.append(padded[:width])

    return pd.DataFrame(records, columns=header)


def read_sheet(path: Path, sheet_name: str) -> pd.DataFrame:
    try:
        return pd.read_excel(path, sheet_name=sheet_name)
    except ImportError:
        return _read_xlsx_sheet_without_openpyxl(path, sheet_name)


def normalize_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0)


def find_column(columns: list[str], target: str) -> str:
    if target in columns:
        return target

    normalized_target = re.sub(r"\s+", " ", target).strip().lower()
    for column in columns:
        normalized_column = re.sub(r"\s+", " ", str(column)).strip().lower()
        if normalized_column == normalized_target:
            return column

    raise KeyError(f"Column not found: {target}")


def find_metric_columns(columns: list[str], target: str, source_brand: str) -> list[str]:
    try:
        return [find_column(columns, target)]
    except KeyError:
        pass

    metric_prefix, _, _ = target.partition(source_brand)
    variant_target = metric_prefix + VARIANT_PREFIXES.get(source_brand, source_brand)
    normalized_target = re.sub(r"\s+", " ", variant_target).strip().lower()
    matches = []
    for column in columns:
        normalized_column = re.sub(r"\s+", " ", str(column)).strip().lower()
        if normalized_column.startswith(normalized_target):
            matches.append(column)

    if not matches:
        raise KeyError(f"Column not found: {target}")
    return matches


def respondent_share_any(dataset: pd.DataFrame, columns: list[str]) -> float:
    flags = pd.DataFrame({col: normalize_numeric(dataset[col]) for col in columns})
    return flags.gt(0).any(axis=1).mean() * 100


def brand_text_share(series: pd.Series, source_brand: str) -> float:
    prefix = VARIANT_PREFIXES.get(source_brand, source_brand)
    values = series.fillna("").astype(str).str.strip()
    return values.str.startswith(prefix).mean() * 100


def build_brand_map(brandlist_df: pd.DataFrame) -> dict[str, str]:
    code_col = find_column(list(brandlist_df.columns), "brand_code")
    name_col = find_column(list(brandlist_df.columns), "brand_name")
    mapping = {}
    for _, row in brandlist_df.iterrows():
        code = str(row[code_col]).strip()
        name = str(row[name_col]).strip()
        if code and name and name.lower() != "nan":
            mapping[code.replace(".0", "")] = name
    return mapping


def calculate_scores(dataset: pd.DataFrame, brandlist: pd.DataFrame) -> pd.DataFrame:
    columns = [str(col) for col in dataset.columns]
    dataset.columns = columns

    bumo_col = find_column(columns, "Q5.Bumo")
    previous_bumo_col = find_column(columns, "Q7. Previous BUMO")

    rows = []
    for display_brand, source_brand in BRANDS.items():
        row = {"Brand": display_brand}

        for metric, template in METRICS.items():
            metric_columns = find_metric_columns(columns, template.format(brand=source_brand), source_brand)
            row[metric] = respondent_share_any(dataset, metric_columns)

        row["BUMO"] = brand_text_share(dataset[bumo_col], source_brand)
        previous_bumo = brand_text_share(dataset[previous_bumo_col], source_brand)
        row["YoY change"] = row["BUMO"] - previous_bumo

        if row["Awareness"] > 0:
            row["Awareness -> P4W"] = row["P4W usage"] / row["Awareness"] * 100
            row["Awareness -> BUMO"] = row["BUMO"] / row["Awareness"] * 100
        else:
            row["Awareness -> P4W"] = 0
            row["Awareness -> BUMO"] = 0

        rows.append(row)

    return pd.DataFrame(rows).set_index("Brand")


def draw_heatmap(scores: pd.DataFrame, output_path: Path) -> None:
    metric_cols = [
        "Awareness",
        "P3M usage",
        "P4W usage",
        "Consideration",
        "BUMO",
        "YoY change",
    ]
    values = scores[metric_cols].copy()

    fig, ax = plt.subplots(figsize=(13.5, 7.2), dpi=180)
    image = ax.imshow(values, cmap="YlGn", aspect="auto")

    ax.set_xticks(np.arange(len(metric_cols)))
    ax.set_xticklabels(metric_cols, fontsize=10)
    ax.set_yticks(np.arange(len(values.index)))
    ax.set_yticklabels(values.index, fontsize=10)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            val = values.iloc[i, j]
            if metric_cols[j] == "YoY change":
                label = f"{val:+.1f}pp"
            else:
                label = f"{val:.1f}%"
            color = "white" if val > values.to_numpy().max() * 0.62 else "#15202b"
            ax.text(j, i, label, ha="center", va="center", color=color, fontsize=9, fontweight="bold")

    ax.set_title(
        "Brand Health Heatmap: Leaders Convert Awareness Into Regular Usage",
        fontsize=16,
        fontweight="bold",
        loc="left",
        pad=26,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(-0.5, len(metric_cols), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(values.index), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.ax.set_ylabel("Higher score", rotation=270, labelpad=14)

    note = (
        "Read: Awareness is aided awareness. Usage, consideration and BUMO are calculated as respondent share. "
        "YoY change compares current BUMO vs previous BUMO in the dataset."
    )
    fig.text(0.075, 0.035, note, fontsize=8.5, color="#4b5563")
    fig.tight_layout(rect=[0.04, 0.07, 0.98, 0.92])
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def write_strategy(scores: pd.DataFrame, output_path: Path) -> None:
    cozy = scores.loc["Cozy"]
    leaders = scores.drop(index="Cozy").sort_values("BUMO", ascending=False).head(2)
    leader_names = ", ".join(leaders.index)

    text = f"""
    Cozy Brand Health Strategy Notes

    Core message:
    Leaders are not only more known; they are better at turning awareness into regular usage.

    What the data shows:
    - Top BUMO competitors in this cut: {leader_names}.
    - Cozy Awareness: {cozy['Awareness']:.1f}%.
    - Cozy P4W usage: {cozy['P4W usage']:.1f}%.
    - Cozy BUMO: {cozy['BUMO']:.1f}%.
    - Cozy Awareness -> P4W conversion: {cozy['Awareness -> P4W']:.1f}%.

    Strategic implication:
    Cozy should not solve only for awareness. The sharper opportunity is conversion:
    move people from knowing Cozy to using it recently and repeatedly.

    Recommended strategy:
    1. Own a clearer daily consumption occasion: everyday light tea, office/home routine, after-meal refreshment.
    2. Strengthen reason-to-drink: natural tea taste, light refreshment, suitable for daily drinking.
    3. Push trial-to-repeat mechanics: office sampling, multi-pack, 7-day routine bundle, shelf display by occasion.
    4. Improve shelf communication: make benefit and occasion readable within two seconds.
    5. Benchmark leaders on funnel conversion, but avoid copying their territory of instant refreshment.
    """
    output_path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize Cozy brand health heatmap from cleaned_dataset.xlsx")
    parser.add_argument("--input", default="cleaned_dataset.xlsx", help="Path to cleaned_dataset.xlsx")
    parser.add_argument("--outdir", default="outputs", help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    dataset = read_sheet(input_path, "Dataset_Clean")
    brandlist = read_sheet(input_path, "Brandlist_Clean")

    scores = calculate_scores(dataset, brandlist)
    scores = scores.sort_values("BUMO", ascending=False)

    csv_path = outdir / "cozy_brandhealth_summary.csv"
    png_path = outdir / "cozy_brandhealth_heatmap.png"
    txt_path = outdir / "cozy_brandhealth_strategy_notes.txt"

    scores.round(2).to_csv(csv_path, encoding="utf-8-sig")
    draw_heatmap(scores, png_path)
    write_strategy(scores, txt_path)

    print(f"Saved: {csv_path}")
    print(f"Saved: {png_path}")
    print(f"Saved: {txt_path}")


if __name__ == "__main__":
    main()
