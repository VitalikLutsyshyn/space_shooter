from pygame import*
WIDTH, HEIGHT = 700,500
FPS =60
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("SPACE SHOOTER")
background = transform.scale(image.load("assets/infinite_starts.jpg"),(WIDTH, HEIGHT))
clock = time.Clock()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    window.blit(background,(0,0))



    
    display.update()
    clock.tick(FPS)