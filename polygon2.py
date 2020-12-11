#Часть Юлии Гусевой, задание рабочего окна и ввод многоугольника на экране
#написан ввод и функция coords
#Часть Павла Гуревича, проверка на выпуклость и превращение невыпуклых многоугольников в выпуклые, разделение координат в списки, закрытие программы
#написаны функции vipukl, tru_v, dev_coords, написано завершение
#Часть Богдана Карповича, сранивание длин сторон многоугольника, поиск точек около самой длинной стороны
#написаны функции side, points
#Часть Софьи Бестужевой, проверка нахождения точки внутри многоугольника, вписывание прямоугольников в многоугольника
#написаны функции inpolygon, rect
'''!!!ОСТАЛОСЬ ПОПРАВИТЬ БАГИ, ПРОЗРАЧНОСТЬ?, ДОПИСАТЬ ВЫВОД В ФАЙЛ'''
import pygame
from pygame.draw import *
import time
import math
pygame.init()
FPS = 30
input('для отрисовки многоуголька: 1)нажмите enter 2) отметьте точки мышкой на поверхности  3)нажмите пробел 2 раза с перерывом')
w = int(input('Введите ширину прямоугольника '))
h = int(input('Введите высоту прямоугольника '))
d, sh = [int(j) for j in input('введите через пробел целочисленные длину и ширину рабочего окна ').split()]
ori = int(input('введите 1, если задаёте многоугольник по часовой стрелке, иначе введите -1 :'))
screen = pygame.display.set_mode((d, sh))
clock = pygame.time.Clock()

def vipukl(coord, ori):
    """ coord - list with starting coordinates of polygon
        ori - ориентация построения многоугольника:
                если ori = 1, следует задавать многоугольник по часовой стрелке,
                если ori = -1, следует задавать против часовой стрелки
    """

    nc = coord.copy()
    kc = []
    z0 = ori
    z1 = 0
    z2 = 0
    l = len(coord)
    for i in range(l):

        AB = [0, 0]
        BC = [0, 0]

        AB[0] = coord[(i+1)%l][0] - coord[i%l][0]
        AB[1] = coord[(i+1)%l][1] - coord[i%l][1]
        BC[0] = coord[(i+2)%l][0] - coord[(i+1)%l][0]
        BC[1] = coord[(i+2)%l][1] - coord[(i+1)%l][1]

        if AB[0]*BC[1] - AB[1]*BC[0] < 0:
            z1 = -1
        elif AB[0]*BC[1] - AB[1]*BC[0] > 0:
            z1 = 1
        elif AB[0]*BC[1] - AB[1]*BC[0] == 0:
            z1 = 0


        if z1*z0 == -1:
            nc.remove(coord[(i+1)%l])
            kc.append(coord[(i+1)%l])
            z2 = 1

    return nc, z2

def coords():
    coord = []
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                '''при нажатии левой кнопки мыши ставит точку, координты точки помещает в список'''
                if event.button == 1:
                    circle(screen, (100, 100, 100), event.pos, 1)
                    s = event.pos
                    coord.append(s)
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                ''' при нажатии пробела рисует многоульник, ждет пару секунд и заверщает цикл'''
                if event.key == pygame.K_SPACE:
                    polygon(screen, (100, 100, 100), coord, 5)
                    pygame.display.update()
                    time.sleep(3)
                    finished = True
    return coord

def tru_v(coor, ori, z =1):
    '''coor - список координат многоугольника
    ori - ориентация вращения (объяснено выше)
    функция возвращает список координат выпуклого многоугольника'''
    while z == 1:
        coor, z = vipukl(coor, ori)
    return coor

def dev_coords(coords):
    '''разбивает список кортежей на координаты х и у. Возвращает 2 списка с иксовыми и игрековыми координатами'''
    x = []
    y = []
    for i in range(len(coords)):
        x.append(coords[i][0])
        y.append(coords[i][1])
    return x, y

def side (x,y):
    length=[]
    for i in range(len(x)):
        length.append(math.sqrt((x[i]-x[i-1])**2 + (y[i]-y[i-1])**2))
    return int(max(length))

'''поиск координат самой длинной стороны'''
def points(max,x,y):
    x0=0
    y0=0
    x1=0
    x2=0
    y1=0
    y2=0
    auxiliary_arr = []

    for i in range(len(x)):
        auxiliary_arr.append(math.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2))
        if max == int(auxiliary_arr[i]):
            x1 = x[i]
            x2 = x[i-1]
            y1 = y[i]
            y2 = y[i - 1]
            if x1 > x2:
                x0=x2
                x2=x1
                x1=x0
                y0 = y2
                y2 = y1
                y1 = y0
    return x1,x2,y1,y2

