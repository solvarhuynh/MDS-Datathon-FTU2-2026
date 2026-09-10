# 🏆 MDS DATATHON 2026 — FTU2
## Phân Tích Sức Khỏe Thương Hiệu & Chiến Lược Tăng Trưởng Cho Trà Cozy (RTD Tea Vietnam)

<div align=\"center\">

[![Competition](https://img.shields.io/badge/Competition-MDS%20Datathon%202026-0052CC?style=for-the-badge&logo=target)](https://github.com/solvarhuynh/MDS-Datathon-FTU2-2026)
[![Organizer](https://img.shields.io/badge/Host-FTU2%20%E2%80%94%20MDS-orange?style=for-the-badge)](https://github.com/solvarhuynh/MDS-Datathon-FTU2-2026)
[![Achievement](https://img.shields.io/badge/Award-TOP%205%20FINALIST-gold?style=for-the-badge&logo=trophy)](deliverables/achievements/certificate_top5_mds2026.png)
[![Team](https://img.shields.io/badge/Team-FUU-2ECC71?style=for-the-badge)](deliverables/achievements/team_lead_huynh_trung_nghia.jpg)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](requirements.txt)
[![Data](https://img.shields.io/badge/Sample%20Size-2%2C600%20Respondents-purple?style=for-the-badge)](data/processed/cleaned_dataset.xlsx)

[**Xem Slide Thuyết Trình Chung Kết (V3)**](deliverables/slides/MDS_FUU_Final_Deck_V3.pdf) • [**Khám Phá Dashboard Tương Tác**](dashboards/brand_funnel_interactive.html) • [**Báo Cáo Phương Pháp Dữ Liệu**](docs/methodology.md)

</div>

---

## 📌 MỤC LỤC
1. [Tổng Quan Dự Án & Thành Tích](#1-tổng-quan-dự-án--thành-tích)
2. [Bối Cảnh Thị Trường & Bài Toán Kinh Doanh](#2-bối-cảnh-thị-trường--bài-toán-kinh-doanh)
3. [Những Phát Hiện Cốt Lõi (Key Insights)](#3-những-phát-hiện-cốt-lõi-key-insights)
4. [Chiến Lược Tăng Trưởng Đề Xuất](#4-chiến-lược-tăng-trưởng-đề-xuất)
5. [Cấu Trúc Thư Mục Kho Lưu Trữ](#5-cấu-trúc-thư-mục-kho-lưu-trữ)
6. [Phương Pháp Làm Sạch & Xử Lý Dữ Liệu](#6-phương-pháp-làm-sạch--xử-lý-dữ-liệu)
7. [Bảng Ánh Xạ Biểu Đồ & Mã Nguồn (Slide ↔ Chart ↔ Code)](#7-bảng-ánh-xạ-biểu-đồ--mã-nguồn)
8. [Hướng Dẫn Cài Đặt & Chạy Mã Nguồn](#8-hướng-dẫn-cài-đặt--chạy-mã-nguồn)
9. [Bản Quyền & Thông Tin Liên Hệ](#9-bản-quyền--thông-tin-liên-hệ)

---

## 1. TỔNG QUAN DỰ ÁN & THÀNH TÍCH

Dự án này là toàn bộ kho lưu trữ mã nguồn, dữ liệu, tài liệu phân tích thị trường và sản phẩm dự thi của **Đội thi FUU** (Trưởng nhóm: **Huỳnh Trung Nghĩa**) tham gia cuộc thi **MDS Datathon 2026** do Câu lạc bộ Khoa học Dữ liệu MDS - Trường Đại học Ngoại Thương Cơ sở II (FTU2) tổ chức vào **Tháng 6/2026**.

- **Đề tài**: *Brand Health Tracking & Growth Acceleration for Cozy Ready-to-Drink (RTD) Tea in Vietnam Market (2024–2026)*.
- **Thành tích đạt được**: **TOP 5 ĐỘI XUẤT SẮC NHẤT TOÀN QUỐC (TOP 5 FINALIST)**.
- **Bộ dữ liệu khảo sát**: Khảo sát sức khỏe thương hiệu thực tế quy mô lớn gồm **2.600 người tiêu dùng** (Wave 2024: =1.300$; Wave 2025: =1.300$) trên 1.068 biến số khảo sát chuyên sâu từ nhận biết, dùng thử, tần suất, rào cản đến hình tượng thương hiệu.

<div align=\"center\">
  <img src=\"deliverables/achievements/certificate_top5_mds2026.png\" alt=\"Certificate Top 5 MDS Datathon 2026\" width=\"750\" />
  <p><em>Chứng nhận Top 5 Chung cuộc MDS Datathon 2026 — Đội thi FUU</em></p>
</div>

---

## 2. BỐI CẢNH THỊ TRƯỜNG & BÀI TOÁN KINH DOANH

### 2.1 Bối Cảnh Thị Trường RTD Tea Việt Nam (2025–2026)
- **Quy mô & Tiềm năng**: Thị trường RTD Tea & Coffee Việt Nam đạt **913.6 triệu USD** (năm 2025) và ước tính chạm mốc **1.677 tỷ USD** vào năm 2033 với tốc độ tăng trưởng kép **CAGR 7.9%**. Trong đó, riêng RTD Tea chiếm đến **73%** tổng thị trường.
- **Cú hích Thuế Tiêu Thụ Đặc Biệt (Sugar Tax - Hiệu lực 1/1/2026)**: Quốc hội Việt Nam thông qua biểu thuế đánh vào đồ uống có đường (10% từ 2026 và nâng lên 20% vào 2030), tạo áp lực chi phí cực lớn lên các dòng trà đại trà có độ ngọt cao như C2 truyền thống hay Không Độ.
- **Làn sóng Healthy & Trà Ít Đường**: **82%** người tiêu dùng coi lượng đường cao là rào cản mua sắm, mở ra cánh cửa vàng cho thương hiệu có định vị trà tự nhiên, thanh nhẹ như Cozy.

### 2.2 Vấn Đề Cốt Lõi Của Trà Cozy
Dù có lịch sử thương hiệu lâu đời và nhận biết thương hiệu tốt, Trà Cozy đang gặp phải điểm nghẽn nghiêm trọng trên phễu chuyển đổi thương hiệu (Brand Conversion Funnel):

`mermaid
flowchart LR
    A[\"Aided Awareness: 91.8%\"/] -->|Chỉ 36.2% dùng thử| B[\"P3M Trial: 33.2%\"/]
    B -->|Tỷ lệ giữ chân ổn| C[\"P4W Usage: 25.8%\"/]
    C -->|Thụt lùi mạnh| D[\"BUMO: 8.8%\"/]

    style A fill:#457B9D,stroke:#fff,color:#fff
    style B fill:#E63946,stroke:#fff,color:#fff
    style C fill:#F4A261,stroke:#fff,color:#fff
    style D fill:#D62828,stroke:#fff,color:#fff
`

- **Aided Awareness rất cao (91.8%)**: Ngang ngửa các ông lớn như Không Độ (92.5%), C2 (97.2%) và OLong Tea+ (98.8%).
- **Nút thắt chuyển đổi sang Dùng thử (P3M Trial) cực thấp**: Chỉ **36.2%** người biết Cozy chuyển sang dùng thử trong 3 tháng gần nhất (trong khi C2 đạt 67.9% và OLong Tea+ đạt 67.6%).
- **Thương hiệu yêu thích nhất (BUMO) thấp kỷ lục**: Cozy chỉ chiếm **8.8%**, bị C2 (32.1%) và OLong Tea+ (30.0%) bỏ xa.

---

## 3. NHỮNG PHÁT HIỆN CỐT LÕI (KEY INSIGHTS)

Dựa trên việc bóc tách định lượng 2.600 mẫu khảo sát và mô hình phân cụm rào cản, Đội thi FUU đã tìm ra 3 nhóm nguyên nhân gốc rễ (Root Causes) giải thích nghịch lý của Cozy:

1. **Rào Cản Vị Giác & Danh Mục (31.4% Tổng Respondents)**:
   - **19.5%** người tiêu dùng phản hồi *"Không thích hương vị hiện tại"* (vị chát gắt hoặc độ ngọt chưa cân bằng).
   - **11.9%** phàn nàn *"Thiếu đa dạng hương vị"* (Cozy bị giới hạn so với C2 có tới 13+ biến thể).
2. **Rào Cản Phân Phối & Chuỗi Lạnh (10.8% Tổng Respondents)**:
   - **5.5%** *"Không tìm thấy tại điểm bán gần nhà"*.
   - **5.3%** *"Sản phẩm không được ướp lạnh sẵn trong tủ mát"*. Đối với ngành RTD Tea, việc không có sẵn chai mát lạnh tại điểm bán khiến tỷ lệ mua tức thì (impulse purchase) sụt giảm hơn 60%.
3. **Cơ Hội Thị Trường Chưa Khai Thác Ở Miền Bắc**:
   - Miền Bắc có **870 khách hàng biết Cozy nhưng chưa từng dùng thử** — chiếm **51%** tổng dung lượng chuyển đổi tiềm năng trên cả nước.
   - Headroom tăng trưởng chuyển đổi tại miền Bắc cao hơn tới **+71%** so với khu vực Mekong.

---

## 4. CHIẾN LƯỢC TĂNG TRƯỞNG ĐỀ XUẤT

Đội thi FUU xây dựng mô hình chiến lược 3 trụ cột (3 Growth Pillars) cùng lộ trình thực thi đến 2027:

`mermaid
graph TD
    subgraph PILLAR 1: SẢN PHẨM & SKU HERO
        P1A[\"Tập trung nguồn lực vào 2 Hero SKUs: Trà Vải & Trà Đào\"/]
        P1B[\"Ra mắt công thức Ít Đường / 0 Calo đón đầu Sugar Tax 2026\"/]
    end
    subgraph PILLAR 2: PHÂN PHỐI & CHUỖI LẠNH
        P2A[\"Phủ sóng chuỗi CVS: Circle K, GS25, 7-Eleven, FamilyMart\"/]
        P2B[\"Chương trình tài trợ Tủ mát & Kệ trưng bày POSM kênh Tạp hóa Miền Bắc\"/]
    end
    subgraph PILLAR 3: ĐỊNH VỊ & KÍCH HOẠT
        P3A[\"Tái định vị: 'Trà Trái Cây Đậm Vị Tự Nhiên Dành Cho Giới Trẻ'\"/]
        P3B[\"Chiến dịch Sampling diện rộng tại trường đại học & văn phòng\"/]
    end

    P1A & P1B --> GOAL((\"MỤC TIÊU 2026 - 2027<br/>BUMO tăng từ 8.8% lên 15%<br/>Trial Rate vượt 50%\"))
    P2A & P2B --> GOAL
    P3A & P3B --> GOAL

    style GOAL fill:#1B7A3D,stroke:#F2B705,stroke-width:3px,color:#fff
`

---

## 5. CẤU TRÚC THƯ MỤC KHO LƯU TRỮ

Kho lưu trữ được tái cấu trúc theo chuẩn mực Data Science & Analytics:

`	ext
MDS-Datathon-FTU2-2026/
├── README.md                           # Hồ sơ dự án & tài liệu tổng quan chuẩn quốc tế
├── requirements.txt                    # Danh sách thư viện Python phụ thuộc
├── .gitignore                          # Cấu hình lọc bỏ cache, checkpoint, file rác
│
├── data/                               # Dữ liệu khảo sát & nghiên cứu
│   ├── processed/
│   │   └── cleaned_dataset.xlsx        # Dataset sạch (2.600 dòng x các biến chuẩn hóa)
│   └── raw/
│       └── raw_dataset.csv             # Dữ liệu thô ban đầu (14.8 MB)
│
├── docs/                               # Tài liệu học thuật, nghiên cứu thị trường & kịch bản
│   ├── methodology.md                  # Tài liệu 9 bước xử lý dữ liệu & phân tích Data gap
│   ├── market_research.md              # Báo cáo thị trường RTD Tea, Sugar Tax 2026, SWOT
│   ├── macro_micro_overview.docx       # Tài liệu PESTLE & Porter's 5 Forces
│   ├── presentation_outline.xlsx       # Kịch bản thuyết trình, flow logic & checklist
│   ├── insight_hypotheses.xlsx         # Danh mục câu hỏi & giả thuyết dữ liệu cần kiểm chứng
│   └── v3_deck_chart_mapping.md        # Bản đồ đối sánh slide - biểu đồ nộp BTC
│
├── dashboards/                         # Bảng điều khiển tương tác trực quan (HTML/JS)
│   ├── brand_funnel_interactive.html   # Dashboard Dark-mode trực quan hóa Phễu & Rào cản Cozy (Chart.js)
│   └── brand_funnel_slide_view.html    # Giao diện Slide Card View trực quan hóa số liệu
│
├── deliverables/                       # Sản phẩm đầu ra cuộc thi & chứng nhận
│   ├── slides/
│   │   ├── MDS_FUU_Final_Deck_V3.pdf       # Slide thuyết trình Vòng Chung kết (31 trang)
│   │   └── MDS_FUU_Preliminary_Deck_V2.pdf # Slide thuyết trình Vòng Sơ loại
│   └── achievements/
│       ├── certificate_top5_mds2026.png    # Chứng nhận Top 5 MDS Datathon 2026
│       └── team_lead_huynh_trung_nghia.jpg # Ảnh đại diện đội thi FUU
│
├── src/                                # Toàn bộ mã nguồn Python
│   ├── pipeline/
│   │   └── clean_data_pipeline.py      # Pipeline làm sạch tự động hóa (Data Cleaning Pipeline)
│   └── charts/                         # 37 scripts sinh biểu đồ xuất hiện trong Slide Deck V3
│       ├── slide03_segmentation_matrix/    # Ma trận phân khúc thị trường & độ hấp dẫn
│       ├── slide05_consumer_profile/       # Chân dung nhân khẩu học & cơ hội Miền Bắc
│       ├── slide06_brand_funnel/           # Phễu chuyển đổi các thương hiệu RTD Tea
│       ├── slide07_root_cause_barriers/    # Phân cụm nguyên nhân rào cản của Cozy
│       ├── slide08_image_void/             # Khoảng trống hình tượng (Image Void Heatmap)
│       ├── slide08b_persona/               # Chân dung khách hàng mục tiêu & nhóm cần tái chiếm
│       ├── slide09_touchpoint/             # Điểm chạm truyền thông (Touchpoint Analysis)
│       ├── slide10_availability/           # Rào cản sẵn có tại điểm bán & độ phủ kênh
│       ├── slide11_sku_hero/               # Phân tích danh mục Hero SKU (Trà Vải vs Trà Đào)
│       ├── slide13_positioning/            # Brand House & Ngôi nhà định vị thương hiệu
│       ├── slide15_roadmap/                # Lộ trình triển khai chiến lược 2026–2027
│       ├── slide16_value_chain_pillars/    # Kế hoạch ngân sách, sizing & 3 trụ cột chuỗi giá trị
│       ├── exploratory/                    # Các script phân tích mở rộng & thống kê mô tả
│       └── misc/                           # Biểu đồ bổ trợ
│
└── archives/                           # Lưu trữ an toàn các file nén nguyên bản
    ├── V2_VISUALIZATION_backup.zip
    ├── V3_Figures_Code_backup.zip
    └── V2_Barrier_Strategy_Solution_backup.zip
`

---

## 6. PHƯƠNG PHÁP LÀM SẠCH & XỬ LÝ DỮ LIỆU

Tài liệu chi tiết tại [docs/methodology.md](docs/methodology.md). Quy trình tiền xử lý được tự động hóa bằng [src/pipeline/clean_data_pipeline.py](src/pipeline/clean_data_pipeline.py) qua 9 bước nghiêm ngặt:

| Bước | Hạng Mục Xử Lý | Số Lượng Cột / Dòng Bị Ảnh Hưởng | Cơ Sở & Biện Pháp Kỹ Thuật |
|:---:|:---|:---:|:---|
| **1** | **Drop Cột 100% NULL** | 76 cột | Loại bỏ các thuộc tính không có dữ liệu (riêng Q6 - Không Độ ghi nhận là Data Gap). |
| **2** | **Drop Cột Zero-Variance** | 72 cột | Xóa bỏ các cột chỉ chứa 1 giá trị duy nhất (không có biến thiên thống kê). |
| **3** | **Xử Lý Cột Trùng Tên .1** | 15 cột | Hợp nhất và chuẩn hóa tên cột do lỗi export Excel tự thêm hậu tố .1. |
| **4** | **Chuẩn Hóa Chuỗi Ký Tự (Typo)** | Đa dạng cột | Đổi En dash (–) thành hyphen (-), sửa Oolong → Olong, chuẩn hóa khoảng trắng thừa. |
| **5** | **Đồng Bộ Nhóm Tuổi** | Toàn bộ mẫu (=2.600$) | Đồng bộ nhãn nhóm tuổi thành 5 phân nhóm chuẩn: 14 - 18, 19 - 24, 25 - 29, 30 - 34, 35 - 40 y.o. |
| **6** | **Xử Lý Mâu Thuẫn Logic BUMO vs P4W** | 13 trường hợp | Nếu respondent chọn thương hiệu là BUMO nhưng P4W lại đánh dấu No, hiệu chỉnh logic về tính nhất quán. |
| **7** | **Mã Hóa Nhị Phân (Binary Encoding)** | Tất cả câu hỏi Yes/No | Chuyển đổi "Yes"/"No" sang 1/0 phục vụ tính toán đại số ma trận và mô hình. |
| **8** | **Mã Hóa Thứ Bậc Tần Suất (Ordinal)** | Các câu hỏi Q6 | Gán điểm trọng số tần suất sử dụng (từ Mỗi ngày = 7 lần/tuần đến Hiếm khi). |
| **9** | **Trọng Số Mẫu Theo Khu Vực (Weighting)** | Cột Weight | Cân bằng tỷ trọng dân số thực tế giữa 4 khu vực: Bắc, Trung, Đông Nam Bộ, Mekong. |

---

## 7. BẢNG ÁNH XẠ BIỂU ĐỒ & MÃ NGUỒN

Tất cả 37 biểu đồ trong Slide Deck Vòng Chung Kết [deliverables/slides/MDS_FUU_Final_Deck_V3.pdf](deliverables/slides/MDS_FUU_Final_Deck_V3.pdf) đều có thể tái tạo 100% bằng code Python:

| Trang Slide | Phân Khu Phân Tích | Tên File Ảnh Biểu Đồ | File Mã Nguồn Tương Ứng |
|:---:|:---|:---|:---|
| **Trang 5** | Ma Trận Phân Khúc | [s3_segmatrix.png](src/charts/slide03_segmentation_matrix/s3_segmatrix.png) | [charts_slide3_matrix.py](src/charts/slide03_segmentation_matrix/charts_slide3_matrix.py) |
| **Trang 7** | Chân Dung & Quy Mô | [s5_cozy_reach_region.png](src/charts/slide05_consumer_profile/s5_cozy_reach_region.png) | [charts_slide5.py](src/charts/slide05_consumer_profile/charts_slide5.py) |
| **Trang 7** | Phễu Thương Hiệu | [s6_funnel.png](src/charts/slide06_brand_funnel/s6_funnel.png) | [charts_slide7.py](src/charts/slide06_brand_funnel/charts_slide7.py) |
| **Trang 8** | Tỷ Lệ Chuyển Đổi | [s6_conversion.png](src/charts/slide06_brand_funnel/s6_conversion.png) | [charts_slide7.py](src/charts/slide06_brand_funnel/charts_slide7.py) |
| **Trang 8** | Đối Sánh Phễu | [s6_funnel_compare.png](src/charts/slide06_brand_funnel/s6_funnel_compare.png) | [charts_slide7.py](src/charts/slide06_brand_funnel/charts_slide7.py) |
| **Trang 9** | Rào Cản Chuyển Đổi | [s7_barriers_cluster.png](src/charts/slide07_root_cause_barriers/s7_barriers_cluster.png) | [charts_slide7.py](src/charts/slide07_root_cause_barriers/charts_slide7.py) |
| **Trang 10** | Khoảng Trống Hình Tượng | [s8_attr_heatmap.png](src/charts/slide08_image_void/s8_attr_heatmap.png) | [charts_slide8.py](src/charts/slide08_image_void/charts_slide8.py) |
| **Trang 10** | Dumbbell Thuộc Tính | [s8_dumbbell.png](src/charts/slide08_image_void/s8_dumbbell.png) | [charts_slide8.py](src/charts/slide08_image_void/charts_slide8.py) |
| **Trang 11** | Điểm Chạm & TOM | [s9_tom.png](src/charts/slide09_touchpoint/s9_tom.png), [s9_touchpoint.png](src/charts/slide09_touchpoint/s9_touchpoint.png) | [charts_slide9.py](src/charts/slide09_touchpoint/charts_slide9.py) |
| **Trang 12** | Sẵn Có & In-store | [s10_barrier.png](src/charts/slide10_availability/s10_barrier.png), [s10_instore.png](src/charts/slide10_availability/s10_instore.png) | [charts_slide10.py](src/charts/slide10_availability/charts_slide10.py) |
| **Trang 14** | Tăng Trưởng Nhóm Tuổi | [s5_cozy_p4w_age_yoy.png](src/charts/slide05_consumer_profile/s5_cozy_p4w_age_yoy.png) | [charts_slide5.py](src/charts/slide05_consumer_profile/charts_slide5.py) |
| **Trang 16** | Chân Dung Persona | [s8b_persona.png](src/charts/slide08b_persona/s8b_persona.png) | [charts_slide8b.py](src/charts/slide08b_persona/charts_slide8b.py) |
| **Trang 17** | Cơ Hội Miền Bắc | [s5_scale_opportunity_north.png](src/charts/slide05_consumer_profile/s5_scale_opportunity_north.png) | [chart_scale_opportunity_north.py](src/charts/slide05_consumer_profile/chart_scale_opportunity_north.py) |
| **Trang 19** | SKU Hero Trà Vải | [sku_herovai.png](src/charts/slide11_sku_hero/sku_herovai.png) | [charts_sku_hero.py](src/charts/slide11_sku_hero/charts_sku_hero.py) |
| **Trang 20** | SKU Hero Trà Đào | [sku_dao.png](src/charts/slide11_sku_hero/sku_dao.png) | [charts_sku_hero.py](src/charts/slide11_sku_hero/charts_sku_hero.py) |
| **Trang 22** | Brand House Định Vị | [s13_house.png](src/charts/slide13_positioning/s13_house.png) | [charts_slide13.py](src/charts/slide13_positioning/charts_slide13.py) |
| **Trang 24** | Lộ Trình Thực Thi | [s15_roadmap.png](src/charts/slide15_roadmap/s15_roadmap.png) | [charts_slide15.py](src/charts/slide15_roadmap/charts_slide15.py) |
| **Trang 29** | Ngân Sách & Sizing | [s16_budget_v2.png](src/charts/slide16_value_chain_pillars/s16_budget_v2.png), [s16_sizing.png](src/charts/slide16_value_chain_pillars/s16_sizing.png) | [charts_slide16.py](src/charts/slide16_value_chain_pillars/charts_slide16.py) |
| **Trang 31** | 3 Trụ Cột Chuỗi Giá Trị | [s16_pillar1_product.png](src/charts/slide16_value_chain_pillars/s16_pillar1_product.png), s16_pillar2_distribution.png, s16_pillar3_activation.png | [charts_slide16.py](src/charts/slide16_value_chain_pillars/charts_slide16.py) |

---

## 8. HƯỚNG DẪN CÀI ĐẶT & CHẠY MÃ NGUỒN

### 8.1 Yêu Cầu Môi Trường
- **Python**: Phiên bản 3.10 trở lên.
- **Hệ điều hành**: Tương thích hoàn toàn với Windows, macOS và Linux.

### 8.2 Cài Đặt Thư Viện Phụ Thuộc
Khởi tạo môi trường ảo và cài đặt các thư viện cần thiết:
`ash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# (Trên macOS/Linux: source venv/bin/activate)

# Cài đặt thư viện
pip install -r requirements.txt
`

### 8.3 Chạy Pipeline Làm Sạch Dữ Liệu
Để chạy lại toàn bộ quy trình tiền xử lý 9 bước và tạo file cleaned_dataset.xlsx:
`ash
python src/pipeline/clean_data_pipeline.py
`

### 8.4 Tái Tạo Biểu Đồ Bất Kỳ
Mỗi script tạo biểu đồ đều hoạt động độc lập và tự động liên kết với dữ liệu sạch tại data/processed/:
`ash
# Sinh biểu đồ phân tích cơ hội Miền Bắc
python "src/charts/slide05_consumer_profile/chart_scale_opportunity_north.py"

# Sinh biểu đồ phễu chuyển đổi thương hiệu
python "src/charts/slide06_brand_funnel/charts_slide7.py"

# Sinh biểu đồ rào cản gốc rễ
python "src/charts/slide07_root_cause_barriers/charts_slide7.py"

# Sinh biểu đồ SKU Hero
python "src/charts/slide11_sku_hero/charts_sku_hero.py"
`

### 8.5 Trải Nghiệm Dashboard Trực Quan Hóa
Mở trực tiếp file HTML trong trình duyệt để xem báo cáo tương tác không cần server:
- Dashboard tương tác Dark-Mode: dashboards/brand_funnel_interactive.html
- Giao diện thẻ Slide: dashboards/brand_funnel_slide_view.html

---

## 9. BẢN QUYỀN & THÔNG TIN LIÊN HỆ

- **Đội ngũ thực hiện**: Team FUU (MDS Datathon 2026 - FTU2)
- **Đại diện**: Huỳnh Trung Nghĩa ([GitHub Profile](https://github.com/solvarhuynh))
- **Email**: solvarhuynh@gmail.com
- **Tổ chức cuộc thi**: MDS Club — Trường Đại học Ngoại Thương Cơ sở II tại TP. Hồ Chí Minh (FTU2)
- **Giấy phép**: Toàn bộ dữ liệu khảo sát và sản phẩm phân tích thuộc bản quyền của Đội thi FUU và Ban tổ chức MDS Datathon 2026. Dự án được chia sẻ công khai với mục đích học thuật và tham khảo chuyên môn.

<div align=\"center\">
  <b>⭐ Đừng ngần ngại nhấn STAR nếu dự án này hữu ích cho bạn trong việc nghiên cứu và chuẩn bị cho các kỳ thi Datathon! ⭐</b>
</div>
