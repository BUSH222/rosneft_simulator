import pygame
import sys
import pickle
import helper
import os
pygame.init()

# Создание окна
TILE_SIZE = 10
window_size = (1920, 1080)
screen = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
pygame.display.set_caption('Rosneft simulator')

# Загрузка изображений
background = pygame.image.load('background.jpg')

map_image = pygame.image.load('map3.jpg')
map_position = (0, 115)  # Initial position of the map
map_speed = 5  # Speed at which the map moves

game = helper.TileGrid(155, 100, 1000000)


clock = pygame.time.Clock()
FPS = 50

pause = False
started = False

images = {}
for f in os.listdir('pipes/'):
    imname = os.path.splitext(f)[0]
    images[imname] = pygame.transform.scale(pygame.image.load('pipes/'+f).convert_alpha(), (10, 10))


class Button:  # Класс для кнопки
    global map_position

    def __init__(self, x, y, w, h, text, color, action=None, toggledaction=None, grid=game):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.action = action
        self.toggledaction = toggledaction
        self.toggled = False
        self.initialxy = []
        self.grid = grid

    def toggle(self):
        self.toggled = not self.toggled
        if self.toggled:
            self.color = (0, 200, 0)
            for button in action_buttons:
                if button != self and button.toggled:
                    button.toggle()
        else:
            self.color = (0, 128, 0)
        self.initialxy = []
        self.finxy = []
        self.pos = []

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the border around the button
        border_width = 2  # Define the width of the border
        border_color = (0, 0, 0)  # Define the color of the border (black in this case)
        pygame.draw.rect(screen, border_color, self.rect, border_width)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(event.pos):
                if self.action:
                    print(f'toggled {self.toggledaction}')
                    self.action()
                    return

            if self.toggledaction == 'build_pipes':

                if pygame.mouse.get_pressed()[2]:
                    if self.toggled and self.initialxy == []:
                        self.initialxy = list(pygame.mouse.get_pos())
                        self.initialxy[0] -= map_position[0]
                        self.initialxy[0] //= TILE_SIZE
                        self.initialxy[1] -= map_position[1]
                        self.initialxy[1] //= TILE_SIZE
                    elif self.toggled and self.initialxy != []:
                        self.finxy = list(pygame.mouse.get_pos())
                        self.finxy[0] -= map_position[0]
                        self.finxy[0] //= TILE_SIZE
                        self.finxy[1] -= map_position[1]
                        self.finxy[1] //= TILE_SIZE  # update with proper coords
                        self.grid.place_pipes(self.initialxy[1], self.initialxy[0],
                                              self.finxy[1], self.finxy[0],
                                              preview=False, delete=True)
                        self.initialxy = []
                        self.finxy = []
                        self.grid.clear_previews()

                elif pygame.mouse.get_pressed()[0]:
                    if self.toggled and self.initialxy == []:
                        self.initialxy = list(pygame.mouse.get_pos())
                        self.initialxy[0] -= map_position[0]
                        self.initialxy[0] //= TILE_SIZE
                        self.initialxy[1] -= map_position[1]
                        self.initialxy[1] //= TILE_SIZE
                    elif self.toggled and self.initialxy != []:
                        self.finxy = list(pygame.mouse.get_pos())
                        self.finxy[0] -= map_position[0]
                        self.finxy[0] //= TILE_SIZE
                        self.finxy[1] -= map_position[1]
                        self.finxy[1] //= TILE_SIZE  # update with proper coords
                        self.grid.place_pipes(self.initialxy[1], self.initialxy[0],
                                              self.finxy[1], self.finxy[0],
                                              preview=False)
                        self.initialxy = []
                        self.finxy = []
                        self.grid.clear_previews()

            if self.toggledaction == 'build_rig':
                if self.toggled:
                    self.pos = list(pygame.mouse.get_pos())
                    self.pos[0] -= map_position[0]
                    self.pos[0] //= TILE_SIZE
                    self.pos[1] -= map_position[1]
                    self.pos[1] //= TILE_SIZE
                    if pygame.mouse.get_pressed()[0]:
                        self.grid.place_rig(self.pos[1], self.pos[0], preview=False, delete=False)
                    elif pygame.mouse.get_pressed()[2]:
                        self.grid.place_rig(self.pos[1], self.pos[0], preview=False, delete=True)

            if self.toggledaction == 'buy_land':
                if pygame.mouse.get_pressed()[0]:
                    if self.toggled and self.initialxy == []:
                        self.initialxy = list(pygame.mouse.get_pos())
                        self.initialxy[0] -= map_position[0]
                        self.initialxy[0] //= TILE_SIZE
                        self.initialxy[1] -= map_position[1]
                        self.initialxy[1] //= TILE_SIZE
                    elif self.toggled and self.initialxy != []:
                        self.finxy = list(pygame.mouse.get_pos())
                        self.finxy[0] -= map_position[0]
                        self.finxy[0] //= TILE_SIZE
                        self.finxy[1] -= map_position[1]
                        self.finxy[1] //= TILE_SIZE  # update with proper coords
                        self.grid.buy_tiles(self.initialxy[0], self.initialxy[1], self.finxy[0], self.finxy[1])
                        self.initialxy = []
                        self.finxy = []
                        self.grid.clear_previews()
                if pygame.mouse.get_pressed()[2]:
                    self.initialxy = []
                    self.finxy = []
                    self.grid.clear_previews()

            if self.toggledaction == 'survey_land':
                if pygame.mouse.get_pressed()[0]:
                    if self.toggled and self.initialxy == []:
                        self.initialxy = list(pygame.mouse.get_pos())
                        self.initialxy[0] -= map_position[0]
                        self.initialxy[0] //= TILE_SIZE
                        self.initialxy[1] -= map_position[1]
                        self.initialxy[1] //= TILE_SIZE
                    elif self.toggled and self.initialxy != []:
                        self.finxy = list(pygame.mouse.get_pos())
                        self.finxy[0] -= map_position[0]
                        self.finxy[0] //= TILE_SIZE
                        self.finxy[1] -= map_position[1]
                        self.finxy[1] //= TILE_SIZE  # update with proper coords
                        self.grid.survey_tiles(self.initialxy[0], self.initialxy[1], self.finxy[0], self.finxy[1])
                        self.initialxy = []
                        self.finxy = []
                        self.grid.clear_previews()
                if pygame.mouse.get_pressed()[2]:
                    self.initialxy = []
                    self.finxy = []
                    self.grid.clear_previews()

        if self.toggled and self.initialxy != [] and self.toggledaction == 'build_pipes':
            self.grid.clear_previews()
            self.finxy = list(pygame.mouse.get_pos())  # update with proper coords
            self.finxy[0] -= map_position[0]
            self.finxy[0] //= 10
            self.finxy[1] -= map_position[1]
            self.finxy[1] //= 10
            self.grid.place_pipes(self.initialxy[1], self.initialxy[0],
                                  self.finxy[1], self.finxy[0],
                                  preview=True)

        if self.toggled and self.toggledaction == 'build_rig':
            self.grid.clear_previews()
            self.pos = list(pygame.mouse.get_pos())  # update with proper coords
            self.pos[0] -= map_position[0]
            self.pos[0] //= 10
            self.pos[1] -= map_position[1]
            self.pos[1] //= 10
            self.grid.place_rig(self.pos[1], self.pos[0], preview=True)

        if self.toggled and self.initialxy != [] and self.toggledaction == 'buy_land':
            self.grid.clear_previews()
            self.finxy = list(pygame.mouse.get_pos())
            self.finxy[0] -= map_position[0]
            self.finxy[0] //= 10
            self.finxy[1] -= map_position[1]
            self.finxy[1] //= 10
            self.grid.buy_tiles(self.initialxy[0], self.initialxy[1],
                                self.finxy[0], self.finxy[1],
                                preview=True)

        if self.toggled and self.initialxy != [] and self.toggledaction == 'survey_land':
            self.grid.clear_previews()
            self.finxy = list(pygame.mouse.get_pos())
            self.finxy[0] -= map_position[0]
            self.finxy[0] //= 10
            self.finxy[1] -= map_position[1]
            self.finxy[1] //= 10
            self.grid.survey_tiles(self.initialxy[0], self.initialxy[1],
                                   self.finxy[0], self.finxy[1],
                                   preview=True)

    def updatetext(self, text):
        self.text = text


