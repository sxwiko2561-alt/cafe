from PIL import Image
import shutil
import os

# กำหนดไฟล์ต้นทางและปลายทาง
replacements = [
    {
        "source": r"e:\AI Detection\Coffee\อเมริกาโน่1.png",
        "target": r"e:\AI Detection\Coffee\images\กาแฟ\americano-cold.png",
        "name": "อเมริกาโน่เย็น"
    },
    {
        "source": r"e:\AI Detection\Coffee\ชาเขียวสตอ1.png",
        "target": r"e:\AI Detection\Coffee\images\ชานม\green-tea-strawberry.png",
        "name": "ชาเขียวสตอเบอรี่"
    }
]

# ขนาดมาตรฐานที่ต้องการ (อ้างอิงจากรูปอื่นๆ)
TARGET_SIZE = (526, 700)  # ประมาณขนาดเฉลี่ยของรูปอื่นๆ

for item in replacements:
    source = item["source"]
    target = item["target"]
    name = item["name"]
    
    if not os.path.exists(source):
        print(f"❌ ไม่พบไฟล์: {source}")
        continue
    
    print(f"\n📷 {name}")
    
    # เปิดรูปต้นฉบับ
    img = Image.open(source)
    original_size = img.size
    print(f"  ขนาดต้นฉบับ: {original_size[0]}x{original_size[1]}")
    
    # คำนวณอัตราส่วนการ resize
    width_ratio = TARGET_SIZE[0] / original_size[0]
    height_ratio = TARGET_SIZE[1] / original_size[1]
    ratio = min(width_ratio, height_ratio) * 1.18  # ขยายเล็กน้อยเหมือนรูปชา
    
    new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
    
    # Resize
    resized = img.resize(new_size, Image.Resampling.LANCZOS)
    print(f"  Resize เป็น: {new_size[0]}x{new_size[1]}")
    
    # Crop ส่วนกลางให้ได้ขนาดพอดี
    if new_size[0] > TARGET_SIZE[0] or new_size[1] > TARGET_SIZE[1]:
        left = (new_size[0] - TARGET_SIZE[0]) // 2
        top = (new_size[1] - TARGET_SIZE[1]) // 2
        right = left + TARGET_SIZE[0]
        bottom = top + TARGET_SIZE[1]
        
        final = resized.crop((left, top, right, bottom))
        print(f"  Crop เป็น: {TARGET_SIZE[0]}x{TARGET_SIZE[1]}")
    else:
        # ถ้าเล็กกว่า ก็ใช้ขนาดที่ resize แล้ว
        final = resized
    
    # บันทึกทับไฟล์เดิม
    final.save(target, optimize=True)
    print(f"  ✅ บันทึกแทนที่: {os.path.basename(target)}")

print("\n🎉 เสร็จสิ้นทั้งหมด!")
