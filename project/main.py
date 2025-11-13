import pygame, json, sys, random,datetime


WIDTH, HEIGHT = 600, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


bg_img = pygame.image.load('background_university.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
click_img = pygame.transform.scale(pygame.image.load('click.png'), (100, 100))
shop_img  = pygame.transform.scale(pygame.image.load('shop.png'),  (50, 50))
home_img  = pygame.transform.scale(pygame.image.load('home.png'),  (50, 50))
coin_img = pygame.transform.scale(pygame.image.load('brain.png'), (20, 20))
energy_img = pygame.transform.scale(pygame.image.load('energy.png'), (20, 20))
magazin_img = pygame.transform.scale(pygame.image.load('magazin.png'), (600, 600))
veganpanini_img = pygame.transform.scale(pygame.image.load('veganpanini.png'), (100, 100))
normalpanini_img = pygame.transform.scale(pygame.image.load('normalpanini.png'), (100, 100))
salat_img = pygame.transform.scale(pygame.image.load('salat.png'), (100, 100))
poncik_img = pygame.transform.scale(pygame.image.load('poncik.png'), (100, 100))
strelka_img = pygame.transform.scale(pygame.image.load('strelka.png'), (100, 100))
autobot_img = pygame.transform.scale(pygame.image.load('autobot.png'), (100, 100))
autobotspeed_img = pygame.transform.scale(pygame.image.load('autobotspeed.png'), (100, 100))
dialogwindow_img = pygame.transform.scale(pygame.image.load('dialogwindow.png'), (255, 200))
frame_img = pygame.transform.scale(pygame.image.load('blocknot.png'), (200, 200))
diplom_img = pygame.transform.scale(pygame.image.load('diplom.png'), (100, 130))
exit_img = pygame.transform.scale(pygame.image.load('exit2.png'), (200, 200))
play_img = pygame.transform.scale(pygame.image.load('play2.png'), (200, 200))
save_img = pygame.transform.scale(pygame.image.load('save2.png'), (200, 200))
pause_img = pygame.transform.scale(pygame.image.load('pause.png'), (100, 50))
finish_img = pygame.transform.scale(pygame.image.load('finish.png'), (600, 600))

click_rect = pygame.Rect(0, 0, WIDTH, HEIGHT )
shop_rect  = pygame.Rect(0, 0, 50, 50)
shop2_rect  = pygame.Rect(510, -12, 100, 100)
home_rect  = pygame.Rect(0, 0, 50, 50)
veganpanini_rect = pygame.Rect(125, 118, 100, 100)
normalpanini_rect = pygame.Rect(375, 120, 100, 100)
salat_rect = pygame.Rect(125, 340, 100, 100)
poncik_rect = pygame.Rect(375, 340, 100, 100)
kompik_rect = pygame.Rect(10, 10, 10, 10)
kompik2_rect = pygame.Rect(50, 0, 50, 50)
profesor_rect = pygame.Rect(440, 220, 440, 220)
save_rect = pygame.Rect(200, 190, 200, 200)
exit_rect = pygame.Rect(200, 360, 200, 200)
play_rect = pygame.Rect(200, 20, 200, 200)
pause_rect = pygame.Rect(-22, 50, 70, 50)

def load_balance():
    try:
        with open('player.data.json', 'r', encoding='utf-8') as f:
            val = json.load(f)
        return int(val)
    except Exception:
        return 0

def save_balance(val):
    with open('player.data.json', 'w', encoding='utf-8') as f:
        json.dump(int(val), f)

player_balance = load_balance()

STATE_START = 'start'
STATE_MAIN = "main"
STATE_SHOP = "shop"
STATE_SHOP2 = "shop2"
STATE_FINAL = "final"
state = STATE_START

coin_active = False
coins = []
coin_radius = 20
coin_angle = 0.0
coin_up_speed = 120.0
coin_ang_speed = 2.5

coin_img = pygame.transform.scale(coin_img, (coin_radius*2, coin_radius*1.5))




data = {'fatigue': 0, 'autobot': 0, 'autobotspeed': 0, 'timeexit':0}

def datasave(datat):
    with open("playerdata2.json", 'w', encoding='utf-8') as f:
        json.dump(datat, f, ensure_ascii=False, indent=4)

def dataload():
    try:
        with open("playerdata2.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

data = dataload()



fatigue = data['fatigue']
profesorpose = 0
fatigue_max = 100
bar_width = 200
bar_height = 16
autobot_level = data['autobot']
autobot_speed = data['autobotspeed']
autobotvarlevel = {0:0,1:1,2:5,3:10,4:20,5:50,6:200,7:500,8:900}
autobotvarspeed = {0:15,1:14,2:11,3:8,4:7,5:6,6:5,7:4,8:2,9:1}

if int(data['autobot']):
    delta_t = (datetime.datetime.now() + datetime.timedelta(seconds=int(autobotvarspeed[data['autobotspeed']])))
else :
    delta_t = 0

if data['timeexit'] != 0:
    s = data['timeexit'].split()
    s1 = s[0].split('-')
    s2 = s[1].split(':')
    s = s1+s2
    g = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
    s1 = g[0].split('-')
    s2 = g[1].split(':')
    g = s1 + s2
    for i in range(len(s)):
        s[i]=int(g[i])-int(s[i])
    seconds = s[0]*31536000 + s[1]*2628288 + s[2]*86400 + s[3]* 3600 + s[4]*60 + s[5]
    player_balance += int(seconds*autobotvarlevel[data['autobot']]/autobotvarspeed[data['autobotspeed']])







def start_coin():
    global coin_active, coin_angle , coins
    coin_active = True
    coins.append({
        "x": random.randint(540,560),
        "y": random.randint(280,290),
        "angle": 0.0})

def draw_bar(surf, x, y, value, max_value, color, bg_color):

    pygame.draw.rect(surf, bg_color, (x, y, bar_width, bar_height), border_radius=6)

    fill = int(bar_width * value / max_value)
    pygame.draw.rect(surf, color, (x, y, fill, bar_height), border_radius=6)

    pygame.draw.rect(surf, (40,40,40), (x, y, bar_width, bar_height), 2, border_radius=6)

def update_coins(dt):
    global coin_angle, coin_active
    if not coin_active:
        return
    for c in coins[:]:
        c["y"] -= coin_up_speed * dt
        c["angle"] += coin_ang_speed * dt
        if c["y"] + coin_radius < 0:
            coins.remove(c)


def draw_coins(surf):
    for c in coins:
        rect = coin_img.get_rect(center=(int(c["x"]), int(c["y"])))
        surf.blit(coin_img, rect.topleft)

        pygame.draw.circle(surf, (126, 126, 90), (int(mx), int(my)), 2)
        tail_len = 12

state = data['state']

running = True
while running:
    dt = clock.tick(60) / 1000.0
    font = pygame.font.SysFont(None, 28)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_balance(player_balance)
            data['fatigue'] = fatigue
            data['autobot'] = autobot_level
            data['autobotspeed'] = autobot_speed
            data['timeexit'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datasave(data)




        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if state == STATE_MAIN:
                if click_rect.collidepoint(mx, my) and fatigue > 0:
                    profesorpose +=1
                    player_balance = int(player_balance) + 1

                    start_coin()
                    fatigue = max(fatigue - 1, 0)
                if shop_rect.collidepoint(mx, my):
                    state = STATE_SHOP
                if pause_rect.collidepoint(mx, my):
                    state = STATE_START
                    pygame.display.flip()
                    screen.fill((0,0,0))
            elif state == STATE_START:
                if play_rect.collidepoint(mx, my):
                    state = STATE_MAIN
                if save_rect.collidepoint(mx, my):
                    save_balance(player_balance)
                    data['fatigue'] = fatigue
                    data['autobot'] = autobot_level
                    data['autobotspeed'] = autobot_speed
                    data['timeexit'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    datasave(data)
                if exit_rect.collidepoint(mx, my):
                    running = False

            elif state == STATE_FINAL:
                screen.blit(finish_img , (0,0))

            elif state == STATE_SHOP:
                if home_rect.collidepoint(mx, my):
                    state = STATE_MAIN
                if veganpanini_rect.collidepoint(mx, my) and player_balance >= 45:
                    player_balance = player_balance - 45
                    fatigue += 65

                if normalpanini_rect.collidepoint(mx, my) and player_balance >= 55:
                    player_balance = player_balance - 55
                    fatigue += 85

                if salat_rect.collidepoint(mx, my) and player_balance >= 60:
                    player_balance = player_balance - 60
                    fatigue += 75

                if poncik_rect.collidepoint(mx, my) and player_balance >= 20:
                    player_balance = player_balance - 20
                    fatigue += 25

                if shop2_rect.collidepoint(mx, my):
                    state = STATE_SHOP2

            elif state == STATE_SHOP2:
                if home_rect.collidepoint(mx, my):
                    state = STATE_MAIN
                if shop2_rect.collidepoint(mx, my):
                    state = STATE_SHOP
                if salat_rect.collidepoint(mx, my) and player_balance >= 1000000:
                    player_balance = player_balance - 1000000
                    state = STATE_FINAL
                    data['state'] = STATE_FINAL
                    datasave(data)
                    screen.fill((0,0,0))
                    screen.blit(finish_img, (0, 0))

                if veganpanini_rect.collidepoint(mx, my) and player_balance >= (autobotvarlevel[data['autobot']]*250)+250 and data['autobot'] <8:
                    player_balance = player_balance - (autobotvarlevel[data['autobot']]*250)+250
                    data['autobot'] += 1
                    autobot_level = data['autobot']


                if normalpanini_rect.collidepoint(mx, my) and player_balance >= ((8 - autobotvarspeed[data['autobotspeed']]) * 750) + 7250 and data['autobotspeed'] <9:
                    player_balance -= ((8 - autobotvarspeed[data['autobotspeed']]) * 750) + 7250
                    data['autobotspeed'] += 1
                    autobot_speed = data['autobotspeed']
                    if delta_t == 0:
                        delta_t = (datetime.datetime.now() + datetime.timedelta(seconds=int(autobotvarspeed[data['autobotspeed']])))



    update_coins(dt)

    if state == STATE_START:
        screen.blit(play_img, play_rect.topleft)
        screen.blit(save_img, save_rect.topleft)
        screen.blit(exit_img, exit_rect.topleft)
    elif state == STATE_MAIN:
        screen.blit(bg_img, (0, 0))

        screen.blit(shop_img, shop_rect)

        bacground_txt = font.render(f"кликайте для получения знаний: ", True, (46, 139, 87))
        screen.blit(bacground_txt, (170, 230))
        txt = font.render(f"знания:", True, (46, 139, 87))
        screen.blit(txt, (400, 50))
        txt = font.render(f"{player_balance}", True, (46, 139, 87))
        screen.blit(txt, (400, 70))
        draw_coins(screen)
        screen.blit(pause_img, pause_rect.topleft)


        draw_bar(screen, 400, 2, fatigue, fatigue_max, (220, 140, 40), (80, 70, 50))
        screen.blit(energy_img, (375, 0))
        if data['autobotspeed'] > 0:
            autobotspeed_img = pygame.transform.scale(pygame.image.load('autobotspeed.png'),(50,50))
            screen.blit(autobotspeed_img, (50, 0))
            autobotspeed_img = pygame.transform.scale(pygame.image.load('autobotspeed.png'), (100, 100))

        if profesorpose == 0:
            profesor_img = pygame.transform.scale(pygame.image.load('profesor1.png'), (200, 200))
        if profesorpose == 1:
            profesor_img = pygame.transform.scale(pygame.image.load('profesor2.png'), (200, 200))
        screen.blit(profesor_img, (440, 220))

        mouse_pos = pygame.mouse.get_pos()
        if profesor_rect.collidepoint(mouse_pos):
            screen.blit(dialogwindow_img, (300, 50))
            text = "     U\nI = - ,     U-напр.\n     R      R-сопр."
            lines = text.split("\n")
            y = 110
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (343, y))
                y += surf.get_height()

        if kompik2_rect.collidepoint(mouse_pos) and data['autobotspeed'] > 0:
            screen.blit(frame_img, (70,0))
            text = "У вас\nакктиви-\nрована\nподписка"
            lines = text.split("\n")
            y=70
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (117, y))
                y += surf.get_height()

        if dt >= 0.019:
            profesorpose = 0
        if dt >= 0.12:
            fatigue += 0.01




    elif state == STATE_SHOP:
        screen.blit(magazin_img, (0,0))
        screen.blit(shop_img, home_rect.topleft)
        screen.blit(veganpanini_img, veganpanini_rect)
        screen.blit(normalpanini_img, normalpanini_rect)
        screen.blit(salat_img, salat_rect)
        screen.blit(poncik_img,poncik_rect)
        screen.blit(strelka_img, shop2_rect.topleft)
        txt = font.render(f"45 brains", True, (255, 255, 255))
        screen.blit(txt, (130, 210))
        txt = font.render(f"55 brains", True, (255, 255, 255))
        screen.blit(txt, (380, 210))
        txt = font.render(f"60 brains", True, (255, 255, 255))
        screen.blit(txt, (130, 425))
        txt = font.render(f"20 brains", True, (255, 255, 255))
        screen.blit(txt, (380, 430))

        mouse_pos = pygame.mouse.get_pos()
        if veganpanini_rect.collidepoint(mouse_pos):
            screen.blit(frame_img, (-10,0))
            text = "Восстана-\nвливает\n65%энер-\nгии"
            lines = text.split("\n")
            y=70
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (37, y))
                y += surf.get_height()
        if normalpanini_rect.collidepoint(mouse_pos):
            screen.blit(frame_img, (160,0))
            text = "Восстана-\nвливает\n85%энер-\nгии"
            lines = text.split("\n")
            y=70
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (207, y))
                y += surf.get_height()

        if salat_rect.collidepoint(mouse_pos):
            screen.blit(frame_img, (-10,200))
            text = "Восстана-\nвливает\n75%энер-\nгии"
            lines = text.split("\n")
            y=270
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (37, y))
                y += surf.get_height()
        if poncik_rect.collidepoint(mouse_pos):
            screen.blit(frame_img, (160,200))
            text = "Восстана-\nвливает\n25%энер-\nгии"
            lines = text.split("\n")
            y=270
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (207, y))
                y += surf.get_height()



    elif state == STATE_SHOP2:
        screen.blit(magazin_img, (0,0))
        screen.blit(shop_img, home_rect.topleft)
        screen.blit(strelka_img, shop2_rect.topleft)
        screen.blit(autobot_img, veganpanini_rect)
        screen.blit(autobotspeed_img, normalpanini_rect)
        screen.blit(diplom_img, salat_rect)
        txt = font.render(f"{(autobotvarlevel[data['autobot']]*250)+250} brains", True, (255, 255, 255))
        screen.blit(txt, (120, 210))
        txt = font.render(f"{((8-autobotvarspeed[data['autobotspeed']])*750)+7250} brains", True, (255, 255, 255))
        screen.blit(txt, (370, 215))
        txt = font.render(f"1000000 brains", True, (255, 255, 255))
        screen.blit(txt, (105, 425))

        mouse_pos = pygame.mouse.get_pos()
        if veganpanini_rect.collidepoint(mouse_pos):
            screen.blit(frame_img, (-10, 0))
            text = "Добав-\nляет\nзнания\nавтомати-\nчески"
            lines = text.split("\n")
            y = 65
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (40, y))
                y += surf.get_height()
        if normalpanini_rect.collidepoint(mouse_pos):
            screen.blit(frame_img, (160, 0))
            text = "Увеличи-\nвает\nскорость\nполуче-\nния\nзнаний"
            lines = text.split("\n")
            y = 55
            for line in lines:
                surf = font.render(line, True, (0, 0, 0))
                screen.blit(surf, (213, y))
                y += surf.get_height()

    if(int(data['autobotspeed']) > 0 and dt >= 0.015 ):
        delta_now = datetime.datetime.now()

        if delta_now >= delta_t:
            delta_t = (datetime.datetime.now() + datetime.timedelta(seconds=int(autobotvarspeed[data['autobotspeed']])))
            player_balance += autobotvarlevel[data['autobot']]




    pygame.display.flip()


pygame.quit()
sys.exit()
