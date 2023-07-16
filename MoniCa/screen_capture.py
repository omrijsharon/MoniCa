import numpy as np
import mss
import multiprocessing
from multiprocessing import shared_memory
import time

from monitor_info import get_window_monitor, set_foreground_window

YOUTUBE_TLWH_SMALL = (160, 2019, 1280, 720)
YOUTUBE_TLWH_LARGE = (80, 1921, 1901, 1135)


class ScreenCaptureBaseMP:
    def __init__(self):
        self.stop_event = multiprocessing.Event()
        self.process = None
        self.monitor = None
        self.sct = None

        # Create a shared memory block that fits a typical image from sct.grab()
        example_image = np.zeros((1080, 1920, 4), dtype=np.uint8)
        self.shared_memory = shared_memory.SharedMemory(create=True, size=example_image.nbytes)
        self.shared_image = np.ndarray(example_image.shape, dtype=example_image.dtype, buffer=self.shared_memory.buf)

        self.is_new_frame_event = multiprocessing.Event()

    def start(self):
        self.process = multiprocessing.Process(target=self.capture_loop)
        self.process.start()

    def stop(self):
        self.stop_event.set()
        self.process.join()

    def capture(self):
        img_byte = self.sct.grab(self.monitor)
        img = np.array(img_byte)
        np.copyto(self.shared_image, img)  # Copy the image data into the shared memory block
        self.is_new_frame_event.set()

    def get_frame(self):
        self.is_new_frame_event.clear()
        return np.copy(self.shared_image)  # Create a copy of the shared image to work with

    def get_is_new_frame(self):
        return self.is_new_frame_event.is_set()

    def capture_loop(self):
        self.sct = mss.mss()
        while not self.stop_event.is_set():
            self.capture()
        self.sct.close()

    def close(self):
        self.stop()
        self.shared_memory.close()
        self.shared_memory.unlink()  # Remove the shared memory block when we're done with it


class ScreenCaptureBase:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = None

    def read(self):
        img_byte = self.sct.grab(self.monitor)
        return True, np.array(img_byte) # ret, frame - maintain compatibility with cv2.VideoCapture

    def release(self):
        self.sct.close()


class ScreenCaptureWindow(ScreenCaptureBase):
    def __init__(self, win_name, is_full_screen=False, monitor_number=1):
        super().__init__()
        self.monitor = get_window_monitor(win_name, monitor_number=monitor_number, is_fullscreen=is_full_screen)
        set_foreground_window(win_name)


class ScreenCaptureYoutube(ScreenCaptureBase):
    def __init__(self, tlwh=YOUTUBE_TLWH_SMALL, monitor_number=1):
        super().__init__()
        mon = self.sct.monitors[monitor_number]
        win_name = "google chrome"
        set_foreground_window(win_name)

        self.monitor = {
            "top": mon["top"] + tlwh[0],
            "left": mon["left"] + tlwh[1],
            "width": tlwh[2],
            "height": tlwh[3],
            "mon": monitor_number,
        }


if __name__ == '__main__':
    N = 50
    cap = ScreenCaptureWindow("uncrashed")
    # cap.start()
    t0 = time.time()
    for i in range(N):
        _, img = cap.read()
    print(N/(time.time() - t0)) # measured more tha 185 fps for a 1080p screen on my machine
    cap.release()