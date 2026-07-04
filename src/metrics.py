import torch
import numpy as np

def calculate_metrics(preds, masks, threshold=0.5):
    """
    preds: (Batch_size, 1, H, W) - Xác suất từ Sigmoid
    masks: (Batch_size, 1, H, W) - Ground truth (0 hoặc 1)
    """
    # Đưa preds về 0 hoặc 1 dựa vào ngưỡng threshold
    preds = (preds > threshold).float()
    masks = (masks > 0.5).float()
    
    # Ép kiểu để chắc chắn
    preds = preds.view(-1)
    masks = masks.view(-1)
    
    intersection = (preds * masks).sum()
    union = preds.sum() + masks.sum() - intersection
    
    # 1. IoU (Intersection over Union)
    # Thêm 1e-6 để tránh chia cho 0
    iou = (intersection + 1e-6) / (union + 1e-6)
    
    # 2. Dice Coefficient (F1-score)
    dice = (2. * intersection + 1e-6) / (preds.sum() + masks.sum() + 1e-6)
    
    # 3. Pixel Accuracy
    correct_pixels = (preds == masks).sum()
    total_pixels = masks.numel()
    pixel_acc = correct_pixels / total_pixels
    
    return {
        'iou': iou.item(),
        'dice': dice.item(),
        'pixel_acc': pixel_acc.item()
    }

if __name__ == '__main__':
    # Test thử hàm tính toán metrics
    print("Test Thành viên 5 - Metrics")
    dummy_pred = torch.rand((2, 1, 256, 256))
    dummy_mask = torch.randint(0, 2, (2, 1, 256, 256)).float()
    metrics = calculate_metrics(dummy_pred, dummy_mask)
    print(metrics)
