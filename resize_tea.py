from PIL import Image
import os

# รูปที่ต้องการปรับขนาด
images_to_resize = [
    r"e:\AI Detection\Coffee\images\ชานม\thai-tea.png",
    r"e:\AI Detection\Coffee\images\ชานม\green-tea.png"
]

for img_path in images_to_resize:
    if not os.path.exists(img_path):
        print(f"ไม่พบไฟล์: {img_path}")
        continue
    
    # เปิดรูปภาพ
    img = Image.open(img_path)
    
    # ขนาดปัจจุบัน
    original_width, original_height = img.size
    print(f"ไฟล์: {os.path.basename(img_path)}")
    print(f"  ขนาดเดิม: {original_width}x{original_height}")
    
    # ขยายขนาดขึ้น 40% (คูณด้วย 1.40)
    new_width = int(original_width * 1.40)
    new_height = int(original_height * 1.40)
    
    # Resize โดยใช้ LANCZOS เพื่อคุณภาพที่ดี
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    print(f"  ขนาดใหม่: {new_width}x{new_height}")
    
    # บันทึกทับไฟล์เดิม
    resized_img.save(img_path, optimize=True)
    print(f"  ✓ บันทึกสำเร็จ")

print("\nเสร็จสิ้น!")
