import pygame
from pygame import Vector2
from pygame import mixer
from pygame.locals import *
from tkinter import *
from tkinter.ttk import *
import os

s_w = 600
s_h = 600
screen_size = Vector2(600, 600)

global menu
menu = False
run = False
game = True


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

class button:
	def __init__(self):
		self.width = 150
		self.height = 75
		self.col = (255, 255, 255)
		self.hcol = (220, 220, 220)
		self.bcol = (0, 255, 0)
		self.buttonText = pygame.font.SysFont('Impact', 30)
		self.pressed = False
		global p1b
		global p2b
		p1b = -1
		p2b = -1

	def draw1P(self, string):
		global p1b
		global p2b
		self.rect = Rect(210, 100, self.width, self.height)
		self.textSurface = self.buttonText.render(str(string), True, (0, 0, 0))
		pygame.draw.rect(screen, self.col, self.rect)
		pygame.draw.rect(screen, self.bcol, self.rect, p1b)
		screen.blit(self.textSurface, (210 + 60, 100 + 20))

		if pygame.mouse.get_pressed() == (1, 0, 0):
			if (pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 100
				and pygame.mouse.get_pos()[0] < (200 + self.width) 
				and pygame.mouse.get_pos()[1] < (100 + self.height)):
				if str(string) == "1P":
					if p1b == -1:
						p1b = 4
					elif p1b == 4:
						p1b = -1
					if p2b != -1:
						p2b = -1
					pygame.time.delay(100)

		if p1b == 4:
			return True
		elif p1b == -1:
			return False

	def draw2P(self, string):
		global p1b
		global p2b
		self.rect = Rect(210, 200, self.width, self.height)
		self.textSurface = self.buttonText.render(str(string), True, (0, 0, 0))
		pygame.draw.rect(screen, self.col, self.rect)
		pygame.draw.rect(screen, self.bcol, self.rect, p2b)
		screen.blit(self.textSurface, (210 + 60, 200 + 20))

		if (pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 200
				and pygame.mouse.get_pos()[0] < (200 + self.width) 
				and pygame.mouse.get_pos()[1] < (200 + self.height)):
			self.col = (220, 220, 220)
		else: self.col = (255, 255, 255)	

		if pygame.mouse.get_pressed() == (1, 0, 0):
			if (pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 200
				and pygame.mouse.get_pos()[0] < (200 + self.width) 
				and pygame.mouse.get_pos()[1] < (200 + self.height)):
				if str(string) == "2P":
					if p2b == -1:
						p2b = 4
					elif p2b == 4:
						p2b = -1
					if p1b != -1:
						p1b = -1
					pygame.time.delay(100)
		if p2b == 4:
			return True
		elif p2b == -1:
			return False

	def drawContinue(self, string):
		global menu
		self.rect = Rect(200, 500, self.width + 20, self.height)
		self.textSurface = self.buttonText.render(str(string), True, (0, 0, 0))
		pygame.draw.rect(screen, self.col, self.rect)
		#pygame.draw.rect(screen, self.bcol, self.rect, p2b)
		screen.blit(self.textSurface, (200 + 30, 500 + 20))

		if pygame.mouse.get_pressed() == (1, 0, 0):
			if (pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 500
				and pygame.mouse.get_pos()[0] < (200 + self.width) 
				and pygame.mouse.get_pos()[1] < (500 + self.height)):
				if str(string) == "Continue":
					print("hey")
					menu = False
					self.pressed = True
		return self.pressed

class buttonState:
	def __init__(self):
		self.twoP = False

	def cont(self):
		global menu
		menu = True


	def twoPlayer(self):
		self.twoP = True


def gameText(string, x, y):
    texting = pygame.font.SysFont('Impact', 40)
    textsurface = texting.render(str(string), True, (255, 255, 255))
    screen.blit(textsurface, (x, y))

ball = ball()

player1 = p1()
player2 = p2()

obstacle = obscl()

btn = buttonState()

clock = pygame.time.Clock()

root = Tk()
root.geometry('400x400+450+250')
#root.eval('tk::PlaceWindow . center')

style = Style()
style.configure('W.TButton', font = ('calibri', 20))

btn1 = Button(root, text = '1 Player', style = 'W.TButton', command = None)
btn1.grid(row = 0, column = 0, padx = 25, pady = 50)

btn2 = Button(root, text = '2 Player', style = 'W.TButton', command = btn.twoPlayer())
btn2.grid(row = 0, column = 2)

btn3 = Button(root,text = 'Continue', style = 'W.TButton', command = btn.cont())
btn3.grid(row = 1, column = 0, columnspan = 3)

root.mainloop()

#screen = pygame.display.set_mode(screen_size)

while menu == True:
	clock.tick(75)
	screen.fill(background)

	btn.draw1P("1P")
	btn.draw2P("2P")
	btn.drawContinue("Continue")

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