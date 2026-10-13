from PIL import Image
import os

# ไฟล์ที่ต้องการปรับ
img_path = r"e:\AI Detection\Coffee\อเมริกาโน่1.png"
target_path = r"e:\AI Detection\Coffee\images\กาแฟ\americano-cold.png"

if not os.path.exists(img_path):
    print(f"❌ ไม่พบไฟล์: {img_path}")
    exit()

print("📷 ปรับขนาดอเมริกาโน่เย็น")

# เปิดรูปต้นฉบับ
img = Image.open(img_path)
original_size = img.size
print(f"  ขนาดต้นฉบับ: {original_size[0]}x{original_size[1]}")

# ขนาดเป้าหมาย - ลดลงจากเดิม
TARGET_SIZE = (526, 700)

# ลด zoom factor ลงเหลือ 1.0 (ไม่ขยายเลย)
width_ratio = TARGET_SIZE[0] / original_size[0]
height_ratio = TARGET_SIZE[1] / original_size[1]
ratio = min(width_ratio, height_ratio) * 1.0  # ไม่ขยาย

new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))

# Resize
resized = img.resize(new_size, Image.Resampling.LANCZOS)
print(f"  Resize เป็น: {new_size[0]}x{new_size[1]}")

# ถ้า resize แล้วยังใหญ่กว่า ให้ crop
if new_size[0] > TARGET_SIZE[0] or new_size[1] > TARGET_SIZE[1]:
    left = (new_size[0] - TARGET_SIZE[0]) // 2
    top = (new_size[1] - TARGET_SIZE[1]) // 2
    right = left + TARGET_SIZE[0]
    bottom = top + TARGET_SIZE[1]
    
    final = resized.crop((left, top, right, bottom))
    print(f"  Crop เป็น: {TARGET_SIZE[0]}x{TARGET_SIZE[1]}")
else:
    # ถ้าเล็กกว่า สร้าง canvas ขาวแล้ววางรูปตรงกลาง
    canvas = Image.new('RGBA', TARGET_SIZE, (255, 255, 255, 0))
    paste_x = (TARGET_SIZE[0] - new_size[0]) // 2
    paste_y = (TARGET_SIZE[1] - new_size[1]) // 2
    canvas.paste(resized, (paste_x, paste_y), resized if resized.mode == 'RGBA' else None)
    final = canvas
    print(f"  วางรูปตรงกลาง canvas: {TARGET_SIZE[0]}x{TARGET_SIZE[1]}")

# บันทึก
final.save(target_path, optimize=True)
print(f"  ✅ บันทึกสำเร็จ: {os.path.basename(target_path)}")
