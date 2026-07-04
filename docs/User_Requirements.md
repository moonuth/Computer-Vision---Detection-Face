# User Requirements

## Mục tiêu
- Phát hiện và phân vùng khuôn mặt trong ảnh đông người.
- Ứng dụng vào hệ thống camera an ninh nhận diện khuôn mặt trong đám đông.

## Yêu cầu chi tiết
- Detection: Sử dụng RetinaFace với dữ liệu WIDER FACE để phát hiện khuôn mặt.
- Segmentation: Sử dụng U-Net hoặc Mask R-CNN với dữ liệu CelebAMask-HQ để phân vùng mặt (face mask).
- Đánh giá mô hình bằng các chỉ số: IoU, Dice, Pixel Accuracy.
