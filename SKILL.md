---
name: reel-doc-3d
description: 'Edit hoàn chỉnh video DỌC 9:16 (Reels/TikTok/Shorts) người nói chuyện: tự cắt khoảng lặng/ậm ừ/câu vấp (giữ lần nói trôi chảy nhất), tăng tốc 1.1-1.2, chỉnh màu + làm mịn da, chữ hiện từng cụm 2 font (Inter Tight + Playfair nghiêng) 3 màu trắng-đen-vàng, B-roll minh hoạ KHỐI 3D lấy từ thư viện 25+ mẫu (bộ đếm số, biểu đồ doanh thu, đơn hàng về, tiền về, lịch, đồng hồ, phễu, bia, tên lửa, bóng đèn, đánh giá sao, khách hàng, trước/sau, so sánh 2 cột, robot AI agent, chat giao việc, tự động hoá…) và tự vẽ thêm mẫu mới đúng nội dung rồi giữ lại thư viện, nền xen kẽ phông thật / xoá phông / chữ to sau đầu, nhiều hiệu ứng âm thanh tự tổng hợp, nhạc nền -15 dB, -14 LUFS, xuất 1080x1920. Kích hoạt khi người dùng đưa video QUAY DỌC và nói "edit video này", "làm reel", "edit reel dọc", "dựng video dọc", hoặc kéo file .MP4 dọc kèm ý muốn edit hoàn chỉnh.'
---

# Reel dọc 3D

Trả lời người dùng bằng ngôn ngữ của họ, dễ hiểu (họ thường không phải dân code). Báo rõ làm được gì / chưa / vì sao. Gửi file nháp/bản chính cho họ xem ngay khi xong. Lệnh lâu (dựng video) chạy nền.

**Python của skill:** `<thư mục skill>\venv\Scripts\python.exe` (tạo bằng `cai-dat.ps1`; chưa có thì hướng dẫn người dùng làm theo `HUONG-DAN-CAI-DAT.md`). Cần `ffmpeg` trong PATH. Dưới đây `py` = Python đó, `S` = `<thư mục skill>\scripts`.

