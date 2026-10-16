# -*- coding: utf-8 -*-
"""TEP CAU HINH 1 VIDEO - copy vao thu muc du an, doi ten thanh du_an.py, sua theo video moi.
(Vi du minh hoa - MANUAL/WRANGES phai soan lai theo ban go bang that cua video ban.)"""

SRC = r"D:\video\clip-cua-ban.mp4"   # video nguon QUAY DOC
SPEED = 1.1                          # LUON tang toc: noi nhanh (> ~4 tu/giay sau khi cat) 1.1, noi cham 1.2
OUT_RES = (1080, 1920)               # bo dong nay = giu nguyen do phan giai nguon
MUSIC = ["chill"]                    # ten nhac da chuan bi bang chuan_bi_nhac.py (<=3 bai, bai sau noi khi bai truoc het)
OUT_NAME = "reel-cua-toi"            # file ra: <OUT_NAME>.mp4 (ban nhap: <OUT_NAME>_nhap720.mp4)
FINAL_DIR = r"D:\Video da xong"     # ban chinh tu chep them vao day: "<ngay-thang> <TEN_GIAO>.mp4" (bo dong nay = khong chep)
TEN_GIAO = "cách có 100 khách đầu tiên"

# Doan giu theo SO THU TU TU (in bang: python liet_ke.py <thu muc du an>). Bo cau vap / cau lap (giu lan noi tron nhat) / am u.
WRANGES = [(0, 40), (46, 120)]

# Chia cum chu BANG TAY, 2-4 dong/cum, tong so tu phai khop WRANGES (kiem bang soat_cum.py).
#   "*chu"  = chu manh Playfair nghieng (tu nhan, hieu ung sang)
#   "!chu"  = chu day Inter Tight Black tren hop vang (hieu ung nang dong)
#   "chu|n" = hien "chu" nhung an n tu cua ban go bang (whisper tach "100" "%", hoac sua chu nghe sai)
MANUAL = [
    ["Hôm nay mình sẽ", "*chia sẻ", "một cách"],
    ["giúp bạn có", "!100 khách|2", "đầu tiên"],
    # ...
]

# B-roll 3D tu thu vien (xem mau-broll\_tat-ca.png): (cum dau, cum cuoi, "TenMau", {tham so}).
# SO CUM lay tu: python reel_engine.py --du-an <thu muc> --draft --list
BROLL = [
    (1, 1, "BCustomers", {"title": "Từ người lạ", "big": "100 KHÁCH ĐẦU", "total": 24, "buyers": 10, "label": "KHÁCH"}),
    # (5, 6, "BRevenue", {"title": "Doanh thu", "big": "TĂNG GẤP 3", "values": [10, 18, 30], "labels": ["T1", "T2", "T3"]}),
]
BEHIND = {}      # {so cum: "TU NGAN"} - chu to nam SAU DAU (2-5 ky tu), 3-5 lan/video
DARK = set()     # {so cum} - xoa phong nen toi, ~8-10 cum rai deu; con lai giu phong that
