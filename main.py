from pygame import*
init()
mixer.init()
mixer.music.load("assets/musictheme.ogg")
mixer.music.play()
mixer.music.set_volume(0.1)
WIDTH, HEIGHT = 700,500
FPS = 60
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("SPACE SHOOTER")
background = transform.scale(image.load("assets/infinite_starts.jpg"),(WIDTH, HEIGHT))
clock = time.Clock()




class Player(sprite.Sprite):
    def __init__(self,sprite_image,x,y):
        self.image = transform.scale(image.load(sprite_image),(65,65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
    
    def draw(self,window):#створюємо функцію draw
        window.blit(self.image,self.rect)

    
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


player = Player("assets/spaceship.png",200,300)#створюємо спрайта 1

player.draw(window)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    player.movement(K_w,K_s,K_a,K_d)
    window.blit(background,(0,0))
    player.draw(window)


    
    display.update()
    clock.tick(FPS)