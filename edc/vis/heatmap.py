import cv2
import numpy as np
from matplotlib import cm


__all__ = ['draw_heatmap']


def draw_heatmap(img, score, colormap="jet", alpha=0.5, score_thr=-1):
    h, w, _ = img.shape
    score = cv2.resize(score, (w, h), interpolation=cv2.INTER_CUBIC)
    score = (score - np.min(score)) / (np.max(score) - np.min(score))
    mask = score > score_thr
    heatmap = (255 * cm.get_cmap(colormap)(score ** 2)[:, :, :3]).astype(np.uint8)

    heatmap_img = np.where(mask[:, :, None], alpha * img[:, :, ::-1] + (1 - alpha) * heatmap, img[:, :, ::-1]).astype(np.uint8)
    heatmap_img = cv2.cvtColor(heatmap_img, cv2.COLOR_RGB2BGR)
    return heatmap_img
