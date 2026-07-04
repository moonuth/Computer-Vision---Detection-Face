import os
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def print_instructions():
    print("="*60)
    print(" HƯỚNG DẪN TẢI DATASET CHO THÀNH VIÊN 1 (DATA PREP)")
    print("="*60)
    
    print("\n⚠️ LƯU Ý QUAN TRỌNG: 2 bộ dataset này nặng gần 10GB. Đừng tải thủ công!")
    print("Cách tốt nhất là cài đặt Kaggle API để tải bằng 2 dòng lệnh dưới đây.\n")
    
    print("Bước 1: Mở Terminal và cài thư viện Kaggle")
    print("  pip install kaggle")
    print("\nBước 2: Lên trang kaggle.com, vào Settings -> Create New API Token.")
    print("  Một file kaggle.json sẽ tải về máy. Bạn copy file đó vào thư mục C:\\Users\\<Tên_User>\\.kaggle\\")
    print("\nBước 3: Chạy 2 lệnh sau trên Terminal để tải dữ liệu thẳng vào thư mục data:")
    
    print("\n---> Tải CelebAMask-HQ (Cho phần Segmentation):")
    print("  cd data/celeb_mask")
    print("  kaggle datasets download -d bllndr/celebaspoof-face-mask-dataset --unzip")
    
    print("\n---> Tải WIDER FACE (Cho phần Detection):")
    print("  cd ../wider_face")
    print("  kaggle datasets download -d mks2192/wider-face --unzip")
    print("\n" + "="*60)

def create_dummy_data(base_dir):
    """
    Tạo một vài ảnh trống (dummy data) để Nhánh 2 (Segmentation) có thể 
    test code train U-Net ngay lập tức mà không cần đợi tải 10GB data thật.
    """
    print("\n[Tính năng phụ] Đang tạo một số ảnh giả lập để test code...")
    import cv2
    import numpy as np
    
    img_dir = os.path.join(base_dir, "celeb_mask", "images")
    mask_dir = os.path.join(base_dir, "celeb_mask", "masks")
    
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(mask_dir, exist_ok=True)
    
    for i in range(5): # Tạo 5 ảnh giả
        # Tạo ảnh đen 256x256
        dummy_img = np.zeros((256, 256, 3), dtype=np.uint8)
        # Tạo mặt nạ đen 256x256
        dummy_mask = np.zeros((256, 256), dtype=np.uint8)
        
        # Vẽ một vòng tròn trắng vào giữa để giả làm khuôn mặt
        cv2.circle(dummy_img, (128, 128), 50, (255, 255, 255), -1)
        cv2.circle(dummy_mask, (128, 128), 50, 255, -1)
        
        # Lưu file
        cv2.imwrite(os.path.join(img_dir, f"{i:05d}.jpg"), dummy_img)
        cv2.imwrite(os.path.join(mask_dir, f"{i:05d}.png"), dummy_mask)
        
    print(f"Đã tạo 5 ảnh test tại: {img_dir} và {mask_dir}")
    print("Thành viên 4 (Trainer) có thể chạy file src/train_seg.py để test ngay!")

if __name__ == "__main__":
    # Đảm bảo đứng từ thư mục gốc
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    
    print_instructions()
    create_dummy_data("data")
