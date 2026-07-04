import sys
import os
import cv2

# Thêm thư mục src vào PATH để import file dễ dàng
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline import FacePipeline

def main():
    print("=== CHƯƠNG TRÌNH DEMO NHẬN DIỆN VÀ PHÂN VÙNG KHUÔN MẶT ===")
    
    # Bạn cần chỉ định đường dẫn ảnh thực tế tại đây
    image_path = input("Nhập đường dẫn ảnh (vd: ../data/sample.jpg): ").strip().strip('"').strip("'")
    
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy ảnh tại {image_path}")
        # Chạy tạm bằng việc bật webcam nếu không có ảnh
        print("Tự động chuyển sang chế độ Webcam...")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("temp_cam.jpg", frame)
            image_path = "temp_cam.jpg"
            cap.release()
        else:
            return
            
    # Khởi tạo Pipeline (Load weights của U-Net nếu có)
    # weights_path = "../models/segmentation/unet_best.pth"
    weights_path = None # Demo chưa có weights thật
    
    pipeline = FacePipeline(unet_weights_path=weights_path, device='cpu')
    
    print(f"Đang xử lý ảnh: {image_path}...")
    result_img = pipeline.process_image(image_path)
    
    # Hiển thị ảnh (Thu nhỏ nếu ảnh quá to để vừa màn hình)
    h, w = result_img.shape[:2]
    max_height = 800
    if h > max_height:
        scale = max_height / h
        display_img = cv2.resize(result_img, (int(w * scale), int(h * scale)))
    else:
        display_img = result_img
        
    cv2.imshow("Result", display_img)
    print("Nhấn phím bất kỳ trên cửa sổ ảnh để thoát...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Xóa file temp nếu có
    if image_path == "temp_cam.jpg" and os.path.exists("temp_cam.jpg"):
        os.remove("temp_cam.jpg")

if __name__ == '__main__':
    main()
