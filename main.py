from tkinter import *
from math import *

root = Tk()
canvas = Canvas(root, width=1800, height=1000)
canvas.pack()

actions = {"left": 0, 'right': 0, "up": 0, 'down': 0, "fire": 0, 'cooldown': 0}
trak = []
second = 0


def right(event):
    actions["right"] = 1


def left(event):
    actions["left"] = 1


def up(event):
    actions['up'] = 1


def down(event):
    actions["down"] = 1


def cooldown(event):
    actions['cooldown'] = 1


def fire(event, fired_tank_index=0):  # create new bullet
    global second
    if event.keysym == 'space':
        actions["fire"] = 1
        actions['cooldown'] = 0
        x = all_Tanks[fired_tank_index].current_shape[4][0] + 10
        y = all_Tanks[fired_tank_index].current_shape[4][1] + 10
        directoin = all_Tanks[fired_tank_index].direction
        all_Bullets.append(Bullet(x, y, directoin))
        second = 0


def cooldown2():
    global second
    second += 1
    if actions['cooldown'] == 1:
        root.after(100, cooldown2)


def collision(tank, wall):
    for angle in range(len(tank.current_shape)):
        if (tank.current_shape[angle][0] > wall.up_left_angle[0]) and (
                tank.current_shape[angle][0] < wall.down_rite_angle[0]) and (
                tank.current_shape[angle][1] > wall.up_left_angle[1]) and (
                tank.current_shape[angle][1] < wall.down_rite_angle[1]):
            tank.color = 'red'
            return True
    tank.color = 'green'
    return False


class Tank:
    def __init__(self, x, y, color='green'):
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = 0
        self.color = color
        self.shape0 = [[-50, -75], [-25, -75], [-25, -55], [-10, -55], [-10, -150], [10, -150], [10, -55], [25, -55],
                       [25, -75], [50, -75], [50, 75], [25, 75], [25, 60], [-25, 60], [-25, 75], [-50, 75]]
        self.current_shape = [[x + self.x, y + self.y] for x, y in self.shape0]

    def draw_tank(self):
        text = canvas.create_text(100, 100, text=f"angle: {round(self.direction, 3)} {round(degrees(self.direction), 2)}", justify=CENTER, font="Verdana 14")
        trak.append(self.current_shape[-5][0])
        trak.append(self.current_shape[-5][1])
        trak.append(self.current_shape[-6][0])
        trak.append(self.current_shape[-6][1])
        trak.append(self.current_shape[-1][0])
        trak.append(self.current_shape[-1][1])
        trak.append(self.current_shape[-2][0])
        trak.append(self.current_shape[-2][1])
        for i in range(8, len(trak), 4):
            canvas.create_line(trak[i], trak[i + 1], trak[i + 2], trak[i + 3])
        canvas.create_polygon(*self.current_shape, fill=self.color)
        if len(trak) > 4 * 2 * 500:
            trak.pop(0)
            trak.pop(1)
            trak.pop(2)
            trak.pop(3)
            trak.pop(4)
            trak.pop(5)
            trak.pop(6)
            trak.pop(7)

    def rotate(self, Al):
        Al = Al % 6.28
        self.direction = Al
        self.current_shape.clear()
        for coord in self.shape0:
            x, y = coord[0], coord[1]
            x_ = self.x + x * cos(Al) + y * sin(Al)
            y_ = self.y + -x * sin(Al) + y * cos(Al)
            self.current_shape.append([x_, y_])

    def move(self):
        global f
        old_current_shape = self.current_shape
        self.x = self.x - self.speed * sin(self.direction)  # Пересчитываем новые координаты центра
        self.y = self.y - self.speed * cos(self.direction)  # Пересчитываем новые координаты центра
        self.rotate(self.direction)  # Одновременно будет повернуто и смщено на новые пересчитанные координат
        for wall in all_Wall:
            if collision(self, wall):
                self.current_shape = old_current_shape
                # self.direction += radians(1)
                # f = degrees(self.direction)

                # if collision(self, wall):
                #     self.direction -= radians(2)
                #     f = degrees(self.direction)
                #     self.current_shape = old_current_shape


    def __repr__(self):
        return f'X:{self.x} Y:{self.y}, color:{self.color}'


