import cv2
import torch
import numpy as np
import torchvision.transforms as transforms
from PIL import Image
import os

from detection_model import FaceDetector
from segmentation_net import UNet

class FacePipeline:
    """
    Pipeline tích hợp:
    1. Phát hiện khuôn mặt bằng RetinaFace
    2. Cắt khuôn mặt và đẩy qua U-Net
    3. Vẽ Mask (Phân vùng) đè lên ảnh gốc
    """
    def __init__(self, unet_weights_path=None, device='cpu'):
        self.device = torch.device(device)
        print(f"Khởi tạo Pipeline trên {self.device}")
        
        # Init Bước 1: Face Detector
        self.detector = FaceDetector()
        
        # Init Bước 2: Segmentation Model
        self.unet = UNet(in_channels=3, out_channels=1).to(self.device)
        if unet_weights_path and os.path.exists(unet_weights_path):
            self.unet.load_state_dict(torch.load(unet_weights_path, map_location=self.device))
            print("Đã load weights cho U-Net thành công.")
        else:
            print("Cảnh báo: Chưa có weights cho U-Net, dùng weights ngẫu nhiên!")
            
        self.unet.eval()
        
        # Transform ảnh để đưa vào U-Net
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])
        
    def process_image(self, image_path):
        # 1. Đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Không thể đọc ảnh từ {image_path}")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result_image = image.copy()
        
        # 2. Detect khuôn mặt
        bboxes = self.detector.detect_faces(image_rgb)
        print(f"Phát hiện được {len(bboxes)} khuôn mặt.")
        
        # 3. Duyệt qua từng khuôn mặt
        for bbox in bboxes:
            x1, y1, x2, y2 = [int(v) for v in bbox]
            
            # Đảm bảo tọa độ hợp lệ
            x1, y1 = max(0, x1), max(0, y1)
            h, w, _ = image.shape
            x2, y2 = min(w, x2), min(h, y2)
            
            # Vẽ Bounding Box
            cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Cắt mặt
            face_crop = image_rgb[y1:y2, x1:x2]
            if face_crop.size == 0:
                continue
                
            # Tiền xử lý đưa vào U-Net
            face_pil = Image.fromarray(face_crop)
            face_tensor = self.transform(face_pil).unsqueeze(0).to(self.device)
            
            # Predict Mask
            with torch.no_grad():
                pred_mask = self.unet(face_tensor)
                pred_mask = (pred_mask > 0.5).float().squeeze().cpu().numpy()
                
            # Resize mask về đúng kích thước của face_crop
            mask_resized = cv2.resize(pred_mask, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
            
            # Tạo lớp phủ (Overlay) màu xanh dương (Blue) cho Mask
            color_mask = np.zeros_like(face_crop)
            color_mask[mask_resized == 1] = [255, 0, 0] # BGR
            
            # Trộn Mask với Ảnh gốc
            alpha = 0.5
            roi = result_image[y1:y2, x1:x2]
            
            # Chỉ tô màu lên những vị trí có mask
            mask_indices = mask_resized == 1
            roi[mask_indices] = cv2.addWeighted(roi, 1 - alpha, color_mask, alpha, 0)[mask_indices]
            result_image[y1:y2, x1:x2] = roi
            
        return result_image

if __name__ == '__main__':
    print("Test Thành viên 5 - Pipeline")
    # pipe = FacePipeline()
    # out_img = pipe.process_image("test.jpg")
    print("Đã khởi tạo Pipeline thành công.")
