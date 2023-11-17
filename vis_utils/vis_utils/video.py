import cv2

from .path_utils import valid_path


class VideoWriter:
    def __init__(self, path, fps=8):
        self.path = valid_path(path, 'w')
        self.format = self.path.suffix
        if self.format == '.mp4':
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        elif self.format == '.avi':
            self.fourcc = cv2.VideoWriter_fourcc(*'XIVD')
        else:
            raise NameError(f'{self.path.as_posix()} is not a valid video save path')

        self.fps = fps

        self._writer = None

    def write(self, frame):
        if self._writer is None:
            h, w, _ = frame.shape
            self._writer = cv2.VideoWriter(self.path.as_posix(), self.fourcc, self.fps, (w, h))
        self._writer.write(frame)
