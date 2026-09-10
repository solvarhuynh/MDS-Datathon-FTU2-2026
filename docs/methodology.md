# DATA CLEANING METHODOLOGY

## Dataset: myInsight 2026 — Brand Health Tracking RTD Tea Vietnam

| Thông tin | Chi tiết |
|-----------|----------|
| Nguồn | myInsight 2026_V2_Dataset.xlsx |
| Kích thước | 2,600 respondents x 1,068 columns |
| Wave | 2024 (n=1,300), 2025 (n=1,300) |
| Ngành hàng | Trà uống liền đóng chai/lon/hộp (RTD Tea) |
| Thương hiệu chính | Trà Cozy, C2, OLong Tea Plus, Không Độ, Dr. Thanh, và 10 brand khác |

---

## 1. Cột 100% NULL — 76 cột hoàn toàn rỗng

### Phát hiện

76 cột không chứa bất kỳ giá trị nào trong toàn bộ 2,600 dòng:

- **`Q6 - Không Độ`** (1 cột): Tần suất sử dụng brand Không Độ — hoàn toàn rỗng trong khi 14 brand khác đều có dữ liệu Q6 bình thường.
- **`QME2` cho 5 brand** (75 cột): Lý do ngừng sử dụng cho Trà sữa C2, Trà Jokky, Búp non 365, Trà mật ong Boncha, Trà thảo mộc VietFuji. Mỗi brand có 15-16 cột attribute, tất cả đều rỗng.
- **Lưu ý quan trọng:** QME2 tổng cộng có 225 cột. Trong đó 149 cột thuộc 10 brand khác (Trà Cozy, Dr. Thanh, C2, Không Độ, OLong Tea Plus...) CÓ dữ liệu Yes/No thực. Chỉ 75 cột của 5 brand trên là rỗng — đây không phải missing by design mà là **dữ liệu không được thu thập** cho các brand này.

### Cách sửa

Loại bỏ toàn bộ 76 cột rỗng ra khỏi bảng dữ liệu. Riêng cột `Q6 - Không Độ` cần ghi nhận trong báo cáo cuối rằng đây là data gap — không thể phân tích tần suất sử dụng cho brand Không Độ, và nên xác nhận lại với team thu thập dữ liệu xem có thể khôi phục không.

### Lý do

- Cột 100% rỗng không mang bất kỳ thông tin phân tích nào. Giữ lại chỉ tăng số chiều dữ liệu, chiếm bộ nhớ, và gây nhầm lẫn khi duyệt danh sách cột.
- Riêng `Q6 - Không Độ` đáng ngờ là **lỗi export hoặc lỗi thu thập** vì Không Độ là brand lớn, có dữ liệu đầy đủ ở các câu hỏi khác (Q1-Q5, QI, QME2). Nên ghi nhận rõ ràng thay vì bỏ qua âm thầm.
- 75 cột QME2 rỗng: 5 brand này có thể là brand mới thêm vào questionnaire nhưng chưa được routing đúng, hoặc sample size quá nhỏ nên không ai trả lời. Dù lý do nào, 100% rỗng đồng nghĩa không có thông tin.

---

## 2. Cột Zero-Variance — 72 cột chỉ có 1 giá trị

### Phát hiện

72 cột có giá trị duy nhất `"No"` cho toàn bộ 2,600 dòng. Phân bố theo nhóm câu hỏi:

- `S2.Category used in P4W_*`: 3 cột — loại đồ uống không ai trong mẫu sử dụng
- `Q1.Total Spontaneous_*`: khoảng 20 cột — brand/variant không ai nhắc đến một cách tự phát
- `Q1Q2.Total aided awareness_*`: khoảng 15 cột — brand/variant không ai biết đến (kể cả khi được gợi ý)
- `Q4.P4W_*`: vài cột — brand/variant không ai dùng trong 4 tuần qua

### Cách sửa

