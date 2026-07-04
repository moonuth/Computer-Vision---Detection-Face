# 🚀 Dự án Nhận diện & Phân vùng khuôn mặt (Face Detection & Segmentation)

> **Lưu ý:** Thời gian chỉ còn khoảng 1 tuần, nhóm chạy hết tốc lực và bám sát timeline dưới đây.

## 📂 Cấu trúc thư mục (Repository Structure)

```text
Face_detection/
├── data/                   # Chứa dữ liệu (WIDER FACE, CelebAMask-HQ)
│   ├── wider_face/
│   └── celeb_mask/
├── models/                 # Chứa trọng số (weights) của mô hình đã train
│   ├── detection/          # Trọng số RetinaFace pretrained
│   └── segmentation/       # Trọng số U-Net (lưu các epochs tốt nhất)
├── notebooks/              # Chứa file .ipynb để chạy nháp, test data
├── src/                    # Source code chính
│   ├── data_utils.py       # Code Dataset, DataLoader, Augmentation
│   ├── detection_model.py  # Code load RetinaFace và lấy Bounding Box
│   ├── segmentation_net.py # Khởi tạo cấu trúc mạng U-Net
│   ├── train_seg.py        # Training loop cho U-Net (Loss, Optimizer)
│   ├── metrics.py          # Code tính IoU, Dice, Pixel Accuracy
│   └── pipeline.py         # Ghép nối Detection -> Crop mặt -> Segmentation
├── demo/                   # Script chạy demo thực tế (trên webcam/video)
├── docs/                   # Tài liệu, thiết kế, báo cáo
└── README.md               # File thông tin chung & Phân chia công việc
```

---

## 👥 Phân chia công việc (Task Assignment)

Dự án chia làm 3 nhánh chạy song song. Các thành viên nhận code và trao đổi liên tục!

### 🟢 Nhánh 1: Data & Detection (Nhiệm vụ: Cung cấp Bounding Box)
*   **Thành viên 1 (Data Prep):** Tải dataset, viết hàm trong `src/data_utils.py` để tiền xử lý và chia tập train/val. Đẩy data lên Drive.
*   **Thành viên 2 (Detection):** Dùng pretrained **RetinaFace**. Viết `src/detection_model.py` nhận ảnh đầu vào và trả ra tọa độ các khuôn mặt (Bbox).

### 🔵 Nhánh 2: Segmentation (Nhiệm vụ: Phân vùng mặt từ Bbox)
*   **Thành viên 3 (Model - U-Net):** Viết cấu trúc mạng U-Net tại `src/segmentation_net.py`. Đảm bảo code chạy qua được một batch data (test nháp).
*   **Thành viên 4 (Trainer):** Code `src/train_seg.py` và cắm máy (Colab/Kaggle) để train. Chịu trách nhiệm lưu lại trọng số tốt nhất vào thư mục `models/segmentation/`.

### 🟡 Nhánh 3: Tích hợp & Báo cáo (Nhiệm vụ: Ghép lúa, chốt sổ)
*   **Thành viên 5 (Pipeline & Metrics):** 
    *   Code hàm tính IoU, Dice trong `src/metrics.py`.
    *   Viết `src/pipeline.py` ghép nối: `Nhận Bbox từ (2) -> Cắt mặt -> Đưa vào (4) -> Lấy kết quả Mask`. 
    *   Làm script chạy demo.
*   **Thành viên 6 (BA & Tài liệu):** Thu thập thông tin, viết báo cáo Word, làm slide trình bày. Tổng hợp số liệu từ (4) và (5). Hỗ trợ quay video demo dự án.

## ⚠️ Quy tắc làm việc
- Code xong tính năng nào push ngay lên Github.
- Không sửa code của người khác nếu chưa báo.
- Ưu tiên mô hình Pre-trained nếu gặp bug quá khó, mục tiêu tối thượng là **có sản phẩm demo chạy được**.
