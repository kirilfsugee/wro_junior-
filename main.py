#!/usr/bin/env python3
#9_05_2021
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_A,OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from time import sleep
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev.ev3 import Screen
from ev3dev2.led import Leds
from sys import stderr

#описываем девайсы
LeftColorSensor = ColorSensor(INPUT_4)
RightColorSensor = ColorSensor(INPUT_2)
ReadColorSensor = ColorSensor(INPUT_3)
zahvatMediumMotor = MediumMotor(OUTPUT_A)
LeftLargeMotor = LargeMotor(OUTPUT_C)
RightLargeMotor = LargeMotor(OUTPUT_B)
ms = MoveSteering(OUTPUT_C, OUTPUT_B) 

btn = Button()
sound = Sound()
lcd = Screen()
leds = Leds()
us = UltrasonicSensor()

#глобальные переменные
#размер поля
rm_x,rm_y=28,12
#     00  01  02  03  04  05  06  07  08  09  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27
k =[['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],#00
    ['#','#','K','#','#','#','#','#','#','#','#','#','#','K','#','#','#','K','#','#','#','K','#','#','#','K','#','#'],#01
    ['#','K','X','K','#','#','#','G','L','L','L','L','L','X','L','L','L','X','L','L','L','X','L','L','L','X','K','#'],#02
    ['#','#','L','#','#','#','#','L','#','#','#','#','#','K','#','#','#','K','#','#','#','K','#','#','#','K','#','#'],#03
    ['#','#','L','#','#','#','#','L','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],#04
    ['#','#','L','#','#','#','#','L','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],#05
    ['#','#','L','#','#','#','#','L','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],#06
    ['#','#','L','#','#','#','#','L','#','#','#','#','#','K','#','#','#','K','#','#','#','K','#','#','#','K','#','#'],#07
    ['#','#','G','L','T','L','L','T','L','L','L','L','L','X','L','L','L','X','L','L','L','X','L','L','L','X','H','#'],#08
    ['#','#','#','#','L','#','#','#','#','#','#','#','#','K','#','#','#','K','#','#','#','K','#','#','#','K','#','#'],#09
    ['#','#','#','#','K','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],#10
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']]#11
p_red=[(13,1),(17,1),(17,7),(21,9)] #поля с красным цветом
p_green=[(21,1),(13,7),(21,7),(25,9)] #поля с зеленым цветом
p_blue=[(25,1),(25,7),(13,9),(17,9)] #поля с синим цветом
p_red1=[(13,1),(17,1),(17,7),(21,9)]
p_green1=[(21,1),(13,7),(21,7),(25,9)] 
p_blue1=[(25,1),(25,7),(13,9),(17,9)] 

p_out=(1,2) #поле выезда
p_in=(3,2) #поле въезда
p_a=(4,10) #поле акккумуляторами
p_sh=[] #поля с шлагбаумами
zona = [[(13, 9), (17, 9), (21, 9), (25, 9)], [(13, 7), (17, 7), (21, 7), (25, 7)], [(13, 1), (17, 1), (21, 1), (25, 1)]]
zona1 = [[(13, 9), (17, 9), (21, 9), (25, 9)], [(25, 7), (21, 7), (17, 7), (13, 7)], [(13, 1), (17, 1), (21, 1), (25, 1)]]
zona2 = [(13, 9), (17, 9), (21, 9), (25, 9), (25, 7), (21, 7), (17, 7), (13, 7), (13, 1), (17, 1), (21, 1), (25, 1)]
zona3 = [(13, 8), (17, 8), (21, 8), (25, 8), (26, 8), (25, 8), (21, 8), (17, 8), (13, 8), (13, 2), (17, 2), (21, 2), (25, 2)]
zona4 = [(13, 7), (17, 7), (21, 7), (25, 7), (25, 9), (21, 9), (17, 9), (13, 9), (13, 1), (17, 1), (21, 1), (25, 1), (4, 8)]

#компасс 0 на север   180 юг   90 восток  270 запад
compass = 0

# позиция робота относительно старта
position_x = 0
position_y = 0

xte, yte = 0, 0
korotkiy_put = []
krasniye_puti = []

count_cars = 3
count_cars_viezd = 6
#global dop_perekrestok
dop_perekrestok = 0 
#global car_in_robot  
car_in_robot = False
dist_rej =-1
#######################################################################################################
#описываем функции

#выводим в консоль карту
def print_consol_karta():
    global karta
    for y in range(rm_y):
        s =''
        for x in range(rm_x):
            z = karta[y][x] 
            if z<10 and z>-1:
                p=' '
            else:
                p=''
            s=s+'|'+p+str(z)
        consol_print(s)
        

# волна
def volna(in_spisok_tochek):
    global schet, karta
    pomechennoe = False
    schet+=1
    #список новых точек
    new_spisok_tochek=[]
    #для всех path точек
    for xt,yt in in_spisok_tochek:
        #проверяем левую точку
        nxt=xt-1
        nyt=yt
        if k[nyt][nxt]!='#' and karta[nyt][nxt]==-1:
            karta[nyt][nxt]=schet
            new_spisok_tochek.append((nxt,nyt))
            pomechennoe = True

        #проверяем правую точку
        nxt=xt+1
        nyt=yt
        if k[nyt][nxt]!='#' and karta[nyt][nxt]==-1:
            karta[nyt][nxt]=schet
            new_spisok_tochek.append((nxt,nyt))
            pomechennoe = True

        #проверяем верхнюю точку
        nxt=xt
        nyt=yt-1
        if k[nyt][nxt]!='#' and karta[nyt][nxt]==-1:
            karta[nyt][nxt]=schet
            new_spisok_tochek.append((nxt,nyt))
            pomechennoe = True

        #проверяем нижнюю точку
        nxt=xt
        nyt=yt+1
        if k[nyt][nxt]!='#' and karta[nyt][nxt]==-1:
            karta[nyt][nxt]=schet
            new_spisok_tochek.append((nxt,nyt))
            pomechennoe = True

    if pomechennoe:
        volna(new_spisok_tochek)


schet = 0
karta = [[-1] * rm_x for i in range(rm_y)]
#поиск пути
def poisk_path(s_x,s_y,e_x,e_y):
    global schet, karta, path
    #создаем пустую карту
    karta= [[-1] * rm_x for i in range(rm_y)]

    #добавляем точку на которой робот в список
    spisok_tochek = [(s_x,s_y)]
    #счет волны с нуля
    schet = 0
    #помечаем 0 точку
    karta[s_y][s_x]=0
    #вызываем рекурсионную функцию волнового обозначения клеток
    volna(spisok_tochek)
    #в результате получаем karta с обозначеним до каждой клетки сколько шагов от стартовой

    
    # по карте ищем наш путь
    #идем от конца к старту
    schet = karta[e_y][e_x]
    consol_print(schet)
    path=[(e_x,e_y)]

    global xt, yt
    xt=e_x
    yt=e_y

    for i in range(schet-1,-1,-1):
        # проверяем левую точку
        nxt = xt - 1
        nyt = yt
    
        if karta[nyt][nxt] == i:
            xt = nxt
            yt = nyt
            if k[nyt][nxt] != 'L':
                path.insert(0, (xt, yt))
            continue

        # проверяем правую точку
        nxt = xt + 1
        nyt = yt
        if karta[nyt][nxt] == i:
            xt = nxt
            yt = nyt
            if k[nyt][nxt] != 'L':
                path.insert(0, (xt, yt))
            continue

        # проверяем нижнюю точку
        nxt = xt
        nyt = yt-1
        if karta[nyt][nxt] == i:
            xt = nxt
            yt = nyt
            if k[nyt][nxt] != 'L':
                path.insert(0, (xt, yt))
            continue

        # проверяем верхнюю точку
        nxt = xt
        nyt = yt+1
        if karta[nyt][nxt] == i:
            xt = nxt
            yt = nyt
            if k[nyt][nxt] != 'L':
                path.insert(0, (xt, yt))
            continue
    path.append((e_x, e_y))
    consol_print('Put: ' + str(path))
    return path

def beep():
    sound.beep() 

def speak(m):
    #0: без цвета   1: черный   2: синий   3: зеленый   4: желтый   5: красный   6: белый   7: коричневый 
    if m == 0:
        sound.speak('none')
    elif m==1:
        sound.speak('black')
    elif m==2:
        sound.speak('blue')
    elif m==3:
        sound.speak('green')
    elif m==4:
        sound.speak('yellow')
    elif m==5:
        sound.speak('red')
    elif m==6:
        sound.speak('white')
    elif m==7:
        sound.speak('brown')
    elif m==10:
        sound.speak('stop')
    elif m==11:
        sound.speak('go')
        
def svetodiod(color):
    '''
    BLACK
    RED
    GREEN
    AMBER
    ORANGE
    YELLOW
    '''
    leds.set_color('LEFT', color)

def lcd_print(string, x = 0, y = 55):
    lcd.clear()
    lcd.draw.text((x,y),string)
    lcd.update()

def consol_print(string):
    print(string, file=stderr) 

def press_any_key():
    while not btn.any():
        sleep(0.2)    
    beep()

def distance_us():
    return (us.distance_centimeters//1)

def ehat_pryamo(v, s):
    ms.on_for_degrees(steering=0, speed=v, degrees=s)

# поворот на месте   90 вправо  -90 влево
def rotate_on_place(ugol, boole = 0):
    global compass 
    ms.on_for_degrees(steering=100, speed=25, degrees=ugol*3.2) 
    #компасс 0 на север   180 юг   90 восток  270 запад
    compass += ugol
    compass = abs(compass % 360)
    return compass

def move_to_crossroads():#1 см - 28,3 градуса, 17,6 см - 360 градусов
    leds.animate_police_lights('RED', 'GREEN', sleeptime=0.15, duration=0.01)
    ss=25
    kP=1
    kD=0.2
    pred_error = 0
    not_black = True
    global dist 
    while not_black:
        lr=LeftColorSensor.reflected_light_intensity  #0..100
        rr=RightColorSensor.reflected_light_intensity #0..100
        error = lr - rr  
        u=error*kP + (pred_error-error)*kD
        u_porog = 10
        if u>u_porog:
            u=u_porog
        if u<-u_porog:
            u=-u_porog
        ms.on(steering=u, speed=ss)
        sleep(0.01)
        if lr<10 or rr<10:
            dist = distance_us()
            svetodiod('ORANGE')
            not_black = False 
        pred_error=error
    
    leds.all_off()

def read_color():
    h,s,v = ReadColorSensor.hsv
    color1 = int(h*100)
    consol_print('h'+str(h)) # оттенок
    consol_print('s'+str(s)) # насыщенность
    consol_print('v'+str(v)) # яркость
    if 60<color1<70:
        return 2
    elif 35<color1<60:
        return 3
    elif 100>color1>70 or color1<3:
        return 5

def color_move():    
    global color
    color = read_color()
    speak(color)
    consol_print(color)

def zahvat_car():
    #захватывает а    
    ehat_pryamo(20, 155)
    color_move()
    ehat_pryamo(20, 90)
    zahvatMediumMotor.on_for_degrees(speed=25, degrees=90)
    ehat_pryamo(20, -245)

def zahvat_car2():
    color_move()
    ehat_pryamo(20, 120)
    zahvatMediumMotor.on_for_degrees(speed=25, degrees=90)
    ehat_pryamo(20, -120)

def otpustit_car():
    #отпустить авто
    ehat_pryamo(20, 265)
    zahvatMediumMotor.on_for_degrees(speed=25, degrees=-90)
    ehat_pryamo(20, -265)    

def vivod_dannih():
    lcd.clear()
    lcd.draw.text((40,42),str('compass: '))
    lcd.draw.text((88,42),str(compass))
    lcd.draw.text((70,62),str('us: '))
    lcd.draw.text((88,62),str(distance_us()))
    lcd.draw.text((10,82),str('l_ref: '))
    lcd.draw.text((48,82),str(LeftColorSensor.reflected_light_intensity))
    lcd.draw.text((80,82),str('r_ref: '))
    lcd.draw.text((118,82),str(RightColorSensor.reflected_light_intensity))

    lcd.update()

def left(state):
    if state:
        sleep(0.1)
        rotate_on_place(-5)
    
def right(state):
    if state:
        sleep(0.1)
        rotate_on_place(5)
    
def up(state):
    if state:
        sleep(0.1)
        ehat_pryamo(20, 10)
    
def down(state):
    if state:
        sleep(0.1)
        ehat_pryamo(20, -10)
schet_zahvat = 0
def enter(state):
    global schet_zahvat
    if state:
        if schet_zahvat == 0:
            zahvatMediumMotor.on_for_degrees(speed = 40, degrees = -80)
            schet_zahvat = 1
        elif schet_zahvat == 1:
            zahvatMediumMotor.on_for_degrees(speed = 40, degrees = -40)
            schet_zahvat = 2
        elif schet_zahvat == 2:
            zahvat_car()
            schet_zahvat = 0

def backspace(state):
    pass
    
btn.on_left = left
btn.on_right = right
btn.on_up = up
btn.on_down = down
btn.on_enter = enter
btn.on_backspace = backspace

proehal = False
doezd = 65
def robot_path(sx, sy, ex, ey, rejim = True):
    poisk_path(sx, sy, ex, ey)    
    sch = 0
    global dist_rej
    global dop_perekrestok
    proehal = False
    if k[sy][sx] == 'K' and k[ey][ex] == 'K' and len(path) == 4:
        rotate_on_place(90)
        rotate_on_place(90)

    if k[sy][sx] == 'K':
        sch += 1
    while sch < (len(path) - 2):
        if path[sch + 1][0] > path[sch][0]:
            if compass == 0:
                if k[path[sch+1][1]][path[sch+1][0]] == 'H':
                    ehat_pryamo(15, 60)
                else:
                    move_to_crossroads()
                    ms.off()
                if distance_us() < 15 and distance_us() > 6:
                    ms.off()
                    beep()
                    ehat_pryamo(20, doezd)
                    dist_rej = 1
                elif distance_us() <= 6:
                    ms.off()
                    beep();beep()
                    ehat_pryamo(20, doezd)
                    dist_rej = 2
                else:
                    ehat_pryamo(20, doezd)
                    dist_rej = 0
                sch += 1
            elif compass > 180 and compass != 0:
                rotate_on_place(90)
            elif compass < 180 and compass != 0:
                rotate_on_place(-90)

        if path[sch + 1][0] < path[sch][0]:
            if compass == 180:
                move_to_crossroads()
                if distance_us() < 15 and distance_us() > 6:
                    ms.off()
                    beep()
                    ehat_pryamo(20, doezd)
                    dist_rej = 1
                elif distance_us() <= 6:
                    ms.off()
                    beep();beep()
                    ehat_pryamo(20, doezd)
                    dist_rej = 2
                else:
                    ehat_pryamo(20, doezd)
                    dist_rej = 0
                

                sch += 1
            elif compass > 180 :
                rotate_on_place(-90)
            elif compass < 180:
                rotate_on_place(90)
        

        if path[sch + 1][1] < path[sch][1]:
            if compass == 270:
                if k[path[sch+1][1]][path[sch+1][0]] == 'K':
                    beep()
                    sch += 1
                else:
                    move_to_crossroads()
                    ehat_pryamo(20, doezd)
                    sch += 1
            elif compass > 90:
                rotate_on_place(90)
            elif compass < 90:
                rotate_on_place(-90)

        if path[sch + 1][1] > path[sch][1]:
            if compass == 90:
                if k[path[sch+1][1]][path[sch+1][0]] == 'K':
                    beep()
                    sch += 1
                else:
                    move_to_crossroads()
                    ehat_pryamo(20, doezd)
                    sch += 1
            elif compass > 90 and compass != 90:
                rotate_on_place(-90)
            elif compass < 90 and compass != 90:
                rotate_on_place(90)
        proehal = True
            
def compass_rotate(ugol):
    while ugol != compass:
        if ugol > compass:
            rotate_on_place(-90)
        elif ugol < compass:
            rotate_on_place(90)

def reglament0():#выезд со старта
    LeftLargeMotor.on_for_degrees(speed=30, degrees=250) 
    ms.on_for_seconds(steering=0, speed=30, seconds=1.1)
    LeftLargeMotor.on_for_degrees(speed=30, degrees=280) 
    LeftLargeMotor.reset()
    RightLargeMotor.reset()
'''
while True:  
    btn.process() 
    vivod_dannih()
    sleep(0.01)
'''
spisok_mimo = []
def reglament1():
    zahvatMediumMotor.on_for_degrees(speed = 20, degrees = -90)
    viezd_car = 0 
    robot_path(4, 8, 7, 8)
    xte, yte = 7, 8

    viezd_car = 0
    povorot_rej = False
    red_car = 0 #координаты красной машинки
    for i in range(0, len(zona3)):
        robot_path(xte, yte, zona3[i][0], zona3[i][1])
        xte = zona3[i][0]
        yte = zona3[i][1]
        
        if i >= 3 and i <= 8 and compass == 180:
            naprav = 1
        else:
            naprav = -1
        if dist_rej == 2:
            spisok_mimo.append((xte, yte + naprav))
            if (xte, yte + naprav) in p_red1:
                p_red1.remove((xte, yte + naprav))
                consol_print('Svobodniye krasniye puti: ' + str(p_red1))
            if (xte, yte + naprav) in p_green1:
                p_green1.remove((xte, yte + naprav))
                consol_print('Svobodniye zeleniye puti: ' + str(p_green1))
            if (xte, yte + naprav) in p_blue1:
                p_blue1.remove((xte, yte + naprav))
                consol_print('Svobodniye siniye puti: ' + str(p_blue1))

        consol_print('Spisok mimo: ' + str(spisok_mimo))
        if dist_rej == 1 and ((xte,yte+naprav) not in spisok_mimo):
            car_in_robot = True
            robot_path(xte, yte, xte, yte + naprav)
            yte = yte + naprav
            ehat_pryamo(15, 155)
            color_move()
            if color == 5:
                red_car = (xte, yte)
                spisok_mimo.append(red_car)
                consol_print('Red car: ' + str(red_car))
                ehat_pryamo(15, -155)
                
            if color == 2 or color == 3:
                ehat_pryamo(15, 90)
                zahvatMediumMotor.on_for_degrees(speed = 25, degrees = 90)
                ehat_pryamo(15, -245)
                if viezd_car == 0:
                    robot_path(xte, yte, 2, 2)
                    xte, yte = 2, 2
                    ehat_pryamo(20, 275)
                    rotate_on_place(-90)
                    ehat_pryamo(20, 170)
                    zahvatMediumMotor.on_for_degrees(speed=25, degrees=-90)
                    ehat_pryamo(20, -170)
                    rotate_on_place(-90)
                    move_to_crossroads()
                    ehat_pryamo(20, 45)
                    viezd_car += 1
                    robot_path(xte, yte, zona3[i][0], zona3[i][1])
                    xte, yte = zona3[i][0], zona3[i][1]
                else:
                    robot_path(xte, yte, 2, 8)
                    xte, yte = 2, 8
                    rotate_on_place(90)
                    ehat_pryamo(20, 650)
                    rotate_on_place(-90)
                    ehat_pryamo(20, 170)
                    zahvatMediumMotor.on_for_degrees(speed=25, degrees=-90)
                    ehat_pryamo(20, -170)
                    rotate_on_place(-90)
                    move_to_crossroads()
                    ehat_pryamo(15, 55)
                dop_perekrestok = 0
                car_in_robot = False

    robot_path(xte, yte, red_car[0], red_car[1])
    xte, yte = red_car[0], red_car[1]
    ehat_pryamo(20, 245)
    zahvatMediumMotor.on_for_degrees(speed=25, degrees=90)
    ehat_pryamo(20, -245)

    krasniye_puti = []
    for i in range(0, len(p_red1)):
        poisk_path(xte, yte, p_red1[i][0], p_red1[i][1])
        if schet != 0:
            krasniye_puti.append(poisk_path(xte, yte, p_red1[i][0], p_red1[i][1]))
        korotkiy_put = min(krasniye_puti, key = len)
    robot_path(xte, yte, korotkiy_put[-1][0], korotkiy_put[-1][1])
    otpustit_car()
    xte, yte = korotkiy_put[-1][0], korotkiy_put[-1][1]
    spisok_mimo.append((xte,yte))
    robot_path(xte, yte, 4, 8)

def reglament2():
    xte, yte = 4, 8
    for i in range(0, count_cars_viezd):
        rotate_on_place(90)
        ehat_pryamo(15, i*250)
        zahvat_car2()
        ehat_pryamo(15, -i*250)
        if color == 5:#красный
            krasniye_puti = []
            for i in range(0, len(p_red1)):
                poisk_path(xte, yte, p_red1[i][0], p_red1[i][1])
                if schet != 0:
                    krasniye_puti.append(poisk_path(xte, yte, p_red1[i][0], p_red1[i][1]))
            korotkiy_put = min(krasniye_puti, key = len)
            robot_path(xte, yte, korotkiy_put[-1][0], korotkiy_put[-1][1])
            otpustit_car()
            xte, yte = korotkiy_put[-1][0], korotkiy_put[-1][1]
            spisok_mimo.append((xte,yte))
            p_red1.remove((xte, yte))
            count_cars_viezd -= 1
            robot_path(xte, yte, 4, 8)
            xte, yte = 4, 8

        if color == 2:#синий
            siniye_puti = []
            for i in range(0, len(p_blue1)):
                poisk_path(xte, yte, p_blue1[i][0], p_blue1[i][1])
                if schet != 0:
                    siniye_puti.append(poisk_path(xte, yte, p_blue1[i][0], p_blue1[i][1]))
            korotkiy_put = min(siniye_puti, key = len)
            robot_path(xte, yte, korotkiy_put[-1][0], korotkiy_put[-1][1])
            otpustit_car()
            xte, yte = korotkiy_put[-1][0], korotkiy_put[-1][1]
            spisok_mimo.append((xte,yte))
            p_blue1.remove((xte, yte))
            count_cars_viezd -= 1
            robot_path(xte, yte, 4, 8)
            xte, yte = 4, 8

        if color == 3:#зелёный
            zeleniye_puti = []
            for i in range(0, len(p_green1)):
                poisk_path(xte, yte, p_green1[i][0], p_green1[i][1])
                if schet != 0:
                    zeleniye_puti.append(poisk_path(xte, yte, p_green1[i][0], p_green1[i][1]))
            korotkiy_put = min(zeleniye_puti, key = len)
            robot_path(xte, yte, korotkiy_put[-1][0], korotkiy_put[-1][1])
            otpustit_car()
            xte, yte = korotkiy_put[-1][0], korotkiy_put[-1][1]
            spisok_mimo.append((xte,yte))
            p_green1.remove((xte, yte))
            count_cars_viezd -= 1
            robot_path(xte, yte, 4, 8)
            xte, yte = 4, 8

reglament0()
reglament1()
reglament2()