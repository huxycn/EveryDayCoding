import cv2

from .path_utils import valid_path
from .video import VideoWriter


__all__ = ['ImageFlow']


KEY_QUIT = 27     # Esc
KEY_PAUSE = 32    # Space
KEY_PREV = 81     # Left
KEY_NEXT = 83     # Right


class ImageFlow():
    def __init__(self, img_dir, wait_ms=100, save_path=None):
        self.img_dir = valid_path(img_dir)
        self.wait_ms = wait_ms
        if save_path is not None:
            self.save_path = valid_path(save_path, 'w')
        else:
            self.save_path = None
        self.img_paths = sorted(self.img_dir.iterdir())
        self.num_frames = len(self.img_paths)
        self.cached_frames = {}

        self.paused = False
        self.frame_idx = 0

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.save_path is not None:
            video_writer = VideoWriter(self.save_path)
            for frame_idx, frame in self.cached_frames.items():
                video_writer.write(frame)
            print(f'video saved as {self.save_path}')
        pass

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if not self.paused:
                # 非暂停状态下
                key = cv2.waitKey(self.wait_ms)

                if key == KEY_NEXT or key == -1:
                    self.frame_idx += 1
                elif key == KEY_QUIT:
                    break
                elif key == KEY_PAUSE:
                    self.paused = not self.paused
                    continue
                else:
                    pass

                if self.frame_idx == self.num_frames:
                    raise StopIteration
            else:
                # 暂停状态下
                key = cv2.waitKey()

                if key == KEY_PREV:
                    self.frame_idx -= 1
                elif key == KEY_NEXT:
                    self.frame_idx += 1
                elif key == KEY_QUIT:
                    raise StopIteration
                elif key == KEY_PAUSE:
                    self.paused = not self.paused
                    self.frame_idx += 1
                else:
                    pass

                self.frame_idx = self.num_frames - 1 if self.frame_idx < 0 else self.frame_idx
                self.frame_idx = 0 if self.frame_idx >= self.num_frames else self.frame_idx

            if self.frame_idx in self.cached_frames:
                img = self.cached_frames[self.frame_idx]
                cv2.imshow('', img)
                cv2.waitKey(1)
            else:
                return self.frame_idx, self.img_paths[self.frame_idx]

    def imshow(self, frame_idx, img):
        h, w, _ = img.shape
        
        # _cv2.getTextSize('F', constant.Color.Red, 1)
        # common.putText(img, (0, 0), f'Frame: {frame_idx}      Option: Space (Pause) | Esc (Quit) | Left (Prev) | Right (Next)')
        self.cached_frames[frame_idx] = img
        cv2.imshow('', img)
        cv2.waitKey(1)