Loại bỏ toàn bộ các cột chỉ chứa một giá trị duy nhất (đồng thời không có giá trị null). Các cột này chỉ có "No" cho mọi dòng, không phân biệt được giữa các respondent nào với nhau.

### Lý do

- Cột chỉ có 1 giá trị có phương sai bằng 0, không có giá trị thống kê trong bất kỳ phân tích nào.
- Trong phân tích Brand Health, một brand mà 0% biết đến hoặc 0% sử dụng thì không cần giữ cột riêng — thông tin đó đã được thể hiện bởi chính việc vắng mặt khỏi kết quả.
- Giảm đáng kể số cột, giúp dữ liệu gọn gàng hơn và dễ thao tác hơn.

---

## 3. Cột trùng tên với hậu tố `.1` — 15 cột

### Phát hiện

Khi đọc file Excel, phần mềm tự động thêm hậu tố `.1` vào tên cột khi phát hiện 2 cột header trùng tên. Phát hiện 15 cặp cột, chia thành 3 tình huống:

| Tình huống | Ví dụ | Cột gốc | Cột .1 |
|------------|-------|---------|--------|
| A: Gốc có data, `.1` zero-var | `Q1.Total Spontaneous_OLong Tea Plus` | Yes/No | chỉ No |
| B: Gốc zero-var, `.1` có data | `Q4. P4W_OLong Tea Plus` | chỉ No | Yes/No |
| C: Cả 2 đều có data | `Q1.Total Spontaneous_Trà lá vối Seventy` | Yes/No | Yes/No |

### Cách sửa

**Tình huống A** (cột gốc có dữ liệu, cột .1 chỉ có "No"): Xóa cột `.1` — cột này đã bị loại sẵn ở bước xử lý zero-variance.

**Tình huống B** (cột gốc chỉ có "No", cột .1 mới có dữ liệu thực): Xóa cột gốc (rỗng) và đổi tên cột `.1` lại thành tên gốc để giữ tính nhất quán trong hệ thống tên cột.

**Tình huống C** (cả 2 cột đều có dữ liệu Yes/No): Đây là trường hợp cần xử lý cẩn thận nhất. Trước khi quyết định, cần đối chiếu với sheet QNR (questionnaire reference) và Brandlist:

- Nếu Brandlist cho thấy 2 mã code khác nhau cho cùng tên brand (ví dụ: "Trà lá vối Seventy" có code 27 và 271), thì 2 cột trong Excel thực tế tương ứng với 2 đối tượng khác nhau (brand cha và sub-brand). Trong trường hợp này, **giữ nguyên cả 2 cột** và đổi tên cột `.1` cho rõ nghĩa hơn (ví dụ thêm mã code vào tên).
- Nếu xác nhận được rằng 2 cột thực sự là duplicate do lỗi thiết kế questionnaire, gộp lại bằng logic: nếu respondent trả lời "Yes" ở bất kỳ cột nào trong 2 cột thì kết quả cuối là "Yes", sau đó xóa cột thừa.

### Lý do

- Tình huống A, B: Rõ ràng 1 cột chứa dữ liệu thực, cột kia là artifact (sản phẩm phụ). Giữ cột có dữ liệu, bỏ cột rỗng là xử lý tự nhiên.
- Tình huống C: Đây là trường hợp **nguy hiểm nhất**. Brandlist thực tế cho thấy 4 brand có 2 code khác nhau (ví dụ Trà lá vối Seventy có code 27 và 271). Trong questionnaire, brand cha và sub-brand có thể được tách thành 2 cột riêng để đo lường riêng. Nếu gộp mù quáng bằng logic OR sẽ **trộn lẫn 2 đối tượng khác nhau**, dẫn đến phóng đại tỷ lệ awareness hoặc usage. Nhất thiết phải đối chiếu QNR trước khi quyết định.

---

## 4. Missing Values có cấu trúc — 826/1,068 cột có null

