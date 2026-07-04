# Solution Design

## Kiến trúc tổng thể
- Pipeline gồm 2 bước: Detection (RetinaFace) → Segmentation (U-Net/Mask R-CNN).
- Tiền xử lý dữ liệu: chuẩn hóa, augment, chia train/val/test.

## Mô hình
- Detection: RetinaFace (pretrained)
- Segmentation: U-Net (code tay) hoặc Mask R-CNN (pretrained)

## Đánh giá
- Sử dụng các chỉ số: IoU, Dice, Pixel Accuracy.
- Demo ứng dụng: Camera an ninh nhận diện và phân tích khuôn mặt trong đám đông.
