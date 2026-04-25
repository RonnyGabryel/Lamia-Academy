# bibliotecas
import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)  # abre a webcam

while True:
    _, frame = cap.read()  # lê a imagem da câmera
    if frame is None: break  # para se a câmera falhar

    roi = frame[100:400, 100:400]  # define a área
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)  # desenha o quadrado na tela

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    low_skin  = np.array([0,  20,  70],  dtype=np.uint8)  # tom de pele minimo
    high_skin = np.array([20, 255, 255], dtype=np.uint8)  # tom de pele maximo
    mask = cv2.inRange(hsv, low_skin, high_skin)  # Cria mascara

    kernel = np.ones((3, 3), np.uint8)  # Define o tamanho
    mask = cv2.dilate(mask, kernel, iterations=4)  # Engrossa o branco
    mask = cv2.erode(mask,  kernel, iterations=2)   # Afina o branco

    # Encontra as bordas do desenho branco
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    dedos = 0  # Contador

    if contours:
        maior = max(contours, key=cv2.contourArea)  # Pega o maior contorno

        if cv2.contourArea(maior) > 5000:  # processa o objeto for grande o suficiente
            hull = cv2.convexHull(maior, returnPoints=False)  # cria um contorno
            cv2.drawContours(roi, [cv2.convexHull(maior)], -1, (255, 0, 0), 2)  # desenha a casca

            defects = cv2.convexityDefects(maior, hull)  # cha os vãos entre a mão e a casca

            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]  # pega pontos início fim e fundo do vão

                    inicio = tuple(maior[s][0])
                    fim    = tuple(maior[e][0])
                    fundo  = tuple(maior[f][0])

                    # calcula os lados do triângulo formado pelo vão
                    a = math.dist(inicio, fim)
                    b = math.dist(fundo,  inicio)
                    c = math.dist(fundo,  fim)

                    # lei dos Cossenos para achar o ângulo do vão entre os dedos
                    angulo = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c + 1e-6)))

                    if angulo < 90:  # se o ângulo for fechado é um espaço entre dedos
                        dedos += 1
                        cv2.circle(roi, fundo, 5, (0, 0, 255), -1)  # marca o ponto do vao

                dedos += 1  # Soma

    # escreve o resultado na tela
    cv2.putText(frame, f'Dedos: {dedos}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow('Contador de Dedos', frame)  # mostra a imagem original
    cv2.imshow('Mascara', mask)  # mostra a imagem em preto e branco

    if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()