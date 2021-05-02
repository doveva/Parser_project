from tkinter import *
from tkinter import messagebox
import time
import random
import math
import numpy as np

tk = Tk()
tk.title('Model')
tk.resizable(0, 0)
# без масштабирования
tk.wm_attributes('-topmost', 1)
# поверх окон
canvas = Canvas(tk, width=1920, height=1280, highlightthickness=0, bg="white")
canvas.pack()
tk.update()
#Нарисовали окно короче

def on_close():
    if messagebox.askokcancel('Выход', 'Действительно хотите закрыть окно?'):
        canvas.destroy()

class ore:
    def __init__(self, canvas, separator, score, generator ,copper, nickel, density, sizeX, sizeY, posX, posY):
        self.canvas = canvas
        self.separator = separator
        self.score = score
        self.generator = generator
        self.copper = copper
        self.nickel = nickel
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.id = canvas.create_rectangle(posX,posY,posX+sizeX,posY+sizeY, tag="ore")
        self.nickel_kg = abs(sizeX) * abs(sizeY) * density * nickel
        self.copper_kg = abs(sizeX) * abs(sizeY) * density * copper
        self.collided = False

    def movement(self):
        self.canvas.move(self.id,0,2)

    def collision(self,hitbox):
        sep_pos_u = self.canvas.coords(hitbox)
        # Проверка верхнего касания
        x_u = [sep_pos_u[0], sep_pos_u[2]]
        y_u = [sep_pos_u[1], sep_pos_u[3]]
        or_pos = self.canvas.coords(self.id)

        if y_u[1] < or_pos[3]:
            A_u = y_u[0] - y_u[1]
            B_u = x_u[1] - x_u[0]
            C_u = y_u[0] * (x_u[0] - x_u[1]) - x_u[0]*(y_u[0] - y_u[1])
            s_1 = (A_u*or_pos[0]+B_u*or_pos[1]+C_u)
            s_2 = (A_u*or_pos[0]+B_u*or_pos[3]+C_u)
            s_3 = (A_u*or_pos[2]+B_u*or_pos[3]+C_u)
            s_4 = (A_u*or_pos[2]+B_u*or_pos[1]+C_u)
            if s_1 * s_2 * s_3 * s_4 == 0:
                if hitbox == self.canvas.find_withtag('u_hb')[0]:
                    self.score.val_nick2 += self.nickel_kg
                    self.score.val_copp2 += self.copper_kg
                else:
                    self.score.val_nick1 += self.nickel_kg
                    self.score.val_copp1 += self.copper_kg
                self.canvas.delete(self.id)
                self.score.update()
                self.generator.ore_list.remove(self)
                self.collided = True
            elif not abs(s_1/abs(s_1)+s_2/abs(s_2)+s_3/abs(s_3)+s_4/abs(s_4)) == 4:
                if hitbox == self.canvas.find_withtag('u_hb')[0]:
                    self.score.val_nick2 += self.nickel_kg
                    self.score.val_copp2 += self.copper_kg
                else:
                    self.score.val_nick1 += self.nickel_kg
                    self.score.val_copp1 += self.copper_kg
                self.canvas.delete(self.id)
                self.score.update()
                self.generator.ore_list.remove(self)
                self.collided = True

            b_l_coord = canvas.coords(self.separator.bottom_left)
            for b_l in canvas.find_overlapping(b_l_coord[0],b_l_coord[1], b_l_coord[2], b_l_coord[3]):
                if b_l == self.id:
                    self.score.val_nick1 += self.nickel_kg
                    self.score.val_copp1 += self.copper_kg
                    self.canvas.delete(self.id)
                    self.score.update()
                    self.generator.ore_list.remove(self)
                    self.collided = True

            d_l_coord = canvas.coords(self.separator.bottom_right)
            for d_l in canvas.find_overlapping(d_l_coord[0],d_l_coord[1], d_l_coord[2], d_l_coord[3]):
                if d_l == self.id:
                    self.score.val_nick2 += self.nickel_kg
                    self.score.val_copp2 += self.copper_kg
                    self.canvas.delete(self.id)
                    self.score.update()
                    self.generator.ore_list.remove(self)
                    self.collided = True


