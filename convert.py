import numpy as np
import cv2
from yakudo_error import YakudoError
import random


def convert_img(file_data):
    nparr = np.fromstring(file_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR).astype(np.float32)
    del nparr
    height, width, _ = img.shape
    if width > 1000 or height > 1000:
        raise YakudoError("File size must be under 1000x1000.")
    center_x, center_y = height/2, width/2
    # blur, iterations = 0.0085, 20
    iterations = 20

    def blur():
        return random.uniform(0.005, 0.010)

    map_x1 = np.fromfunction(
        lambda x, y: np.vectorize(lambda x: np.float32(max(min(x + (x - center_x) * blur(), height-1), 0)))(x),
        (height, width), dtype=np.float32)
    map_y1 = np.fromfunction(
        lambda x, y: np.vectorize(lambda y: np.float32(max(min(y + (y - center_y) * blur(), width-1), 0)))(y),
        (height, width), dtype=np.float32)
    map_x2 = np.fromfunction(
        lambda x, y: np.vectorize(lambda x: np.float32(max(min(x - (x - center_x) * blur(), height-1), 0)))(x),
        (height, width), dtype=np.float32)
    map_y2 = np.fromfunction(
        lambda x, y: np.vectorize(lambda y: np.float32(max(min(y - (y - center_y) * blur(), width-1), 0)))(y),
        (height, width), dtype=np.float32)

    for i in range(iterations):
        enlarged = cv2.remap(img, map_y1, map_x1, cv2.INTER_LINEAR)
        shrinked = cv2.remap(img, map_y2, map_x2, cv2.INTER_LINEAR)
        img = cv2.addWeighted(enlarged, 0.5, shrinked, 0.5, 0, img)

    _, buf = cv2.imencode('.jpg', img)
    return buf.tobytes()
