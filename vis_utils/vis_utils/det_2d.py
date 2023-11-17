from ._cv2 import valid_pts, rect, filled_rect_with_text, get_text_size_and_offset


# __all__ = ['draw_bbox2d', 'draw_point', 'put_text', 'draw_table']
__all__ = ['draw_bbox2d']


@valid_pts
def draw_bbox2d(img, coords, color, label='', pos='left-top'):
    rect(img, coords, color)

    if label:
        if pos == 'left-top':
            filled_rect_with_text(img, coords[:2], 10, label, color, 0.5)
            # _cv2._put_text(img, coords[:2], label, color=text_color.value, bg_alpha=0.5, bg_color=color)
        if pos == 'right-bottom':
            x1, y1 = coords[2:]
            tw, th, _, _ = get_text_size_and_offset(label, 10)
            tx, ty = x1 - tw, y1 - th
            filled_rect_with_text(img, (tx, ty), 10, label, color, 0.5)
            # _cv2._put_text(img, (tx, ty), label, color=text_color.value, bg_alpha=0.5, bg_color=color)


def draw_point(img, coord, color, label=''):
    h, w, _ = img.shape

    x0, y0 = coord

    text_color = Color.Black if sum(color) > 128 * 3 else Color.White

    if label:
        w, h, _ = _cv2._get_text_size_and_offset(label, *Font.S.value, 1)

        _cv2._put_text(img, (x0-w/2, y0-h/2), label, *Font.S.value, color=text_color.value, thickness=1, bg_alpha=0.5, bg_color=color, bg_shape='circle')
        # _put_text(img, (100, 100), '1', cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, bg_alpha=0.5, bg_color=(0, 0, 255), bg_shape='circle')
    else:
        _cv2._circle(img, coord, 3, color, thickness=0, bg_alpha=1)


def put_text(img, coord, text, font, color, thickness=1, bg_alpha=0, bg_color=None):
    _cv2._put_text(img, coord, text, *font.value, color.value, thickness, bg_alpha, bg_color.value)


def draw_table(img, table, start_pos, col_colors):
    h, w, _ = img.shape
    thickness = h // 1440 + 1
    fontScale = (h // 720 + 1) * 0.3

    _, text_h, _ = _cv2._get_text_size_and_offset('dummy', fontScale, thickness)

    cell_widths = [0] * len(table[0])
    for j, row in enumerate(table):
        for i, col in enumerate(row):
            text_width, _, _ = _cv2._get_text_size_and_offset(col, fontScale, thickness)
            cell_widths[i] = max(cell_widths[i], text_width)
    cell_widths = [w + 10 for w in cell_widths]

    for j, row in enumerate(table):
        for i, col in enumerate(row):
            tx = start_pos[0] + sum(cell_widths[:i])
            ty = start_pos[1] + j * text_h
            _cv2._put_text(img, (tx, ty), col, col_colors[i].value)

    return img
