import cv2, time, requests, json
import numpy as np
camera = cv2.VideoCapture(0)
last_time = time.time()
current_time = time.time()

data = []

for i in range(50):

    requests.get(f"http://pi-tree:5000/calibrate/{i}")
    current_time = time.time()
    
    time.sleep(0.05)
    # success, frame = camera.read()
    # if not success:
    #     print("error getting frame")
    #     break
    # print(frame.shape)
    # new_frame = np.mean(frame, axis=2)
    # flat_idx = np.argmax(new_frame) 

    # # 2. Convert to (row, col) coordinates
    # row, col = np.unravel_index(flat_idx, new_frame.shape)
    # print(f"Brightest pixel: ({row}, {col})")
    # data.append((row, col))
    # # for y in frame.shape[0]:
    # #     for x in frame.shape[1]:
    # #         print(frame[y][x])
    # last_time = current_time
    # cv2.imshow("hello", frame)

# with open("calibration.json", "w") as f:
#     json.dump(data, f)