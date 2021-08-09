import pygame
import os #import os untuk ngebantu define path
import random
import numpy as np
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Site-X")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (0, 200, 0)

PLANE_WIDTH , PLANE_HEIGHT = 75, 15
MISSILE_WIDTH, MISSILE_HEIGHT = 16,30

SITE_X_START_FONT = pygame.font.SysFont('comicsans', 100)
PRESS_ENTER_FONT = pygame.font.SysFont('comicsans', 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
COOLDOWN_FONT = pygame.font.SysFont('comicsans', 40)
GAMEOVER_SCORE_FONT = pygame.font.SysFont('comicsans', 60)

EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'sounds', 'Doom-Barrel-Exp.wav')) #collide
FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'sounds', 'Probe-Gun.wav')) #shoots

FPS = 60
VEL = 5
ENEMY_VEL = 2
BULLET_VEL = 7
MAX_BULLETS = 3

# Hit Event
PLAYER_HIT = pygame.USEREVENT + 1 
ENEMIES_HIT = pygame.USEREVENT + 2

PLAYER_PLANE_IMAGE = pygame.image.load(os.path.join('assets', 'images', 'f35.png'))
PLAYER_PLANE = pygame.transform.scale(PLAYER_PLANE_IMAGE,(PLANE_WIDTH, PLANE_HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'background.png')), (WIDTH, HEIGHT))
ENEMIES_PLANE_IMAGE = pygame.image.load(os.path.join('assets', 'images', 'sylph.png'))
ENEMIES_PLANE = pygame.transform.scale(ENEMIES_PLANE_IMAGE,(PLANE_WIDTH, PLANE_HEIGHT))
MISSILE_IMAGE = pygame.image.load(os.path.join('assets', 'images', 'missile1.png'))
MISSILE = pygame.transform.scale(MISSILE_IMAGE, (MISSILE_WIDTH, MISSILE_HEIGHT))
EXPLOSION = pygame.image.load(os.path.join('assets', 'images', 'explosion1.png'))
EXPLOSION = pygame.transform.scale(EXPLOSION, (50,50))

