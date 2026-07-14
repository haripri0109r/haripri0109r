from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "projects"
OUT.mkdir(parents=True, exist_ok=True)

CARDS = [
    ("focustube.png", "FocusTube", "Deep focus productivity platform for creators", (76, 201, 255)),
    ("coursefinder.png", "Course Finder", "AI-curated learning paths and recommendations", (142, 136, 255)),
    ("assetflow.png", "AssetFlow", "Digital asset orchestration and analytics", (80, 227, 194)),
    ("researchassistant.png", "Smart Research Assistant", "RAG + citation engine for reliable answers", (182, 140, 255)),
    ("onlinebookstore.png", "Online Bookstore", "Scalable e-commerce storefront and fulfillment", (114, 197, 255)),
    ("mentormentee.png", "Mentor Mentee Allocation", "Automated matching with fairness scoring", (159, 164, 255)),
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
    img = Image.new("RGB", (width, height), (8, 11, 28))
    px = img.load()

    top = (8, 12, 30)
    bottom = (30, 18, 60)

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
        draw.line((x, 0, x, height), fill=(36, 60, 110), width=1)
    for y in range(0, height, 40):
        draw.line((0, y, width, y), fill=(36, 60, 110), width=1)

    glow1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g1 = ImageDraw.Draw(glow1)
    g1.ellipse((-120, -100, 560, 420), fill=(*accent, 80))
    g1.ellipse((860, 340, 1420, 760), fill=(*accent, 62))
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

    draw.text((86, 150), title, fill=(240, 246, 255), font=title_font)
    draw.text((90, 255), subtitle, fill=(210, 222, 247), font=sub_font)

    panel = (90, 335, 540, 400)
    draw.rounded_rectangle(panel, radius=12, fill=(*accent, 70), outline=(*accent, 230), width=2)
    draw.text((112, 353), "Production Portfolio Build", fill=(246, 250, 255), font=tag_font)

    draw.text((90, 625), "github.com/haripri0109r", fill=(187, 203, 236), font=meta_font)

    img.save(OUT / filename, "PNG", optimize=True)


for card in CARDS:
    make_card(*card)

print("Generated", len(CARDS), "project cards in", OUT)
