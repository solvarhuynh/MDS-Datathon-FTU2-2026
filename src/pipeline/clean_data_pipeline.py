"""
CLEAN DATA PIPELINE — tuân thủ methodology.md
================================================
Chạy file này để tạo dataset sạch: cleaned_dataset.xlsx

Thứ tự xử lý:
  Bước 1: Drop cột 100% null
  Bước 2: Drop cột zero-variance
  Bước 3: Xử lý cột trùng .1
  Bước 4a: En dash → hyphen
  Bước 4b: Oolong → Olong
  Bước 4c: Sửa space thừa trong nhãn tần suất
  Bước 4d: Brandlist strip + deduplicate
  Bước 5: Chuẩn hóa nhóm tuổi
  Bước 6: Sửa mâu thuẫn BUMO vs P4W
  Bước 7: Convert Yes/No → 1/0
  Bước 8: Tạo ordinal mapping tần suất
  Bước 9: Tạo weight theo khu vực
  Ghi chú: Missing by design — không sửa, nhắc lại nguyên tắc
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
RAW_CANDIDATES = [
    os.path.join(BASE_DIR, "..", "..", "data", "raw", "data.xlsx"),
    os.path.join(BASE_DIR, "..", "..", "data", "raw", "myInsight 2026_V2_Dataset.xlsx"),
    os.path.join(BASE_DIR, "..", "data.xlsx"),
    os.path.join(os.getcwd(), "data", "raw", "data.xlsx")
]
FILE = next((c for c in RAW_CANDIDATES if os.path.exists(c)), RAW_CANDIDATES[0])
OUTPUT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data", "processed", "cleaned_dataset.xlsx"))

print("Loading data...")
df = pd.read_excel(FILE, sheet_name="Dataset")
bl = pd.read_excel(FILE, sheet_name="Brandlist - RTDT")
qnr = pd.read_excel(FILE, sheet_name="QNR - Cozy - Reference for data")
print(f"Dataset gốc: {df.shape[0]} dòng x {df.shape[1]} cột")
original_cols = len(df.columns)

# ============================================================
# BƯỚC 1: Drop cột 100% NULL
# Methodology: Loại bỏ toàn bộ 76 cột rỗng.
#   Q6 - Không Độ → ghi nhận data gap.
#   75 cột QME2 cho 5 brand → dữ liệu không được thu thập.
# ============================================================
print("\n[Bước 1] Drop cột 100% NULL...")
all_null_cols = df.columns[df.isnull().all()].tolist()
df = df.drop(columns=all_null_cols)
print(f"  Đã xóa {len(all_null_cols)} cột")
print(f"  GHI NHẬN: Q6 - Không Độ bị rỗng hoàn toàn — data gap, "
      "không thể phân tích tần suất cho brand Không Độ.")

# ============================================================
# BƯỚC 2: Drop cột zero-variance
# Methodology: Loại bỏ cột chỉ chứa 1 giá trị duy nhất
#   (đồng thời không có null). Phương sai = 0.
# ============================================================
print("\n[Bước 2] Drop cột zero-variance...")
zero_var_cols = [
    c for c in df.columns
    if df[c].nunique(dropna=True) <= 1 and df[c].notna().all()
]
df = df.drop(columns=zero_var_cols)
print(f"  Đã xóa {len(zero_var_cols)} cột")

# ============================================================
# BƯỚC 3: Xử lý cột trùng .1
# Methodology:
#   A: Gốc có data, .1 zero-var → drop .1 (đã xử lý ở bước 2)
#   B: Gốc zero-var, .1 có data → drop gốc, rename .1
#   C: Cả 2 có data → ĐỐI CHIẾU Brandlist/QNR.
#      Nếu là 2 brand code khác nhau → giữ cả 2, rename .1
#      Nếu thực sự duplicate → gộp OR rồi drop .1
# ============================================================
print("\n[Bước 3] Xử lý cột trùng .1...")

# Xác định 4 brand có 2 code trong Brandlist (tình huống C)
bl_names_stripped = bl["Unnamed: 1"].str.strip()
dup_brand_names = bl_names_stripped[bl_names_stripped.duplicated(keep=False)].unique().tolist()

dup_suffix_cols = [c for c in df.columns if c.endswith(".1")]
fix3_a = 0
fix3_b = 0
fix3_c_rename = 0
fix3_c_merge = 0

for c in dup_suffix_cols:
    base = c[:-2]
    if base not in df.columns:
        continue

    base_nunique = df[base].nunique(dropna=True)
    dup_nunique = df[c].nunique(dropna=True)

    if dup_nunique <= 1 and base_nunique > 1:
        # Tình huống A: .1 zero-var → đã bị drop ở bước 2,
        # nhưng nếu còn sót (vd có null) thì drop ở đây
        if c in df.columns:
            df = df.drop(columns=[c])
            fix3_a += 1

    elif base_nunique <= 1 and dup_nunique > 1:
        # Tình huống B: gốc zero-var, .1 có data
        df = df.drop(columns=[base])
        df = df.rename(columns={c: base})
        fix3_b += 1

    else:
        # Tình huống C: cả 2 đều có data
        # Kiểm tra xem brand này có nằm trong danh sách duplicate Brandlist không
        brand_in_col = base.split("_")[-1] if "_" in base else base
        is_dup_brand = any(brand_in_col in dn for dn in dup_brand_names)

        if is_dup_brand:
            # 2 brand code khác nhau → giữ cả 2, rename .1 cho rõ
            new_name = f"{base}_variant"
            df = df.rename(columns={c: new_name})
            fix3_c_rename += 1
            print(f"    Giữ cả 2: '{base}' + '{new_name}' (2 brand code khác nhau)")
        else:
            # Thực sự duplicate → gộp OR
            df[base] = ((df[base] == "Yes") | (df[c] == "Yes")).map(
                {True: "Yes", False: "No"}
            )
            df = df.drop(columns=[c])
            fix3_c_merge += 1

print(f"  Tình huống A (drop .1 zero-var): {fix3_a}")
print(f"  Tình huống B (rename .1 → gốc): {fix3_b}")
print(f"  Tình huống C — rename (2 brand code): {fix3_c_rename}")
print(f"  Tình huống C — merge OR (duplicate thật): {fix3_c_merge}")

# ============================================================
# BƯỚC 4a: Chuẩn hóa en dash → hyphen
# Methodology: Thay toàn bộ – (U+2013) thành - (U+002D)
#   trong tên cột VÀ giá trị text (Q5.Bumo, Q1.TOM, Q7).
# ============================================================
print("\n[Bước 4a] Chuẩn hóa en dash → hyphen...")
en_dash_count = sum(1 for c in df.columns if "–" in c)
df.columns = [c.replace("–", "-") for c in df.columns]

text_cols = ["Q5.Bumo", "Q1.TOM", "Q7. Previous BUMO"]
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].str.replace("–", "-", regex=False)

print(f"  Đã chuẩn hóa {en_dash_count} tên cột + giá trị trong {text_cols}")

# ============================================================
# BƯỚC 4b: Chuẩn hóa Oolong → Olong
# Methodology: Thay "Oolong" thành "Olong" (đa số 76 vs 3).
# ============================================================
print("\n[Bước 4b] Chuẩn hóa Oolong → Olong...")
oolong_count = sum(1 for c in df.columns if "Oolong" in c)
df.columns = [c.replace("Oolong", "Olong") for c in df.columns]

for col in ["Q5.Bumo", "Q1.TOM"]:
    if col in df.columns:
        df[col] = df[col].str.replace("Oolong", "Olong", regex=False)
print(f"  Đã chuẩn hóa {oolong_count} tên cột + giá trị text")

# ============================================================
# BƯỚC 4c: Sửa space thừa trong nhãn tần suất
# Methodology: "4-6 times/ week" → "4-6 times/week".
#   KHÔNG sửa sự khác biệt "Less than once per month" — thiết kế hợp lý.
# ============================================================
print("\n[Bước 4c] Sửa space thừa trong nhãn tần suất...")
freq_fix = {"4-6 times/ week": "4-6 times/week"}

s3b_col = [c for c in df.columns if "S3b" in c][0]
df[s3b_col] = df[s3b_col].replace(freq_fix)

q6_cols = [c for c in df.columns if c.startswith("Q6 ")]
for c in q6_cols:
    df[c] = df[c].replace(freq_fix)

print(f"  Đã sửa nhãn trong cột S3b + {len(q6_cols)} cột Q6")

# ============================================================
# BƯỚC 4d: Brandlist — strip trailing spaces + deduplicate
# Methodology: Cắt khoảng trắng thừa, loại bản ghi trùng tên.
# ============================================================
print("\n[Bước 4d] Clean Brandlist...")
bl["brand_name"] = bl["Unnamed: 1"].str.strip()
space_count = (bl["Unnamed: 1"] != bl["brand_name"]).sum()
print(f"  Đã strip {space_count} entries có trailing spaces")

before_bl = len(bl)
bl_clean = bl.drop_duplicates(subset="brand_name", keep="first")
bl_clean = bl_clean[["Brandlist", "brand_name"]].rename(
    columns={"Brandlist": "brand_code"}
)
print(f"  Deduplicate: {before_bl} → {len(bl_clean)} entries")

# ============================================================
# BƯỚC 5: Chuẩn hóa nhóm tuổi
# Methodology: "36 - 40 y.o." → "35 - 40 y.o." (gap 35 tuổi).
#   Ghi chú đây là giả định.
# ============================================================
print("\n[Bước 5] Chuẩn hóa nhóm tuổi...")
age_before = sorted(df["D3.Age"].unique().tolist())
df["D3.Age"] = df["D3.Age"].replace("36 - 40 y.o.", "35 - 40 y.o.")
age_after = sorted(df["D3.Age"].unique().tolist())
print(f"  Trước: {age_before}")
print(f"  Sau:   {age_after}")
print(f"  GIẢ ĐỊNH: gap tại 35 tuổi là lỗi nhãn, không phải thiết kế chủ đích.")

# ============================================================
# BƯỚC 6: Sửa mâu thuẫn BUMO vs P4W
# Methodology: Nếu BUMO = brand X thì Q4.P4W_X phải = Yes.
#   Sửa Q4 (dễ bỏ sót khi tick) thay vì sửa Q5 (respondent chủ động nêu).
#   Phải chạy TRƯỚC bước convert Yes/No → 1/0.
# ============================================================
print("\n[Bước 6] Sửa mâu thuẫn BUMO vs P4W...")
fix_count = 0
mismatch_details = []
for idx, row in df.iterrows():
    bumo = row["Q5.Bumo"]
    q4_col = f"Q4. P4W_{bumo}"
    if q4_col in df.columns and row[q4_col] != "Yes":
        df.at[idx, q4_col] = "Yes"
        mismatch_details.append(
            {"serial": row["Serial number"], "bumo": bumo}
        )
        fix_count += 1
print(f"  Đã sửa {fix_count} dòng (set Q4.P4W = 'Yes' cho brand BUMO)")

# ============================================================
# BƯỚC 7: Convert Yes/No → 1/0
# Methodology: Chuyển tất cả cột Yes/No sang dạng số.
#   NaN giữ nguyên (missing by design).
# ============================================================
print("\n[Bước 7] Convert Yes/No → 1/0...")
yn_converted = 0
for c in df.columns:
    vals = set(df[c].dropna().unique())
    if vals and vals <= {"Yes", "No"}:
        df[c] = df[c].map({"Yes": 1, "No": 0})
        yn_converted += 1
print(f"  Đã convert {yn_converted} cột")

# ============================================================
# BƯỚC 8: Tạo ordinal mapping tần suất
# Methodology: Tạo thang đo thứ tự cho S3b và Q6.
#   Chạy SAU convert Yes/No (tần suất là string, không phải Yes/No).
# ============================================================
print("\n[Bước 8] Tạo ordinal mapping tần suất...")
freq_order = {
    "Less than once per month": 1,
    "Once per month": 2,
    "2-3 times/month": 3,
    "Once per week": 4,
    "2-3 times/week": 5,
    "4-6 times/week": 6,
    "Once per day": 7,
}

df["S3b_ordinal"] = df[s3b_col].map(freq_order)
print(f"  Đã tạo cột S3b_ordinal từ '{s3b_col}'")

for c in q6_cols:
    if c in df.columns:
        ordinal_col = c.replace("Q6 ", "Q6_ordinal_")
        df[ordinal_col] = df[c].map(freq_order)
print(f"  Đã tạo {len(q6_cols)} cột Q6_ordinal_* cho từng brand")

# ============================================================
# BƯỚC 9: Tạo weight theo khu vực
# Methodology: weight = tỷ lệ dân số / tỷ lệ mẫu.
#   LƯU Ý: tỷ lệ dân số là ước tính, cần thay bằng số liệu chính thức.
# ============================================================
print("\n[Bước 9] Tạo weight theo khu vực...")
pop_pct = {
    "North": 0.35,
    "South": 0.30,
    "Central": 0.18,
    "Mekong": 0.17,
}
sample_pct = df["Region"].value_counts(normalize=True).to_dict()
df["weight_region"] = df["Region"].map(
    lambda r: pop_pct.get(r, 0.25) / sample_pct.get(r, 0.25)
)
print("  Weight theo region:")
for region in sorted(pop_pct.keys()):
    w = pop_pct[region] / sample_pct[region]
    n = (df["Region"] == region).sum()
    print(f"    {region}: n={n}, weight={w:.4f}")
print("  LƯU Ý: Tỷ lệ dân số là ước tính — cần thay bằng số liệu chính thức!")

# ============================================================
# GHI CHÚ: Missing by design
# Methodology: KHÔNG fill, KHÔNG drop. Phân tích trên đúng base.
# ============================================================
print(f"\n{'='*60}")
print("GHI CHÚ: MISSING BY DESIGN")
print(f"{'='*60}")
print("""
  Các cột sau có missing values CÓ CẤU TRÚC (MNAR):
    - QI (Brand Image): chỉ hỏi respondent biết brand (awareness base)
    - Q6 (Frequency): chỉ hỏi respondent dùng brand trong P4W
    - Q7 (Previous BUMO): chỉ hỏi Wave 2025 + thay đổi brand
    - QME2 (Lý do ngừng dùng): chỉ hỏi respondent ngừng dùng brand

  NGUYÊN TẮC:
    - KHÔNG fill NaN bằng 0 hoặc "No"
    - KHÔNG drop dòng có NaN
    - Khi phân tích, lọc đúng base rồi mới tính tỷ lệ
    - Luôn ghi chú base size (n=) trong biểu đồ/bảng
""")

# ============================================================
# TỔNG KẾT & EXPORT
# ============================================================
print(f"{'='*60}")
print("TỔNG KẾT")
print(f"{'='*60}")
final_cols = len(df.columns)
dropped = original_cols - final_cols
added_cols = [c for c in df.columns if c.startswith(("S3b_ordinal", "Q6_ordinal_", "weight_"))]
print(f"  Dataset gốc:   {original_cols} cột")
print(f"  Dataset sạch:   {final_cols} cột")
print(f"  Đã xóa:        ~{dropped + len(added_cols)} cột gốc")
print(f"  Đã thêm:       {len(added_cols)} cột mới "
      f"(S3b_ordinal, {len(q6_cols)} Q6_ordinal, weight_region)")
print(f"  Số dòng:        {len(df)} (không thay đổi)")
print(f"  Brandlist:      {len(bl_clean)} brands (sạch)")

print(f"\n  Đang export '{OUTPUT}'...")
with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Dataset_Clean", index=False)
    bl_clean.to_excel(writer, sheet_name="Brandlist_Clean", index=False)
print(f"  HOÀN TẤT: {OUTPUT}")
