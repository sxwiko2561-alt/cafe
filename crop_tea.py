from PIL import Image
import os

# รูปที่ต้องการ crop
images_to_crop = [
    r"e:\AI Detection\Coffee\images\ชานม\thai-tea.png",
    r"e:\AI Detection\Coffee\images\ชานม\green-tea.png"
]

for img_path in images_to_crop:
    if not os.path.exists(img_path):
        print(f"ไม่พบไฟล์: {img_path}")
        continue
    
    # เปิดรูปภาพ
    img = Image.open(img_path)
    
    # ขนาดปัจจุบัน
    width, height = img.size
    print(f"ไฟล์: {os.path.basename(img_path)}")
    print(f"  ขนาดเดิม: {width}x{height}")
    
    # คำนวณ crop box เพื่อซูมเข้าไปในภาพ (เอาส่วนกลางออกมา 85%)
    crop_factor = 0.85  # เอา 85% ของภาพ (ซูมเข้า ~1.18x)
    
    new_width = int(width * crop_factor)
    new_height = int(height * crop_factor)
    
    # หา center
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height
    
    # Crop
    cropped = img.crop((left, top, right, bottom))
    
    # Resize กลับไปเป็นขนาดเดิมเพื่อให้ดูใหญ่ขึ้น
    final = cropped.resize((width, height), Image.Resampling.LANCZOS)
    
    print(f"  Crop: {new_width}x{new_height} -> Resize: {width}x{height}")
    
    # บันทึกทับไฟล์เดิม
    final.save(img_path, optimize=True)
    print(f"  ✓ บันทึกสำเร็จ (ซูมเข้า {int((1/crop_factor)*100)}%)")

print("\nเสร็จสิ้น!")
