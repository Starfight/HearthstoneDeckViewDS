
from PIL import Image, ImageDraw, ImageFilter

from db.font import FONT_TITLE

async def place_rank_in_image(account: str, rank: str, chart: Image) -> Image:
    """Place the name and rank in the image"""
    temp = Image.open(f"backs/rank.png")
    image = Image.new("RGBA", temp.size, (0, 0, 0, 0))
    image.paste(temp, (0, 0))

    # Print blur
    blurred = Image.new('RGBA', temp.size)
    draw = ImageDraw.ImageDraw(blurred)
    # Compute rank size
    _, _, w, h = draw.textbbox((0, 0), rank, font=FONT_TITLE)
    draw.text((400, 80), account, font=FONT_TITLE, fill=(0, 0, 0))
    draw.text((190-w/2, 80), rank, font=FONT_TITLE, fill=(0, 0, 0))
    blurred = blurred.filter(ImageFilter.BoxBlur(7))
    image.paste(blurred,blurred)

    # Print text
    draw = ImageDraw.ImageDraw(image)
    draw.text((400, 80), account, font=FONT_TITLE, fill=(255, 255, 255))
    draw.text((190-w/2, 80), rank, font=FONT_TITLE, fill=(255, 255, 255))

    # Print chart
    image.paste(chart, (190, 200), chart)

    return image
