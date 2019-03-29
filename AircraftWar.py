import pygame
from pygame.locals import *
import time
import random
class Base(object):
	"""抽取基类"""
	def __init__(self, screen_temp,x,y,image_name):
		self.x = x
		self.y = y
		self.image = pygame.image.load(image_name)
		self.screen = screen_temp
		
class BasePlane(Base):
	"""抽取飞机基类"""
	def __init__(self,screen_temp,x,y,image_name):
		Base.__init__(self,screen_temp,x,y,image_name)
		self.bullet_list = []
		
class HeroPlane(BasePlane):
	'''玩家英雄'''
	def __init__(self,screen_temp):
		BasePlane.__init__(self,screen_temp,195,600,"./飞机大战/images/me1.png")

		#爆炸效果用的如下属性
		self.hit = False #表示是否要爆炸
		self.bomb_list = [] #用来存储爆炸时需要的图片
		self.__crate_images() #调用这个方法向bomb_list中添加图片
		self.image_num = 0#用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
		self.image_index = 0#用来记录当前要显示的爆炸效果的图片的序号

	def __crate_images(self):
		self.bomb_list.append(pygame.image.load("./飞机大战/images/hero_blowup_n1.png"))
		self.bomb_list.append(pygame.image.load("./飞机大战/images/hero_blowup_n2.png"))
		self.bomb_list.append(pygame.image.load("./飞机大战/images/hero_blowup_n3.png"))
		self.bomb_list.append(pygame.image.load("./飞机大战/images/hero_blowup_n4.png"))

	
	def display(self):
		if self.hit == True:
			self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
			self.image_num+=1
			if self.image_num == 7:
				self.image_num=0
				self.image_index+=1
			if self.image_index>3:
				time.sleep(1)
				exit()#调用exit让游戏退出
				#self.image_index = 0
		else:
			self.screen.blit(self.image,(self.x,self.y))
		
		for bullet in self.bullet_list:
			bullet.display()
			bullet.move()
			if bullet.judge():#判断子弹是否越界
				self.bullet_list.remove(bullet)

	def move_left(self):
		self.x -= 15
	def move_right(self):
		self.x += 15
	def fire(self):
		self.bullet_list.append(Bullet(self.screen,self.x,self.y))
	def bomb(self):
		self.hit = True
class EnemyPlane(BasePlane):
	'''敌机类'''
	def __init__(self,screen_temp):
		BasePlane.__init__(self,screen_temp,0,0,"./飞机大战/images/a2-1.png")
		self.direction = "right"

	def display(self):
		self.screen.blit(self.image,(self.x,self.y))
		for bullet in self.bullet_list:
			bullet.display()
			bullet.move()
			if bullet.judge():#判断子弹是否越界
				self.bullet_list.remove(bullet)

	def move(self):
		if self.direction == "right":
			self.x += 5
		elif self.direction == "left":
			self.x -= 5
		if self.x > 512-58:
			self.direction = "left"
		elif self.x < 0:
			self.direction = "right"

	def fire(self):
		random_num = random.randint(1,50)
		if random_num == 10 or random_num == 20:
			self.bullet_list.append(EnemyBullet(self.screen,self.x,self.y))

class BaseBullet(Base):
	"""抽取子弹基类"""
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))
		
class Bullet(BaseBullet):
	"""英雄子弹类"""
	def __init__(self, screen_temp,x,y):
		BaseBullet.__init__(self,screen_temp,x+30,y-20,"./飞机大战/images/p-f02.png")
	def move(self):
		self.y -= 5
	def judge(self):
		if self.y < 0:
			return True
		else:
			return False
class EnemyBullet(BaseBullet):
	"""敌机子弹类"""
	def __init__(self, screen_temp,x,y):
		BaseBullet.__init__(self,screen_temp,x+20,y+69,"./飞机大战/images/buttle2.png")
	def move(self):
		self.y += 5
	def judge(self):
		if self.y > 768:
			return True
		else:
			return False

def key_control(hero_temp):
	#获取按键
	for event in pygame.event.get():
		#判断是否点击了退出按钮
		if event.type == QUIT:
			print("exit")
			exit()
		#判断
		elif event.type == KEYDOWN:
			#检测按键是否是a或者left
			if event.key == K_a or event.key == K_LEFT:
				print('left')
				hero_temp.move_left()
			#检测按键是否是d或者right
			elif event.key == K_d or event.key == K_RIGHT:
				print('right')
				hero_temp.move_right()
			elif event.key == K_SPACE:
				print('space')
				hero_temp.fire()
			elif event.key == K_b:
				print('b')
				hero_temp.bomb()

def main():
	#1.创建窗口
	screen = pygame.display.set_mode((512,768),0,32)
	#2.创建背景图片
	backgroud = pygame.image.load("./飞机大战/images/img_bg_level_1.jpg")
	#3.创建飞机对象
	hero = HeroPlane(screen)
	#4.创建一个敌机
	enemy = EnemyPlane(screen)
	while True:
		screen.blit(backgroud,(0,0))
		hero.display()
		enemy.display()
		enemy.move()  #调用敌机的移动
		enemy.fire()
		pygame.display.update()

		key_control(hero)

		time.sleep(0.02)

if __name__ == "__main__":
	main()