### Phát hiện

Đây là dataset khảo sát có **routing logic** (skip pattern): respondent chỉ được hỏi câu tiếp theo nếu đáp ứng điều kiện ở câu trước. Do đó, phần lớn missing values là **Missing Not At Random (MNAR)** — chúng mang ý nghĩa, chứ không phải lỗi dữ liệu.

Các tầng routing được phát hiện:

| Nhóm câu hỏi | Điều kiện để được hỏi | Null rate |
|---------------|----------------------|-----------|
| QI - Brand Image (19 attribute x 15 brand) | Respondent biết brand đó (Q1Q2 awareness = Yes) | 1.2% - 97.4% |
| Q6 - Frequency per brand | Respondent dùng brand đó trong P4W (Q4 = Yes) | 42% - 99.9% |
| Q7 - Previous BUMO | Wave 2025 + có thay đổi brand (khác Q5 wave trước) | 71.5% |
| QME2 - Lý do ngừng dùng (149 cột có data) | Respondent biết brand nhưng ngừng dùng | 43% - 97% |

### Cách sửa

**KHÔNG điền giá trị thay thế (fill), KHÔNG xóa dòng (drop).** Giữ nguyên các ô trống. Thay vào đó, khi phân tích từng chỉ số, phải lọc dữ liệu đúng theo logic routing để chỉ tính trên đúng nhóm respondent được hỏi (gọi là "base" hay mẫu số).

Ví dụ cụ thể:
- Khi tính Brand Image của C2: chỉ lấy những respondent biết đến C2 (awareness = Yes), rồi tính tỷ lệ trên nhóm này. Không lấy toàn bộ 2,600 người.
- Khi tính tần suất sử dụng (Q6): chỉ lấy những respondent đã dùng brand đó trong 4 tuần qua (P4W = Yes).
- Khi phân tích lý do ngừng dùng (QME2): chỉ lấy những respondent từng biết brand nhưng đã ngừng sử dụng.
- Luôn ghi chú base size (n=) trong mọi biểu đồ và bảng số liệu.

### Lý do

- Trong nghiên cứu thị trường, **base** (mẫu số) quyết định tính đúng đắn của mọi chỉ số. Brand Image phải tính trên awareness base, không phải total base. Nếu điền 0 vào ô trống, brand ít người biết sẽ bị "pha loãng" nghiêm trọng — ví dụ Trà Jokky (97.4% null) sẽ có tất cả attribute gần 0%, nhưng thực tế trong 67 người biết Jokky, tỷ lệ đánh giá có thể rất cao.
- Điền "No" hay 0 vào ô trống biến "không được hỏi" thành "trả lời Không" — hai điều hoàn toàn khác nhau về ý nghĩa. Người không biết brand thì không thể đánh giá brand image, việc gán cho họ câu trả lời "Không" là sai lệch bản chất.
- Ngược lại, xóa dòng có ô trống sẽ loại bỏ hầu hết respondent — vì mỗi người chỉ biết vài brand, ai cũng có ô trống ở brand không biết. Kết quả chỉ giữ lại "super-user" biết tất cả brand, gây thiên lệch chọn mẫu (selection bias).

---

## 5. Khoảng trống nhóm tuổi — D3.Age thiếu 35 tuổi

### Phát hiện

Nhóm tuổi: `14-18, 19-24, 25-29, 30-34, 36-40`. Nhảy từ 34 lên 36 — người 35 tuổi không thuộc nhóm nào.

### Cách sửa

Đổi nhãn nhóm `"36 - 40 y.o."` thành `"35 - 40 y.o."` để đảm bảo các nhóm tuổi liên tục, không bỏ sót. Tuy nhiên, cần ghi chú rõ ràng đây là giả định của nhóm phân tích, vì có khả năng nhỏ đây là thiết kế có chủ đích của cuộc khảo sát.

### Lý do

