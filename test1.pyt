import cv2
import numpy as np
import pandas as pd

# Открываем видео файл
video = cv2.VideoCapture('video1.mp4')

# Создаем пустой массив для хранения времени начала движений
motion_times = []

# Инициализируем переменную для хранения предыдущего кадра
prev_frame = None

# Читаем видео покадрово
while video.isOpened():
    # Захватываем кадр из видео
    ret, frame = video.read()

    if not ret:
        break

    # Преобразуем кадр в черно-белый формат
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Если это первый кадр, запоминаем его и переходим к следующему
    if prev_frame is None:
        prev_frame = gray_frame
        continue

    # Вычисляем разницу между текущим и предыдущим кадром
    frame_diff = cv2.absdiff(prev_frame, gray_frame)

    # Применяем пороговую фильтрацию для выделения движения
    _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # Выполняем операцию морфологического закрытия для устранения шумов
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # Вычисляем контуры объектов на кадре
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Если найдены контуры, добавляем время начала движения в массив
    if len(contours) > 0:
        motion_times.append(video.get(cv2.CAP_PROP_POS_MSEC))

    # Запоминаем текущий кадр как предыдущий для следующей итерации
    prev_frame = gray_frame

# Закрываем видео файл
video.release()

# массив, где время будет в секундах, минутах, часах
array_time_video = []

for i in range(len(motion_times)):
    for j in range(1):
        time = '0:' + str(int(motion_times[i]))
        if 60 * 60 > motion_times[i] >= 60:
            time = str(int(motion_times[i] // 60)) + ':' + str(int(motion_times[i]%60))
        elif 60 * 60 <= motion_times[i]:
            time = str(int(motion_times[i] // (60*60))) + ':' + str(int(int((motion_times[i]%(60 * 60)) // 60))) + ':' + str(int((motion_times[i]%(60*60))%60))
        array_time_video.append(time)
# Создаем таблицу Excel и записываем массив в нее
df = pd.DataFrame({'Time (ms)': array_time_video})
df.to_excel('motion_times.xlsx', index=False)