## Bộ đồ nghề (`scripts\`)
| Tệp | Việc |
|---|---|
| `go_bang.py <video> <du an>` | gỡ băng (faster-whisper) → `tj.json` (từ + mốc giây + khoảng lặng) |
| `liet_ke.py <du an>` | in lời kèm số thứ tự từ để chọn đoạn giữ |
| `soat_cum.py <du an>` | soát `MANUAL` khớp lời, chỉ chỗ lệch |
| `reel_engine.py --du-an <du an> [--draft] [--list] [--png <giây> <ảnh>] [--meta]` | dựng hình + **thư viện mẫu B-roll** |
| `mix_engine.py --du-an <du an> [--draft]` | giọng + nhạc + hiệu ứng âm thanh, cân −14 LUFS, chặn đỉnh → file cuối |
| `thu_broll.py <du an>` | chạy khô mọi khung B-roll của dự án (bắt lỗi trước khi dựng) |
| `thu_mau.py <du an>` / `anh_mau_broll.py <du an>` | vẽ thử mọi mẫu / ảnh xem trước `mau-broll\_tat-ca.png` |
| `chuan_bi_nhac.py <bài.mp3> <tên>` | chuẩn bị nhạc nền vào `<skill>\nhac\` |
| `du_an_mau.py` | tệp cấu hình mẫu |
| `skin.py`, `fx3d.py` | làm mịn da; bộ vẽ giả 3D (extrude, tilt, block, coin, iso_box, soft_shadow) |
| `so_sanh_tach_phong.py <video> <giây> <số giây> <thư mục ra>` | so các cách tách phông cạnh nhau (tốc độ + độ nhấp nháy mép) |

**Tách phông:** mặc định **RobustVideoMatting bản nét** (`models\rvm_resnet50_fp32.onnx`, `cai-dat.ps1` tự tải) — mô hình tách người cho video, mép tóc/vai ổn định, dùng màu đã khử nền ở mép để hết viền sáng. `du_an.py`: `MATTE = "rvm"` (mặc định) / `"rvm-nhe"` (máy yếu, nhanh gấp ~2) / `"u2net"` (dự phòng). Thiếu file mô hình → tự dùng u2net.

Mỗi video = **một thư mục dự án** có `tj.json` + `du_an.py`. Engine không phải sửa cho từng video.

## Quy trình (nhiều video thì làm lần lượt)
1. **Xem video**: `ffprobe` (phải là dọc) + ảnh ghép khung (`ffmpeg -vf "fps=1/10,scale=160:-1,tile=13x2"`).
2. **Gỡ băng**: `py S\go_bang.py <video> <du an>` (dự án ví dụ `D:\reel\<tên>-edit`).
3. **Đọc lời** `py S\liet_ke.py <du an>`. Soát chữ nghe sai (tên riêng, thuật ngữ — ghi lại để báo người dùng xác nhận). Chọn đoạn giữ: bỏ câu vấp/lặp (**câu nói 2–3 lần giữ lần trôi chảy nhất**), bỏ câu bỏ lửng, từ đệm thừa ("thì", "đấy", "à ừ"), đoạn lan man. Lặp dính liền không có khoảng nghỉ thì để nguyên.
4. **Soạn `du_an.py`** (từ `du_an_mau.py`): `SRC`, `SPEED` (luôn tăng tốc: nói nhanh > ~4 từ/giây → 1.1, chậm → 1.2), `OUT_RES = (1080, 1920)`, `MUSIC` (≤3 bài đã chuẩn bị; video > ~2 phút cần 2 bài), `OUT_NAME`, `WRANGES` (đoạn giữ theo số thứ tự từ), `MANUAL` (chia cụm bằng tay 2–4 dòng; `*` chữ mảnh nhấn, `!` chữ dày nhấn, `"chữ|n"` khi sửa chữ nghe sai). Soát `soat_cum.py` → phải "OK".
5. **In số cụm**: `reel_engine.py --du-an <du an> --draft --list` → gán theo số trong ngoặc:
   - `BROLL`: ~6 cái/phút, mỗi cái 2–6 s (≤ 3 cụm), dồn ở **phần đầu** và chỗ có **số lớn / cần mô tả**; khi B-roll chạy thì phụ đề ẩn. Engine in "khoảng cách sự kiện lớn nhất" — phải ≤ 7 s.
   - `BEHIND` chữ to sau đầu 3–5 lần (từ ngắn 2–5 ký tự). `DARK` xoá phông nền tối ~8–10 cụm rải đều. Còn lại giữ phông thật (KHÔNG xoá phông hết).
6. **Chạy khô** `thu_broll.py <du an>` → "KHONG LOI". Xem thử vài khung `--png`, ghép bằng ffmpeg `hstack/xstack` để nhìn một lượt.
7. **Nháp 720p** (~10 phút / 1 phút video): `reel_engine.py --du-an <du an> --draft` rồi `mix_engine.py --du-an <du an> --draft` → gửi người dùng xem.
8. **Bản chính 1080×1920** (~25–30 phút / 1 phút video): bỏ `--draft`, chạy nền, lần lượt từng video. Chỉ đổi tiếng thì không dựng lại hình: `reel_engine.py ... --meta` rồi chạy lại `mix_engine.py`.
   - Đặt `FINAL_DIR` (thư mục thành phẩm của người dùng) + `TEN_GIAO` trong `du_an.py` → bản chính tự chép thêm vào đó tên `<ngày-tháng> <TEN_GIAO>.mp4`. Hỏi người dùng muốn để thành phẩm ở đâu ở video đầu tiên rồi ghi nhớ.
9. **Kiểm rồi báo**: độ dài, độ phân giải, LUFS/đỉnh (dòng "ket qua" của mix), số hiệu ứng âm thanh; nói thẳng phần chưa kiểm (AI không nghe được nhạc; chữ phải đoán). Dọn thư mục `work*` khi người dùng đã duyệt.

## THƯ VIỆN MẪU B-ROLL — luôn lớn dần
Xem tất cả: `mau-broll\_tat-ca.png`. Mỗi mẫu là 1 class trong `reel_engine.py`, chỉ đổi tham số:

| Mẫu | Kiểu | Dùng khi nói về | Tham số |
|---|---|---|---|
| `BCount` | lower | số lớn: follow, doanh thu, giá, số ngày | target, top, label, suffix |
| `BRevenue` | full | doanh thu/số liệu tăng theo thời gian | title, big, values, labels, total |
| `BOrders` | full | đơn hàng về liên tục | title, big, count, item, line |
| `BMoneyIn` | full | tiền về tài khoản, chốt đơn | title, amount, bank, line, suffix |
| `BCalendar` | full | thử thách N ngày, hạn chót | title, big, days, label |
| `BClock` | full | tiết kiệm thời gian, tốc độ | title, big, spins |
| `BFunnel` | full | phễu bán hàng, chuyển đổi | title, stages, numbers |
| `BTarget` | full | mục tiêu, đúng khách | title, big, foot |
| `BRocket` | full | tăng trưởng mạnh, bứt phá | title, big, foot |
| `BIdea` | full | ý tưởng, nhiều hướng | title, big, items[4] |
| `BStars` | full | đánh giá, review | title, rating, review, who, count |
| `BCustomers` | full | khách hàng, cộng đồng | title, big, total, buyers, label |
| `BBeforeAfter` | full | trước/sau, cũ vs mới | title, before, after, b_items, a_items |
| `BSplit` | full | so sánh 2 phía | title, left, left_items, right, right_items, me_ci |
| `BDonut` | full | tỉ lệ %, giảm giá % | title, pct, center, rest |
| `BProgress` | card | % hoàn thành | top, big, pct |
| `BStairs` | full | các giai đoạn tiến bộ, lộ trình | title, big, steps, foot |
| `BFx` | full | danh sách 4–6 hạng mục | title, big, items, icons |
| `BTimeline` | full | quy trình/phần mềm tự chạy | title, big, chip, foot, tracks |
| `BWave` | lower | cắt ghép âm thanh (CHỈ khi nói về âm thanh) | big, sub |
| `BGift` | lower | quà tặng, miễn phí, CTA, phần sau | big, sub |
| `BAgentTeam` | full | công ty AI agent, phân việc cho AI | title, big, boss, agents[4] |
| `BChatTask` | full | giao việc cho AI qua chat | title, user, items, done, agent |
| `BBugFix` | full | lỗi, trục trặc | title, big, sub, count |
| `BAutomate` | full | tự động hoá | title, big, inp, out, foot |
| `BScale` | full | cân nặng giảm từ A → B kg (bàn cân 3D, số chạy, thẻ "-N KG"); start == end → chững cân | title, start, end, unit, big, foot, badge |
| `BCalo` | full | thâm hụt calo: cột ăn vào vs cột đốt đi + "THÂM HỤT N CALO" | title, eat, burn, eat_label, burn_label, eat_txt, burn_txt, result |

**Quy tắc thư viện (quan trọng nhất):**
1. **Nội dung có ý chưa có mẫu hợp → VẼ MẪU MỚI** đúng ý (không gượng ép mẫu cũ). Viết class mới trong `reel_engine.py` cùng kiểu: nền đen; chỉ trắng + vàng #FFC400 (+ sắc tối của chúng cho mặt bên); khối 3D (`t3d`, `put3`, `F3.block/tilt/coin/iso_box/extrude/soft_shadow`, `robot()`, `person()`); có chuyển động bên trong (phần tử bật lần lượt, xoay, nảy); hàm `sfx()` trả danh sách tiếng; chữ dài phải tự co (`fit_font`); kẹp kích thước tối thiểu khi phần tử bật ra từ 0.
2. **GIỮ LẠI mẫu mới** trong `reel_engine.py` của skill, thêm 1 dòng vào bảng trên, chạy `thu_mau.py` (phải "KHONG LOI") rồi `anh_mau_broll.py` để cập nhật ảnh. Càng nhiều video, thư viện càng dày.
3. **Minh hoạ phải đúng ý câu nói** — không dùng sóng nhạc cho "lỗi", không gắn thứ không liên quan.
4. Muốn dùng icon/ảnh tải từ mạng thì phải hỏi người dùng trước (bản quyền).

## B-ROLL CỦA NGƯỜI DÙNG — cảnh quay / ảnh thật (`BUser`, thêm 16/10/2026)
Người dùng có cảnh riêng: quay sản phẩm, quay màn hình app, ảnh khách, hậu trường… → bỏ vào một thư mục (đặt `BROLL_DIR` trong `du_an.py`, đường dẫn trong `src` tính từ đó). Mỗi cảnh là 1 dòng trong `BROLL`, dùng xen kẽ với mẫu 3D:
`(cụm đầu, cụm cuối, "BUser", {"src": "app.mp4", "layout": "phone", "title": "Hormozi OS", "label": "Quay màn hình app"})`

| `layout` | Trông thế nào | Hợp với | Phụ đề |
|---|---|---|---|
| `full` | toàn màn hình, đẩy vào chậm | cảnh quay dọc đẹp, cảnh "khoe" | ẩn |
| `split` | cảnh ở trên 56%, mặt người nói ở dưới, vạch vàng ngăn | cảnh quay ngang khi vẫn cần thấy mặt người nói | **giữ** |
| `card` | cảnh trong thẻ bo góc viền vàng nghiêng 3D, nền là chính cảnh đó làm mờ | cảnh quay ngang, quay màn hình máy tính, ảnh ngang | ẩn |
| `phone` | cảnh trong khung điện thoại 3D nghiêng | **quay màn hình điện thoại / app** | ẩn |
| `polaroid` | 2–5 ảnh khung trắng rơi xuống xếp chồng, chữ dưới mỗi ảnh (`items`) | ảnh khách, kết quả, hậu trường, bằng chứng | ẩn |
| `sticker` | tách vật thể khỏi nền + viền trắng kiểu nhãn dán, lơ lửng trên nền tối | ảnh sản phẩm, đồ vật (PNG trong suốt càng đẹp) | ẩn |
| `pip` | cảnh toàn màn hình + mặt người nói trong bong bóng tròn viền vàng ở góc | demo dài mà vẫn cần mặt người nói | **giữ** |
| `montage` | nhiều cảnh/ảnh cắt nhanh 0,45–0,8 s, chớp trắng nhẹ giữa các cảnh | liệt kê nhiều thứ, "rất nhiều khách / đơn / sản phẩm" | ẩn |
| `cards` | nhiều ảnh lần lượt, mỗi ảnh GIỮ NGUYÊN KHUNG trong thẻ viền vàng nghiêng 3D, nền là ảnh đó làm mờ, `items` = nhãn vàng dưới từng ảnh; ≥1,3 s/ảnh | **ảnh trước/sau ghép đôi**, ảnh vuông, ảnh thành tích (montage/full sẽ cắt mất một nửa) | ẩn |
| `auto` (mặc định) | tự chọn: nhiều ảnh → polaroid; nhiều video → montage; PNG trong suốt → sticker; ảnh → card; video dọc → full/phone; video ngang → card/split | | |

Tham số khác: `inpoint` (`"auto"` = tự chọn đoạn NÉT + có chuyển động vừa, tránh rung và 0,3 s đầu; hoặc số giây), `focus` (0–1, vị trí cắt ngang khi cảnh ngang đưa vào khung dọc), `label` (nhãn vàng nhỏ), `title`, `items` (chữ dưới ảnh polaroid), `audio` (0 = tắt tiếng cảnh chèn; 0,2–0,5 = giữ tiếng nền nhỏ cho thật), `motion` (`push` / `pull` / `pan`), `captions` (ép giữ/ẩn phụ đề).

Tự động làm sẵn: cảnh **vào sớm hơn từ khoá 0,12 s**; chỉnh màu cảnh chèn **giống video chính** (`GRADE`); ảnh tĩnh luôn có chuyển động (Ken Burns); 4 kiểu vào cảnh luân phiên (trượt lên / bật phóng / mở tròn / quét ngang có nhoè); tiếng vút vào–ra, polaroid có tiếng chụp ảnh, montage có swish mỗi cảnh; hết clip thì dừng ở khung cuối.

**Quy tắc chọn & đặt cảnh (tổng hợp từ hướng dẫn edit video ngắn):** mỗi cảnh chèn 2–4 s (montage 0,45–0,8 s/cảnh); cảnh phải **CỤ THỂ đúng câu đang nói**, không chung chung; ~3–6 cảnh chèn mỗi phút, đừng phủ kín thành phim ghép — người xem cần thấy mặt người nói (không để mặt vắng > ~6 s trừ `split`/`pip`); chủ thể để giữa khung dọc; cảnh lệch tỉ lệ → `card` (nền mờ) hoặc `split` thay vì cắt mất chủ thể; quay màn hình → `phone`; hiệu ứng nổi khối/parallax chỉ dùng cho khoảnh khắc đặc biệt, không dùng cho mọi cảnh. Chưa rõ cảnh nào hợp câu nào → xem vài khung từng cảnh (ffmpeg trích khung) rồi tự ghép, báo người dùng danh sách để duyệt.



## Phong cách đã chốt
- 2 font: Inter Tight (mọi độ đậm) + Playfair Display Italic (thư mục `fonts\`). 3 màu: trắng, đen #0C0C0C, vàng #FFC400.
- Chữ mảnh (Playfair) → hiện mờ + trôi lên + gạch chân vàng + sao lấp lánh. Chữ dày (Inter Black) → hộp vàng quét + bật nảy + rung. Chữ thường → nổi lên / trượt trái / trượt phải luân phiên.
- Máy quay 3 kiểu luân phiên theo cụm (đẩy vào chậm, giật nhấn rồi lùi, lùi ra + trôi ngang); đổi nền có chớp trắng 1–2 khung.
- Chỉnh màu ấm nhẹ + làm mịn da vùng mặt (`skin.py`).
- **Âm thanh nhiều nhưng nhỏ dưới giọng**: B-roll (vút vào/ra, tích tắc khi đếm, ding, pop, chuông tin nhắn, gõ phím), chữ (bóp nhẹ ở chữ dày, lấp lánh ở chữ mảnh, swish + đập trầm khi chữ sau đầu, swish khi đổi nền); boom ≤ 3 (thừa tự đổi thành thud), riser ≤ 1. Nhạc −15 dB so với giọng, hạ khi nói, nhỏ dần cuối. Cân −14 LUFS rồi chặn đỉnh −1,5 dB.

## Bẫy đã gặp
- Hình bật ra từ kích thước 0 → PIL lỗi kích thước âm giữa lúc dựng → luôn chạy khô trước.
- Gán số cụm bằng đếm nhẩm dễ lệch 1 → luôn dùng `--list`.
- Bộ đệm ảnh chữ 3D đã giới hạn; khi sửa nhớ xoá bộ đệm TRƯỚC khi thêm.
- Video 2K/4K dọc: bản chính để 1080×1920 cho nhanh và nhẹ; RAM 16 GB thì dựng lần lượt, không chạy song song.
- Mặt nạ tách người có thể dính lưng ghế cạnh vai — soi khung đoạn `DARK`.
- Tiếng ngắn sắc (gõ phím, lấp lánh) đẩy đỉnh vượt 0 dB sau khi nâng độ to → mix đã có chặn đỉnh; đừng bỏ.
