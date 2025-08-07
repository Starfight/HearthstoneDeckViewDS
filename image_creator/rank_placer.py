import statistics
from PIL import Image, ImageDraw, ImageFilter

from db.font import FONT_TITLE, FONT_DETAILS
from image_creator.rank_chart import get_rank_chart

async def place_rank_in_image(account: str, data: list) -> Image:
    """Place the name and rank in the image"""
    rank = str(max(data, key=lambda x: x[0])[1])
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

    # Print title
    draw = ImageDraw.ImageDraw(image)
    draw.text((400, 80), account, font=FONT_TITLE, fill=(255, 255, 255))
    draw.text((190-w/2, 80), rank, font=FONT_TITLE, fill=(255, 255, 255))

    # print details
    ranks = [row[1] for row in data]
    draw.text((350, 950), f"Meilleur classement: {min(ranks)}", font=FONT_DETAILS, fill=(126, 89, 51))
    draw.text((350, 1050), f"Pire classement: {max(ranks)}", font=FONT_DETAILS, fill=(126, 89, 51))
    draw.text((1050, 950), f"Classement moyen: {int(sum(ranks) / len(ranks))}", font=FONT_DETAILS, fill=(126, 89, 51))
    draw.text((1050, 1050), f"Classement median: {int(statistics.median(ranks))}", font=FONT_DETAILS, fill=(126, 89, 51))

    # Print chart
    chart = await get_rank_chart(data)
    image.paste(chart, (190, 200), chart)

    return image
