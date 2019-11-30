import random
import pygame
import time


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
        self.pic = pygame.image.load("img/bullet.png")

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
        self.pic = pygame.image.load("img/bullet1.png")

    def draw(self):
        """用来画子弹"""
        self.screen.blit(self.pic, (self.x, self.y))
        self.move()

    def move(self):
        self.y += 5


pygame.init()  # 游戏初始化
# 使用变量screen 接收返回值，代表整个窗口对象
screen = pygame.display.set_mode((480, 650))  # 元组中320表示宽度， 568表示高度
# 修改游戏名称
pygame.display.set_caption("飞机大战")
# 修改游戏图标
icon = pygame.image.load("img/icon72x72.png")
pygame.display.set_icon(icon)
# 加载背景图片
bg_img = pygame.image.load("img/background.png")
# 加载英雄飞机
hero_img1 = pygame.image.load("img/hero1.png")
hero_img2 = pygame.image.load("img/hero2.png")
# 加载英雄爆炸图片
hero_bomb_list = ["img/hero_blowup_n1.png", "img/hero_blowup_n2.png", "img/hero_blowup_n3.png","img/hero_blowup_n4.png"]
# 加载敌机精灵
enemy_img = pygame.image.load("img/enemy1.png")
# 加载敌机爆炸图片
enemy_bomb_list = ["img/enemy1_down1.png", "img/enemy1_down2.png", "img/enemy1_down3.png",
                   "img/enemy1_down4.png"]

