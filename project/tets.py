import pygame
import os
from button import Button
import time


def main(screen, name, level=1):
    match level:
        case 1:
            map_file = 'map1.map'
        case 2:
            map_file = 'map2.map'
        case 3:
            map_file = 'map3.map'

    def load_image(name, color_key=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Не удаётся загрузить:', name)
            raise SystemExit(message)
        image = image.convert_alpha()
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        return image

    pygame.init()
    screen_size = screen.get_size()
    FPS = 60

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png'),
        'key_exit': load_image('key_exit.png'),
        'key_door': load_image('key_door.png'),
        'exit': load_image('exit.png'),
        'door': load_image('door.png'),
        'chest1': load_image('chest1.png'),
        'chest2': load_image('chest2.png'),
        'monster1': load_image('monster1.png'),
        'monster2': load_image('monster2.png')
    }
    player_image = load_image('mar.png')

    tile_width = tile_height = 50

    class SpriteGroup(pygame.sprite.Group):

        def __init__(self):
            super().__init__()

        def shift(self, vector):
            global level_map
            if vector == "up":
                max_lay_y = max(self, key=lambda sprite:
                sprite.abs_pos[1]).abs_pos[1]
                for sprite in self:
                    sprite.abs_pos[1] -= (tile_height * max_y
                                          if sprite.abs_pos[1] == max_lay_y else 0)
            elif vector == "down":
                min_lay_y = min(self, key=lambda sprite:
                sprite.abs_pos[1]).abs_pos[1]
                for sprite in self:
                    sprite.abs_pos[1] += (tile_height * max_y
                                          if sprite.abs_pos[1] == min_lay_y else 0)
            elif vector == "left":
                max_lay_x = max(self, key=lambda sprite:
                sprite.abs_pos[0]).abs_pos[0]
                for sprite in self:
                    if sprite.abs_pos[0] == max_lay_x:
                        sprite.abs_pos[0] -= tile_width * max_x
            elif vector == "right":
                min_lay_x = min(self, key=lambda sprite:
                sprite.abs_pos[0]).abs_pos[0]
                for sprite in self:
                    sprite.abs_pos[0] += (tile_height * max_x
                                          if sprite.abs_pos[0] == min_lay_x else 0)

    class Sprite(pygame.sprite.Sprite):

        def __init__(self, group):
            super().__init__(group)
            self.rect = None

        def get_event(self, event):
            pass

    class Tile(Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(sprite_group)
            image = tile_images[tile_type]
            self.image = pygame.transform.scale(image, (50, 50))
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            self.abs_pos = [self.rect.x, self.rect.y]

        def set_pos(self, x, y):
            self.abs_pos = [x, y]

    class Player(Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(hero_group)
            image = player_image
            self.image = pygame.transform.scale(image, (24, 40))
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 15, tile_height * pos_y + 5)
            self.pos = (pos_x, pos_y)
            self.abs_pos = [self.rect.x, self.rect.y]

            self.weapon = 0
            self.got_exit_key = False
            self.got_door_key = False

        def set_pos(self, x, y):
            self.abs_pos = [x, y]

        def move(self, x, y):
            camera.dx += tile_width * (x - self.pos[0])
            camera.dy += tile_height * (y - self.pos[1])
            print(camera.dx, camera.dy)
            self.pos = (x, y)
            for sprite in hero_group:
                camera.apply(sprite)

    class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            obj.rect.x = obj.abs_pos[0] + self.dx
            obj.rect.y = obj.abs_pos[1] + self.dy

        def update(self, target):
            self.dx = 0
            self.dy = 0

    player = None
    running = True
    clock = pygame.time.Clock()
    sprite_group = SpriteGroup()
    hero_group = SpriteGroup()

    win = False
    game_end = False

    def start_screen():

        fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
        screen.blit(fon, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)

    def load_level(filename):
        filename = "maps/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

    def generate_level(level):
        screen = pygame.display.set_mode((50 * len(level[0]) + 100, 50 * len(level)))
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                    level[y][x] = "."
                elif level[y][x] == '+':
                    Tile('key_exit', x, y)
                elif level[y][x] == '-':
                    Tile('key_door', x, y)
                elif level[y][x] == '*':
                    Tile('exit', x, y)
                elif level[y][x] == '/':
                    Tile('door', x, y)
                elif level[y][x] == '1':
                    Tile('chest1', x, y)
                elif level[y][x] == '2':
                    Tile('chest2', x, y)
                elif level[y][x] == '4':
                    Tile('monster1', x, y)
                elif level[y][x] == '5':
                    Tile('monster2', x, y)
        return new_player, x, y

    def move(hero, movement):

        x, y = hero.pos
        if movement == "up":
            prev_y = y - 1 if y != 0 else max_y
            if level_map[prev_y][x] != "#":
                if level_map[prev_y][x] == '*' and hero.got_exit_key:
                    print('Победа')
                    return True, True
                elif level_map[prev_y][x] == '*':
                    pass
                elif level_map[prev_y][x] == '/' and not hero.got_door_key:
                    pass
                else:
                    if prev_y == max_y:
                        hero.move(x, prev_y - 1)
                    else:
                        hero.move(x, prev_y)

                    match level_map[prev_y][x]:
                        case '+':
                            hero.got_exit_key = True
                            level_map[prev_y][x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '-':
                            hero.got_door_key = True
                            level_map[prev_y][x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '/':
                            hero.got_door_key = False
                            level_map[prev_y][x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '1':
                            if hero.weapon < 1:
                                hero.weapon = 1
                                level_map[prev_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '2':
                            if hero.weapon < 2:
                                hero.weapon = 2
                                level_map[prev_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '4':
                            if hero.weapon >= 1:
                                if hero.weapon == 1:
                                    hero.weapon = 0
                                level_map[prev_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False
                        case '5':
                            if hero.weapon >= 2:
                                hero.weapon = 0
                                level_map[prev_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False

        elif movement == "down":
            next_y = y + 1 if y != max_y else 0
            if level_map[next_y][x] != "#":
                if level_map[next_y][x] == '*' and hero.got_exit_key:
                    print('Победа')
                    return True, True
                elif level_map[next_y][x] == '*':
                    pass
                elif level_map[next_y][x] == '/' and not hero.got_door_key:
                    pass
                else:
                    if next_y == 0:
                        hero.move(x, next_y + 1)
                    else:
                        hero.move(x, next_y)

                    match level_map[next_y][x]:
                        case '+':
                            hero.got_exit_key = True
                            level_map[next_y][x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '-':
                            hero.got_door_key = True
                            level_map[next_y][x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '/':
                            hero.got_door_key = False
                            level_map[next_y][x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = load_image('grass.png')
                        case '1':
                            if hero.weapon < 1:
                                hero.weapon = 1
                                level_map[next_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '2':
                            if hero.weapon < 2:
                                hero.weapon = 2
                                level_map[next_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '4':
                            if hero.weapon >= 1:
                                if hero.weapon == 1:
                                    hero.weapon = 0
                                level_map[next_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False
                        case '5':
                            if hero.weapon >= 2:
                                hero.weapon = 0
                                level_map[next_y][x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False

        elif movement == "left":
            prev_x = x - 1 if x != 0 else max_x
            if level_map[y][prev_x] != "#":
                if level_map[y][prev_x] == '*' and hero.got_exit_key:
                    print('Победа')
                    return True, True
                elif level_map[y][prev_x] == '*':
                    pass
                elif level_map[y][prev_x] == '/' and not hero.got_door_key:
                    pass
                else:
                    if prev_x == max_x:
                        hero.move(prev_x - 1, y)
                    else:
                        hero.move(prev_x, y)

                    match level_map[y][prev_x]:
                        case '+':
                            hero.got_exit_key = True
                            level_map[y][prev_x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '-':
                            hero.got_door_key = True
                            level_map[y][prev_x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '/':
                            hero.got_door_key = False
                            level_map[y][prev_x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '1':
                            if hero.weapon < 1:
                                hero.weapon = 1
                                level_map[y][prev_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '2':
                            if hero.weapon < 2:
                                hero.weapon = 2
                                level_map[y][prev_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '4':
                            if hero.weapon >= 1:
                                if hero.weapon == 1:
                                    hero.weapon = 0
                                level_map[y][prev_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False
                        case '5':
                            if hero.weapon >= 2:
                                hero.weapon = 0
                                level_map[y][prev_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False

        elif movement == "right":
            next_x = x + 1 if x != max_x else 0
            if level_map[y][next_x] != "#":
                if level_map[y][next_x] == '*' and hero.got_exit_key:
                    print('Победа')
                    return True, True
                elif level_map[y][next_x] == '*':
                    pass
                elif level_map[y][next_x] == '/' and not hero.got_door_key:
                    pass
                else:
                    if next_x == 0:
                        hero.move(next_x + 1, y)
                    else:
                        hero.move(next_x, y)

                    match level_map[y][next_x]:
                        case '+':
                            hero.got_exit_key = True
                            level_map[y][next_x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '-':
                            hero.got_door_key = True
                            level_map[y][next_x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '/':
                            hero.got_door_key = False
                            level_map[y][next_x] = '.'
                            cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                            for sp in cols:
                                sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '1':
                            if hero.weapon < 1:
                                hero.weapon = 1
                                level_map[y][next_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '2':
                            if hero.weapon < 2:
                                hero.weapon = 2
                                level_map[y][next_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                        case '4':
                            if hero.weapon >= 1:
                                if hero.weapon == 1:
                                    hero.weapon = 0
                                level_map[y][next_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False
                        case '5':
                            if hero.weapon >= 2:
                                hero.weapon = 0
                                level_map[y][next_x] = '.'
                                cols = pygame.sprite.spritecollide(hero, sprite_group, False)
                                for sp in cols:
                                    sp.image = pygame.transform.scale(load_image('grass.png'), (50, 50))
                            else:
                                print('game over')
                                return True, False
        return False, False

    f = pygame.font.Font(None, 24)
    text_color = 'white'
    text1 = f.render('Name:', True, text_color)
    text2 = f.render(name, True, text_color)

    f1 = pygame.font.Font(None, 60)
    text_ok = f1.render('OK', True, text_color)
    btn_ok = Button(270, 170, text_ok, text_color)

    camera = Camera()
    level_map = load_level(map_file)
    hero, max_x, max_y = generate_level(level_map)
    camera.update(hero)

    if game_end:
        screen = pygame.display.set_mode((600, 600))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and not game_end:
                if event.key == pygame.K_UP:
                    game_end, win = move(hero, "up")
                elif event.key == pygame.K_DOWN:
                    game_end, win = move(hero, "down")
                elif event.key == pygame.K_LEFT:
                    game_end, win = move(hero, "left")
                elif event.key == pygame.K_RIGHT:
                    game_end, win = move(hero, "right")

                if game_end:
                    screen = pygame.display.set_mode((600, 600))
        screen.fill(pygame.Color("black"))

        if not game_end:
            sprite_group.draw(screen)
            hero_group.draw(screen)

            text3 = f.render('Weapon', True, text_color)
            text4 = f.render('level: ' + str(hero.weapon), True, text_color)
            screen.blit(text1, (50 * len(level_map[0]) + 10, 10))
            screen.blit(text2, (50 * len(level_map[0]) + 10, 30))
            screen.blit(text3, (50 * len(level_map[0]) + 10, 60))
            screen.blit(text4, (50 * len(level_map[0]) + 10, 75))
        else:
            if win:
                text = f1.render('YOU WON!', True, text_color)

                screen.blit(text, (200, 100))
            else:
                text = f1.render('GAME OVER', True, text_color)
                screen.blit(text, (175, 100))

            btn_ok.draw(screen)

            if btn_ok.mouse_check(pygame.mouse.get_pos()):
                btn_ok.color = 'red'
            else:
                btn_ok.color = text_color

            pressed = pygame.mouse.get_pressed()
            if pressed[0]:  # обработка нажатий левой кнопки мыши
                x1, y1 = pygame.mouse.get_pos()
                if btn_ok.mouse_check((x1, y1)):
                    running = False
                    time.sleep(0.5)

        clock.tick(FPS)
        pygame.display.flip()
    # pygame.quit()
    return win


if __name__ == '__main__':
    screen = pygame.display.set_mode((600, 600))
    main(screen, 'user', 2)
