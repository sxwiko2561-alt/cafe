from PIL import Image
import os

# ไฟล์ที่ต้องการปรับ
img_path = r"e:\AI Detection\Coffee\ชาเขียวสตอ1.png"
target_path = r"e:\AI Detection\Coffee\images\ชานม\green-tea-strawberry.png"

if not os.path.exists(img_path):
    print(f"❌ ไม่พบไฟล์: {img_path}")
    exit()

print("📷 ปรับขนาดชาเขียวสตอเบอรี่")

# เปิดรูปต้นฉบับ
img = Image.open(img_path)
original_size = img.size
print(f"  ขนาดต้นฉบับ: {original_size[0]}x{original_size[1]}")

# ขนาดเป้าหมายมาตรฐาน
TARGET_SIZE = (526, 700)

# ไม่ขยายเลย ใช้ขนาดจริง (zoom 0.95x เพื่อให้เล็กลงนิดหน่อย)
width_ratio = TARGET_SIZE[0] / original_size[0]
height_ratio = TARGET_SIZE[1] / original_size[1]
ratio = min(width_ratio, height_ratio) * 0.95  # ลดลงเล็กน้อย

new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))

# Resize
resized = img.resize(new_size, Image.Resampling.LANCZOS)
print(f"  Resize เป็น: {new_size[0]}x{new_size[1]}")

# สร้าง canvas โปร่งใสแล้ววางรูปตรงกลาง
canvas = Image.new('RGBA', TARGET_SIZE, (255, 255, 255, 0))
paste_x = (TARGET_SIZE[0] - new_size[0]) // 2
paste_y = (TARGET_SIZE[1] - new_size[1]) // 2
canvas.paste(resized, (paste_x, paste_y), resized if resized.mode == 'RGBA' else None)

print(f"  วางรูปตรงกลาง canvas: {TARGET_SIZE[0]}x{TARGET_SIZE[1]}")

# บันทึก
canvas.save(target_path, optimize=True)
print(f"  ✅ บันทึกสำเร็จ: {os.path.basename(target_path)}")