def inpolygon(x, y, xc, yc):
    c=0
    for i in range(len(xc)):
        if (((yc[i]<=y and y<yc[i-1]) or (yc[i-1]<=y and y<yc[i])) and
            (x > (xc[i-1] - xc[i]) * (y - yc[i]) / (yc[i-1] - yc[i]) + xc[i])):
            c = 1 - c
    return c

'''x1, y1, x2, y2 координаты точек стороны с наибольшей длиной x1<x2
inpolygon - проверяет что точка в многоугольнике
l- длина стороны длинной
w - ширина прямоугольника
h - высота прямоугольника'''

def rect(x1,x2,y1,y2,d,sh):
    '''xw yw - смещение вдоль ширины
xh yh - смещение вдоль высоты'''
    xw = ((w*(x2-x1))/l)
    yw = ((w*(y2-y1))/l)
    xh = -((h*(y2-y1))/l)
    yh = ((h*(x2-x1))/l)
    xt = x1
    yt = y1
    '''сначала строится первый ряд, чтобы понять в какую сторону достраивать прямоугольники'''
    while ((xw+x1)<=x2)  :
        if ((inpolygon(x1+xw+xh, y1+yw+yh, xc, yc)) > 0) and ((inpolygon(x1+xh, y1+yh, xc, yc)) > 0) :
            polygon(screen, (100, 200, 200, 200), [(x1,y1),(x1+xw,y1+yw),(x1+xw+xh,y1+yw+yh),(x1+xh,y1+yh)])
            polygon(screen, (3, 10, 100), [(x1,y1),(x1+xw,y1+yw),(x1+xw+xh,y1+yw+yh),(x1+xh,y1+yh)], 2)
            xt=x1+xw+xh
            yt=y1+yw+yh
            n=1
        elif ((inpolygon(x1+xw-xh, y1+yw-yh, xc, yc)) > 0) and ((inpolygon(x1-xh, y1-yh, xc, yc)) > 0):
            polygon(screen, (100, 200, 200, 200), [(x1,y1),(x1+xw,y1+yw),(x1+xw-xh,y1+yw-yh),(x1-xh,y1-yh)])
            polygon(screen, (3, 10, 100), [(x1,y1),(x1+xw,y1+yw),(x1+xw-xh,y1+yw-yh),(x1-xh,y1-yh)], 2)
            xt=x1-xw-xh
            yt=y1-yw-yh
            n=0


        x1 += xw
        y1 += yw
    '''достраиваются ряды прямоугольников'''
    for i in range (int(((math.sqrt(d**2+sh**2))//h))-1):
        while ((xw+x1)<=x2)  :
            if (n>0) and ((inpolygon(x1+xw+xh, y1+yw+yh, xc, yc)) > 0) and ((inpolygon(x1+xh, y1+yh, xc, yc)) > 0) and ((inpolygon(x1+xw, y1+yw, xc, yc)) > 0):
                polygon(screen, (100, 200, 200, 200), [(x1,y1),(x1+xw,y1+yw),(x1+xw+xh,y1+yw+yh),(x1+xh,y1+yh)])
                polygon(screen, (3, 10, 100), [(x1,y1),(x1+xw,y1+yw),(x1+xw+xh,y1+yw+yh),(x1+xh,y1+yh)], 2)
                xt=x1+xw+xh
                yt=y1+yw+yh
            elif( n==0) and ((inpolygon(x1+xw-xh, y1+yw-yh, xc, yc)) > 0) and ((inpolygon(x1-xh, y1-yh, xc, yc)) > 0) and ((inpolygon(x1+xw, y1+yw, xc, yc)) > 0):
                polygon(screen, (100, 200, 200, 200), [(x1,y1),(x1+xw,y1+yw),(x1+xw-xh,y1+yw-yh),(x1-xh,y1-yh)])
                polygon(screen, (3, 10, 100), [(x1,y1),(x1+xw,y1+yw),(x1+xw-xh,y1+yw-yh),(x1-xh,y1-yh)], 2)
                xt=x1-xw-xh
                yt=y1-yw-yh


            x1 += xw
            y1 += yw
        x1=xt
        y1=yt
        while inpolygon(x1+xw,y1+yw,xc,yc)>0:
            x1=x1+xw
            y1=y1+yw
            x2=x2+xw
            y2=y2+yw
        while inpolygon(x1-xw,y1-yw,xc,yc)>0:
            x1=x1-xw
            y1=y1-yw


t = coords()
newc = tru_v(t, ori)

polygon(screen, (11, 111, 32), newc)
xc, yc = dev_coords(newc)
print(xc, yc)
l = side (xc, yc)
x1,x2,y1,y2 = points(l,xc,yc)
rect(x1,x2,y1,y2,d,sh)
pygame.display.update()
clock = pygame.time.Clock()
finished = False




while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
