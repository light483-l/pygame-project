import pygame
from tets import main
from button import Button
import time
import sqlite3


def menu(screen, name, maps):
    pygame.init()
    screen_size = screen.get_size()
    FPS = 60
    clock = pygame.time.Clock()
    running = True

    f1 = pygame.font.Font(None, 60)
    f2 = pygame.font.Font(None, 28)
    text_color = 'white'

    text1 = f1.render('Играть', True, text_color)
    btn_start = Button(230, 150, text1, text_color)
    text2 = f1.render('Правила игры', True, text_color)
    btn_rules = Button(160, 250, text2, text_color)

    text3 = f1.render('OK', True, text_color)
    btn_ok = Button((screen_size[0] - text3.get_width() + 20) / 2, 350, text3, text_color)

    text_rules_1 = f1.render('Правила игры:', True, text_color)
    text_rules_2 = f2.render('Главный герой попал в лабиринт и ему нужно ', True, text_color)
    text_rules_3 = f2.render('пройти все его уровни, чтобы выйти из него.', True, text_color)
    text_rules_4 = f2.render('В лабиринте находятся ключи от дверей, которые нужно', True, text_color)
    text_rules_5 = f2.render('открывать, чтобы продвигаться далее,', True, text_color)
    text_rules_6 = f2.render('но рядом с ними находятся враги.', True, text_color)
    text_rules_7 = f2.render('В лабиринте может попасться два вида врагов и оружия', True, text_color)
    text_rules_8 = f2.render('Один из врагов — Эканс — большая фиолетовая змея,', True, text_color)
    text_rules_9 = f2.render('ее можно убить любым оружием, найденым в лабиринте,', True, text_color)
    text_rules_10 = f2.render('но только меч с красной рукояткой выдержит удар по ней.', True, text_color)
    text_rules_11 = f2.render('Второй враг — Хонтер — фиолетовый призрак, может', True, text_color)
    text_rules_12 = f2.render('быть убит только мечом, но меч сразу ломается.', True, text_color)

    rules = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color("black"))

        if not rules:

            btn_start.draw(screen)
            btn_rules.draw(screen)

            if btn_start.mouse_check(pygame.mouse.get_pos()):
                btn_start.color = 'red'
            else:
                btn_start.color = text_color

            if btn_rules.mouse_check(pygame.mouse.get_pos()):
                btn_rules.color = 'red'
            else:
                btn_rules.color = text_color

            pressed = pygame.mouse.get_pressed()
            if pressed[0]:  # обработка нажатий левой кнопки мыши
                x1, y1 = pygame.mouse.get_pos()
                if btn_start.mouse_check((x1, y1)):
                    time.sleep(0.4)
                    win = main(screen, name, maps + 1)
                    screen = pygame.display.set_mode(screen_size)
                    if win and maps < 3:
                        maps += 1
                        con = sqlite3.connect("data/users.db")
                        cur = con.cursor()
                        cur.execute(f'''
                        UPDATE users SET maps = {maps} WHERE name LIKE "{name}"
                        ''')
                        con.close()
                elif btn_rules.mouse_check((x1, y1)):
                    time.sleep(0.4)
                    rules = True
        else:
            screen.blit(text_rules_1, ((screen_size[0] - text_rules_1.get_width()) / 2, 10))
            screen.blit(text_rules_2, ((screen_size[0] - text_rules_2.get_width()) / 2, 70))
            screen.blit(text_rules_3, ((screen_size[0] - text_rules_3.get_width()) / 2, 90))
            screen.blit(text_rules_4, ((screen_size[0] - text_rules_4.get_width()) / 2, 120))
            screen.blit(text_rules_5, ((screen_size[0] - text_rules_5.get_width()) / 2, 140))
            screen.blit(text_rules_6, ((screen_size[0] - text_rules_6.get_width()) / 2, 160))
            screen.blit(text_rules_7, ((screen_size[0] - text_rules_7.get_width()) / 2, 190))
            screen.blit(text_rules_8, ((screen_size[0] - text_rules_8.get_width()) / 2, 210))
            screen.blit(text_rules_9, ((screen_size[0] - text_rules_9.get_width()) / 2, 230))
            screen.blit(text_rules_10, ((screen_size[0] - text_rules_10.get_width()) / 2, 250))
            screen.blit(text_rules_11, ((screen_size[0] - text_rules_11.get_width()) / 2, 270))
            screen.blit(text_rules_12, ((screen_size[0] - text_rules_12.get_width()) / 2, 290))

            btn_ok.draw(screen)

            if btn_ok.mouse_check(pygame.mouse.get_pos()):
                btn_ok.color = 'red'
            else:
                btn_ok.color = text_color

            pressed = pygame.mouse.get_pressed()
            if pressed[0]:  # обработка нажатий левой кнопки мыши
                x1, y1 = pygame.mouse.get_pos()
                if btn_ok.mouse_check((x1, y1)):
                    time.sleep(0.4)
                    rules = False

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    screen_size = (600, 600)
    screen = pygame.display.set_mode(screen_size)
    menu(screen, 'user', 0)
