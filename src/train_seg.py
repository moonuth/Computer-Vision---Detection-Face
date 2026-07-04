import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import os

from segmentation_net import UNet
from data_utils import get_segmentation_dataloaders
from metrics import calculate_metrics

def train_model(data_dir, num_epochs=10, batch_size=8, lr=1e-4):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Đang dùng thiết bị: {device}")
    
    # 1. Khởi tạo Data
    train_loader, val_loader = get_segmentation_dataloaders(data_dir, batch_size=batch_size)
    if train_loader is None:
        return
        
    # 2. Khởi tạo Mô hình, Loss, Optimizer
    model = UNet(in_channels=3, out_channels=1).to(device)
    criterion = nn.BCELoss() # Binary Cross Entropy cho mask (0 hoặc 1)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    best_val_iou = 0.0
    save_dir = "../models/segmentation"
    os.makedirs(save_dir, exist_ok=True)
    
    # 3. Vòng lặp Training
    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        
        # --- Train Phase ---
        model.train()
        train_loss = 0.0
        for images, masks in tqdm(train_loader, desc="Training"):
            images, masks = images.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * images.size(0)
            
        train_loss = train_loss / len(train_loader.dataset)
        
        # --- Validation Phase ---
        model.eval()
        val_loss = 0.0
        val_iou = 0.0
        
        with torch.no_grad():
            for images, masks in tqdm(val_loader, desc="Validation"):
                images, masks = images.to(device), masks.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, masks)
                val_loss += loss.item() * images.size(0)
                
                # Tính metrics
                metrics = calculate_metrics(outputs, masks)
                val_iou += metrics['iou'] * images.size(0)
                
        val_loss = val_loss / len(val_loader.dataset)
        val_iou = val_iou / len(val_loader.dataset)
        
        print(f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val IoU: {val_iou:.4f}")
        
        # 4. Lưu mô hình tốt nhất
        if val_iou > best_val_iou:
            best_val_iou = val_iou
            save_path = os.path.join(save_dir, "unet_best.pth")
            torch.save(model.state_dict(), save_path)
            print(f"Đã lưu mô hình tốt nhất tại: {save_path}")

if __name__ == '__main__':
    print("Thành viên 4: Bắt đầu train...")
    # Vì mình đang đứng ở thư mục gốc (Face_detection) nên đường dẫn là data/celeb_mask
    train_model(data_dir="data/celeb_mask", num_epochs=3)
