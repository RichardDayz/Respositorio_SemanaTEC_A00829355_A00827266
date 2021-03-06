#José Andrés Villarreal Montemayor  A00829355
#Ricardo Daniel Díaz Granados       A00827266

#link a GitHub: https://github.com/RichardDayz/Respositorio_SemanaTEC_A00829355_A00827266.git

"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""
# se hace import de las librerias necesarias al inicio
from random import choice
from turtle import *
from freegames import floor, vector

# almacena el score (cantidad de bolas comidas por pacman)
state = {'score': 0}

# hace invisible la flecha creando 2 objetos de turtle
path = Turtle(visible=False)
writer = Turtle(visible=False)
info = Turtle(visible=False)

# diercción del pacman igual snake
aim = vector(5, 0)

# crea pacman en la posición del vector
pacman = vector(-40, -80)

# lista de listas de la posición y dirección de cada fantasma
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# lista del tablero para simular 20 columnas y 20 renglones actualizado
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

# regresa True si point es un tile válido
def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    # si la celda es 0 regresa False - pared
    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    # si la celda es 0 regresa False - pared
    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    # recorre toda la lista de tiles
    for index in range(len(tiles)):
        # extrae el valor que existe en la posición index
        tile = tiles[index]

        # si el valor es 1
        if tile > 0:
            # calcula x, y donde se dibuja el square
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y) # dibuja el square(0, 180)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')
    info.up()
    info.goto(-140,180)
    info.color('white')
    info.write('José Andrés Villarreal Montemayor  A00829355', font=('Arial', 8, 'normal'))
    info.up()
    info.goto(-140,-200)
    info.color('white')
    info.write('Ricardo Daniel Díaz Granados       A00827266', font=('Arial', 8, 'normal'))
def move():
    global options
    # establece los colores de los fantasmas
    colores = ['red', 'white', 'pink', 'cyan']
    k = 0
    "Move pacman and all ghosts."
    writer.undo()
    #writer.write(state['score'])
    valor = state['score']
    writer.write(f'Score: {valor}')

    
    # limpia la ventana
    clear()

    # si es una posición válida no es pared
    if valid(pacman + aim):
        pacman.move(aim)

    # regresa la posición del pacman en el tablero
    index = offset(pacman)

    # 1 = hay camino
    if tiles[index] == 1:
        # se le asigna 2 a la posición que ya no tiene galleta
        tiles[index] = 2
        # se incrementa el score
        state['score'] += 1
        # calcula posición x, y de pacman
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        # dibuja square sin galleta
        square(x, y)

    up()
    # se va a la posición del pacman
    goto(pacman.x + 10, pacman.y + 10)
    # dibuja el pacman
    dot(20, 'yellow')

    
    for point, course in ghosts:
        # valida si el fantasma point se puede mover en course
        if valid(point + course):
            point.move(course)
        # si no se puede mover el fantasma en esa dirección
        else:
            # se actualiza la dirección de movimiento del mismo
            # plan guarda la nueva dirección del fantasma
            # aqui se le agrega inteligencia a los fantasmas
            if pacman.x > point.x:
                options = vector(5,0)
            elif pacman.y > point.y:
                options = vector(0, 5)
            elif pacman.x < point.x:
                options = vector(-5,0)
            elif pacman.y < point.y:
                options = vector(0, -5)
            else:
                movimientos = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                ]
                options = choice(movimientos)
            course.x = options.x
            course.y = options.y

        # levanta
        up()
        # mueve la posición del fantasma
        goto(point.x + 10, point.y + 10)
        # dibuja el fantasma
        dot(20, colores[k])
        k = k + 1

    update()

    # recorre la lista de fantasmas para ver si coinciden las
    # posiciones del Pacman y de algún fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            writer.goto(-120, 10)
            writer.write('Game Over', font=('Arial', 30, 'normal'))
            writer.goto(-90, -20)
            writer.write(f'Score: {valor}', font=('Arial', 20, 'normal'))
            return

    # vuelve a llamar la función dentro de 25 milisegundos
    ontimer(move, 25)

def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

# inicializa la ventana ancho y alto 420, 420
# 370, 0 indica la posición de la esquina superior izq. de la ventana
setup(420, 420, 370, 0)
# esconde la |> de la turtle default
hideturtle()
# oculta toda forma de dibujar
tracer(False)
# mueve la turtle writer a la posición 160, 160
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
# activa escuchar los eventos del teclado
listen()
# en caso de que se oprima la tecla indicada
# se llama a la función change y cambian dirección del pacman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
# llama la función world y dibuja el tablero
world()
# llama a la función move()
move()
done()