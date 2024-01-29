import pygame
from sys import exit
from random import randint
def display_Score():
    current_Time = int(pygame.time.get_ticks()/1000) - defult_Score
    Score_surf = Score_font.render(f'Score: {current_Time}',False,(64,64,64))
    Score_rect = Score_surf.get_rect(center=(400, 50))
    screen.blit(Score_surf,Score_rect)
    return current_Time

def obs_movement(obs_list):
    if obs_list:
        for obs_rect_list in obs_list:
            obs_rect_list.x -= 5
            if obs_rect_list.bottom == 300: screen.blit(Pokeball_surf, obs_rect_list)
            else: screen.blit(beedrill_surf, obs_rect_list)

        obs_list = [obs for obs in obs_list if obs.x > -100]
        return obs_list
    else: return []

def collision (pikachu,obs):
     if obs:
         for obs_rect_list in obs:
             if pikachu.colliderect(obs_rect_list): return False
     return True

def Pika_animation():
    global Pikachu_surf,Pikachu_index
    if Pikachu_rect.bottom < 300:
        Pikachu_surf = Pikachu_jump
    else:
        Pikachu_index += 0.1
        if Pikachu_index >= len(Pikachu_walk):Pikachu_index = 0
        Pikachu_surf = Pikachu_walk[int(Pikachu_index)]

pygame.init()
screen =pygame.display.set_mode((800,400))
pygame.display.set_caption('Pikachu Hop')
clock = pygame.time.Clock()
Score_font = pygame.font.Font('font/Pixeltype.ttf',80)
game_active= False
defult_Score = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

Sky_surf = pygame.image.load('graphics/Sky.png').convert()
Ground_surf = pygame.image.load('graphics/ground.png').convert()

#Score_surf = Score_font.render('Start Now',False,(64,64,64))
#Score_rect = Score_surf.get_rect(center=(400,50))

Pokeball_roll1 = pygame.image.load('graphics/pokeball/pokeball1.png').convert_alpha()
Pokeball_roll2 = pygame.image.load('graphics/pokeball/pokeball2.png').convert_alpha()
Pokeball_frame = [Pokeball_roll1, Pokeball_roll2]
Pokeball_frame_index = 0
Pokeball_surf = Pokeball_frame[Pokeball_frame_index]

bee_fly1 = pygame.image.load('graphics/beedrill/Fly1.png').convert_alpha()
bee_fly2 = pygame.image.load('graphics/beedrill/Fly2.png').convert_alpha()
beedrill_frame = [bee_fly1, bee_fly2]
beedrill_frame_index = 0
beedrill_surf = beedrill_frame[beedrill_frame_index]

obs_rect_list = []

Pikachu_walk1 =pygame.image.load('graphics/Pikachu/player_walk_1.png').convert_alpha()
Pikachu_walk2 =pygame.image.load('graphics/Pikachu/player_walk_2.png').convert_alpha()
Pikachu_walk = [Pikachu_walk1,Pikachu_walk2]
Pikachu_index =0
Pikachu_jump =pygame.image.load('graphics/Pikachu/jump.png').convert_alpha()
Pikachu_surf = Pikachu_walk[Pikachu_index]
Pikachu_rect = Pikachu_walk1.get_rect(midbottom =(80, 300))
Pikachu_gravity = 0
Jump_sound = pygame.mixer.Sound('audio/jump.mp3')
Jump_sound.set_volume(0.5)

Pikachu_stand =pygame.image.load('graphics/Pikachu/player_stand.png').convert_alpha()
Pikachu_stand = pygame.transform.rotozoom(Pikachu_stand,0,2)
Pikachu_stand_rect = Pikachu_stand.get_rect(center = (400,200))

game_title = Score_font.render('Pikachu Hop',False,'#ebd834')
game_title_rect =game_title.get_rect(center=(400,80))

game_message = Score_font.render('Press space to Run',False,'#ebd834')
game_message_rect =game_message.get_rect(center=(400,320))

obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer,1500)

pokeball_timer = pygame.USEREVENT + 2
pygame.time.set_timer(pokeball_timer,500)

beedrill_timer = pygame.USEREVENT + 3
pygame.time.set_timer(beedrill_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN and Pikachu_rect.bottom >=300:
                if event.key == pygame.K_SPACE:
                    Pikachu_gravity = -20
                    Jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                defult_Score = int(pygame.time.get_ticks()/1000)
        if game_active:
            if event.type == obs_timer:
                if randint(0,2):
                    obs_rect_list.append(Pokeball_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obs_rect_list.append(beedrill_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == pokeball_timer:
                if Pokeball_frame_index == 0: Pokeball_frame_index = 1
                else: Pokeball_frame_index = 0
                Pokeball_surf = Pokeball_frame[Pokeball_frame_index]

            if event.type == beedrill_timer:
                if beedrill_frame_index == 0: beedrill_frame_index = 1
                else: beedrill_frame_index = 0
                beedrill_surf = beedrill_frame[beedrill_frame_index]


       # if event.type == pygame.KEYUP:
    if game_active:
        screen.blit(Sky_surf,(0,0))
        screen.blit(Ground_surf, (0, 300))
        score = display_Score()

        Pikachu_gravity += 1
        Pikachu_rect.y += Pikachu_gravity
        if Pikachu_rect.bottom >= 300: Pikachu_rect.bottom = 300
        Pika_animation()
        screen.blit(Pikachu_surf, Pikachu_rect)

        obs_rect_list = obs_movement(obs_rect_list)

        game_active = collision(Pikachu_rect,obs_rect_list)

        #
    else:
        screen.fill('#34a1eb')
        screen.blit(Pikachu_stand,Pikachu_stand_rect)
        obs_rect_list.clear()
        Pikachu_rect.midbottom=(80,300)
        Pikachu_gravity = 0

        score_message = Score_font.render(f'Your Score:{score}', False, '#ebd834')
        score_message_rect = score_message.get_rect(center=(400, 320))
        screen.blit(game_title, game_title_rect)
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)