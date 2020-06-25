import pygame # pip install pygame
import math
import random
import time

# Initialize 
pygame.init()

# Create the screen
SCREEN_HEIGHT = 600 
SCREEN_WIDTH = 800
SHIPSIZE = 80
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# background
background = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background, (800, 700))

# Set caption and icon
pygame.display.set_caption("Chicken Invaders")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
OPENNING_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
GEN_FONT = pygame.font.SysFont("comicsans", 40)

#Img
playerImg = pygame.image.load('images/spaceship.png').convert_alpha()
enemyImg = pygame.image.load('images/alien.png').convert_alpha()
covidImg = pygame.image.load('images/virus.png').convert_alpha()
# enemyImg = pygame.transform.scale(enemyImg, (45, 45))
bulletImg = pygame.image.load('images/bullet.png').convert_alpha()

movingPace = 5 # player's speed
virusPace = 5 # covid's speed

class SpaceObj:

	def __init__(self, Img, x, y):
		self.X = x
		self.Y = y
		self.Img = Img

	def render(self):
		screen.blit(self.Img, (self.X, self.Y))
				
class Player(SpaceObj):

	def __init__(self, Img, x, y, speed):
		super().__init__(Img, x, y)
		self.moveLeft = False
		self.moveRight = False
		self.moveUp = False
		self.moveDown = False
		self.speed = speed

	def update(self):
		nextX = self.X + (self.moveRight - self.moveLeft) * self.speed
		nextY = self.Y + (-self.moveUp + self.moveDown) * self.speed
		if nextX >= 5 and nextX < SCREEN_WIDTH - SHIPSIZE:
			self.X = nextX
		if nextY >= 5 and nextY < SCREEN_HEIGHT - SHIPSIZE:
			self.Y = nextY

	def goLeft(self, status):
		self.moveLeft = status
	def goRight(self, status):
		self.moveRight = status
	def goUp(self, status):
		self.moveUp = status
	def goDown(self, status):
		self.moveDown = status

	def render(self):
		screen.blit(self.Img, (self.X, self.Y))

class Bullet(SpaceObj):

	def __init__(self, Img, x, y, speed, dame):
		super().__init__(Img, x, y)
		self.speed = speed
		self.finish = False
		self.damage = dame

	def update(self):
		if self.Y < -10:
			self.finish = True
		self.Y -= self.speed

	def checkReach(self, enemy):
		x = enemy.X + 16
		y = enemy.Y + 16
		distance = math.sqrt( ((self.X - x)**2) + ((self.Y - y)**2) )
		if distance <= 20:
			enemy.getHurt(self.damage)
			self.finish = True

class Virus(SpaceObj):
	def __init__(self, Img, x, y, speed):
		super().__init__(Img, x, y)
		self.speed = speed

	def update(self):
		self.Y += self.speed

	def explode(self, spaceship):
		x = spaceship.X + 32
		y = spaceship.Y + 32
		distance = math.sqrt( ((self.X + 8 - x)**2) + ((self.Y + 8 - y)**2) )
		if distance <= 28:
			# pygame.draw.circle(screen, (255,255,255), (x, y), 28)
			return True
		return False
		
class Enermy(SpaceObj):

	def __init__(self, Img, x, y, health, speed):
		super().__init__(Img, x, y)
		self.hp = health
		self.start_time = time.time()
		self.fire_delay = random.random()
		self.getDown = True
		self.speed = speed
		self.maxHP = health

	def move(self):
		if self.getDown:
			self.Y += self.speed
			if self.Y >= 100:
				self.getDown = False
		else:
			return

	def getHurt(self, dame):
		self.hp -= dame

	def fire(self):
		if time.time() - self.start_time >= self.fire_delay * 5:
			newVirus = Virus(covidImg, self.X + 16, self.Y + 16, virusPace)
			viruses.append(newVirus)
			self.start_time = time.time()
			self.fire_delay = random.random()

	def render(self):
		super().render()
		if self.hp / self.maxHP > 0.6:
			hp_color = (0, 200, 0)
		elif self.hp > 0.3:
			hp_color = (255,255,0)
		else:
			hp_color = (255, 0, 0)
		pygame.draw.rect(screen, hp_color, (self.X, self.Y + 70, self.hp / self.maxHP * 65, 7))

# Space Characters
player = Player(playerImg, 370, 460, movingPace)
enemies = []
bullets = []
viruses = []

def end_screen():
	noti_label = END_FONT.render("You got coronavirus!!!", 1, (255,0,0))
	death_label = END_FONT.render("You will die in the next 14 days!!!", 1, (255,0,0))

	screen.blit(noti_label, (125, 250))
	screen.blit(death_label, (25, 300))

	pygame.display.update()
	pending = True
	while pending:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pending = False
				break
			elif event.type == pygame.KEYDOWN:
				if event.key == 27:
					pending = False
					pygame.quit()
					quit()
					break
				elif event.key == pygame.K_SPACE:
					main()

def newLevel(enemyHP):
	global viruses, enemies, bullets
	viruses = []
	enemies = [Enermy(enemyImg, 100 * i, -100, enemyHP, movingPace / 2) for i in range(1, 7)]
	bullets = []
	player.X = 370
	player.Y = 460
	player.goRight(False)
	player.goLeft(False)
	player.goUp(False)
	player.goDown(False)

def endRound():
	return len(enemies) == 0

def main():
	start = False
	lost = False
	running = True
	Round = 1

	newLevel(Round * 100)

	while running:
		if endRound():
			Round += 1
			newLevel(Round * 100)
			continue
		if lost:
			end_screen()
			break

		screen.fill((0, 0, 0))
		screen.blit(background, (0, 0))
		round_text = GEN_FONT.render("Round: " + str(Round), 1, (255, 255, 255))
		screen.blit(round_text, (SCREEN_WIDTH - round_text.get_width(), 15))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False # break the loop
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if not start:
					start = True
				else:
					if event.key == 27: # Esc pressed
						running = False
						pygame.quit()
						quit()
					elif event.key == 275: # Right pressed
						player.goRight(True)
					elif event.key == 276: # Left pressed
						player.goLeft(True)
					elif event.key == 273: # Up pressed
						player.goUp(True)
					elif event.key == 274: # Down pressed
						player.goDown(True)
					elif event.key == pygame.K_SPACE:
						bullets.append(Bullet(bulletImg, player.X + 20, player.Y, 15, 20))

			elif event.type == pygame.KEYUP:
				if event.key == 275: # Right pressed
					player.goRight(False)
				elif event.key == 276: # Left pressed
					player.goLeft(False)
				elif event.key == 273: # Up pressed
					player.goUp(False)
				elif event.key == 274: # Down pressed
					player.goDown(False)

		if start:			
			# update
			player.update()

			for virus in viruses:
				virus.update()
				if virus.Y >= 800:
					viruses.remove(virus)
				if virus.explode(player):
					lost = True
					break

			for bullet in bullets:
				bullet.update()
				for enemy in enemies:
					bullet.checkReach(enemy)
					if bullet.finish:
						break

				if bullet.finish:
					bullets.remove(bullet)

			for enemy in enemies:
				if enemy.hp <= 0:
					enemies.remove(enemy)
					continue
				enemy.move()
				enemy.fire()

		else: # Press any button to start game
			openning_label = OPENNING_FONT.render("Press any button to start game", 1, (149, 62, 189))
			screen.blit(openning_label, (125, 300))

		# render
		player.render()

		for virus in viruses:
			virus.render()

		for bullet in bullets:
			bullet.render()

		for enemy in enemies:
			enemy.render()

		pygame.display.update()

if __name__ == "__main__":
	main()