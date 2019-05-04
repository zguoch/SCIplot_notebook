from colored import fg, bg, attr
from console_progressbar import ProgressBar
C_GREEN = fg('green')
C_RED = fg('red')
C_BLUE = fg('blue')
C_DEFAULT = attr('reset')


def init(total, title='Progress', decimals=3, length=50, fill='#', zfill='-'):
    pb = ProgressBar(total=total, prefix=C_BLUE+title+': '+C_DEFAULT, suffix=' Completed' +
                     C_DEFAULT, decimals=decimals, length=length, fill=C_GREEN+fill, zfill=C_DEFAULT+zfill)
    return pb


def update(pb, i):
    pb.print_progress_bar(i+1)
