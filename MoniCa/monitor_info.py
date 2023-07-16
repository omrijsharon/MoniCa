import win32con
import win32gui
import win32process
import mss
import mss.tools
import numpy as np


def isRealWindow(hWnd):
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False


def getWindowSizes():
    '''
    Return a list of dict for each real window within the screen boundaries.
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        rect = list(win32gui.GetWindowRect(hWnd))
        name = win32gui.GetWindowText(hWnd)
        ctid, cpid = win32process.GetWindowThreadProcessId(hWnd)
        w, h = rect[2] - rect[0], rect[3] - rect[1]
        if all([r >= 0 for r in rect]):
            windows.append({"name": name, "hWnd":hWnd, "pid": cpid, "rect": rect, "width": w, "height": h})
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows


def get_window_names():
    windows = getWindowSizes()
    return [w["name"] for w in windows]


def get_window_of_interest(window_name):
    windows = getWindowSizes()
    # extract the window of interest using list comprehension
    win_info = [w for w in windows if window_name.lower() in w['name'].lower()]
    assert len(win_info) > 0, "No window found with name: {}".format(window_name)
    return win_info[0]

def get_window_monitor(window_name, monitor_number=0, is_fullscreen=False):
    window_info = get_window_of_interest(window_name)
    # compression = 6
    if not is_fullscreen:
        window_info["rect"][0] += 8
        window_info["rect"][1] += 31
        window_info["rect"][2] -= 8
        window_info["rect"][3] -= 8
        w, h = window_info["rect"][2] - window_info["rect"][0], window_info["rect"][3] - window_info["rect"][1]
        window_info["width"] = w
        window_info["height"] = h
    monitor = {
        "top": window_info["rect"][1],
        "left": window_info["rect"][0],
        "width": window_info["width"],
        "height": window_info["height"],
        "mon": monitor_number,
    }
    return monitor

def set_foreground_window(window_name):
    window_info = get_window_of_interest(window_name)
    hwnd = window_info["hWnd"]
    # Restore window if minimized. Do it again if the window is stubborn
    # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


if __name__ == '__main__':
    windows = getWindowSizes()
    # extract the window of interest using list comprehension
    win_name = 'google chrome'
    win_info = get_window_monitor(win_name)
    set_foreground_window(win_name)
    print(win_info)