- Các nhóm tuổi trong khảo sát thường được thiết kế liên tục, không chồng chéo. Gap tại 35 tuổi nhiều khả năng là lỗi đánh nhãn vì:
  - Mọi nhóm khác đều liên tục: 14-18 tiếp nối 19-24 tiếp nối 25-29 tiếp nối 30-34
  - 35 tuổi nằm trong target audience (người trưởng thành), không có lý do loại trừ
- Tuy nhiên, nếu đây là thiết kế có chủ đích (ví dụ quotation sampling cố tình loại 35 tuổi), việc đổi nhãn sẽ sai. Ghi chú giả định trong báo cáo cuối.

---

## 6. Không nhất quán ký tự gạch ngang — En dash vs Hyphen

### Phát hiện

- 563 cột dùng dấu `-` (hyphen, U+002D): `C2 - Vị chanh`
- 30 cột dùng dấu `–` (en dash, U+2013): `C2 – Hồng Trà`

Cùng brand C2, cùng định dạng `Brand – Variant`, nhưng 2 ký tự Unicode khác nhau. Ngoài tên cột, giá trị bên trong các cột text như Q5.Bumo, Q1.TOM, Q7 cũng có tình trạng tương tự.

### Cách sửa

Thay thế toàn bộ dấu en dash `–` thành dấu gạch nối `-` trong cả tên cột lẫn giá trị bên trong các cột chứa tên brand (Q5.Bumo, Q1.TOM, Q7. Previous BUMO). Chọn chuẩn hóa về hyphen vì đây là ký tự chiếm đa số (563 so với 30).

### Lý do

- Hai ký tự trông giống nhau trên màn hình nhưng khác hoàn toàn về mã Unicode. Khi lọc hoặc tìm kiếm theo tên cột chứa `"C2 - "` sẽ bỏ sót 30 cột dùng en dash — mất dữ liệu mà không hay biết.
- Chuẩn hóa về hyphen vì đây là ký tự phổ biến hơn, dễ gõ trên bàn phím, và không gây vấn đề encoding.
- Phải sửa cả giá trị bên trong các cột text vì khi tra cứu chéo (ví dụ dùng giá trị Q5.Bumo để tìm cột Q4.P4W tương ứng), sự không khớp ký tự sẽ khiến tra cứu thất bại.

---

## 7. Không nhất quán chính tả "Olong" vs "Oolong"

### Phát hiện

- 76 cột viết `Olong` / `OLong`: tên brand Tea Plus và tên category
- 3 cột viết `Oolong`: `TH True Tea – Trà Oolong Tự Nhiên`

### Cách sửa

Thay thế toàn bộ "Oolong" thành "Olong" trong cả tên cột lẫn giá trị bên trong các cột chứa tên brand. Chọn chuẩn hóa về "Olong" vì đây là cách viết chiếm đa số tuyệt đối (76 so với 3) và cũng là tên thương mại chính thức của brand OLong Tea Plus.

### Lý do

- Hai cách viết cho cùng một loại trà sẽ gây tách nhóm khi thống kê hoặc lọc dữ liệu theo category trà Ô Long.
- Dù "Oolong" là cách viết đúng theo tiếng Anh quốc tế (từ gốc Hán 烏龍), trong ngữ cảnh dataset này, tên brand và tên category đều thống nhất dùng "Olong". Thống nhất theo đa số để tránh mất dữ liệu khi lọc.

---

## 8. Không nhất quán nhãn tần suất

### Phát hiện

Hai vấn đề:

**a) Dấu cách thừa:** Nhãn `"4-6 times/ week"` có dấu cách sau dấu `/`, trong khi `"2-3 times/week"` thì không có. Lỗi này xuất hiện ở cả câu hỏi S3b (tần suất chung) và Q6 (tần suất theo brand).

