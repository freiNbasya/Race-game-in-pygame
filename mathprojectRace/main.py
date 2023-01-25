import pgzrun
import random
from pgzhelper import *

#В папці з проєктом має бути також відео-інструкція

#розмірність вікна гри
WIDTH = 900
HEIGHT = 700

#діставання та програвання музичного файлу з відповідної папки
music.play("deja_vu.mp3")
music.set_volume(0.3)



class Car(Actor):
    def __init__(self, x, y):
        # super() відповідає за успадкування властивостей іншого певного класу, в цьому випадку класу Actor
        super().__init__("car.png", (x,y))
        # оголошення змінних кута та швидкості
        self.angle = 0
        self.speed = 0
    # функція яка використовує вбудованний метод переміщення вперед
    def move(self):
        self.move_forward(self.speed)
    
    #ф-ія яка повертає машину використовуючи характеристику успадковану з класу Actor
    def rotate(self, turnAngle):
        self.angle += turnAngle
        self.angle = self.angle % 360
        
    # ф-ія збільшення швидкості
    def accelerate(self):
        self.speed += 0.02
    # ф-ія зменшення швидкості/гальмування
    def brake(self):
        self.speed -= 0.02
    # ф-ія яка змінює/перевіряє стан машинки
    def update(self):

        global lives
        global game_finish
        # перевірка  того чи вдарилася машинка в бічні границя вікна гри
        if self.x > WIDTH or self.x < 0:
            lives -=1
            car.x = 50
            car.y = 50
            car.speed = 0
        #  перевірка того чи вдарилася машинка в верхню/нижню границі вікна
        if self.y > HEIGHT or self.y < 0:
            lives -=1
            car.x = 50
            car.y = 50
            car.speed = 0
        # в обидвах випадках при виконанні умови, гравець втрачає життя та машинка повератається на початкові координати
        # закінчення гри якщо у гравця закінчились життя
        if lives == 0:
            game_finish = True
        # зчитування клавіші яку натиснув гравець, та відповідно до цього виконується певна ф-ія обертання/пришвидшення/сповільнення
        if keyboard.left:
            self.rotate(5)    
        elif keyboard.right:
            self.rotate(-5)
        if keyboard.up:
            self.accelerate()
        elif keyboard.down:
            self.brake()
        
        self.move()
#створення списку перешкод та заповнення його екземплярами класу Actor які мають випадкові координати
obstacles = []
for i in range(25):
    obstacles.append(Actor("obstacle.png", (random.randint(80, 900)+10, random.randint(0, 690)+10)))
    
#стоверння екземляру класу Actor для фінішу
finish_line = Actor("finish.png", (800, 690))
#стоверння екземляру класу Car
car = Car(30, 30)
#ф-ія перевірки стикання автомобіля та перешкоди задопомогою вбудованого метода, при виконнані умови відбуваються ті самі
#що і при вдарянні в границі вікна
def check_collision():
    global game_finish
    global lives
    for obstacle in obstacles:
        if car.colliderect(obstacle):
            lives -=1
            car.x = 50
            car.y = 50
            car.speed =0
        if lives == 0:
            game_finish = True
            
#перевірка того чи перетнув автомобіль фініш, при виконанні умови - гравець перемагає
def check_finish():
    global game_finish
    global game_won
    if car.colliderect(finish_line):
        game_finish = True
        game_won = True
#логічні змінні які відповідають за стан гри
game_finish = False
game_won = False
#к-сть життів
lives = 3

#ф-ія бібліотеки pygame zero яка відповідає за виведення об'єктів на екран
def draw():
    #перевірка того чи закінчилась гра і якщо так то чи перемогою гравця
    if game_finish:
        #очищення екрану
        screen.clear()
        if game_won:
            #виведення на екран певного зображення як бекграунду
            screen.blit("win_screen.png", (0,0))
            #виведення напису про перемогу/(нижче) поразки гравця
            screen.draw.text("You won!", (360, 300), color=(255,255,255), fontsize=60)
        else:
            screen.draw.text("You lost!", (360, 300), color=(255,255,255), fontsize=60)
    else:
        screen.clear()
        #виведення на екран ігрового поля
        screen.blit("track_b.png", (0, 0))
        # виведення на екран машинки
        car.draw()
        #проходження по списку з перешкодами та при невиконанні умови, виведення їх на екран
        for obstacle in obstacles:
            #ця перевірка має звести до мінімуму, якщо не повністю прибрати, ситуації коли при випадковій генерації
            #перешкод, ці самі перешкоди повністю закривають доступ до фінішу або з'являються прямо на машині
            if  (obstacle.pos[0] > 730 and  obstacle.pos[1] > 630) or (obstacle.pos[0] < 100 and obstacle.pos[1] < 100):
                continue
            else:
                obstacle.draw()
        #виведення на екран фінішу
        finish_line.draw()
        #виведення на екран к-сть життів
        for i in range(lives):
            screen.blit("takumi_h.png", (30*i, 650))
#також ф-ія бібліотеки pygame zero яка відповідає за оновлення об'єктів, викликається 60 разів на секунду
def update():
    #оновлення стану машинки та послідуючи перевірки зіткнень з певними об'єктами
    car.update()
    check_collision()
    check_finish()
    # перемикачі музики
    if keyboard[keys.P]:
        music.pause()
    if keyboard[keys.R]:
        music.unpause()

    
#початок роботи програми
pgzrun.go()