class Bullet:
    def __init__(self, x0, y0, dir, planned_distace, speed=10, color='red'):
        self.x0 = x0
        self.y0 = y0  # Start coords DO not change
        self.x = x0
        self.y = y0  # current position

        self.planned_distace = planned_distace  # Расстояние на котором пуля исчезнет
        self.distance_passed = 0  # Skolko proletela ot starta
        self.direction = dir
        self.speed = speed
        self.force = second
        self.color = color

    def draw_bullet(self):
        canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill=self.color)

    def move_bullet(self):
        self.x = self.x - self.speed * sin(self.direction)  # Пересчитываем новые координаты центра
        self.y = self.y - self.speed * cos(self.direction)  # Пересчитываем новые координаты центра
        self.distance_passed = (self.x0 - self.x) ** 2 + (self.y0 - self.y) ** 2  # Without ROOT !!


class Wall:
    def __init__(self, x0, y0, x1, y1, color='black'):
        self.up_left_angle = [x0, y0]
        self.down_rite_angle = [x1, y1]
        self.color = color
        self.flag = 0

    def destruction(self, if_hit):
        if if_hit:
            self.flag += 1

    def draw_wall(self):
        canvas.create_rectangle(self.up_left_angle[0], self.up_left_angle[1],
                                self.down_rite_angle[0], self.down_rite_angle[1], fill=self.color)


all_Tanks = []
all_Tanks.append(Tank(500, 500))
all_Bullets = []
all_Wall = []
all_Wall.append(Wall(800, 400, 1000, 500))
f = 0

t = 0  # Time of pressing "Space" for fire


def start_timer_(event):  # if Space pressed start countown
    actions['fire'] = 1


def end_timer_(event):  # Space button released
    if event.keysym == 'space':
        actions['fire'] = 0


def draw_sphere(x, y, r):
    canvas.create_arc(x - r, y - r, x + r, y + r, start=0, extent=359.9, style=ARC, outline='red', width=2)


def loop():  # Main Loop of the game
    canvas.delete('all')
    global f
    global t
    if actions['fire'] == 1:
        t += 20
        draw_sphere(all_Tanks[0].x, all_Tanks[0].y, t)
    else:  # Space button released Can start fire
        all_Bullets.append(Bullet(all_Tanks[0].x, all_Tanks[0].y, all_Tanks[0].direction, t))
        t = 0
    for bullet in all_Bullets:  # loop on Bullets
        if bullet.distance_passed > bullet.planned_distace ** 2:
            all_Bullets.remove(bullet)
        else:
            bullet.move_bullet()
            bullet.draw_bullet()

    tank = all_Tanks[0]

    if actions['right'] == 1:
        f -= 10
        tank.rotate(radians(f))
        actions['right'] = 0
    if actions["left"] == 1:
        f += 10
        tank.rotate(radians(f))
        actions["left"] = 0
    if actions['up'] == 1:
        tank.move()
        actions['up'] = 0
    if actions['down'] == 1:
        tank.speed *= -1
        tank.move()
        tank.speed *= -1
        actions['down'] = 0

    for tank in all_Tanks:  # loop on Tanks
        tank.draw_tank()

    for wall in all_Wall:
        for bullet in all_Bullets:
            if (bullet.x < wall.down_rite_angle[0]) and (bullet.x > wall.up_left_angle[0]) and (
                    bullet.y < wall.down_rite_angle[1]) and (bullet.y > wall.up_left_angle[1]):
                wall.destruction(1)
                all_Bullets.remove(bullet)
                if wall.flag == 2:
                    all_Wall.remove(wall)




        wall.draw_wall()

    root.after(10, loop)


loop()

canvas.bind_all('<KeyPress-Right>', right)
canvas.bind_all('<KeyPress-Left>', left)
canvas.bind_all('<KeyPress-Up>', up)
canvas.bind_all('<KeyPress-Down>', down)
canvas.bind_all('<space>', start_timer_)
root.bind_all("<KeyRelease>", end_timer_)

root.mainloop()