**b) Nhãn khác nhau giữa các câu hỏi:** Q6 có thêm giá trị `"Less than once per month"` (ít hơn 1 lần/tháng) mà S3b không có. Điều này hợp lý về mặt thiết kế: S3b là câu sàng lọc (screening) nên ai dùng quá ít sẽ bị loại khỏi khảo sát, trong khi Q6 hỏi từng brand riêng nên một người có thể dùng brand phụ rất ít.

### Cách sửa

**Với vấn đề a:** Xóa dấu cách thừa, thống nhất `"4-6 times/ week"` thành `"4-6 times/week"` trong tất cả các cột tần suất (S3b và Q6).

**Với vấn đề b:** Không sửa — đây là thiết kế hợp lý, không phải lỗi. Thay vào đó, khi cần so sánh hoặc sắp xếp tần suất, tạo thang đo thứ tự (ordinal) thống nhất cho tất cả giá trị tần suất ở cả S3b lẫn Q6: từ thấp nhất "Less than once per month" (1) đến cao nhất "Once per day" (7). Thang đo này giúp tính trung bình, trung vị, hoặc so sánh tần suất giữa các brand.

### Lý do

- **Dấu cách thừa:** Hai chuỗi `"4-6 times/ week"` và `"4-6 times/week"` khác nhau trong máy tính dù trông giống nhau trên màn hình. Khi thống kê phân bố hoặc nhóm dữ liệu, chúng sẽ bị tách thành 2 nhóm riêng — gây sai số liệu mà rất khó phát hiện bằng mắt.
- **Thang ordinal:** Tần suất có thứ tự tự nhiên (ít đến nhiều). Chuyển sang dạng số giúp tính toán trung bình, trung vị, hoặc tương quan. Mapping thống nhất đảm bảo cùng một thang đo khi so sánh tần suất chung (S3b) với tần suất từng brand (Q6).
- **Không sửa** sự khác biệt `"Less than once per month"` vì đây là thiết kế questionnaire hợp lý, phản ánh đúng bản chất khác nhau giữa 2 câu hỏi.

---

## 9. Trailing spaces trong Brandlist

### Phát hiện

14 trong 55 tên brand ở sheet Brandlist có 2-3 khoảng trắng thừa ở cuối tên. Ví dụ: `'C2 - Không xác định   '`, `'OLong Tea Plus   '`.

### Cách sửa

Cắt bỏ khoảng trắng thừa ở đầu và cuối tất cả tên brand trong Brandlist.

### Lý do

- Khoảng trắng thừa khiến 2 chuỗi trông giống nhau nhưng thực tế khác nhau trong máy tính. Khi dùng Brandlist để tra cứu hoặc nối (join) với bảng Dataset, 14 brand sẽ nối thất bại — mất dữ liệu âm thầm mà không có thông báo lỗi.
- Cắt khoảng trắng là thao tác an toàn, không thay đổi nội dung thực tế của tên brand.

---

## 10. Trùng tên brand trong Brandlist — 4 cặp

### Phát hiện

4 tên brand (sau khi cắt khoảng trắng) xuất hiện 2 lần với mã code khác nhau:

| Brand | Code 1 | Code 2 |
|-------|--------|--------|
| Trà sữa ít đường Vinamilk Happy Milktea | 26 | 261 |
| Trà lá vối Seventy | 27 | 271 |
| Trà sữa không độ/ Trà sữa Macchiato | 3000 | 3001 |
| Trà mật ong Boncha | 6000 | 6001 |

### Cách sửa

Đối chiếu với sheet QNR để xác định mã code nào là brand cha, mã nào là sub-brand hoặc variant. Sau khi xác định rõ, giữ lại một bản ghi duy nhất cho mỗi brand, loại bỏ bản ghi trùng. Nếu cả 2 code đều xuất hiện trong các câu hỏi khác nhau với ý nghĩa khác nhau, giữ cả 2 nhưng đổi tên cho rõ ràng (ví dụ thêm mã code vào tên).