heroIndexShift = 0
# 定义英雄飞机的rect
hero_rect = pygame.rect.Rect(190, 526, 100, 124)
# 定义敌机精灵的rect
enemy_rect = pygame.rect.Rect(206, 0, 50, 56)  # x= 480//2-69//2
# 敌机精灵的x,y轴坐标
enemyPlaneX = enemy_rect.x
enemyPlaneY = enemy_rect.y
direct = '左'  # 定义敌机初始移动方向
# 创建游戏时钟
clock = pygame.time.Clock()
# 英雄精灵的x,y轴坐标
heroPlaneX = hero_rect.x
heroPlaneY = hero_rect.y
pygame.key.set_repeat(20, 30)  # 重复按键操作
# 存放英雄机子弹的列表
HeroBiulist = []
# 存放敌机子弹列表
EnemyBiulist = []
enemy_is_bomb = False  # 敌机爆炸条件
enemy_bomb_index = 0  # 敌机爆炸图片索引
hero_is_bomb = False # 英雄机爆炸条件
hero_bomb_index = 0  # 英雄机爆炸图片索引
while True:  # 游戏循环 ->意味着游戏正式开始
    clock.tick(60)  # 60表示每秒钟刷新60次
    # 将背景图片加载到窗口中，（0,0）表示背景图片放到原点位置
    screen.blit(bg_img, (0, 0))
    # 修改英雄飞机的y轴值
    hero_rect.y -= 1
    # 让英雄精灵飞机从底部飞进
    if hero_rect.bottom <= 0:
        hero_rect.y = 650

    # 将英雄的飞机绘制到窗口上
    if heroIndexShift == 0:
        screen.blit(hero_img1, (heroPlaneX, heroPlaneY))
        heroIndexShift += 1
    else:
        screen.blit(hero_img2, (heroPlaneX, heroPlaneY))
        heroIndexShift = 0

    # 获取所有的事件
    event_list = pygame.event.get()
    #  捕获窗口退出事件
    for event in event_list:
        if event.type == pygame.QUIT:  # 加上这个模块就不卡了
            print("游戏结束了.......")
            pygame.quit()  # 卸载模块
            exit(0)  # 终止Python程序， exit(0)表示正常退出    exit(1)表示异常退出
        # 控制英雄精灵移动
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 向左移动
                heroPlaneX = heroPlaneX - 5 if heroPlaneX >= 5 else 0
            elif event.key == pygame.K_RIGHT:  # 向右移动
                heroPlaneX = heroPlaneX + 5 if heroPlaneX <= 375 else 380
            elif event.key == pygame.K_DOWN:  # 向下移动
                heroPlaneY = heroPlaneY + 5 if heroPlaneY <= 521 else 526
            elif event.key == pygame.K_UP:  # 向上移动
                heroPlaneY = heroPlaneY - 5 if heroPlaneY >= 5 else 0
            elif event.key == pygame.K_SPACE:  # 英雄机控制发射子弹
                hero_bullet = HeroBullet(heroPlaneX + 50 - 11, heroPlaneY - 22, screen)
                HeroBiulist.append(hero_bullet)

    # # 绘制敌机精灵
    # screen.blit(enemy_img, (enemyPlaneX, enemyPlaneY))
    # 控制敌机精灵移动
    if direct == "左":
        enemyPlaneX -= 5
        if enemyPlaneX <= 0:
            direct = "右"
    elif direct == "右":
        enemyPlaneX += 5
        if enemyPlaneX >= 480 - 69:
            direct = "左"

    # 画出英雄战机的子弹每一个子弹
    for bullet in HeroBiulist:
        bullet.draw()  # 绘制子弹
        # 让子弹到最上边的时候消失
        HeroBiulist.remove(bullet) if bullet.y < 0 else ""
        hero_bullet_rect = pygame.rect.Rect(bullet.x, bullet.y, 10, 10)  # 定义英雄子弹的rect
        flag = hero_bullet_rect.colliderect(enemy_rect)  # 检测敌机和子弹的矩形是否相交
        if flag:
            print("敌机爆炸了......")
            enemy_is_bomb = True  # 爆炸条件为真
            HeroBiulist.remove(bullet)

    # 绘制敌机爆炸的图片
    if enemy_is_bomb == False:
        # 如果没有检测到爆炸，就绘制没有爆炸敌机的图片
        screen.blit(enemy_img, (enemyPlaneX, enemyPlaneY))
    else:  # 绘制敌机爆炸
        if enemy_bomb_index == len(enemy_bomb_list):  # 当敌机爆炸图片的下表和图片总数相同时，说明爆炸图片已经绘制结束
            time.sleep(0.2)
            exit(0)  # 结束程序
        enemy_bomb_img = pygame.image.load(enemy_bomb_list[enemy_bomb_index])  # 加载敌机爆炸图片
        screen.blit(enemy_bomb_img, (enemyPlaneX, enemyPlaneY))  # 绘制敌机爆炸图片
        enemy_bomb_index += 1
        time.sleep(0.2)

    # 画出敌机子弹
    # 产是生随机数
    x = random.randint(0, 100)
    if x == 5 or x == 78:
        # 实例化一个子弹
        enemy_bullet = EnemyBullet(enemyPlaneX + 69 // 2 - 9 // 2, enemyPlaneY + 89, screen)
        # 产生的每一个子弹放到一个列表里
        EnemyBiulist.append(enemy_bullet)
    for bullet in EnemyBiulist:
        bullet.draw()  # 绘制子弹
        EnemyBiulist.remove(bullet) if bullet.y > 650 - 89 - 21 // 2  else ""  # 让子弹到最下面的时候消失
        enemy_bullet_rect = pygame.rect.Rect(bullet.x, bullet.y, 9, 21)  # 定义敌机子弹rect
        flag = enemy_bullet_rect.colliderect(hero_rect)  # 英雄机爆炸的条件
        if flag:
            print("英雄爆炸了.....")
            hero_is_bomb = True  # 爆炸条件为真
            EnemyBiulist.remove(bullet)# 当战机爆炸的时候，移除子弹

    if hero_is_bomb == False:
        # 将英雄的飞机绘制到窗口上
        if heroIndexShift == 0:
            screen.blit(hero_img1, (heroPlaneX, heroPlaneY))
            heroIndexShift += 1
        else:
            screen.blit(hero_img2, (heroPlaneX, heroPlaneY))
            heroIndexShift = 0
    else:
        if hero_bomb_index == len(hero_bomb_list):# 当爆炸图片加载结束后
            time.sleep(0.3)
            exit()
        # 加载英雄机爆炸图片
        hero_bomb_img = pygame.image.load(hero_bomb_list[hero_bomb_index])
        # 绘制英雄机爆炸的图片
        screen.blit(hero_bomb_img,(heroPlaneX,heroPlaneY))
        hero_bomb_index += 1
        time.sleep(0.2)
    pygame.display.update()
