import pygame
from pygame import Vector2
from pygame import mixer
from pygame.locals import *
import os

s_w = 600
s_h = 600
screen_size = Vector2(600, 600)

menu = True
run = True
game = True

screen = pygame.display.set_mode(screen_size)

background = (0, 0, 0)

pygame.init()
mixer.init()

if os.path.exists("sfx"):
    if os.path.exists("sfx/score.mp3"):
        score = pygame.mixer.Sound("sfx/score.mp3")
    else:
        print("Could not find SFX: score.mp3")

def intersect_rectangle_circle(target_pos, sx, sy,
                               ball_pos, ball_radius, ball_speed):

    top = (target_pos.y) - ball_pos.y
    bottom = (target_pos.y + sy) - ball_pos.y
    left = (target_pos.x) - ball_pos.x
    right = (target_pos.x + sx) - ball_pos.x

    r = ball_radius
    intersecting = left <= r and top <= r and right >= -r and bottom >= -r

    if intersecting:
        impulse = ball_speed
        if abs(left) <= r and impulse.x > 0:
            impulse.x = -impulse.x
        if abs(right) <= r and impulse.x < 0:
            impulse.x = -impulse.x
        if abs(top) <= r and impulse.y > 0:
            impulse.y = -impulse.y
        if abs(bottom) <= r and impulse.y < 0:
            impulse.y = -impulse.y
        return impulse
    return None


class p1:
	def __init__(self):
		self.width = 100
		self.height = 10
		self.position = Vector2(300, 580)
		self.col = (233, 43, 13)
		self.rect = Rect(self.position.x, self.position.y, self.width, self.height)
		self.speed = 10
	
	def move(self):
		self.direction = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = -1
		if key[pygame.K_RIGHT] and self.rect.right < s_w:
			self.rect.x += self.speed
			self.direction = 1

	def draw(self):
		pygame.draw.rect(screen, self.col, self.rect)

	def reset(self):
		self.__init__()

class p2:
	def __init__(self):
		self.width = 100
		self.height = 10
		self.position = Vector2(300, 10)
		self.col = (233, 43, 13)
		self.rect = Rect(self.position.x, self.position.y, self.width, self.height)
		self.speed = 10
	
	def move(self):
		self.direction = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_a] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = -1
		if key[pygame.K_d] and self.rect.right < s_w:
			self.rect.x += self.speed
			self.direction = 1

	def draw(self):
		pygame.draw.rect(screen, self.col, self.rect)

	def reset(self):
		self.__init__()

class ball:
	def __init__(self):
		self.radius = 5
		self.position = Vector2(300,300)
		self.color = (213, 44, 124)
		self.speed = Vector2(4, -4)
		self.stat = 0
	def move(self):

		if self.position.y > screen_size.y:
			#self.speed.y *= -1
			#p2 wins
			self.stat = 2
			#print("Bottom")
		if self.position.y < 0:
			#self.speed.y *= -1
			#p1 wins
			self.stat = 1
			#print("Top")
		if self.position.x > screen_size.x:
			self.speed.x *= -1
			#print("Right")
		if self.position.x < 0:
			self.speed.x *= -1
			#print("Left")

		collision_p1 = intersect_rectangle_circle(player1.rect, player1.width, 
													player1.height, self.position, 
													self.radius, self.speed)

		collision_p2 = intersect_rectangle_circle(player2.rect, player2.width, 
													player2.height, self.position, 
													self.radius, self.speed)

		collision_obscl = intersect_rectangle_circle(obstacle.rect, obstacle.width, 
													obstacle.height, self.position, 
													self.radius, self.speed)

		self.position += self.speed

		return self.stat

	def draw(self):
		pygame.draw.circle(screen, self.color, self.position, self.radius)

	def reset(self):
		self.__init__()

class obscl:
	def __init__(self):
		self.width = 200
		self.height = 30
		self.position = Vector2(0, 300)
		self.col = (33, 143, 113)
		self.rect = Rect(self.position.x, self.position.y, self.width, self.height)
		self.speed = 4
	
	def move(self):
		self.rect.x += self.speed
		if self.rect.x > screen_size.x:
			self.speed *= -1
			print("Right")
		if self.rect.x < -200:
			self.speed *= -1
			print("Right")

	def draw(self):
		pygame.draw.rect(screen, self.col, self.rect)

	def reset(self):
		self.__init__()

class button1P:
	def __init__(self):
		self.width = 150
		self.height = 75
		self.col = (255, 255, 255)
		self.buttonText = pygame.font.SysFont('Impact', 30)

	def draw(self, string, x, y, xText, yText):
		self.rect = Rect(x, y, self.width, self.height)
		self.textSurface = self.buttonText.render(str(string), True, (0, 0, 0))
		pygame.draw.rect(screen, self.col, self.rect)
		screen.blit(self.textSurface, (x + xText, y + yText))

		if pygame.mouse.get_pos() > (x, y) and pygame.mouse.get_pos() < (x + self.width, y + self.height):
			if pygame.mouse.get_pressed() == (1, 0, 0):
				print(str(string))

class button2P:
	def __init__(self):
		self.width = 150
		self.height = 75
		self.col = (255, 255, 255)
		self.buttonText = pygame.font.SysFont('Impact', 30)

	def draw(self, string, x, y, xText, yText):
		self.rect = Rect(x, y, self.width, self.height)
		self.textSurface = self.buttonText.render(str(string), True, (0, 0, 0))
		pygame.draw.rect(screen, self.col, self.rect)
		screen.blit(self.textSurface, (x + xText, y + yText))

		if (pygame.mouse.get_pos()[0] > x and pygame.mouse.get_pos()[1] > y
			and pygame.mouse.get_pos()[0] < (x + self.width) 
			and pygame.mouse.get_pos()[1] < (y + self.height)):
			if pygame.mouse.get_pressed() == (1, 0, 0):
				print(str(string))
		

def gameText(string, x, y):
    texting = pygame.font.SysFont('Impact', 40)
    textsurface = texting.render(str(string), True, (255, 255, 255))
    screen.blit(textsurface, (x, y))


ball = ball()

player1 = p1()
player2 = p2()

obstacle = obscl()

btn1P = button1P()
btn2P = button2P()

clock = pygame.time.Clock()

while menu == True:
	clock.tick(75)
	screen.fill(background)

	#btn1P.draw("1P", 200, 100, 60, 20)
	btn2P.draw("1P", 200, 100, 60, 20)
	btn2P.draw("2P", 200, 200, 60, 20)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				exit()

	pygame.display.update()

while run == True:
	clock.tick(75)
	screen.fill(background)

	player1.draw()
	player1.move()

	player2.draw()
	player2.move()

	obstacle.draw()
	obstacle.move()

	if game == True:
		ball.draw()
		stat = ball.move()
		if stat == 1:
			score.play()
			print("Player 1 scores!")
			game = False
		if stat == 2:
			score.play()
			print("Player 2 scores!")
			game = False
	if game == False and stat != 0:
		while game == False:
			screen.fill(background)

			if stat == 1:
				gameText("Player 1 scores!", (s_w / 3.4), (s_h // 2))
			if stat == 2:
				gameText("Player 2 scores!", (s_w / 3.4), (s_h // 2))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						exit()
					ball.reset()
					player1.reset()
					player2.reset()
					game = True

			pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				exit()
				

	pygame.display.update()

pygame.quit()