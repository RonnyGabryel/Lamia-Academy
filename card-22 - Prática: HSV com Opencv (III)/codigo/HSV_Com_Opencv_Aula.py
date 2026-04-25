import cv2  # Importa a biblioteca de visão computacional
import numpy as np  # Importa a biblioteca para lidar com calculos

cap = cv2.VideoCapture(0)  # Liga a sua webcam

while True:  # Cria um loop infinito para os frames da camera um por um
    _, frame = cap.read()  # Captura a imagem atual da camera
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Converte a cor da imagem

    low_red = np.array([161, 155, 84])  # Define o tom de vermelho mais escuro
    high_red = np.array([179, 255, 255])  # Define o tom de vermelho mais claro
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)  # Cria uma máscara preta e branca onde só o que é vermelho fica branco
    red = cv2.bitwise_and(frame, frame, mask=red_mask)  # Recorta o vermelho da imagem original usando a máscara

    # Blue color range in HSV
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)  # Cria a máscara para detectar azul
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)  # Recorta apenas o que for azul na imagem

    # Green color range in HSV
    low_green = np.array([35, 50, 50])
    high_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)  # Cria a máscara para detectar verde
    green = cv2.bitwise_and(frame, frame, mask=green_mask)  # Recorta apenas o que for verde na imagem

    # Every color except white
    low = np.array([0, 42, 0])  # Define o mínimo de cor
    high = np.array([179, 255, 255])  # Define o máximo de todas as cores
    mask = cv2.inRange(hsv_frame, low, high)  # Cria a máscara que ignora tons
    result = cv2.bitwise_and(frame, frame, mask=mask)  # Gera o resultado final

    cv2.imshow("Frame", frame)  # Abre uma janela mostrando a imagem
    cv2.imshow("Red mask", mask)  # Abre uma janela mostrando a máscara

    key = cv2.waitKey(1)
    if key == 27:  # Se a tecla pressionada for ESC sai do loop
        break

cap.release()  # Desliga a câmera para que outros apps possam usar
cv2.destroyAllWindows()