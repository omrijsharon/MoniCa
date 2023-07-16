# MoniCa

MoniCa (MONItor CApturer) is a high-speed, user-friendly library designed for live screen capture. It leverages the power of mss, pypiwin32, and multiprocessing to offer seamless and efficient screen capture capabilities.

## Features

- Efficient Live Screen Capture: MoniCa uses a combination of MSS and multiprocessing to provide efficient and high-speed screen capture.
- Versatile: Capture the whole screen, a specific window, or a defined region of the screen.
- User-friendly: Easy-to-use API, start capturing screen with just a few lines of code.

## Installation

MoniCa can be installed via pip:
```
pip install MoniCa
```

## Usage

MoniCa is designed to maintain the same API as opencv-python VideoCapture.
Below is a simple example of how to use MoniCa:

```python
import time
from MoniCa import ScreenCaptureWindow

N = 100
cap = ScreenCaptureWindow("google chrome")
t0 = time.time()
for i in range(N):
    _, img = cap.read()
print(N/(time.time() - t0)) # measured FPS
cap.release()
```

## Development
MoniCa is open source and welcomes contributions. Please refer to our contribution guidelines before making a pull request.