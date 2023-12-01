import pygame
import random
import time
from pygame import mixer

pygame.init()
pygame.mixer.init()  # To initialize the mixer module used to play sound
# windows
screen = pygame.display.set_mode((650, 500))
pygame.display.set_caption('StandOFF!')
clock = pygame.time.Clock()

# bg and title
sky = pygame.image.load('graphics/sky/sky.png')
ground = pygame.image.load('graphics/ground/ground.png')
title = pygame.image.load('graphics/title/title.png')

# buttons
play = pygame.image.load('graphics/play_button_n_exit/real play buttob.png').convert_alpha()
exitbutton = pygame.image.load('graphics/play_button_n_exit/real exit button.png.').convert_alpha()

# Fonts and text
font = pygame.font.Font(None, 80)
warning = font.render("!", False, "black")  # Sign that shows when you can shoot your enemy
text_rect = warning.get_rect(center=(325, 300))  # Rectangle to position the text on screen

# Sounds
bg_music = mixer.Sound('sounds/bg_music.mp3')
shoot_sound = mixer.Sound('sounds/shoot.mp3')

# Player and enemy classes
class Player:
    def __init__(self):
        # I create a dictionary of images to store the player different states
        self.player_sprites = {
            "stand": pygame.image.load("graphics/player/stanceplayer.png").convert_alpha(),
            "fire": pygame.image.load("graphics/player/firegunplayer.png").convert_alpha(),
            "wins": pygame.image.load("graphics/player/winplayer.png").convert_alpha(),
            "death": pygame.image.load("graphics/player/deadplayer.png").convert_alpha()
        }
        # I load the standing image at beginning since is the default one
        self.player_image = self.player_sprites["stand"]
        # I create a rectangle to store the player position and center it
        self.player_rect = self.player_image.get_rect(center=(120, 375))
        # I create a variable to store the player state
        self.player_state = "stand"

    # I draw the image of the player depending on his state
    def draw(self):
        self.player_image = self.player_sprites[self.player_state]
        screen.blit(self.player_image, self.player_rect)

    def shoot(self):
        self.player_state = "fire"

    def die(self):
        self.player_state = "death"

    def win(self):
        self.player_state = "wins"


class Enemy:
    def __init__(self):
        # I create a dictionary of images to store the enemy different states
        self.player_sprites = {
            "stand": pygame.image.load("graphics/enemy/stanceenemy.png").convert_alpha(),
            "fire": pygame.image.load("graphics/enemy/firegunenemy.png").convert_alpha(),
            "wins": pygame.image.load("graphics/enemy/winenemy.png").convert_alpha(),
            "death": pygame.image.load("graphics/enemy/deadenemy.png").convert_alpha()
        }
        # I load the standing image at beginning since is the default one
        self.player_image = self.player_sprites["stand"]
        # I create a rectangle to store the enemy position and center it
        self.player_rect = self.player_image.get_rect(center=(530, 375))
        # I create a variable to store the enemy state
        self.player_state = "stand"

    # I draw the image of the player depending on his state
    def draw(self):
        self.player_image = self.player_sprites[self.player_state]
        screen.blit(self.player_image, self.player_rect)

    def shoot(self):
        self.player_state = "fire"

    def die(self):
        self.player_state = "death"

    def win(self):
        self.player_state = "wins"


class Button:
    def __init__(self, x, y, image, scale):
        height = image.get_height()
        width = image.get_width()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        # pos n zixe
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self):
        action = False
        # mouse pos
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class Game:
    def __init__(self):
        self.game_state = "intro"
        self.chance = 0  # Chance number used to stablish some random time before the signal (!) appears
        # shoot_state can be "waiting" "ready "or "finished", is used to check whether you can shoot or not,
        # or if you already shoot
        self.shoot_state = "waiting"

    # Basic function to run the game
    def run(self):
        if self.game_state == "intro":
            self.play_intro()
        else:
            self.play_game()

    def play_intro(self):
        play_button.draw()
        exit_button.draw()

        # Button functionality
        if play_button.is_clicked():
            self.game_state = "playing"
            bg_music.play()  # Starts playing the background music when you click the play button
            time.sleep(0.5)  # Some delay time for the mouse button to be released (so it doesn't count as if you are shooting)
        if exit_button.is_clicked():
            pygame.quit()
            exit()

    def play_game(self):
        # Draw the two players on screen
        player.draw()
        enemy.draw()
        pygame.display.update()

        # Use random numbers and checks the state of the game to see if you can already shoot
        if random.randint(0, self.chance) > 300 and self.shoot_state == "waiting":
            self.shoot_state = "ready"
        self.chance += 1

        # if you or your enemy already shoot change the animations to show who wins
        if self.shoot_state == "finished":
            if player.player_state == "fire" or enemy.player_state == "fire":
                shoot_sound.play()  # Plays the shooting sound if someone shoots the other
                time.sleep(1)  # Waits for the sound to finish playing for 1 second and keeps the shooting animation
            if player.player_state == "fire":  # If the players was the one that shoots, then he wins
                player.player_state = "wins"
            elif enemy.player_state == "fire":  # If the enemy was the one that shoots, then he wins
                enemy.player_state = "wins"

        # if you can already shoot draws the sign (!) on the screens and checks if some player shoots and wich one shoots first
        if self.shoot_state == "ready":
            screen.blit(warning, text_rect)
            if pygame.mouse.get_pressed()[0]:
                player.shoot()
                self.shoot_state = "finished"  # Finished shooting
                # Draws the two players on screen again and checks if some player shoots and wich one shoots first
                player.draw()
                enemy.draw()
                player.shoot()
                enemy.die()
            if random.randint(0, 1000) > 950:  # There is a chance the enemy shoots, the more you wait, the more can happens
                enemy.shoot()
                self.shoot_state = "finished"  # Finished shooting
                player.draw()
                enemy.draw()
                enemy.shoot()
                player.die()

        # Checks if you shoot before the sign (!) appears and makes the enemy shoot you instead
        if self.shoot_state == "waiting" and pygame.mouse.get_pressed()[0]:
            enemy.shoot()
            self.shoot_state = "finished"  # Finished shooting
            player.draw()
            enemy.draw()
            enemy.shoot()
            player.die()


play_button = Button(255, 225, play, 0.7)
exit_button = Button(255, 295, exitbutton, 0.7)
game = Game()  # instantiate game
player = Player()  # instantiate player
enemy = Enemy()  # instantiate enemy

# main code
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Drawing in screen
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 0))
    screen.blit(title, (0, 0))
    game.run()  # run game

    # Updating screen
    pygame.display.update()
    clock.tick(60)
