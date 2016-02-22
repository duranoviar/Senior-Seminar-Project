import pygame
import time
import random
from pygame.locals import *

from globals import *
from objects import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# set up the display
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Test Game')

# set up the clock
clock = pygame.time.Clock()
backgroundImg = pygame.image.load('backgrounds/Grid2.png').convert()

# create one player
player = Player()

# generate basic enemy group
basic_enemies = pygame.sprite.Group()

# generate power_up group
power_ups = pygame.sprite.Group()

# generate missile Group
missiles = pygame.sprite.Group()
enemy_missiles = pygame.sprite.Group()

# set up the sounds
sound_laser = pygame.mixer.Sound('sounds/laser.wav')
sound_explosion = pygame.mixer.Sound('sounds/explosion.wav')

# start music
pygame.mixer.music.load('sounds/theme.wav')
pygame.mixer.music.play(-1)

def enemy_hit_count_display(count):
    font = pygame.font.Font('fonts/future.ttf', 20)
    text = font.render("Enemies Hit: " + str(count), True, WHITE)
    gameDisplay.blit(text,(0,0))

def enemy_dodge_count_display(count):
	font = pygame.font.Font('fonts/future.ttf', 20)
	text = font.render("Enemies Dodged: " + str(count), True, WHITE)
	gameDisplay.blit(text,(0,20))

def level_display(count):
	font = pygame.font.Font('fonts/future.ttf', 20)
	text = font.render("Level: " + str(count), True, WHITE)
	gameDisplay.blit(text,(650,0))

def text_objects(text, font):
	textSurface = font.render(text, True, WHITE)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('fonts/future.ttf', 75)
	textSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2))
	gameDisplay.blit(textSurf, TextRect)
	pygame.display.update()
	time.sleep(2)

def crash():
	message_display('You Crashed')
	enemy_missiles.empty()
	basic_enemies.empty()
	missiles.empty()
	game_loop()

def game_menu():

	button_start = Button('ui/button_start.png', 280, 300)
	button_quit = Button('ui/button_quit.png', 280, 350)
	button_highscore = Button('ui/button_highscore.png', 280, 400)
	button_instructions = Button('ui/button_instructions.png', 280, 450)

	menu = True
	while menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_start.pressed(event.pos):
					game_loop()
				if button_quit.pressed(event.pos):
					pygame.quit()
					quit()
				if button_highscore.pressed(event.pos):
					pygame.quit()
					quit()
				if button_instructions.pressed(event.pos):
					pygame.quit()
					quit()

		gameDisplay.blit(backgroundImg, (0,0))
		font = pygame.font.Font('fonts/future.ttf', 75)
		TextSurf, TextRect = text_objects("3045", font)
		TextRect.center = (400, 250)
		gameDisplay.blit(TextSurf, TextRect)

		button_start.update()
		button_quit.update()
		button_highscore.update()
		button_instructions.update()
		pygame.display.update()
		clock.tick(15)

def game_loop():

	# set up counters
	enemy_hit_count = 0
	enemy_dodge_count = 0
	level = 1

	enemy_speed = 2

	power_up_active = False

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.change_x = -player.speed
				elif event.key == pygame.K_RIGHT:
					player.change_x = player.speed
				elif event.key == pygame.K_SPACE:
					missiles.add(Missile(player, BASIC_MISSILE_PLAYER))
					pygame.mixer.Sound.play(sound_laser)
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					player.change_x = 0

		# update speeds
		if enemy_hit_count + enemy_dodge_count >= 1200:
			enemy_speed = 7
			level = 6
		elif enemy_hit_count + enemy_dodge_count >= 800:
			enemy_speed = 6
			level = 5
		elif enemy_hit_count + enemy_dodge_count >= 600:
			enemy_speed = 5
			level = 4
		elif enemy_hit_count + enemy_dodge_count >= 400:
			enemy_speed = 4
			level = 3
		elif enemy_hit_count + enemy_dodge_count >= 200:
			enemy_speed = 3
			level = 2

		# generate more basic enemies if needed
		if len(basic_enemies) < MAX_BASIC_ENEMIES:
			basic_enemies.add(BasicEnemy(enemy_speed))

		# generate random power up
		rand = random.randrange(0, 5000)
		if rand == 1:
		    power_ups.add(PowerUp())

		# fire enemy missiles
		for enemy in basic_enemies:
			rand = random.randrange(0, 1000)
			if rand == 1:
				enemy_missiles.add(Missile(enemy, BASIC_MISSILE_ENEMY, False))

		# redraw graphics
		gameDisplay.blit(backgroundImg, (0,0))
		basic_enemies.update()
		missiles.update()
		enemy_missiles.update()
		player.update()
		power_ups.update()

		# update counters to screen
		enemy_hit_count_display(enemy_hit_count)
		enemy_dodge_count_display(enemy_dodge_count)
		level_display(level)

        # crash game if player gets hit by enemy
		if pygame.sprite.spritecollide(player,basic_enemies,True):
			crash()

		if pygame.sprite.spritecollide(player,enemy_missiles,True):
			crash()

		# if user hits enemy with missile, destroy both sprites
		if pygame.sprite.groupcollide(basic_enemies, missiles, True, True):
			enemy_hit_count += 1
			pygame.mixer.Sound.play(sound_explosion)

		# Delete missiles that hit eachother
		pygame.sprite.groupcollide(enemy_missiles, missiles, True, True)

		if pygame.sprite.spritecollide(player, power_ups, True):
			player.speed = 10

		# Delete missiles that run off the screen
		for missile in missiles:
			if missile.rect.y < 0:
				missile.kill()

		for missile in enemy_missiles:
			if missile.rect.y > 600:
				missile.kill()

		for power_up in power_ups:
			if power_up.rect.y > 600:
				power_up.kill()

		# teleport player to opposite edge if he goes off screen
		if player.rect.x > DISPLAY_WIDTH:
			player.rect.x = -35
		if player.rect.x < -35:
			player.rect.x = DISPLAY_WIDTH - 30

		# kill basic enemy if it runs off the screen
		for enemy in basic_enemies:
			if enemy.rect.y > DISPLAY_HEIGHT:
				enemy_dodge_count += 1
				enemy.kill()

		# update the display
		pygame.display.update()
		clock.tick(FPS)

game_menu()
game_loop()
pygame.quit()
quit()
