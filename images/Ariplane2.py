import pygame
import time
from pygame import locals
import random


class HeroPlane:
    def __init__(self, x, y, screen_temp, plane_image_temp):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.plane_image = pygame.image.load(plane_image_temp)
        self.bullet_list = []

        self.hit = False  # 表示是否要爆炸
        self.bomb_list = []  # 用来存储爆炸时需要的图片
        self.__crate_images()  # 调用这个方法向bomb_list中添加图片
        self.image_num = 0  # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号

    def __crate_images(self):
        self.bomb_list.append(pygame.image.load("./images/me_die1.png"))
        self.bomb_list.append(pygame.image.load("./images/me_die2.png"))
        self.bomb_list.append(pygame.image.load("./images/me_die3.png"))
        self.bomb_list.append(pygame.image.load("./images/me_die4.png"))

    def display(self, screen_temp):

        if self.hit == True:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:
                self.image_num = 0
                self.image_index += 1
            if self.image_index > 3:
                time.sleep(1)
                exit()  # 调用exit让游戏退出
                # self.image_index = 0
        else:
            screen_temp.blit(self.plane_image, (self.x, self.y))
            for bullet in self.bullet_list:
                bullet.display(self.screen)
                bullet.move()
                bullet_pop_list = []
                if bullet.judge(self.y):
                    bullet_pop_list.append(bullet)
                    for bullet_pop in bullet_pop_list:
                        self.bullet_list.remove(bullet_pop)
                else:
                    pass

    def move(self, right_left, up_down):
        self.x += right_left
        self.y += up_down

    def fire(self):
        self.bullet_list.append(HeroBullet(self.x + 40, self.y - 20, self.screen))

    def bomb(self):
        self.hit = True

class EnemyPlane:
    def __init__(self, x, y, screen_temp, plane_image_temp):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.plane_image = pygame.image.load(plane_image_temp)

        self.bullet_list = []

        self.hit = False  # 表示是否要爆炸
        self.bomb_list = []  # 用来存储爆炸时需要的图片
        self.__crate_images()  # 调用这个方法向bomb_list中添加图片
        self.image_num = 0  # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号
        self.direction = 'right'
    def __crate_images(self):
        self.bomb_list.append(pygame.image.load("./images/plain1_die1.png"))
        self.bomb_list.append(pygame.image.load("./images/plain1_die2.png"))
        self.bomb_list.append(pygame.image.load("./images/plain1_die3.png"))

    def display(self, screen_temp):
        if self.hit == True:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:
                time.sleep(0.8)
                self.image_num = 0
                self.image_index += 1
            if self.image_index > 2:
                # time.sleep(1)
                # exit()  # 调用exit让游戏退出
                self.image_index = 0
                # pass
        else:
            screen_temp.blit(self.plane_image, (self.x, self.y))
            for bullet in self.bullet_list:
                bullet.display(self.screen)
                bullet.move()
                if bullet.judge():
                    bullet_pop_list = []
                    bullet_pop_list.append(bullet)
                    for bullet_pop in bullet_pop_list:
                        self.bullet_list.remove(bullet_pop)

    def move(self):

        if self.direction == 'right':
            self.x += 0.5
            self.y += 0.5
            if self.x >= 430:
                self.direction = 'left'

        elif self.direction == 'left':
            self.x -= 1
            self.y += 1
            if self.x <= 0:
                self.direction = 'right'

    def bomb(self):
        self.hit = True

    def fire(self):
        randint_num = random.randint(1, 600)
        if randint_num == 7 or randint_num == 88:
            self.bullet_list.append(EnemyBullet(self.x, self.y, self.screen))

    def judge(self):
        if self.y > 853:
            return True
        else:
            return False

class HeroBullet:
    def __init__(self, x, y, screen_temp):
        self.x = x
        self.y = y
        self.plane_image = pygame.image.load('./images/bullet_1.png')

    def display(self, screen_temp):
        screen_temp.blit(self.plane_image, (self.x, self.y))

    def move(self):
        self.y -= 4

    def judge(self, heroplane_x):
        if self.y < heroplane_x - 500 or self.y < 0:
            return True
        else:
            return False

