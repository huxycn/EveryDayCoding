import numpy as np

from matplotlib import cm
from addict import Dict


class DictNoDefault(Dict):
    def __missing__(self, key):
        raise KeyError(f"Key '{key}' not found in {list(self.keys())}.")


__all__ = ['SimpleNamedColormap', 'SimpleIndexedColormap']


def paired_colormap():
    # reference: https://www.matplotlib.org.cn/tutorials/colors/colormaps.html#miscellaneous
    _paired_colors = [[int(v * 255) for v in color][::-1] for color in cm.get_cmap('Paired').colors]
    return DictNoDefault({
        'none': [-1, -1, -1],
        'black': [0, 0, 0],
        'white': [255, 255, 255],
        'blue': _paired_colors[0],
        'BLUE': _paired_colors[1],
        'green': _paired_colors[2],
        'GREEN': _paired_colors[3],
        'red': _paired_colors[4],
        'RED': _paired_colors[5],
        'yellow': _paired_colors[6],
        'YELLOW': _paired_colors[7],
        'purple': _paired_colors[8],
        'PURPLE': _paired_colors[9],
        'brown': _paired_colors[10],
        'BROWN': _paired_colors[11]
    })


SimpleNamedColormap = paired_colormap()


def voc_colormap(N=256):
    def bit_get(val, idx):
        return (val & (1 << idx)) != 0

    ret = np.zeros((N, 3), dtype=np.uint8)
    for i in range(N):
        r = g = b = 0
        c = i
        for j in range(8):
            r |= (bit_get(c, 0) << 7 - j)
            g |= (bit_get(c, 1) << 7 - j)
            b |= (bit_get(c, 2) << 7 - j)
            c >>= 3
        ret[i, :] = [r, g, b]
    return ret.tolist()


SimpleIndexedColormap = voc_colormap()

