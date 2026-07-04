import cv2
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]

try:
    from retinaface import RetinaFace
except ImportError:
    print("Vui lòng cài đặt thư viện: pip install retina-face")
    RetinaFace = None

class FaceDetector:
    """
    Module phát hiện khuôn mặt sử dụng RetinaFace (Pretrained)
    Nhiệm vụ: Nhận vào ảnh gốc, trả về tọa độ Bounding Box của khuôn mặt
    """
    def __init__(self, use_gpu=False):
        # RetinaFace tự động down weights trong lần chạy đầu tiên
        self.use_gpu = use_gpu
        print("Đã khởi tạo mô hình Face Detector (RetinaFace).")

    def detect_faces(self, image_path_or_numpy):
        """
        Nhận vào đường dẫn ảnh hoặc numpy array (RGB/BGR)
        Trả về list các bounding box: [[x1, y1, x2, y2], ...]
        """
        if RetinaFace is None:
            raise ImportError("Chưa cài đặt retina-face.")

        # RetinaFace.detect_faces trả về 1 dict chứa tọa độ và các điểm landmarks
        faces = RetinaFace.detect_faces(image_path_or_numpy)
        
        bboxes = []
        if type(faces) == dict:
            for key, face in faces.items():
                # Lấy tọa độ facial area (bounding box)
                bbox = face["facial_area"] # [x1, y1, x2, y2]
                bboxes.append(bbox)
                
        return bboxes

    def crop_faces(self, image_numpy, bboxes):
        """
        Cắt các khuôn mặt từ ảnh dựa trên bounding box để đưa vào U-Net
        """
        cropped_faces = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            # Đảm bảo tọa độ không vượt quá kích thước ảnh
            x1, y1 = max(0, x1), max(0, y1)
            # Cắt ảnh
            crop = image_numpy[y1:y2, x1:x2]
            cropped_faces.append(crop)
            
        return cropped_faces

if __name__ == "__main__":
    # Test thử code cho Thành viên 2
    print("Test Thành viên 2 - Detection")
    detector = FaceDetector()
    print("Sẵn sàng nhận diện khuôn mặt.")
