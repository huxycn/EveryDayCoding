import numpy as np

from addict import Dict
from skimage.io import imshow

from matplotlib import cm, pyplot as plt

from _cv2 import put_text

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


def simple_indexed_colormap_vis(labels, row_size=50, col_size=500):
    num_labels = len(labels)
    cmap = np.array(SimpleIndexedColormap)
    # colors = [f'{tuple(color)}' for color in cmap[:num_labels]]
    array = np.empty((row_size*(num_labels), col_size, cmap.shape[1]), dtype=cmap.dtype)
    for i in range(num_labels):
        array[i*row_size:i*row_size+row_size, :] = cmap[i]

        text = str(tuple(cmap[i]))
        text_color = (0, 0, 0) if sum(cmap[i]) > 128 * 3 else (255, 255, 255)

        put_text(array, (250, 50*i+25), 25, text, text_color, pt_type='center')

    fig = plt.figure()
    imshow(array)
    plt.yticks([row_size*i+row_size/2 for i in range(num_labels)], labels)
    plt.xticks([])

    def fig2data(fig):
        """
        fig = plt.figure()
        image = fig2data(fig)
        @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
        @param fig a matplotlib figure
        @return a numpy 3D array of RGBA values
        """
        import PIL.Image as Image
        # draw the renderer
        fig.canvas.draw()

        # Get the RGBA buffer from the figure
        w, h = fig.canvas.get_width_height()
        buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
        buf.shape = (w, h, 4)

        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        buf = np.roll(buf, 3, axis=2)
        image = Image.frombytes("RGBA", (w, h), buf.tobytes())
        image = np.asarray(image)
        return image

    return fig2data(fig)
