import pygame
from menu import menu
from button import Button
import sqlite3


def reg():
    pygame.init()
    screen_size = (600, 400)
    screen = pygame.display.set_mode(screen_size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True

    con = sqlite3.connect("data/users.db")
    cur = con.cursor()

    f1 = pygame.font.Font(None, 60)
    f2 = pygame.font.Font(None, 32)
    text_color = 'white'

    standart_width = 300
    standart_height = 32
    input_box1 = pygame.Rect(150, 75, standart_width, standart_height)
    input_box2 = pygame.Rect(150, 175, standart_width, standart_height)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive

    text1 = f2.render('Имя:', True, text_color)
    text2 = f2.render('Пароль:', True, text_color)
    text3 = f2.render('Зарегистрироваться', True, text_color)
    btn_enter = Button(220, 240, text3, text_color)

    text_warning = f2.render('', True, text_color)

    text_login = ''
    write_login = False
    text_password = ''
    write_password = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if write_login:
                    # if event.key == pygame.K_RETURN:
                    #    return text
                    if event.key == pygame.K_BACKSPACE:
                        text_login = text_login[:-1]
                    else:
                        text_login += event.unicode
                elif write_password:
                    if event.key == pygame.K_BACKSPACE:
                        text_password = text_password[:-1]
                    else:
                        text_password += event.unicode
        screen.fill(pygame.Color("black"))

        # Render the current text.
        txt_surface1 = f2.render(text_login, True, 'white')
        txt_surface2 = f2.render(text_password, True, 'white')
        # Resize the box if the text is too long.
        width1 = max(standart_width, txt_surface1.get_width() + 10)
        input_box1.w = width1
        width2 = max(standart_width, txt_surface2.get_width() + 10)
        input_box2.w = width2
        # Blit the text.
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
        screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)

        screen.blit(text1, (150, 50))
        screen.blit(text2, (150, 150))

        btn_enter.draw(screen)
        screen.blit(text_warning, (180, 300))

        if btn_enter.mouse_check(pygame.mouse.get_pos()):
            btn_enter.color = 'red'
        else:
            btn_enter.color = text_color

        pressed = pygame.mouse.get_pressed()
        if pressed[0]:  # обработка нажатий левой кнопки мыши
            x1, y1 = pygame.mouse.get_pos()
            if input_box1.x <= x1 <= input_box1.x + input_box1.width and input_box1.y <= y1 <= input_box1.y + input_box1.height:
                color1 = color_active
                write_login = True
                color2 = color_inactive
                write_password = False
            elif input_box2.x <= x1 <= input_box2.x + input_box2.width and input_box2.y <= y1 <= input_box2.y + input_box2.height:
                color1 = color_inactive
                write_login = False
                color2 = color_active
                write_password = True
            else:
                color1 = color_inactive
                write_login = False
                color2 = color_inactive
                write_password = False

            if btn_enter.mouse_check((x1, y1)):
                if text_login and text_password:
                    res = cur.execute('''
                                SELECT name, maps from users WHERE name LIKE "{}"
                                '''.format(text_login, text_password)).fetchall()
                    if len(res) == 0:
                        cur.execute('''
                        INSERT INTO users (name, password, maps) VALUES ("{}", "{}", 0) 
                        '''.format(text_login, text_password))
                        con.commit()
                        name, maps = text_login, 0
                        menu(screen, name, maps)
                    else:
                        text_warning = f2.render('Пользователь уже существует', True, text_color)
                else:
                    text_warning = f2.render('Заполните все поля', True, text_color)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
