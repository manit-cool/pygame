import pygame, sys
clock = pygame.time.Clock()
from pygame.locals import *

# system defs
pygame.init()
pygame.display.set_caption("Platformer")

# how you name the screen
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # this is how you set the display mode
display = pygame.Surface((300, 200))
true_scroll = [0, 0]

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


# player vars
player_img = pygame.image.load("platformer game/Pyplay.png") # this is how you load images
player_img.set_colorkey((255,255,255)) # this value will remove all white in the background or in general of the photo :)
y_momentum = 0
air_timer = 0
moving_right = False
moving_left = False
player_rect = pygame.Rect(50, 50, player_img.get_width(), player_img.get_height())

# game vars
grass_img = pygame.image.load("platformer game/grass.png")
TILE_SIZE = grass_img.get_width()
dirt_img = pygame.image.load("platformer game/dirt.png")

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('platformer game/map')

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top':False,'bottom':False,'right':False,"left":False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

while True:
    display.fill((146,244,255))  # this does 2 things
    # 1 - change the background color into what we want
    # 2 - clear the screen every frame so that there isn't any
    # smearing :)

    true_scroll[0] += (player_rect.x - true_scroll[0]-152)/20# 152 = 150 (half of small display x)
    # + 2 is half of player.get_width :D
    true_scroll[1] += (player_rect.y - true_scroll[1]-106)/20# 106 = 100 (half of small display y) +
    # 6 which is half of player.get_height :D
    
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # Now we will begin the rendering of the tilemap:
    tile_rects = []
    y = 0 
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += y_momentum
    y_momentum += 0.2
    if y_momentum > 3:
        y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    if collisions['top']:
        y_momentum += 2

    display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))  # puts one surface on the other

    for event in pygame.event.get(): # this for-loop is how you would normally do events
        if event.type == QUIT: # this is asking if the keyboard state is something
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: # these event.type look for keyboard states and then those states have their own parts to keys and yada yada
            # the code above will trigger any time a key is pressed down :)
            if event.key == K_RIGHT:  # as you can see the first if (keydown) is broad saying that if any key is pressed and now this is saying if I am pressed then do that
                moving_right = True  # *that
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE) # this resizes our small display to the window_size or like a zoom in :)
    screen.blit(surf, (0, 0)) # this now puts that surface (display) on to the screen =D
    pygame.display.update()
    clock.tick(60)

            