class separator:
    def __init__(self,canvas,score):
        # Исходные данные для створки
        self.canvas = canvas
        self.score = score
        self.posX = 960
        self.posY = 1200
        self.line_length = 212
        self.rot_speed = 2
        self.direction = 1
        self.angle = 0
        #Создаём линию, хитбоксы и биндим кнопки для ручного управления (а то вдруг человек тоже захочет поиграть)
        self.id = canvas.create_line(self.posX, self.posY, self.posX, self.posY-self.line_length, width = 10)
        self.up_hitbox = canvas.create_line(self.posX + 3, self.posY, self.posX + 3, self.posY - self.line_length, fill=None, tag="u_hb")
        self.down_hitbox = canvas.create_line(self.posX - 3, self.posY, self.posX - 3, self.posY - self.line_length, fill=None, tag="d_hb")
        self.bottom_left = canvas.create_rectangle(self.posX,self.posY,self.posX-200,self.posY+200, fill=None, tag="btm_lft")
        self.bottom_right =  canvas.create_rectangle(self.posX,self.posY,self.posX+200,self.posY+200, fill=None, tag="btm_rht")
        self.canvas.bind_all('<KeyPress-1>', self.turn_left)
        self.canvas.bind_all('<KeyPress-2>', self.turn_right)
        self.canvas.bind_all('<KeyPress-3>', self.idle)
    # Функции смены направления и ничего не делания
    def turn_left(self,event):
        self.direction = -1

    def turn_right(self,event):
        self.direction = 1

    def idle(self,event):
        self.direction = 0

    #Функция поворота створки
    def rotation(self):
        if self.direction == -1:
            self.angle = self.angle + self.rot_speed
            if self.angle >= 45:
                self.angle = 45
            #расчёт координатов визуальной линии
            end_x = self.posX - self.line_length * math.sin(self.angle * math.pi / 180)
            end_y = self.posY - self.line_length * math.cos(self.angle * math.pi / 180)
            #расчёт координатов хитбоксов
            end_x_uhb = self.posX + 3 - self.line_length * math.sin(self.angle * math.pi / 180)
            end_y_uhb = self.posY - self.line_length * math.cos(self.angle * math.pi / 180)

            end_x_dhb = self.posX - 3 - self.line_length * math.sin(self.angle * math.pi / 180)
            end_y_dhb = self.posY - self.line_length * math.cos(self.angle * math.pi / 180)

            #отрисовка визуала и хитбоксов
            self.canvas.coords(self.id, self.posX, self.posY, end_x, end_y)
            self.canvas.coords(self.up_hitbox, self.posX + 3, self.posY, end_x_uhb, end_y_uhb)
            self.canvas.coords(self.down_hitbox, self.posX - 3, self.posY, end_x_dhb, end_y_dhb)
            return

        elif self.direction == 1:
            self.angle = self.angle - self.rot_speed
            if self.angle <= -45:
                self.angle = -45
            end_x = self.posX - self.line_length * math.sin(self.angle * math.pi / 180)
            end_y = self.posY - self.line_length * math.cos(self.angle * math.pi / 180)

            end_x_uhb = self.posX + 3 - self.line_length * math.sin(self.angle * math.pi / 180)
            end_y_uhb = self.posY - self.line_length * math.cos(self.angle * math.pi / 180)

            end_x_dhb = self.posX - 3 - self.line_length * math.sin(self.angle * math.pi / 180)
            end_y_dhb = self.posY - self.line_length * math.cos(self.angle * math.pi / 180)

            self.canvas.coords(self.id, self.posX, self.posY, end_x, end_y)
            self.canvas.coords(self.up_hitbox, self.posX + 3, self.posY, end_x_uhb, end_y_uhb)
            self.canvas.coords(self.down_hitbox, self.posX - 3, self.posY, end_x_dhb, end_y_dhb)

            return
        else:
            return

# Фон в виде конвейера
class conveyor:
    def __init__(self, canvas):
        self.id = canvas.create_line(810, 100, 810, 1200)
        self.id = canvas.create_line(1110, 100, 1110, 1200)
        self.id = canvas.create_line(810, 100, 1110, 100)

