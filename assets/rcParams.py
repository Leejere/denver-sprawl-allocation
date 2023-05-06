import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cycler
from matplotlib.ticker import FuncFormatter

import colors

plt.style.use("seaborn-whitegrid")

mpl.rcParams["figure.titlesize"] = 12

mpl.rcParams["axes.titlesize"] = 10
mpl.rcParams["axes.labelsize"] = 9.2
# mpl.rcParams['axes.labelcolor'] = "gray"

mpl.rcParams["axes.linewidth"] = 1.5
mpl.rcParams["axes.spines.top"] = False
mpl.rcParams["axes.spines.right"] = False
mpl.rcParams["axes.spines.left"] = False

mpl.rcParams["grid.linestyle"] = ":"
mpl.rcParams["grid.linewidth"] = 0.4
mpl.rcParams["grid.color"] = "gray"

mpl.rcParams["xtick.labelcolor"] = "gray"
mpl.rcParams["xtick.labelsize"] = 8
mpl.rcParams["ytick.labelcolor"] = "gray"
mpl.rcParams["ytick.labelsize"] = 8

mpl.rcParams["lines.linewidth"] = 0.6

mpl.rcParams["axes.prop_cycle"] = cycler(
    color=[
        colors.palette_hero,
        colors.palette_primary,
        colors.palette_hero_faded,
        colors.palette_water,
    ]
)
mpl.rcParams["figure.subplot.hspace"] = 0.3
mpl.rcParams["figure.subplot.wspace"] = 0.1

mpl.rcParams["legend.fontsize"] = 8.5
mpl.rcParams["legend.title_fontsize"] = 10
mpl.rcParams["legend.labelcolor"] = "gray"
mpl.rcParams["legend.frameon"] = True
mpl.rcParams["legend.framealpha"] = 0.4


def thousands(x, pos):
    return "{:1.0f}K".format(x * 1e-3)


def millions(x, pos):
    return "{:1.1f}M".format(x * 1e-6)


formatter_thousands = FuncFormatter(thousands)  # Number formatting for tick labels
formatter_millions = FuncFormatter(millions)
