import kagglehub

print("Đang khởi tạo kết nối tải dữ liệu...")
print("⚠️ Chú ý: Trình duyệt sẽ mở ra để bạn xác nhận đăng nhập Kaggle. Vui lòng bấm Cho phép (Allow) nhé!")
kagglehub.login()

print("Đang tải dữ liệu (có thể mất vài phút)...")
path = kagglehub.dataset_download('bllndr/celebaspoof-face-mask-dataset')
print(f'\nTẢI THÀNH CÔNG! Dữ liệu đã được lưu tại: {path}')
print("Bạn có thể vào đường dẫn trên để copy dữ liệu bỏ vào thư mục data/celeb_mask nhé!")
