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
    chart = plt.figure(figsize=(15, 7))
    ax = chart.add_subplot(111)
    ax.plot(dates, ranks, 'o', markersize=10, linestyle='-', color=CHART_DATA_COLOR, linewidth=4)

    # Configure axes
    ax.set_xlabel('Jour', fontdict={'fontsize': 20, 'color': CHART_BORDER_COLOR})
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    ax.tick_params(axis='x', labelsize=16, colors=CHART_BORDER_COLOR)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.set_ylabel('Classement', fontdict={'fontsize': 20, 'color': CHART_BORDER_COLOR})
    ax.tick_params(axis='y', labelsize=16, colors=CHART_BORDER_COLOR)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))
    ax.invert_yaxis()

    # Configure background
    ax.set_facecolor("none")
    ax.set_alpha(0)
    # set thick of all sides of the figure framework
    for spine in ax.spines.values():
        spine.set_linewidth(4)
        spine.set_color(CHART_BORDER_COLOR)
    ax.set_title('Évolution du classement', fontdict={'fontsize': 24, 'color': CHART_BORDER_COLOR, 'fontweight': 'bold'})

    # Draw canvas
    chart.patch.set_alpha(0)
    chart.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = chart.canvas.get_width_height()
    buf = np.fromstring(chart.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)
    # Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis = 2)

    # Export to image
    return Image.frombytes('RGBA', chart.canvas.get_width_height(), buf) 