# Класс для поля
class Field:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)

    def draw(self, screen):
        screen.blit(self.surface, (self.rect.x, self.rect.y))


def start_new_game():
    global field1, field2, field3_right, field3_top, started

    screen_size = pygame.display.get_surface().get_size()
    width, height = screen_size
    # Создание полей
    field1 = Field(0, 0, 1920, 100, (222, 184, 135))
    field2 = Field(0, height // 11, width, 1920, (150, 150, 150))
    field3_right = Field(width, 0, 1920 // 5, 1920, (222, 184, 135))
    field3_top = Field(1920 - 1820 // 5, 1000 // 10, width, 1020, (222, 184, 135))
    game.place_export_pipe()
    game.generate_oil_deposits()
    started = True


def save_game_state(game_state, file_name):
    try:
        with open(file_name, 'wb') as file:
            pickle.dump(game_state, file)
            print("Game state saved successfully!")
    except IOError:
        print("Error: Unable to save game state.")


game_state = {
    'player_x': 400,
    'player_y': 500
}
# Modify the "New Game" button action
start_button = Button(850, 400, 200, 50, "New game", (0, 128, 0),
                      lambda: (start_new_game()) if not started else False)
quit_button = Button(850, 500, 200, 50, "Exit", (128, 0, 0),
                     lambda: ((pygame.quit() or sys.exit()) if not started else False), toggledaction='quit_new_game')


def draw_title(screen, title):  # Функция для отображения названия
    title_font = pygame.font.SysFont('Arial', 50)
    title_surface = title_font.render(title, True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(window_size[0] // 2, 50))
    screen.blit(title_surface, title_rect)


# Создание кнопок действия
action_button1 = Button(window_size[0] - 360, 100, 360, 90, "1.Buy land", (0, 128, 0),
                        lambda: action_button1.toggle(), toggledaction='buy_land', grid=game)
action_button2 = Button(window_size[0] - 360, 180, 360, 90, "2. Survey", (0, 128, 0),
                        lambda: action_button2.toggle(), toggledaction='survey_land', grid=game)
action_button3 = Button(window_size[0] - 360, 260, 360, 90, "3. Buld pipe", (0, 128, 0),
                        lambda: action_button3.toggle(), toggledaction='build_pipes', grid=game)
action_button4 = Button(window_size[0] - 360, 340, 360, 90, "4. Build oil rig", (0, 128, 0),
                        lambda: action_button4.toggle(), toggledaction='build_rig', grid=game)

action_buttons = [action_button1, action_button2, action_button3, action_button4]

action_button5 = Button(window_size[0] - 360, 1000, 130, 90, "||", (0, 128, 0), lambda: paused())
action_button6 = Button(window_size[0] - 240, 1000, 130, 90, "SAVE", (0, 128, 0),
                        lambda: save_game_state(game_state, 'save_game.pickle'))
action_button7 = Button(window_size[0] - 120, 1000, 130, 90, "Quit", (0, 128, 0),
                        lambda: pygame.quit() or sys.exit(), toggledaction='quit')
# Создание кнопок для полосы
button1_field3_1 = Button(0, 10, 160, 85, "%", (0, 128, 0), lambda: print("%"))
button2_field3_2 = Button(150, 10, 160, 85, "$", (0, 128, 0), lambda: print("$"))
button3_field3_3 = Button(300, 10, 160, 85, "m/month", (0, 128, 0), lambda: print("$/month"))

# Создание кнопок паузы
continue_button1 = Button(window_size[0] // 2 - 100, window_size[1] // 2 - 80, 200, 80, "Continue", (0, 128, 0),
                          lambda: paused() if pause else False)
quit_button1 = Button(window_size[0] // 2 - 100, window_size[1] // 2 + 10, 200, 80, "Quit", (128, 0, 0),
                      lambda: ((pygame.quit() or sys.exit()) if pause else False))


# создание поверхности паузы
def create_pause_surface():
    pause_surface = pygame.Surface((window_size[0], window_size[1]), pygame.SRCALPHA, 32)
    pause_surface.fill((0, 0, 0, 128))  # Fill with semi-transparent black
    return pause_surface


def paused():
    global pause
    pause_surface = create_pause_surface()
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button1.rect.collidepoint(event.pos):
                    pause = False
                elif quit_button1.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pause_surface.fill((241, 238, 140, 128))  # Clear the surface
        draw_title(pause_surface, "Paused")
        continue_button1.draw(pause_surface)
        quit_button1.draw(pause_surface)
        screen.blit(pause_surface, (0, 0))  # Blit the pause surface on the game screen
        pygame.display.flip()


# Главный цикл игры
running = True
cnt = 0  # Count fps
while running:
    screen.fill((189, 183, 107))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                g = game.calculate_connected_rigs()
                print(g)

        start_button.handle_event(event)
        quit_button.handle_event(event)
        action_button1.handle_event(event)
        action_button2.handle_event(event)
        action_button3.handle_event(event)
        action_button4.handle_event(event)
        action_button5.handle_event(event)
        continue_button1.handle_event(event)
        quit_button1.handle_event(event)
        action_button7.handle_event(event)
        action_button6.handle_event(event)

    # Заполнение экрана черным цветом
    draw_title(screen, "Rosneft Simulator")  # Отображение названия
    start_button.draw(screen)  # Отображение кнопки "Начать игру"
    quit_button.draw(screen)  # Отображение кнопки "Выход"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        map_position = (map_position[0] - map_speed, map_position[1])
    if keys[pygame.K_RIGHT]:
        map_position = (map_position[0] + map_speed, map_position[1])
    if keys[pygame.K_UP]:
        map_position = (map_position[0], map_position[1] - map_speed)
    if keys[pygame.K_DOWN]:
        map_position = (map_position[0], map_position[1] + map_speed)


    if 'field2' in globals():  # Отображение карты
        field2.draw(screen)
        draw_title(screen, "Map")  # Отображение названия
        screen.blit(map_image, (map_position[0], map_position[1]))
        for i, x in enumerate(game.grid):
            for j, y in enumerate(x):
                rect = pygame.Rect(j*TILE_SIZE+map_position[0], i*TILE_SIZE+map_position[1], TILE_SIZE, TILE_SIZE)
                color = y.draw()

                if color[0] is not None:
                    pygame.draw.rect(screen, color[0], rect)
                if color[1] is not None:
                    screen.blit(images[color[1]], rect)
    if 'field1' in globals():
        field1.draw(screen)
        button1_field3_1.draw(screen)  # Draw buttons in Field3
        button2_field3_2.draw(screen)
        button3_field3_3.draw(screen)
    if 'field3_right' in globals():
        field3_right.draw(screen)
    if 'field3_top' in globals():
        field3_top.draw(screen)
        action_button1.draw(screen)  # Draw action buttons
        action_button2.draw(screen)
        action_button3.draw(screen)
        action_button4.draw(screen)
        action_button5.draw(screen)
        action_button6.draw(screen)
        action_button7.draw(screen)
    if cnt % 50 == 0:
        g = game.calculate_net_income()
        button3_field3_3.updatetext(str(g)+'$/month')
    elif cnt % 50 == 1:  # change later, temp
        game.validate_all()
    button2_field3_2.updatetext(str(game.budget)+'$')
    clock.tick(FPS)
    pygame.display.flip()  # Обновление экрана
    cnt += 1

# Завершение работы с Pygame
pygame.quit()
sys.exit()
