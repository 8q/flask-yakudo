import numpy as np
import cv2


def convert_img(file_data):
    nparr = np.fromstring(file_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR).astype(np.float32)
    del nparr
    height, width, _ = img.shape
    center_x, center_y = height/2, width/2
    blur, iterations = 0.0085, 20

    map_x1 = np.fromfunction(
        lambda x, y: x + (x - center_x) * blur, (height, width),
        dtype=np.float32)
    map_y1 = np.fromfunction(
        lambda x, y: y + (y - center_y) * blur, (height, width),
        dtype=np.float32)
    map_x2 = np.fromfunction(
        lambda x, y: x - (x - center_x) * blur, (height, width),
        dtype=np.float32)
    map_y2 = np.fromfunction(
        lambda x, y: y - (y - center_y) * blur, (height, width),
        dtype=np.float32)

    for i in range(iterations):
        enlarged = cv2.remap(img, map_y1, map_x1, cv2.INTER_LINEAR)
        shrinked = cv2.remap(img, map_y2, map_x2, cv2.INTER_LINEAR)
        img = cv2.addWeighted(enlarged, 0.5, shrinked, 0.5, 0, img)
        del enlarged
        del shrinked

    # _, buf = cv2.imencode('.png', img[15:height-15, 15:width-15])
    _, buf = cv2.imencode('.png', img)
    del img
    return buf.tobytes()
