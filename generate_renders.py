import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Output directories
os.makedirs("mockups", exist_ok=True)
artifact_dir = "/Users/artemmovsisan/.gemini/antigravity/brain/0ff9e980-285e-4a2d-850e-f1a3c94f5eea"
os.makedirs(artifact_dir, exist_ok=True)

# System Fonts (macOS verified)
SERIF_BODONI = "/System/Library/Fonts/Supplemental/Bodoni 72.ttc"
SERIF_GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SANS_REG = "/System/Library/Fonts/HelveticaNeue.ttc"
SANS_MED = "/System/Library/Fonts/HelveticaNeue.ttc"
SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# Strict Brand Palette (#F3EBE7 exact studio sample from new photo, #080808, #FFFFFF, #DDD8D3, #E5E0DB)
BG_IVORY = (243, 235, 231)        # #F3EBE7
COLOR_BLACK = (8, 8, 8)           # #080808
COLOR_WHITE = (255, 255, 255)     # #FFFFFF
COLOR_SUBTITLE = (23, 23, 23)     # #171717
COLOR_BORDER = (221, 216, 211)    # #DDD8D3
COLOR_BORDER_BTN = (229, 224, 219)# #E5E0DB

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow_ne(draw, cx, cy, size=6, color=(255, 255, 255), width=2):
    """Draws an elegant diagonal north-east arrow inside the circular badge."""
    # Diagonal line from bottom-left to top-right
    x0, y0 = cx - size + 1, cy + size - 1
    x1, y1 = cx + size - 1, cy - size + 1
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    # Arrow heads: horizontal left and vertical down from top-right tip
    draw.line([(x1, y1), (x1 - size + 1, y1)], fill=color, width=width)
    draw.line([(x1, y1), (x1, y1 + size - 1)], fill=color, width=width)