class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.val_nick1 = 0
        self.val_copp1 = 0
        self.val_nick2 = 0
        self.val_copp2 = 0

        self.text1 = canvas.create_text(1500, 35, text="1 конвейер", font=('Courier', 20), fill="black")
        self.nick1 = canvas.create_text(1700, 20, text=str(self.val_nick1) + " тонн никеля", font=('Courier', 15), fill="gray", anchor = NW)
        self.copp1 = canvas.create_text(1700, 50, text=str(self.val_copp1) + " тонн меди", font=('Courier', 15), fill="orange",anchor = NW)

        self.text2 = canvas.create_text(1500, 95, text="2 конвейер", font=('Courier', 20), fill="black")
        self.nick2 = canvas.create_text(1700, 80, text=str(self.val_nick2) + " тонн никеля", font=('Courier', 15), fill="gray", anchor = NW)
        self.copp2 = canvas.create_text(1700, 110, text=str(self.val_copp2) + " тонн меди", font=('Courier', 15), fill="orange", anchor = NW)

    def update(self):
        self.canvas.itemconfig(self.nick1,text=str(self.val_nick1) + " тонн никеля")
        self.canvas.itemconfig(self.copp1, text=str(self.val_copp1) + " тонн меди")
        self.canvas.itemconfig(self.nick2,text=str(self.val_nick2) + " тонн никеля")
        self.canvas.itemconfig(self.copp2, text=str(self.val_copp2) + " тонн меди")

class generator:
    def __init__(self, canvas, separator, score):
        self.x1_brd = 810
        self.x2_brd = 1110
        self.y1_brd = 100
        self.y2_brd = 250
        self.canvas = canvas
        self.separator = separator
        self.score = score
        self.x_brd = np.linspace(self.x1_brd, self.x2_brd, 11)
        self.y_brd = np.linspace(self.y1_brd, self.y2_brd, 6)
        self.stage_n = 1
        self.stage_max = 5
        self.ore_list = []
        self.fill_check = False

    def generate(self):
        spawn = np.zeros((5,10))
        for i in range(0,5):
            spawn_row = np.random.random_integers(0,1,10)
            spawn[i] = spawn_row
        i1=0
        for row in spawn:
            i2 = 0
            for item in row:
                if item == 1:
                    x1 = self.x_brd[i2] + random.randrange(0,15,1)
                    x2 = self.x_brd[i2+1] - random.randrange(0,5,1)
                    y1 = self.y_brd[i1] + random.randrange(0,15,1)
                    y2 = self.y_brd[i1+1] - random.randrange(0,5,1)
                    sizeX = x2 - x1
                    sizeY = y2 - y1
                    nickel = 0.007 + random.random()*0.005
                    copper = 0.006 + random.random()*0.005
                    density = 4.92 + random.random()*0.15
                    ore_part = ore(self.canvas,self.separator,self.score,self,copper,nickel,density,sizeX,sizeY,x1,y1)
                    self.ore_list.append(ore_part)
                i2 += 1
            i1 += 1

    def check(self):
        olp_item = canvas.find_overlapping(self.x1_brd,self.y1_brd,self.x2_brd,self.y2_brd)
        item = self.ore_list
        count = 0
        for overlap in olp_item:
            for i in item:
                if i.id == overlap:
                    count +=1
        if count == 0:
            self.fill_check = False
        else:
            self.fill_check = True

    def play(self):
        while not not self.ore_list:
            self.stage()
            self.separator.rotation()
            for ore_item in self.ore_list:
                ore_item.movement()
                if ore_item.collided == False:
                    ore_item.collision(sep.up_hitbox)
                if ore_item.collided == False:
                    ore_item.collision(sep.down_hitbox)
            tk.update_idletasks()
            tk.update()
            time.sleep(0.05)
            tk.protocol('WM_DELETE_WINDOW', on_close)

    def stage(self):
        self.check()
        if self.stage_n < self.stage_max:
            if self.fill_check == False:
                self.generate()
                self.stage_n +=1


conv = conveyor(canvas)
scr = Score(canvas)
sep = separator(canvas, scr)
gen = generator(canvas, sep, scr)

gen.generate()
gen.play()

