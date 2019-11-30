# encoding:utf-8
_date_ = "2019/11/29 16:01"

import pygame
import random
import time
import os

def get_pic(path):
    # 拼接图片路径
    pic_path = os.path.join("img", path)
    # 返回pygame对象
    return pygame.image.load(pic_path)  # <Surface>

class HeroPlane():
    """英雄战机类"""

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.normal_image_list = ["hero1.png", "hero2.png"]
        self.normal_image_index = 0
        self.bomb_image_list = ["hero_blowup_n1.png", "hero_blowup_n2.png", "hero_blowup_n3.png","hero_blowup_n4.png", ]
        self.bomb_image_index = 0
        self.isBomb = False # 碰撞检测
        self.bullet_list = []
        self.hero_rect = pygame.rect.Rect(190, 526, 100, 124)

    def draw(self):
        if self.isBomb == False:  # 如果没有爆炸
            pic = get_pic(self.normal_image_list[self.normal_image_index])  # 获取图片
            self.screen.blit(pic, (self.x, self.y))  # 绘制英雄战机
            self.normal_image_index = (self.normal_image_index + 1) % len(self.normal_image_list)  # 利用取余运算进行循环
        else:
            if self.bomb_image_index == len(self.bomb_image_list):  # 当敌机爆炸图片的下表和图片总数相同时，说明爆炸图片已经绘制结束
                time.sleep(0.2)
                exit()
            enemy_bomb_img = get_pic(self.bomb_image_list[self.bomb_image_index])  # 加载英雄爆炸图片
            screen.blit(enemy_bomb_img, (self.x, self.y))  # 绘制敌机爆炸图片
            self.bomb_image_index += 1
            time.sleep(0.2)
        # 绘制子弹
        for bullet in self.bullet_list:
            bullet.draw()
            self.bullet_list.remove(bullet) if bullet.y < 0 else ""
            # 碰撞检测
            self.check_collide(bullet)

    def deal_event(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:  # 如果是退出事件
                exit(0)
            elif event.type == pygame.KEYDOWN:  # 检测鼠标按下事件
                if event.key == pygame.K_LEFT:
                    self.x = self.x - 5 if self.x >= 5 else 0
                elif event.key == pygame.K_RIGHT:  # 向右移动
                    self.x = self.x + 5 if self.x <= 480 - 100 - 5 else 480 - 100
                elif event.key == pygame.K_DOWN:  # 向下移动
                    self.y = self.y + 5 if self.y <= 650 - 124 - 5 else 0
                elif event.key == pygame.K_UP:  # 向上移动
                    self.y = self.y - 5 if self.y >= 5 else 0
                elif event.key == pygame.K_SPACE:
                    one_bullet = HeroBullet(self.x + 39, self.y - 22, screen)
                    self.bullet_list.append(one_bullet)

    def check_collide(self,bullet):
        """碰撞检测"""
        hero_bullet_rect = pygame.rect.Rect(bullet.x, bullet.y, 10, 10)  # 定义英雄子弹的rect
        flag = hero_bullet_rect.colliderect(enemy_plane.enemy_rect)  # 检测敌机和子弹的矩形是否相交
        if flag:
            print("敌机爆炸了......")
            enemy_plane.isBomb = True  # 敌机爆炸条件为真
            hero_plane.bullet_list.remove(bullet) # 移除战机子弹

class EnemyPlane():
    """敌机类"""

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.normal_image_list = ["enemy1.png"]
        self.normal_image_index = 0
        self.bomb_image_list = ["enemy1_down1.png", "enemy1_down2.png", "enemy1_down3.png", "enemy1_down4.png", ]
        self.bomb_image_index = 0
        self.isBomb = False
        self.bullet_list = []
        # 定义敌机精灵的rect
        self.enemy_rect = pygame.rect.Rect(206, 0, 50, 56)  # x= 480//2-69//2
        self.direct = "左"

    def draw(self):
        # 绘制
        if self.isBomb == False:  # 如果没有爆炸
            pic = get_pic(self.normal_image_list[self.normal_image_index])  # 获取图片
            self.screen.blit(pic, (self.x, self.y))  # 绘制敌机战机
            self.normal_image_index = (self.normal_image_index + 1) % len(self.normal_image_list)  # 利用循环让敌机进行循环
        else:
            if self.bomb_image_index == len(self.bomb_image_list):  # 当敌机爆炸图片的下表和图片总数相同时，说明爆炸图片已经绘制结束
                time.sleep(0.2)
                exit(0)  # 结束程序
            enemy_bomb_img = get_pic(self.bomb_image_list[self.bomb_image_index])  # 加载敌机爆炸图片
            screen.blit(enemy_bomb_img, (self.x, self.y))  # 绘制敌机爆炸图片
            self.bomb_image_index += 1
            time.sleep(0.2)
        # 调用移动函数
        self.move()
        # 敌机开火
        self.fire()

    def move(self):
        """让敌机移动"""
        if self.direct == "左":
            self.x -= 5
            if self.x <= 0:
                self.direct = "右"
        elif self.direct == "右":
            self.x += 5
            if self.x >= 480 - 69:
                self.direct = "左"

    def fire(self):
        """敌机子弹"""
        # 画出敌机子弹
        # 产是生随机数
        x = random.randint(0, 100)
        if x == 5 or x == 78:
            # 实例化一个子弹
            enemy_bullet = EnemyBullet(self.x + 69 // 2 - 9 // 2, self.y + 89, screen)
            # 产生的每一个子弹放到一个列表里
            self.bullet_list.append(enemy_bullet)
        for bullet in self.bullet_list:
            bullet.draw()  # 绘制子弹
            self.bullet_list.remove(bullet) if bullet.y > 650 - 89 - 21 // 2  else ""  # 让子弹到最下面的时候消失
            # 检测敌机爆炸
            self.check_collide(bullet)

    def check_collide(self,bullet):
        """碰撞检测"""
        enemy_bullet_rect = pygame.rect.Rect(bullet.x, bullet.y, 9, 21)  # 定义英雄子弹的rect
        flag = enemy_bullet_rect.colliderect(hero_plane.hero_rect)  # 检测敌机和子弹的矩形是否相交
        if flag:
            print("英雄机爆炸了......")
            hero_plane.isBomb = True  # 爆炸条件为真
            enemy_plane.bullet_list.remove(bullet) # 移除战机子弹

class HeroBullet():
    """
    英雄精灵子弹的类
    """

    def __init__(self, x, y, screen):
        """
        :param x: x坐标
        :param y: y 坐标
        :param screen: 窗口对象
        """
        self.x = x
        self.y = y
        self.screen = screen
        self.pic = get_pic("bullet.png")

    def draw(self):
        """用来画子弹"""
        self.screen.blit(self.pic, (self.x, self.y))
        self.move()

    def move(self):
        self.y -= 5

class EnemyBullet():
    """敌机精灵子弹类"""

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.pic = get_pic("bullet1.png")

    def draw(self):
        """用来画子弹"""
        self.screen.blit(self.pic, (self.x, self.y))
        self.move()

    def move(self):
        self.y += 5

# 游戏初始化
pygame.init()
# 设置背景图片
screen = pygame.display.set_mode((480, 650))
# 设置标题
pygame.display.set_caption("飞机大战")
# 设置图标
pygame.display.set_icon(get_pic("icon72x72.png"))
# 设置按键灵敏度
pygame.key.set_repeat(20, 30)
# 实例化英雄飞机对象
hero_plane = HeroPlane(480 // 2 - 100 // 2, 650 - 124, screen)
# 实例化敌机对象
enemy_plane = EnemyPlane(480 // 2 - 69 // 2, 0, screen)

while True:
    # 绘制背景图
    bg = get_pic("background.png")
    screen.blit(bg, (0, 0))
    hero_plane.draw()  # 绘制英雄精灵
    enemy_plane.draw()  # 绘制敌机精灵
    hero_plane.deal_event(pygame.event.get())  # 事件检测
    pygame.display.update()
