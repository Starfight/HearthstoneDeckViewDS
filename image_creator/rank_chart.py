from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image

CHART_DATA_COLOR = '#FF9100'
CHART_BORDER_COLOR = '#7E5933'

async def get_rank_chart(data: list) -> Image:
    # Format data
    dates = [row[0] for row in data]
    ranks = [row[1] for row in data]

    # Create chart
    plt.plot(dates, ranks, 'o', markersize=10, linestyle='-', color=CHART_DATA_COLOR, linewidth=4)

    # Configure style
    plt.xlabel('Jour', fontdict={'fontsize': 20, 'color': CHART_BORDER_COLOR})
    date_formatter = mdates.DateFormatter('%d')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().tick_params(axis='x', labelsize=16, colors=CHART_BORDER_COLOR)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.ylabel('Classement', fontdict={'fontsize': 20, 'color': CHART_BORDER_COLOR})
    plt.gca().tick_params(axis='y', labelsize=16, colors=CHART_BORDER_COLOR)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))
    plt.gca().invert_yaxis()
    plt.gca().set_facecolor("none")
    plt.gca().set_alpha(0)
    # set thick of all sides of the figure framework
    for spine in plt.gca().spines.values():
        spine.set_linewidth(4)
        spine.set_color(CHART_BORDER_COLOR)
    plt.title('Évolution du classement', fontdict={'fontsize': 24, 'color': CHART_BORDER_COLOR, 'fontweight': 'bold'})

    # Draw canvas
    plt.gcf().set_size_inches(15, 7)
    plt.gcf().patch.set_alpha(0)
    plt.gcf().canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = plt.gcf().canvas.get_width_height()
    buf = np.fromstring(plt.gcf().canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)
    # Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis = 2)

    # Export to image
    return Image.frombytes('RGBA', plt.gcf().canvas.get_width_height(), buf) 