### Lý do

- Brandlist dùng để chuyển đổi giữa mã code và tên brand. Nếu 1 tên có 2 code, việc chuyển đổi ngược (từ tên sang code) trở nên mập mờ, có thể gây nhầm lẫn trong thống kê.
- Dựa theo quy luật mã code (26 so với 261, 27 so với 271), code lớn hơn có vẻ là variant được thêm vào sau. Cần đối chiếu QNR xem 2 code này được sử dụng ở câu hỏi nào — nếu cùng câu hỏi thì thực sự trùng lặp, nếu ở câu hỏi khác thì có thể là brand cha so với sub-brand.

---

## 11. Mâu thuẫn logic Q5.BUMO vs Q4.P4W — 29 dòng

### Phát hiện

29 respondent có brand "dùng nhiều nhất" (BUMO) tại Q5 nhưng brand đó KHÔNG được đánh dấu "Yes" tại Q4 (đã dùng trong 4 tuần qua).

Ví dụ: Respondent nói brand dùng nhiều nhất là "C2 - Vị chanh" nhưng cột `Q4. P4W_C2 - Vị chanh` lại ghi "No".

### Cách sửa

Với 29 dòng bị mâu thuẫn, sửa cột Q4 (P4W usage) thành "Yes" cho brand BUMO tương ứng. Nghĩa là: nếu respondent khai brand X là brand dùng nhiều nhất, thì mặc nhiên coi rằng họ đã dùng brand X trong 4 tuần qua.

### Lý do

- Về mặt logic: nếu một người dùng brand X nhiều nhất trong 4 tuần qua, thì chắc chắn họ đã dùng brand X trong 4 tuần qua. Q5 (BUMO) là tập con của Q4 (P4W). Mâu thuẫn này chỉ có thể xảy ra do lỗi nhập liệu hoặc lỗi routing trong phần mềm khảo sát.
- Chọn sửa Q4 thay vì sửa Q5 vì: Q5 (BUMO) là câu hỏi tự do (respondent chủ động nêu tên brand dùng nhiều nhất), phản ánh suy nghĩ rõ ràng của họ. Còn Q4 là câu multi-choice (tick nhiều brand), dễ bỏ sót khi chọn. Do đó, Q5 có độ tin cậy cao hơn Q4.
- 29 trên 2,600 = 1.1% — tỷ lệ nhỏ, không ảnh hưởng lớn đến tổng thể nhưng nếu không sửa sẽ gây lỗi khi phân tích chéo giữa BUMO và P4W (ví dụ tính conversion rate từ usage sang BUMO).

---

## 12. Mẫu bất cân đối theo khu vực

### Phát hiện

| Region | n | % mẫu | Tỷ lệ dân số (ước tính) |
|--------|---|-------|------------------------|
| North | 1,200 | 46.2% | ~35% |
| South | 600 | 23.1% | ~30% |
| Central | 400 | 15.4% | ~18% |
| Mekong | 400 | 15.4% | ~17% |

North chiếm gần nửa mẫu, gấp 3 lần Central/Mekong.

### Cách sửa

Tạo cột trọng số (weight) cho mỗi respondent. Trọng số được tính bằng: tỷ lệ dân số thực tế của khu vực chia cho tỷ lệ mẫu khảo sát của khu vực đó. Respondent miền Bắc sẽ có trọng số nhỏ hơn 1 (giảm ảnh hưởng), respondent miền Nam sẽ có trọng số lớn hơn 1 (tăng ảnh hưởng).

Khi phân tích tổng thể (total), dùng trọng số này để tính weighted mean thay vì mean thông thường. Khi phân tích riêng theo từng khu vực (ví dụ so sánh North vs South), **không cần** dùng trọng số vì đã tách mẫu rồi.

