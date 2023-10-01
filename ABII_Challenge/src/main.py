from djitellopy import Tello
from utils import cartesian_to_polar
import time

class ControleTello:
    def __init__(self, altura):
        self.tello = Tello()
        self.tello.connect()
        self.tello.takeoff()
        time.sleep(1)
        self.tello.move_up(altura)
        self.x, self.y, self.yaw = 0, 0, 0
    def missao_1(self):
        lista_coordenadas = []
        lista_coordenadas.append(((3, 0), 0))
        lista_coordenadas.append(((0, -3), 90))
        lista_coordenadas.append(((-2, 3), 180))
        return lista_coordenadas
    def missao_2(self):
        lista_coordenadas = []
        lista_coordenadas.append(((2, 0), 0))
        lista_coordenadas.append(((0, 2), 0))
        lista_coordenadas.append(((3, 0), 90))
        lista_coordenadas.append(((1, 0), 0))
        lista_coordenadas.append(((0, 1), 90))
        lista_coordenadas.append(((0, 1), 0))
        lista_coordenadas.append(((-1, 0), 90))
        lista_coordenadas.append(((-2, 0), 90))
        return lista_coordenadas
    
    def executar_missao(self, lista_coordenadas):
        for i in range(len(lista_coordenadas)):
            x_novo, y_novo = lista_coordenadas[i][0]
            self.x += x_novo
            self.y += y_novo
            self.yaw = lista_coordenadas[i][1]
            print(self.x, self.y, self.yaw)
            modulo, angulo = cartesian_to_polar(lista_coordenadas[i][0])
            print(angulo)
            print(modulo)
            if self.tello:
                time.sleep(1)
                self.tello.rotate_clockwise(angulo)
                time.sleep(1)
                self.tello.move_forward(modulo)
                time.sleep(1)
                self.tello.rotate_clockwise(lista_coordenadas[i][1])

        if self.tello:
            self.tello.land()

if __name__ == "__main__":
    altura_de_voo = 185
    controle_tello = ControleTello(altura_de_voo)
    
    missao = controle_tello.missao_1()  # ou missao_1()
    
    controle_tello.executar_missao(missao)




'''

from djitellopy import Tello
from utils import cartesian_to_polar
import time
import keyboard

def run_tello(altura):
    tello = Tello()
    tello.connect()
    tello.takeoff()
    time.sleep(1)
    tello.move_up(altura)
    return tello
def missao_1():
    lista_coordenadas = []
    lista_coordenadas.append(((2, 0), 0))
    lista_coordenadas.append(((0, -2), 90))
    lista_coordenadas.append(((-2, 2), 180))
    return lista_coordenadas
def missao_2():
    lista_coordenadas = []
    lista_coordenadas.append(((2, 0), 0))
    lista_coordenadas.append(((0, 2), 0))
    lista_coordenadas.append(((3, 0), 90))
    lista_coordenadas.append(((1, 0), 0))
    lista_coordenadas.append(((0, 1), 90))
    lista_coordenadas.append(((0, 1), 0))
    lista_coordenadas.append(((-1, 0), 90))
    lista_coordenadas.append(((-2, 0), 90))
    return lista_coordenadas

def main():
    x ,y, yaw = (0 , 0 , 0)
    ultima_orientacao = 0
    #tello = False #run_tello(170)
    tello = run_tello(170)
    lista_coordenadas = missao_2()
    for i in range(len(lista_coordenadas)):
        x_novo,y_novo = lista_coordenadas[i][0]
        x+= x_novo
        y+= y_novo
        yaw = lista_coordenadas[i][1]
        print(x,y,yaw)
        modulo, angulo = cartesian_to_polar(lista_coordenadas[i][0])
        print(angulo)
        print(modulo)
        if tello:
            time.sleep(1)
            tello.rotate_clockwise(angulo)
            time.sleep(1)
            tello.move_forward(modulo)
            time.sleep(1)
            tello.rotate_clockwise(lista_coordenadas[i][1])
    if tello:
        tello.land()

main()



'''
'''
altura_inicial = 0  # Defina a altura inicial como desejado
velocidade_inicial = 0  # Defina a velocidade inicial como desejar
tello.takeoff()
while True:
    try:
        aceleracao_vertical = tello.get_height()
        tempo = 1  # Defina o intervalo de tempo em segundos

        # Calcule a altura usando a fórmula
        altura = 0.5 * aceleracao_vertical * tempo**2 + velocidade_inicial * tempo + altura_inicial

        # Atualize a velocidade inicial e a altura inicial para a próxima iteração
        velocidade_inicial = aceleracao_vertical
        altura_inicial = altura

        # Imprima a altura atual
        print(f"Altura atual do drone: {altura} cm")

        # Aguarde um curto período de tempo antes da próxima medição
        time.sleep(tempo)
        tello.land()
    except KeyboardInterrupt:
        # Para o loop se o usuário pressionar Ctrl+C
        break

# print(tello.get_height())
'''
