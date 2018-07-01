import numpy as np
import cv2


def convert_img(file_data):
    nparr = np.fromstring(file_data, np.uint8)
    orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR).astype(np.float32)
    height, width, _ = orig.shape
    center_x, center_y = height/2, width/2
    blur, iterations = 0.007, 25

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

    dst = np.copy(orig)
    for i in range(iterations):
        enlarged = cv2.remap(dst, map_y1, map_x1, cv2.INTER_LINEAR)
        shrinked = cv2.remap(dst, map_y2, map_x2, cv2.INTER_LINEAR)
        dst = cv2.addWeighted(enlarged, 0.5, shrinked, 0.5, 0, dst)

    _, buf = cv2.imencode('.png', dst[15:height-15, 15:width-15])
    return buf.tobytes()
