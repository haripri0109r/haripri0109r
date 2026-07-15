from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "projects"
OUT.mkdir(parents=True, exist_ok=True)

CARDS = [
    ("focustube.png", "FocusTube", "Deep focus productivity platform for creators", (193, 18, 31)),
    ("coursefinder.png", "Course Finder", "AI-curated learning paths and recommendations", (155, 17, 30)),
    ("assetflow.png", "AssetFlow", "Digital asset orchestration and analytics", (208, 208, 208)),
    ("researchassistant.png", "Smart Research Assistant", "RAG + citation engine for reliable answers", (245, 245, 245)),
    ("ecertificate.png", "E-Certificate", "Secure digital certificates with QR verification", (193, 18, 31)),
    ("onlinebookstore.png", "Online Bookstore", "Scalable e-commerce storefront and fulfillment", (170, 170, 170)),
    ("mentormentee.png", "Mentor Mentee Allocation", "Automated matching with fairness scoring", (155, 17, 30)),
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates += [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
    candidates += [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def build_background(width: int, height: int, accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (width, height), (13, 13, 13))
    px = img.load()

    top = (13, 13, 13)
    bottom = (26, 26, 26)

    for y in range(height):
        t = y / max(height - 1, 1)
        row = (
            lerp(top[0], bottom[0], t),
            lerp(top[1], bottom[1], t),
            lerp(top[2], bottom[2], t),
        )
        for x in range(width):
            px[x, y] = row

    draw = ImageDraw.Draw(img)

    for x in range(0, width, 40):
        draw.line((x, 0, x, height), fill=(52, 22, 22), width=1)
    for y in range(0, height, 40):
        draw.line((0, y, width, y), fill=(52, 22, 22), width=1)

    glow1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g1 = ImageDraw.Draw(glow1)
    g1.ellipse((-120, -100, 560, 420), fill=(*accent, 88))
    g1.ellipse((860, 340, 1420, 760), fill=(208, 208, 208, 42))
    img = Image.alpha_composite(img.convert("RGBA"), glow1).convert("RGB")

    return img


def make_card(filename: str, title: str, subtitle: str, accent: tuple[int, int, int]) -> None:
    width, height = 1280, 720
    img = build_background(width, height, accent)
    draw = ImageDraw.Draw(img)

    title_font = load_font(64, bold=True)
    sub_font = load_font(30)
    tag_font = load_font(23, bold=True)
    meta_font = load_font(24)

    draw.text((86, 150), title, fill=(245, 245, 245), font=title_font)
    draw.text((90, 255), subtitle, fill=(208, 208, 208), font=sub_font)

    panel = (90, 335, 540, 400)
    draw.rounded_rectangle(panel, radius=12, fill=(*accent, 78), outline=(*accent, 235), width=2)
    draw.text((112, 353), "Production Portfolio Build", fill=(245, 245, 245), font=tag_font)

    draw.text((90, 625), "github.com/haripri0109r", fill=(170, 170, 170), font=meta_font)

    img.save(OUT / filename, "PNG", optimize=True)


for card in CARDS:
    make_card(*card)

print("Generated", len(CARDS), "project cards in", OUT)