def render_desktop_exact(output_filename):
    W, H = 1440, 810  # 16:9 exact ratio of reference
    canvas = Image.new("RGBA", (W, H), BG_IVORY + (255,))
    
    # 1. Right Side: Group Girls Visual (Large & impressive: height 88% of viewport, 100% visible, no clipping)
    grp_orig = Image.open("assets/group-girls-hero.png").convert("RGBA")
    
    scale = (H * 0.88) / grp_orig.height
    new_w = int(grp_orig.width * scale)
    new_h = int(grp_orig.height * scale)
    grp_scaled = grp_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Position: right bottom (bottom of blazers at bottom of screen, right girl at right edge)
    paste_x = W - new_w
    paste_y = H - new_h
    
    canvas.alpha_composite(grp_scaled, (paste_x, paste_y))

    # 2. Main Drawing Context
    draw = ImageDraw.Draw(canvas)

    # ---------------- ШАПКА САЙТА (HEADER) ----------------
    # Left padding: 80px, Height: 100px
    header_h = 100
    
    # Logo: Horizontal Helen Akopova Makeup Academy (Refined width 170px)
    logo = Image.open("assets/logo-horizontal-transparent.png").convert("RGBA")
    logo_w = 170
    logo_h = int(logo.height * (logo_w / logo.width))
    logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    
    logo_x = 80
    logo_y = (header_h - logo_h) // 2
    canvas.alpha_composite(logo_resized, (logo_x, logo_y))

    # Center Nav Capsule: 580px wide, 52px high
    # Items: Главная (активна), Услуги, Работы, Отзывы, Контакты
    nav_w = 570
    nav_h = 52
    nav_x = (W - nav_w) // 2
    nav_y = (header_h - nav_h) // 2
    
    # Draw translucent white pill with border
    draw_rounded_rect(draw, [nav_x, nav_y, nav_x + nav_w, nav_y + nav_h], radius=26, fill=(255, 255, 255, 175), outline=COLOR_BORDER, width=1)
    
    # Active pill for "Главная"
    act_w = 98
    act_h = 40
    act_x = nav_x + 6
    act_y = nav_y + 6
    draw_rounded_rect(draw, [act_x, act_y, act_x + act_w, act_y + act_h], radius=20, fill=COLOR_WHITE, outline=None)
    
    try:
        f_nav = ImageFont.truetype(SANS_MED, 14, index=1)
        f_nav_act = ImageFont.truetype(SANS_MED, 14, index=1)
    except:
        f_nav = ImageFont.truetype(SANS_REG, 14)
        f_nav_act = ImageFont.truetype(SANS_BOLD, 14)
        
    draw.text((act_x + 18, act_y + 11), "Главная", font=f_nav_act, fill=COLOR_BLACK)
    
    # Navigation items strictly per prompt: Услуги, Работы, Отзывы, Контакты
    items = [
        ("Услуги", nav_x + 128),
        ("Работы", nav_x + 236),
        ("Отзывы", nav_x + 342),
        ("Контакты", nav_x + 452)
    ]
    for text, ix in items:
        draw.text((ix, nav_y + 17), text, font=f_nav, fill=COLOR_BLACK)

    # Header CTA Button: Аккуратная и низкая (высота 42px, ширина 132px)
    btn_w = 132
    btn_h = 42
    btn_x = W - 80 - btn_w
    btn_y = (header_h - btn_h) // 2
    draw_rounded_rect(draw, [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=21, fill=COLOR_WHITE, outline=COLOR_BORDER_BTN, width=1)
    draw.text((btn_x + 24, btn_y + 12), "Записаться", font=f_nav, fill=COLOR_BLACK)

    # ---------------- HERO LEFT SECTION ----------------
    content_x = 80
    y_cursor = 250

    # Headline in 2 lines: normal, balanced, editorial (~66px)
    try:
        f_headline = ImageFont.truetype(SERIF_BODONI, 66, index=0)
    except:
        f_headline = ImageFont.truetype(SERIF_GEORGIA, 64)

    draw.text((content_x, y_cursor), "Макияж —", font=f_headline, fill=COLOR_BLACK)
    y_cursor += 74
    draw.text((content_x, y_cursor), "это искусство", font=f_headline, fill=COLOR_BLACK)
    
    # Subtitle: Manrope Regular (~19px)
    y_cursor += 98
    try:
        f_sub = ImageFont.truetype(SANS_REG, 19)
    except:
        f_sub = ImageFont.truetype(SANS_REG, 18)
    draw.text((content_x, y_cursor), "Академия макияжа и красоты Helen Akopova", font=f_sub, fill=COLOR_SUBTITLE)

    # ---------------- HERO CTA GROUP: ДВЕ КНОПКИ (Фото 6 и 7) ----------------
    # 1. Кнопка «Записаться» с черным круглым значком со стрелкой
    # 2. Кнопка «Смотреть работы →» справа
    y_cursor += 46
    hero_btn_w = 210
    hero_btn_h = 60
    draw_rounded_rect(draw, [content_x, y_cursor, content_x + hero_btn_w, y_cursor + hero_btn_h], radius=30, fill=COLOR_WHITE, outline=COLOR_BORDER, width=1)
    
    try:
        f_btn_hero = ImageFont.truetype(SANS_MED, 17, index=1)
    except:
        f_btn_hero = ImageFont.truetype(SANS_BOLD, 17)
        
    draw.text((content_x + 30, y_cursor + 18), "Записаться", font=f_btn_hero, fill=COLOR_BLACK)
    
    # Circular black badge with white arrow inside primary button
    circle_r = 21
    circle_cx = content_x + hero_btn_w - 9 - circle_r
    circle_cy = y_cursor + (hero_btn_h // 2)
    draw.ellipse([circle_cx - circle_r, circle_cy - circle_r, circle_cx + circle_r, circle_cy + circle_r], fill=COLOR_BLACK)
    draw_arrow_ne(draw, circle_cx, circle_cy, size=5, color=COLOR_WHITE, width=2)

    # 2. Secondary Button: «Смотреть работы →» (как на фото 7)
    sec_x = content_x + hero_btn_w + 32
    draw.text((sec_x, y_cursor + 18), "Смотреть работы", font=f_btn_hero, fill=COLOR_BLACK)
    
    # Arrow text or symbol
    arrow_x = sec_x + 160
    draw.text((arrow_x, y_cursor + 16), "→", font=f_btn_hero, fill=COLOR_BLACK)

    # (Примечание: блок адреса полностью удален по требованию Фото 3)

    # ---------------- BOTTOM RIGHT INFO BLOCK OVER DARK CLOTHES ----------------
    info_x = W - 75 - 190
    info_y = H - 50 - 90
    
    f_info_title = ImageFont.truetype(SANS_BOLD, 13)
    draw.text((info_x, info_y), "HELEN AKOPOVA", font=f_info_title, fill=COLOR_WHITE)
    
    f_info_sub = ImageFont.truetype(SANS_REG, 10)
    draw.text((info_x, info_y + 18), "MAKEUP ACADEMY", font=f_info_sub, fill=(255, 255, 255, 220))
    
    draw.line([(info_x, info_y + 36), (info_x + 180, info_y + 36)], fill=(255, 255, 255, 120), width=1)
    
    f_info_tag = ImageFont.truetype(SANS_REG, 13)
    draw.text((info_x, info_y + 46), "Искусство макияжа", font=f_info_tag, fill=COLOR_WHITE)
    draw.text((info_x, info_y + 64), "и внимание к деталям", font=f_info_tag, fill=COLOR_WHITE)

    # Save output
    final_rgb = canvas.convert("RGB")
    final_rgb.save(output_filename, quality=96)
    print(f"Rendered: {output_filename}")
    
    # Save copy to artifact dir
    artifact_copy = os.path.join(artifact_dir, os.path.basename(output_filename))
    final_rgb.save(artifact_copy, quality=96)
    print(f"Copied to artifact: {artifact_copy}")

def render_mobile_exact(output_filename):
    W, H = 390, 844
    canvas = Image.new("RGBA", (W, H), BG_IVORY + (255,))
    draw = ImageDraw.Draw(canvas)

    # Mobile Header
    draw.line([(0, 74), (W, 74)], fill=COLOR_BORDER + (80,), width=1)
    
    # Logo
    logo = Image.open("assets/logo-horizontal-transparent.png").convert("RGBA")
    logo_w = 130
    logo_h = int(logo.height * (logo_w / logo.width))
    logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(logo_resized, (20, 20))
    
    # Hamburger
    ham_x = W - 20 - 42
    ham_y = 16
    draw_rounded_rect(draw, [ham_x, ham_y, ham_x + 42, ham_y + 42], radius=21, fill=COLOR_WHITE, outline=COLOR_BORDER, width=1)
    draw.line([(ham_x + 13, ham_y + 17), (ham_x + 29, ham_y + 17)], fill=COLOR_BLACK, width=2)
    draw.line([(ham_x + 13, ham_y + 25), (ham_x + 29, ham_y + 25)], fill=COLOR_BLACK, width=2)

    # Mobile Typography
    y = 96
    try:
        f_title_m = ImageFont.truetype(SERIF_BODONI, 48, index=0)
    except:
        f_title_m = ImageFont.truetype(SERIF_GEORGIA, 44)
        
    draw.text((22, y), "Макияж —", font=f_title_m, fill=COLOR_BLACK)
    y += 50
    draw.text((22, y), "это искусство", font=f_title_m, fill=COLOR_BLACK)
    
    y += 62
    try:
        f_sub_m = ImageFont.truetype(SANS_REG, 15)
    except:
        f_sub_m = ImageFont.truetype(SANS_REG, 14)
    draw.text((22, y), "Академия макияжа и красоты Helen Akopova", font=f_sub_m, fill=COLOR_SUBTITLE)

    # Group Photo on Mobile (lower section)
    grp_orig = Image.open("assets/group-girls-hero.png").convert("RGB")
    m_w, m_h = W - 44, 340
    scale = max(m_w / grp_orig.width, m_h / grp_orig.height) * 1.05
    new_w = int(grp_orig.width * scale)
    new_h = int(grp_orig.height * scale)
    grp_scaled = grp_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
    crop_x = new_w - m_w  # Focus on models
    grp_cropped = grp_scaled.crop((crop_x, 0, crop_x + m_w, m_h))
    
    # Soft rounded corners
    m_mask = Image.new("L", (m_w, m_h), 255)
    m_draw = ImageDraw.Draw(m_mask)
    m_draw.rounded_rectangle([0, 0, m_w, m_h], radius=16, fill=255)
    grp_cropped.putalpha(m_mask)
    
    y_photo = 265
    canvas.alpha_composite(grp_cropped, (22, y_photo))

    # Badge overlay inside mobile photo
    draw_rounded_rect(draw, [32, y_photo + m_h - 60, W - 32, y_photo + m_h - 12], radius=10, fill=(8, 8, 8, 160))
    f_badge_m = ImageFont.truetype(SANS_REG, 11)
    draw.text((46, y_photo + m_h - 44), "HELEN AKOPOVA • Искусство макияжа и детали", font=f_badge_m, fill=COLOR_WHITE)

    # Mobile Button Group (Пункт 6 ТЗ)
    y_btn = y_photo + m_h + 24
    draw_rounded_rect(draw, [22, y_btn, W - 22, y_btn + 56], radius=28, fill=COLOR_WHITE, outline=COLOR_BORDER, width=1)
    try:
        f_btn_m = ImageFont.truetype(SANS_MED, 16, index=1)
    except:
        f_btn_m = ImageFont.truetype(SANS_BOLD, 16)
        
    draw.text((60, y_btn + 18), "Записаться", font=f_btn_m, fill=COLOR_BLACK)
    
    # Circle arrow on mobile button
    m_cir_r = 18
    m_cir_cx = W - 22 - 10 - m_cir_r
    m_cir_cy = y_btn + 28
    draw.ellipse([m_cir_cx - m_cir_r, m_cir_cy - m_cir_r, m_cir_cx + m_cir_r, m_cir_cy + m_cir_r], fill=COLOR_BLACK)
    draw_arrow_ne(draw, m_cir_cx, m_cir_cy, size=4, color=COLOR_WHITE, width=2)

    # Secondary action link below on mobile
    y_sec = y_btn + 70
    draw.text((120, y_sec), "Смотреть работы →", font=f_btn_m, fill=COLOR_BLACK)

    final_rgb = canvas.convert("RGB")
    final_rgb.save(output_filename, quality=96)
    print(f"Rendered: {output_filename}")
    
    artifact_copy = os.path.join(artifact_dir, os.path.basename(output_filename))
    final_rgb.save(artifact_copy, quality=96)
    print(f"Copied to artifact: {artifact_copy}")

if __name__ == "__main__":
    # Render desktop 1440x810 matching exact reference
    render_desktop_exact("mockups/helen-akopova-hero-exact.png")
    
    # Render mobile 390x844
    render_mobile_exact("mockups/helen-akopova-mobile-exact.png")