class Enemy():
  def __init__(self,surface):
    self.surface = surface
    self.missile = []
    self.missile_cooldown = random.randint(120,240)
  
  def fire(self):
    self.missile.append(pygame.Rect(self.surface.x+self.surface.width//2,self.surface.y+self.surface.height,30,30))
    self.missile_cooldown = random.randint(120,240)

def player_handle_movement(keys_pressed, player):
  if keys_pressed[pygame.K_a] and player.x - VEL > 0:  # LEFT
    player.x -= VEL
  if keys_pressed[pygame.K_d] and player.x + VEL + player.width < WIDTH:  # RIGHT (note: ditambah player.width karena kita gambar dari ujung kiri)
    player.x += VEL
  if keys_pressed[pygame.K_w] and player.y - VEL > 0:  # UP
    player.y -= VEL
  if keys_pressed[pygame.K_s] and player.y + VEL + player.height < HEIGHT - 15:  # DOWN
    player.y += VEL

def draw_start_screen():
  WIN.fill(BLACK)
  site_x_start = SITE_X_START_FONT.render("Site-X", 1, LIGHT_GREEN)
  press_enter = PRESS_ENTER_FONT.render("Press ENTER to start", 1, WHITE)
  WIN.blit(site_x_start, (WIDTH//2 - site_x_start.get_width()/2, 100))
  WIN.blit(press_enter, (WIDTH//2 - press_enter.get_width()/2, 300))

  pygame.display.update()

def draw_window(player, enemies, score, bullets, cooldown, kaboom, enemy_get_hit, alive, combo, comboTime):
  if alive:
    
    WIN.blit(BACKGROUND, (0,0))
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    cooldowntxt = COOLDOWN_FONT.render("Cooldown: 0." + str(cooldown), 1, WHITE)
    combotxt = COOLDOWN_FONT.render("Combo: " + str(combo), 1, WHITE)
    if comboTime > 0:
      WIN.blit(combotxt, (WIDTH//2, HEIGHT - 30))
    WIN.blit(score_text, (15,HEIGHT-30))
    if cooldown > 0:
      WIN.blit(cooldowntxt, (WIDTH - cooldowntxt.get_width() - 15, HEIGHT-30))
    
    for enemy in enemies:
      WIN.blit(ENEMIES_PLANE,(enemy.surface.x,enemy.surface.y))
      for missile in enemy.missile:
        x = player.x-missile.x
        y = player.y-missile.y
        
        degree = np.rad2deg(np.arctan2(x, y))
        WIN.blit(pygame.transform.rotate(MISSILE,degree),(missile.x,missile.y))

    # for enemy in enemies:
    #   WIN.blit(ENEMIES_PLANE, (enemy.surface.x, enemy.surface.y))
    WIN.blit(PLAYER_PLANE, (player.x,player.y))
    
    for bullet in bullets:
      WIN.blit(pygame.transform.rotate(MISSILE,90), (bullet.x, bullet.y))

    if kaboom > 0:
      WIN.blit(EXPLOSION, (enemy_get_hit[0], enemy_get_hit[1]))
    
  else:
    WIN.fill(BLACK)
    gameover = GAMEOVER_SCORE_FONT.render('Game Over', 1, RED)
    scoretxt = GAMEOVER_SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    press_enter = PRESS_ENTER_FONT.render("Press ENTER to restart", 1, WHITE)
    WIN.blit(gameover, (WIDTH//2 - gameover.get_width()/2, 100))
    WIN.blit(scoretxt, (WIDTH//2 - scoretxt.get_width()/2, 300))
    WIN.blit(press_enter, (WIDTH//2 - press_enter.get_width()/2, 400))

  pygame.display.update()

def draw_game_over(score):
  WIN.fill(BLACK)
  gameover = GAMEOVER_SCORE_FONT.render('Game Over', 1, RED)
  scoretxt = GAMEOVER_SCORE_FONT.render("Score: " + str(score), 1, WHITE)
  press_enter = PRESS_ENTER_FONT.render("Press ENTER to restart", 1, WHITE)
  WIN.blit(gameover, (WIDTH//2 - gameover.get_width()/2, 100))
  WIN.blit(scoretxt, (WIDTH//2 - scoretxt.get_width()/2, 100))
  WIN.blit(press_enter, (WIDTH//2 - press_enter.get_width()/2, 100))

def handle_enemy_missile(enemy_missile,player,player_laser):

  for missile in enemy_missile:

    missile.x+=(player.x>missile.x)*2 + (player.x<missile.x)*-2
    missile.y+=(player.y>missile.y)*2 + (player.y<missile.y)*-2
    
    if player.colliderect(missile):
      pygame.event.post(pygame.event.Event(PLAYER_HIT))
      enemy_missile.remove(missile)
        
    if any(laser.colliderect(missile) for laser in player_laser):
      enemy_missile.remove(missile)
        
    if missile.x > WIDTH or missile.x < 0 or missile.y < 0 or missile.y> HEIGHT:
      enemy_missile.remove(missile)

def handle_enemies(enemies, player, bullets):
  for enemy in enemies:
    handle_enemy_missile(enemy.missile,player, bullets)
    if enemy.missile_cooldown > 0:
      enemy.missile_cooldown -= 1
    else:
      enemy.fire()
    enemy.surface.x -= ENEMY_VEL
    if enemy.surface.colliderect(player):
      pygame.event.post(pygame.event.Event(PLAYER_HIT))
    if enemy.surface.x < -PLANE_WIDTH:
      try:
        enemies.remove(enemy)
      except ValueError:
        pass

def handle_bullets(bullets, enemies, bullets_score):
  toRemove = (-1, -1)
  idx = 0
  for bullet in bullets:
    bullet.x += BULLET_VEL

    for enemy in enemies:
      if enemy.surface.colliderect(bullet):
        pygame.event.post(pygame.event.Event(ENEMIES_HIT))
        toRemove = (enemy.surface.x, enemy.surface.y)
        idx = bullets.index(bullet)
        bullets_score[idx] += 1
        try:
          enemies.remove(enemy)
        except ValueError:
          pass
      elif bullet.x > WIDTH:
        try:
          bullets_score.pop(bullets.index(bullet))
        except ValueError:
          pass
        try:
          bullets.remove(bullet)
        except ValueError:
          pass
  return idx, toRemove
    

def main():
  player = pygame.Rect(400, 400, PLANE_WIDTH, PLANE_HEIGHT)
  start = False
  alive = True
  bullets = []
  bullets_score = [0]
  enemies = []
  score = 0
  enemy_get_hit = (-50, -50)
  cooldown = 0
  enemy_spawn = 0
  kaboom = 0
  combo = 0
  getcombo = 0
  comboTime = 0
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(FPS)
    if cooldown > 0:
      cooldown -= 1
    if enemy_spawn > 0:
      enemy_spawn -= 1
    if kaboom > 0:
      kaboom -= 1
    idx, isHit = handle_bullets(bullets, enemies, bullets_score)
    try:
      getcombo = max(bullets_score)
    except ValueError:
      getcombo = 0
    if getcombo > 0:
      comboTime = 120
      combo = getcombo
    if comboTime > 0:
      comboTime -= 1
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()

      # cek apakah kita tekan sebuah key (Hold cuma terhitung 1x jalan)
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and start == False:
          start = True
        elif event.key == pygame.K_RETURN and start == True and alive == True and cooldown == 0:
          bullet = pygame.Rect(player.x + player.width, player.y + player.height//2 - 2, 10, 5)
          bullets.append(bullet)
          bullets_score.append(0)
          FIRE_SOUND.play()
          cooldown = 80
        elif event.key == pygame.K_RETURN and start == True and alive == False:
          run = False
          break

      if event.type == PLAYER_HIT:
        EXPLOSION_SOUND.play()
        alive = False

      if event.type == ENEMIES_HIT:
        EXPLOSION_SOUND.play()
        score += bullets_score[idx]

    if enemy_spawn == 0 and start and alive:
      enemy = Enemy(pygame.Rect(random.randint(700,800), random.randint(20,400), PLANE_WIDTH, PLANE_HEIGHT))
      enemies.append(enemy)
      enemy_spawn = random.randint(60,120)

    keys_pressed = pygame.key.get_pressed()
    player_handle_movement(keys_pressed, player)
    if isHit != (-1, -1):
      kaboom = 30
      enemy_get_hit = isHit
    handle_enemies(enemies, player, bullets)
    if start == False:
      draw_start_screen()
    elif start == True:
      draw_window(player, enemies, score, bullets, cooldown, kaboom, enemy_get_hit, alive, combo, comboTime)
    # else:
    #   draw_game_over(score)
    
  main()






if __name__ == "__main__":
  main()