# Implementation Plan

## Sprint 1: Chuẩn bị dữ liệu
- Tải và tiền xử lý WIDER FACE, CelebAMask-HQ
- Data augmentation, chia train/val/test

## Sprint 2: Xây dựng mô hình
- Detection: Sử dụng RetinaFace (pretrained)
- Segmentation: Code tay U-Net hoặc dùng Mask R-CNN (pretrained)

## Sprint 3: Huấn luyện & Đánh giá
- Training loop, tính IoU, Dice, Pixel Acc
- So sánh kết quả các mô hình

## Sprint 4: Tích hợp & Demo
- Ghép pipeline, viết script demo, chuẩn bị báo cáo, slide thuyết trình
