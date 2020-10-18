import PIL.ImageFont
import PIL.ImageDraw
import PIL.Image
import unidecode
from pathlib import Path
import io

BASE_DIR = Path(__file__).resolve().parent

subsample_scale = 3
font_1 = PIL.ImageFont.truetype(str(BASE_DIR / "fonts" / "PlayfairDisplay-BoldItalic.ttf"), 40 * subsample_scale)
font_2 = PIL.ImageFont.truetype(str(BASE_DIR / "fonts" / "ChopinScript.otf"), 90 * subsample_scale)
font_3 = PIL.ImageFont.truetype(str(BASE_DIR / "fonts" / "PlayfairDisplay-Regular.ttf"), 30 * subsample_scale)


def draw_centered(x: int, y: int, draw: PIL.ImageDraw.ImageDraw, font: PIL.ImageFont.ImageFont, text: str):
    w, h = font.getsize(text)
    draw.text((x - (w / 2), y - (h / 2)), text, fill="black", font=font)


def draw_cert(title: str, artist: str, role: str):
    base_img = PIL.Image.open(BASE_DIR / "base.png")
    img = PIL.Image.new("RGBA", (base_img.width * subsample_scale, base_img.height * subsample_scale), (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(img)

    artist = unidecode.unidecode(artist)
    title = unidecode.unidecode(title)
    role = unidecode.unidecode(role)

    img_centre = img.width // 2
    draw_centered(img_centre, 245 * subsample_scale, draw, font_1, "On behalf of Neko Desu awarded to")
    draw_centered(img_centre, 380 * subsample_scale, draw, font_2, artist)
    draw_centered(img_centre, 465 * subsample_scale, draw, font_1, title)
    draw_centered(img_centre, 520 * subsample_scale, draw, font_3, role)

    img_resized = img.resize((base_img.width, base_img.height), PIL.Image.ANTIALIAS)
    base_img.alpha_composite(img_resized)

    img_b = io.BytesIO()
    base_img.save(img_b, format='PNG')
    img_b.seek(0)
    return img_b.getvalue()
