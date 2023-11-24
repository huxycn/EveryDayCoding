import functools

import cv2

import numpy as np

FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX

THICKNESS = 1
LINE_TYPE = cv2.LINE_AA


def valid_pts(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        img = args[0]
        pts = args[1]
        h, w, _ = img.shape

        if isinstance(pts, tuple) or isinstance(pts, list):
            pts = np.around(np.array(pts)).astype(np.int32)
        elif isinstance(pts, np.ndarray):
            if not np.issubdtype(pts.dtype, np.integer):
                pts = np.around(pts).astype(np.int32)
        else:
            raise TypeError(f'not supported coords type: {type(pts)}')
        
        pts[::2] = np.clip(pts[::2], 0, w)
        pts[1::2] = np.clip(pts[1::2], 0, h)
        
        args = list(args)
        args[1] = pts
        args = tuple(args)
        return func(*args, **kwargs)
    return wrapper


def get_text_size_and_offset(text, height):
    """ opencv text

               left_top ___________
            putText.org|_abcdefghi_| text_size[1]  \ height
                       |___________| baseline      /
                        text_size[0]
                           width
    """

    fontScale = cv2.getFontScaleFromHeight(FONT_FACE, height, THICKNESS)
    text_size, baseline = cv2.getTextSize(text, FONT_FACE, fontScale, THICKNESS)

    # assert text_size[1] == height

    width = text_size[0]
    height = text_size[1] if text.isnumeric() else text_size[1] + baseline
    offset = text_size[1]
    return width, height, offset, fontScale


def put_text(img, pt, height, text, color, pt_type='left_top'):
    h, w, _ = img.shape

    tw, th, to, fontScale = get_text_size_and_offset(text, height)
    # assert height == th, f'{height}, {th}'

    if pt_type == 'left_top':
        x0, y0 = pt
    elif pt_type == 'center':
        x0, y0 = pt[0]-tw//2, pt[1]-th//2
    else:
        raise ValueError(f'Not support pt_type: {pt_type}')

    cv2.putText(img, text, (x0, y0 + to-1), FONT_FACE, fontScale, color, THICKNESS, LINE_TYPE)
    return x0 + tw, y0 + th


@valid_pts
def rect(img, pts, color):
    x0, y0, x1, y1 = pts
    cv2.rectangle(img, (x0, y0), (x1, y1), color, THICKNESS, LINE_TYPE)


@valid_pts
def filled_rect(img, pts, color, alpha):
    x0, y0, x1, y1 = pts
    w, h = x1 - x0, y1 - y0

    region = np.zeros((h, w, 3), np.uint8)
    cv2.rectangle(region, (0, 0), (w, h), color, thickness=-1)
    img[y0:y1, x0:x1] = cv2.addWeighted(img[y0:y1, x0:x1], 1-alpha, region, alpha, 0)

@valid_pts
def filled_rect_with_text(img, pt, height, text, color, alpha):
    x0, y0  = pt
    tw, th, to, fontScale = get_text_size_and_offset(text, height)
    x1, y1 = x0 + tw, y0 + th
    text_color = (0, 0, 0) if sum(color) > 128 * 3 else (255, 255, 255)
    filled_rect(img, (x0, y0, x1, y1), color, alpha)
    put_text(img, pt, height, text, text_color)


@valid_pts
def circle(img, pt, radius, color, thickness):
    x0, y0 = pt
    r = int(radius)
    cv2.circle(img, (x0, y0), radius, color, thickness, LINE_TYPE)
    

@valid_pts
def filled_circle(img, pt, radius, color, alpha):
    x0, y0 = pt
    r = int(radius)
    region = np.ones((2*r, 2*r, 3), np.uint8)
    cv2.circle(region, (r, r), r, color, -1)
    img[y0-r:y0+r, x0-r:x0+r] = np.where(region==1, img[y0-r:y0+r, x0-r:x0+r], cv2.addWeighted(img[y0-r:y0+r, x0-r:x0+r], 1-alpha, region, alpha, 0))


@valid_pts
def filled_circle_with_text(img, pt, radius, text, color, alpha):
    x0, y0  = pt
    radius = int(radius)
    text_radius = radius - 1
    # tw, th, to, fontScale = get_text_size_and_offset(text, 2*radius)
    # x1, y1 = x0 + tw, y0 + th
    text_color = (0, 0, 0) if sum(color) > 128 * 3 else (255, 255, 255)
    filled_circle(img, pt, radius, color, alpha)
    put_text(img, (x0-text_radius, y0-text_radius), 2*text_radius, text, text_color)
