from pygame import*
from random import*
init()
font.init()
mixer.init()
mixer.music.load("assets/musictheme.ogg")
mixer.music.play()
mixer.music.set_volume(0.1)

WIDTH, HEIGHT = display.Info().current_w, display.Info().current_h
FPS = 60
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
spawn_interwval = randint(1000,2000)# в мілісекундах
enemy_image = image.load("assets/alien.png")
fire_image = image.load("assets/fire.png")
fire_sound = mixer.Sound("assets/laser.wav")
fire_sound.set_volume(0.2)

flags = FULLSCREEN
window = display.set_mode((1920, 1080), flags, vsync=1)

display.set_caption("SPACE SHOOTER")
background = transform.scale(image.load("assets/infinite_starts.jpg"),(WIDTH, HEIGHT))
clock = time.Clock()


sprites = sprite.Group()

class Player(sprite.Sprite):
    def __init__(self,sprite_image,x,y):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image),(65,65))
        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.hp = 15
        self.points = 0
        self.fires = sprite.Group()
        sprites.add(self)
    

    def movement(self, key_up, key_down, key_left, key_right):
        keys = key.get_pressed()#створюємо зміну в яку буде записуватись ключі від кнопок
        if keys[key_up] and self.rect.y > 0:#підключаємо рух до другого спрайта
            self.rect.y -= 5
        
        if keys[key_down] and self.rect.bottom < HEIGHT:#підключаємо рух до другого спрайта
            self.rect.y += 5

        if keys[key_left] and self.rect.x > 0:#підключаємо рух до другого спрайта
            self.rect.x -= 5

        if keys[key_right] and self.rect.right < WIDTH:#підключаємо рух до другого спрайта
            self.rect.x += 5

    def fire(self):
        new_fire = Fire(self.rect.centerx, self.rect.top)
        self.fires.add(new_fire)
        fire_sound.play()







class Enemy(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = transform.scale(enemy_image,(80,60))
        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        self.rect.x = randint(0,WIDTH-70)
        self.rect.y = randint(-HEIGHT,-40)
        self.speed = 2
        self.hp = 15
        sprites.add(self)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT or self.hp <= 0:
            self.kill()
        

class Fire(sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = transform.scale(fire_image,(20,40))
        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5
        sprites.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


player = Player("assets/spaceship.png",WIDTH/2-100,HEIGHT-150)#створюємо спрайта 1
enemies = sprite.Group()
enemies.add(Enemy(),Enemy())#додавання в групу

enemy_timer = time.get_ticks()

font1 = font.SysFont("Impact",50)
font2 = font.SysFont("Impact",25)
font3 = font.SysFont("Impact",50)

hp_text = font2.render(f"HP:{player.hp}",True,WHITE)
points_text = font2.render(f"POINTS:{player.points}",True,WHITE)
game_over = font1.render("GAME OVER",True,RED)   
start_text = font3.render("Press Y to start",True,WHITE)
youwin = font1.render("YOU WIN",True,GREEN)

game = True
finish = False
start = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_y:
                start = True

    if not start:
        window.blit(background,(0,0))
        window.blit(start_text,(WIDTH/2-100,HEIGHT/2-35))

    elif not finish:
        if time.get_ticks() - enemy_timer >= spawn_interwval:
            enemies.add(Enemy())
            enemy_timer = time.get_ticks()
            spawn_interwval = randint(1000,2000)
        
        collide_list = sprite.spritecollide(player,enemies,True,sprite.collide_mask)
        for hit in collide_list:
            player.hp -= 5
            hp_text = font2.render(f"HP:{player.hp}",True,WHITE)
            if player.hp <= 0:
                finish = True

        collide_list =sprite.groupcollide(enemies,player.fires,False,True,sprite.collide_mask)
        for enemy in collide_list:
            enemy.hp -=5
            if enemy.hp <= 0:
                enemy.kill()
                player.points += 10
                points_text = font2.render(f"POINTS:{player.points}",True,WHITE)
                if player.points >= 100:
                    finish = True
                    

            



        player.movement(K_w,K_s,K_a,K_d)
        sprites.update()
    if start:
        window.blit(background,(0,0))
        sprites.draw(window)
        window.blit(hp_text,(20,20))
        window.blit(points_text,(20,50))
        if finish:
            if player.points >= 100:
                window.blit(youwin,(WIDTH/2-100,HEIGHT/2-35))
            else:
                window.blit(game_over,(WIDTH/2-150,HEIGHT/2-35))

    display.update()
    clock.tick(FPS)