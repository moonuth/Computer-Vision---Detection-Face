import os

import cv2

import numpy as np

import torch

from torch.utils.data import Dataset, DataLoader

import torchvision.transforms as transforms

from PIL import Image

class CelebAMaskDataset(Dataset):
    """
    Dataset class cho CelebAMask-HQ (Phục vụ Segmentation)
    Cấu trúc thư mục giả định:
    data_dir/
        images/ -> chứa các file ảnh gốc (.jpg)
        masks/  -> chứa các file mask tương ứng (.png)
    """
    def __init__(self, data_dir, transform=None, mask_transform=None):
        self.data_dir = data_dir
        self.image_dir = os.path.join(data_dir, 'images')
        self.mask_dir = os.path.join(data_dir, 'masks')
        
        # Lấy danh sách tên file hợp lệ (kiểm tra tồn tại ở cả 2 thư mục)
        if os.path.exists(self.image_dir) and os.path.exists(self.mask_dir):
            self.image_names = sorted(os.listdir(self.image_dir))
        else:
            self.image_names = []
            
        self.transform = transform
        self.mask_transform = mask_transform
        
        # Default transforms nếu không truyền vào (Resize về 256x256 cho nhẹ)
        if self.transform is None:
            self.transform = transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                     std=[0.229, 0.224, 0.225])
            ])
            
        if self.mask_transform is None:
            self.mask_transform = transforms.Compose([
                transforms.Resize((256, 256), interpolation=transforms.InterpolationMode.NEAREST),
                transforms.ToTensor()
            ])

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx):
        img_name = self.image_names[idx]
        img_path = os.path.join(self.image_dir, img_name)
        
        # Mask thường có đuôi .png trong CelebAMask-HQ
        mask_name = os.path.splitext(img_name)[0] + '.png' 
        mask_path = os.path.join(self.mask_dir, mask_name)
        
        # Đọc ảnh gốc bằng PIL (RGB)
        image = Image.open(img_path).convert("RGB")
        
        # Đọc mask (Grayscale)
        mask = Image.open(mask_path).convert("L")
        
        if self.transform:
            image = self.transform(image)
        if self.mask_transform:
            mask = self.mask_transform(mask)
            # Thresholding mask để đảm bảo chỉ có giá trị 0 và 1
            mask = (mask > 0.5).float()
            
        return image, mask

def get_segmentation_dataloaders(data_dir, batch_size=16, val_split=0.2, num_workers=2):
    """
    Tạo DataLoader cho quá trình Train và Validation
    """
    dataset = CelebAMaskDataset(data_dir=data_dir)
    
    # Chia train/val
    dataset_size = len(dataset)
    if dataset_size == 0:
        print(f"Cảnh báo: Không tìm thấy data trong {data_dir}. Dataloader sẽ rỗng.")
        return None, None
        
    val_size = int(val_split * dataset_size)
    train_size = dataset_size - val_size
    
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return train_loader, val_loader

if __name__ == "__main__":
    # Test thử code
    print("Test Thành viên 1 - Data Utils")
    dummy_loader, _ = get_segmentation_dataloaders("data/celeb_mask")
    print("Done init DataLoader.")