**Lưu ý quan trọng:** Tỷ lệ dân số cần dùng số liệu chính thức (Tổng cục Thống kê, hoặc target universe thực tế của ngành RTD Tea). Nếu cuộc thi cung cấp weight sẵn, ưu tiên dùng weight chính thức.

### Lý do

- Phân tích tổng thể mà không dùng trọng số sẽ bị thiên lệch về hành vi tiêu dùng miền Bắc. Ví dụ: nếu miền Bắc ưa chuộng C2 hơn, kết quả tổng thể sẽ phóng đại thị phần của C2 so với thực tế.
- Trọng số giúp "cân bằng" lại mẫu để đại diện đúng cơ cấu dân số. Đây là kỹ thuật chuẩn trong nghiên cứu thị trường khi mẫu khảo sát không tỷ lệ thuận với dân số.

---

## 13. Encoding Yes/No dạng string — 864 cột

### Phát hiện

864 cột dùng giá trị `"Yes"` / `"No"` dạng chuỗi ký tự (string). Bao gồm tất cả cột awareness, usage, brand image, consideration.

### Cách sửa

Chuyển đổi tất cả các cột Yes/No từ dạng chuỗi ký tự sang dạng số: "Yes" thành 1, "No" thành 0. Các ô trống (NaN) giữ nguyên, không bị chuyển đổi. Thao tác này áp dụng cho mọi cột mà chỉ chứa 2 giá trị "Yes" và "No" (hoặc 1 trong 2 kèm ô trống).

### Lý do

- Dữ liệu dạng chuỗi ký tự không thể tính toán trực tiếp. Chuyển sang dạng số cho phép:
  - Tính trung bình (mean) = tỷ lệ phần trăm (ví dụ: awareness rate)
  - Tính tổng (sum) = đếm số người (ví dụ: absolute count)
  - Tính tương quan (correlation) giữa các brand hoặc attribute
  - Tính trung bình có trọng số kết hợp với cột weight ở bước 12
- Các ô trống (NaN) cần giữ nguyên vì chúng là missing by design (xem mục 4), không phải "No".

---

## Thứ tự thực hiện khuyến nghị

| Bước | Hành động | Phạm vi |
|------|-----------|---------|
| 1 | Loại bỏ cột 100% rỗng | Giảm 76 cột |
| 2 | Loại bỏ cột zero-variance | Giảm khoảng 72 cột |
| 3 | Xử lý cột trùng .1 | Giảm hoặc rename khoảng 15 cột |
| 4a | Chuẩn hóa en dash thành hyphen | 30 tên cột + giá trị text |
| 4b | Chuẩn hóa Oolong thành Olong | 3 tên cột + giá trị text |
| 4c | Sửa dấu cách thừa trong nhãn tần suất | Cột S3b và Q6 |
| 4d | Cắt khoảng trắng và loại trùng trong Brandlist | Sheet Brandlist |
| 5 | Sửa mâu thuẫn BUMO vs P4W | 29 dòng |
| 6 | Chuyển đổi Yes/No sang 1/0 | 864 cột |
| 7 | Tạo thang đo thứ tự cho tần suất | Cột S3b |
| 8 | Tạo trọng số theo khu vực | Cột mới weight_region |
| 9 | Ghi chú missing by design | Không sửa dữ liệu, sửa cách phân tích |

Thứ tự này đảm bảo:
- Giảm số chiều trước (bước 1-3) để các bước sau chạy nhanh hơn trên tập dữ liệu gọn hơn
- Chuẩn hóa văn bản trước (bước 4) để bước chuyển đổi 1/0 (bước 6) không gặp giá trị bất thường
- Trọng số và thang thứ tự tạo sau cùng vì chúng là cột phái sinh mới, không ảnh hưởng đến các bước làm sạch trước đó
- Missing by design để cuối cùng vì đây không phải sửa dữ liệu mà là nguyên tắc phân tích — cần được nhớ xuyên suốt quá trình làm việc với dữ liệu
