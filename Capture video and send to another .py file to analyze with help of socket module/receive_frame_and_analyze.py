import socket
import cv2
import pickle
import struct
from fer import FER
import time

time_emotion = 0

"""
The analysis of this function prevents the frame flow. 
Our main goal is to make an analysis without stopping this flow and to ensure that different features can continue.
"""


def detect_emotion(frame):
    global time_emotion

    zaman = time.time()

    print(zaman-time_emotion)

    if zaman-time_emotion > 15: # set to analyze every 15 seconds
        detector = FER(mtcnn=True)
        result = detector.detect_emotions(frame)

        emotions = result[0]["emotions"]

        print(emotions)

        time_emotion = time.time()

        return result


HOST = ''
PORT = 1881

socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

socket_object.bind((HOST, PORT))
print('Socket bind complete')


socket_object.listen(10)
print('Socket now listening')

conn, address = socket_object.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))



while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    # receive image row data form client socket
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]

    msg_size = struct.unpack(">L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]

    data = data[msg_size:]

    # unpack image using pickle
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    try:
        result = detect_emotion(frame)
        print(result)

    except:
        pass

    cv2.imshow('Frame_analyze', frame)
    cv2.waitKey(1)
