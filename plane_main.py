from plane_sprites import *


class PlaneGame(object):
    """
    飞机大战主程序
    """

    def __init__(self):
        print("游戏初始化")
        # 1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵组创建
        self.creat_sprites()
        # 4. 设置定时器事件，创建敌机
        pygame.time.set_timer(CREAT_ENEMY_EVENT, 1000)
        # 4. 设置定时器事件，创建子弹
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def creat_sprites(self):
        # 创建背景精灵
        bg1 = Background()
        bg2 = Background(True)
        # bg2.rect.y = -bg2.rect.height
        self.back_ground = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_ground = pygame.sprite.Group()

        # 创建英雄和英雄精灵组
        self.hero = Hero()
        self.hero_ground =pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始")
        while True:
            # 1设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2设置监听
            self.__event_handler()
            # 3.设置碰撞检测
            self.__check_collid()
            # 4.更新精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()

            elif event.type == CREAT_ENEMY_EVENT:
                # print("敌机出现")
                # 创建敌机精灵，
                enemy = Enemy()
                # 将敌机精灵添加到精灵组
                self.enemy_ground.add(enemy)

            elif event.type ==HERO_FIRE_EVENT:
                self.hero.fire()

            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                # print("向右移动")
        # 使用键盘提供的方法
        key_pressed = pygame.key.get_pressed()
        # 判断元组中的键值
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collid(self):
        # 销毁敌机（两个精灵组碰撞检测）
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_ground, True, True)
        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_ground, True)
        if len(enemies) > 0:
            # 让英雄牺牲
            self.hero.kill()
            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.back_ground.update()
        self.back_ground.draw(self.screen)
        self.enemy_ground.update()
        self.enemy_ground.draw(self.screen)
        self.hero_ground.update()
        self.hero_ground.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")

        pygame.quit()
        exit()

if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()
    # 游戏启动
    game.start_game()
