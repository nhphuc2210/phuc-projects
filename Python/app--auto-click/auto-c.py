import random
import win32api, win32con
import time
import win32com.client as comclt

def click(x,y):

    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

x = 0

# while (x < 500):
while True:
    a, b = win32api.GetCursorPos()
    click(a, b)
    print('clicked')
    x = x + 1
    
    time.sleep(0.5 + 1.5*random.random())
s