class EnemyFactory:
    def __init__(self, screen_temp):
        self.screen = screen_temp
        self.enemy_list = []

    def product(self):
        randint_num = random.randint(1, 100000)
        if randint_num > 99000:
            randint_x = random.randint(0, 420)
            self.enemy_list.append(EnemyPlane(randint_x, -36, self.screen, './images/plain1.png'))

    def display(self, screen_temp):
        for enemy in self.enemy_list:
            enemy.display(screen_temp)
            enemy.move()
            enemy.fire()
            enemy_pop_list = []
            if enemy.judge():
                enemy_pop_list.append(enemy)
                for enemy_pop in enemy_pop_list:
                    self.enemy_list.remove(enemy_pop)

class EnemyBullet:
    def __init__(self, x, y, screen_temp):
        self.x = x
        self.y = y
        self.plane_image = pygame.image.load('./images/bullet.png')

    def display(self, screen_temp):
        screen_temp.blit(self.plane_image, (self.x + 20, self.y + 40))

    def move(self):
        self.y += 2

    def judge(self):
        if self.y > 853:
            return True
        else:
            return False

class GamePanel:
    def control(self, hero):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                exit()

            elif event.type == locals.KEYDOWN:

                if event.key == locals.K_a or event.key == locals.K_LEFT:
                    hero.move(-10, 0)

                elif event.key == locals.K_d or event.key == locals.K_RIGHT:
                    hero.move(+10, 0)

                elif event.key == locals.K_w or event.key == locals.K_UP:
                    hero.move(0, -10)
                elif event.key == locals.K_s or event.key == locals.K_DOWN:
                    hero.move(0, +10)
                elif event.key == locals.K_b:
                    hero.bomb()
                elif event.key == locals.K_SPACE:
                    hero.fire()

    def shoot(self, enemy_factory_temp, hero_temp, screen_temp):
        for enemy in enemy_factory_temp.enemy_list:
            for bullet in hero_temp.bullet_list:
                bullet_pop_list = []
                enemy_pop_list = []
                if ((bullet.x >= enemy.x) and (bullet.x <= enemy.x + 36)) and (
                    (bullet.y >= enemy.y) and bullet.y <= enemy.y + 59):
                    bullet_pop_list.append(bullet)
                    enemy_pop_list.append(enemy)
                    for bullet_pop, enemy_pop in zip(bullet_pop_list, enemy_pop_list):
                        enemy_pop.bomb()
                        enemy_pop.display(screen_temp)
                        hero_temp.bullet_list.remove(bullet_pop)
                        enemy_factory_temp.enemy_list.remove(enemy_pop)

            if ((enemy.x + 36 >= hero_temp.x) and (enemy.x + 36 <= hero_temp.x + 98)) and (
                (enemy.y + 59 >= hero_temp.y) and (enemy.y + 59 <= hero_temp.y + 122)):
                hero_temp.bomb()
                enemy.bomb()
                enemy.display(screen_temp)
                hero_temp.display(screen_temp)

            for bullet in enemy.bullet_list:
                if ((bullet.x >= hero_temp.x) and (bullet.x <= hero_temp.x + 98)) and (
                    (bullet.y >= hero_temp.y) and (bullet.y <= hero_temp.y + 122)):
                    hero_temp.bomb()
                    hero_temp.display(screen_temp)

    def main(self):
        # 创建一个window
        screen = pygame.display.set_mode((480, 853), 0, 32)
        # 背景图片
        back_image = pygame.image.load('./images/bg.jpg')
        # 英雄飞机
        hero = HeroPlane(180, 700, screen, './images/me.png')
        # 地方飞机
        # enemy = EnemyPlane(200,0,screen,'./images/plain1.png')
        # 敌方飞机工厂
        enemy_factory = EnemyFactory(screen)

        temp = False

        while True:
            screen.blit(back_image, (0, 0))  # 将背景图片放入window
            self.control(hero)
            hero.display(screen)
            enemy_factory.product()
            enemy_factory.display(screen)
            self.shoot(enemy_factory, hero, screen)
            pygame.display.update()  # 刷新
            time.sleep(0.01)  # 防止内存占用率过高

if __name__ == '__main__':
    gamepanel = GamePanel()
    gamepanel.main()
