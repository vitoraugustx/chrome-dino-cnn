# Importando as bibliotecas
import time
from PIL import Image
from mss import mss
import keyboard
import uuid
from pathlib import Path
import cv2
import numpy as np


# Caixa do printscreen
# [x, y, width, height]
x, y, w, h = 230, 350, 360, 360
bboxes = [np.array([x, y, w, h])]

frame = {"top":0, "left":0, "width":1920, "height":1080} # Caixa do print da tela inteira
roi_frame = {"top": y, "left": x, "width": w, "height": h} # Caixa da região de interesse

ss_manager = mss() # Gerenciador de printscreen 
count = 0 # Contador de imagens        
is_exit = False # Variável para encerrar o programa 

# Função para desenhar as caixas
def draw_bboxes(img, bboxes, color=(0, 0, 255), thickness=2):
    for bbox in bboxes:
        cv2.rectangle(img, tuple(bbox[:2]), tuple(bbox[:2]+bbox[-2:]), color, thickness)

# Função para tirar o printscreen
def take_screenshot(ss_id, key, path="./images/"):
    global count
    count += 1
    print(f"{key}: {count}")

    # Tira o print da região de interesse e da tela inteira
    roi = ss_manager.grab(roi_frame)
    img = ss_manager.grab(frame)

    # Converte o printscreen para imagem e salva
    image = Image.frombytes("RGB", roi.size, roi.rgb)
    image.save(path +f"{key}_{ss_id}_{count}.png")
    
    screen = np.asarray(img)

    # Converte de BGRA para BGR
    screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

    # Desenha as caixas
    draw_bboxes(screen, bboxes)

    # Redimensiona a imagem
    resized = cv2.resize(screen, (1366, 768))

    # Mosta a imagem
    cv2.imshow("OpenCV/Numpy normal", resized)
    cv2.waitKey()
    time.sleep(1.5)


# Função para encerrar o programa
def exit():
    global is_exit
    is_exit = True


# Main
def main():
    Path("./images/").mkdir(parents=True, exist_ok=True) # Cria o diretório de imagens se não existir
    Path("./images/up").mkdir(parents=True, exist_ok=True) # Cria o diretório "up" se não existir
    Path("./images/down").mkdir(parents=True, exist_ok=True) # Cria o diretório "down" se não existir
    Path("./images/none").mkdir(parents=True, exist_ok=True) # Cria o diretório "none" se não existir
    keyboard.add_hotkey("esc", exit)    # Chama a função exit() ao apertar esc
    ss_id = uuid.uuid4()                # Gera um id único para o printscreen

    while True: # Loop principal
        if is_exit == True: 
            break

        try:
            # Se a tecla 'up' for pressionada, chama a função para tirar print com o parâmetro "up"
            if keyboard.is_pressed(keyboard.KEY_UP):        
                take_screenshot(ss_id, "up", path="./images/up/")
                time.sleep(0.01)

            # Se a tecla 'down' for pressionada, chama a função para tirar print com o parâmetro "down"
            elif keyboard.is_pressed(keyboard.KEY_DOWN):    
                take_screenshot(ss_id, "down", path="./images/down/")
                time.sleep(0.01)

            # Se a tecla 'right' for pressionada, chama a função para tirar print com o parâmetro "none"
            elif keyboard.is_pressed("right"):              
                take_screenshot(ss_id, "right", path="./images/none/")
                time.sleep(0.01)
        except RuntimeError: 
            continue

main()