# Importando as bibliotecas
import time
from PIL import Image
from mss import mss
import keyboard
import numpy as np
from keras.models import model_from_json

# PC 2 deixar left =330, PC 1 deixar left = 230
frame = {"top":350, "left":330, "width":360, "height":360} # Caixa do printscreen
ss_manager = mss()  # Gerenciador de printscreen
is_exit = False # Variável para encerrar o programa  

width = 100 # Largura da imagem     
height = 100 # Altura da imagem    


# Função para ir para abaixar
def down():
    keyboard.release(keyboard.KEY_UP)
    keyboard.press(keyboard.KEY_DOWN)


# Função para pular
def up():
    keyboard.release(keyboard.KEY_DOWN)
    keyboard.press(keyboard.KEY_UP)

# Função para soltar as teclas
def none():
    keyboard.release(keyboard.KEY_DOWN)
    keyboard.release(keyboard.KEY_UP)

# A function for stopping the program
def exit():
    global is_exit
    is_exit = True

# Main
def main():
    keyboard.add_hotkey("esc", exit) # Encerra o programa ao apertar esc

    # Carrega o modelo treinado
    model = model_from_json(open("model.json","r").read())
    model.load_weights("weights.h5")

    while True:
        if is_exit == True:
            keyboard.release(keyboard.KEY_DOWN)
            keyboard.release(keyboard.KEY_UP)
            break

        # Tira o print da região configurada
        screenshot = ss_manager.grab(frame)

        # Converte o printscreen para imagem
        image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Converte a imagem para escala de cinza
        grey_image = image.convert("L")        

        # Redimensiona a imagem               
        a_img = np.array(grey_image.resize((width, height))) 

        # Normaliza a imagem
        img = a_img / 255                                     
            
        # Adiciona uma dimensão para a imagem
        X = np.array([img])                                 
        X = X.reshape(X.shape[0], width, height, 1) 

        # Faz a predição 
        prediction = model.predict(X)                       
        
        # Pega o maior valor da predição
        result = np.argmax(prediction)     
 
        # Abaixa
        if result == 0:  
            down()
            print("down")

        # Pula
        elif result == 2:  
            up()
            print("up")

        # Solta as teclas
        elif result == 1:
            none()
            print("none")
        
        # Tempo de espera para não sobrecarregar o processador
        time.sleep(0.000000000001)

main()