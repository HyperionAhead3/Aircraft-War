import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 512, 768)
# 定时器时钟常数
FRAME_PER_SEC = 60

# 创建敌机的定时器常量
CREAT_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprites(pygame.sprite.Sprite):
    def __init__(self, image_name, speed = 1):

        # 调用父类的初始化方法
        super().__init__()

        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 图片向下移动
        self.rect.y += self.speed


class Background(GameSprites):
    """
    游戏背景精灵
    """
    def __init__(self, is_alt=False):
        # 调用父类方法,实现精灵和精灵组的创建(image/rect/speed)
        super().__init__("./images/img_bg_level_1.jpg")
        # 判断是否是交替图像
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 调用父类的方法实现
        super().update()
        # 判断是否移出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprites):
    """敌机精灵"""
    def __init__(self):
        # 调用父类的初始化
        super().__init__("./images/a2-1.png")
        # 指定敌机的初始随机速度
        self.speed = random.randint(1, 3)
        # 指定敌机的初始随机位置
        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 调用父类方法
        super().update()
        # 判断敌机是否飞出屏幕，是则从精灵组中删除
        if self.rect.y >= SCREEN_RECT.height:
            # print("敌机飞出了屏幕")
            self.kill()

    def __del__(self):
        # print("敌机挂了")
        pass


class Hero(GameSprites):
    def __init__(self):
        # 调用父类方法
        super().__init__("./images/me1.png", 0)
        # 设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄在水平移动
        self.rect.x += self.speed
        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rec .x = 0
        elif self.rect.x > SCREEN_RECT.right:
            self.rect.x = SCREEN_RECT.right

    def fire(self):
        print("发射子弹事件")
        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet()
            # 设置子弹精灵组的位置
            bullet.rect.bottom = self.rect.y - i*20
            bullet.rect.centerx = self.rect.centerx
            # 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprites):
    """子弹精灵"""
    def __init__(self):
        # 调用父类方法
        super().__init__("./images/p-f02.png", -2)

    def update(self):
        # 调用父类方法
        super().update()

        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print("子弹被销毁")
        pass
