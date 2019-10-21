import pygame

pygame.init()

screen_width = 890
screen_height = 480

win = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Second Part")

clock = pygame.time.Clock()
fps = 27

x = 50
y = 100

width = 64
height = 64
velocity = 5

isJump = False
jumpExtent = 5
jumpCount = jumpExtent

left = False
right = False
flyCount = 0

bird_right = pygame.image.load('bird.png').convert()
bird_left = pygame.transform.flip(bird_right, True, False)

bird_moving_right = []
bird_moving_left = []

bird_left = pygame.image.load('./bird_sprites/row-1-col-1.png')
bird_right = pygame.transform.flip(pygame.image.load('./bird_sprites/row-1-col-1.png'), True, False)
# bird_moving_right = pygame.image.load('bird.png').convert()
bird_moving_left= [pygame.image.load('./bird_sprites/row-1-col-1.png'),
                  pygame.image.load('./bird_sprites/row-1-col-2.png'),
                  pygame.image.load('./bird_sprites/row-1-col-3.png'),
                  pygame.image.load('./bird_sprites/row-1-col-4.png'),
                  pygame.image.load('./bird_sprites/row-1-col-5.png'),
                  pygame.image.load('./bird_sprites/row-2-col-1.png'),
                  pygame.image.load('./bird_sprites/row-2-col-2.png'),
                  pygame.image.load('./bird_sprites/row-2-col-3.png'),
                  pygame.image.load('./bird_sprites/row-2-col-4.png'),
                  pygame.image.load('./bird_sprites/row-2-col-5.png'),
                  pygame.image.load('./bird_sprites/row-3-col-2.png'),
                  pygame.image.load('./bird_sprites/row-3-col-3.png'),
                  pygame.image.load('./bird_sprites/row-3-col-4.png'),
                  pygame.image.load('./bird_sprites/row-3-col-5.png')]
bird_moving_right= [pygame.transform.flip(pygame.image.load('./bird_sprites/row-1-col-1.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-1-col-2.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-1-col-3.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-1-col-4.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-1-col-5.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-2-col-1.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-2-col-2.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-2-col-3.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-2-col-4.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-2-col-5.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-3-col-2.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-3-col-3.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-3-col-4.png'), True, False),
                 pygame.transform.flip(pygame.image.load('./bird_sprites/row-3-col-5.png'), True, False)]
background = pygame.image.load('background_2.png')
background_x = 0

tree = pygame.image.load('tree.gif')
tree_x = 890*3

tree_appear_interval = 750

run = True

prevLeft = 0

def redrawGameWindow():
    global flyCount
    global prevLeft
    global background_x
    global tree_x
    win.fill((255,255,255))
    win.blit(background, (background_x, 0))
    win.blit(background, (background_x+2160, 0))
    for i in range(tree_appear_interval, 2160, tree_appear_interval):
        win.blit(tree, (tree_x-i, 250))
    background_x-=10
    tree_x -= 10
    
    if background_x <= 2160*-1:
        background_x = 0
    if tree_x <= 0:
        tree_x = 890 * 3
    
#     pygame.draw.rect(win, (255, 125, 65), (x,y,width,height))
    if flyCount + 1 >= (14*3):
        flyCount = 0
    if left:
        win.blit(bird_moving_left[flyCount//3], (x,y))
        flyCount += 1
        prevLeft = 1
    elif right:
        win.blit(bird_moving_right[flyCount//3], (x,y))
        flyCount += 1
        prevLeft = 0
    else:
        if prevLeft:
            win.blit(bird_moving_left[flyCount//3], (x,y))
            flyCount += 1
        else:
            win.blit(bird_moving_right[flyCount//3], (x,y))
            flyCount += 1
    pygame.display.update()
    
while run:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > velocity:
        x -= velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < screen_width - width:
        x += velocity
        right = True
        left = False
    else:
        left = False
        right = False
        
    if not(isJump):
        if keys[pygame.K_UP] and y > velocity:
            y -= velocity
        if keys[pygame.K_DOWN] and y < screen_height - height:
            y += velocity
        if keys[pygame.K_SPACE]:
            isJump = True
            left = False
            right = False
            flyCount = 0
    else:
        if jumpCount >= -1*jumpExtent:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = jumpExtent
    
    redrawGameWindow()
    
pygame.quit()