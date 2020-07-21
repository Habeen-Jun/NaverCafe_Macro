## 기존에 쓰던 pyperclip 모듈은 image 호환 안됨..
## PIL (Python Image Library)
from PIL import ImageGrab

img = ImageGrab.grabclipboard()
# or ImageGrab.grab() to grab the whole screen!

print(img.show())
