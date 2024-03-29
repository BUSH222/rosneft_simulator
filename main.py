import pygame
import sys
import helper
import os
import webbrowser

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Load assets, initialise variables, create window
TILE_SIZE = 10

window_size = (1920, 1080)
screen = pygame.display.set_mode(window_size, pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN, vsync=1)
infoObject = pygame.display.Info()
pygame.display.set_caption('Rosneft simulator')

dir_path = os.path.dirname(os.path.realpath(__file__))

background = pygame.image.load(os.path.join(dir_path, 'rosneft.jpg'))
background = pygame.transform.scale(background, (infoObject.current_w, infoObject.current_h))
map_image = pygame.image.load(os.path.join(dir_path, 'map3.jpg'))
place_effect = pygame.mixer.Sound(os.path.join(dir_path, 'zvuk11.mp3'))

map_position = (0, 115)  # Initial position of the map
map_speed = 5  # Speed at which the map moves

game = helper.TileGrid(155, 100, 20000)

clock = pygame.time.Clock()
FPS = 50

pause = False
started = False

font1 = pygame.font.Font(None, 20)
oiltext = []

images = {}
for f in os.listdir(os.path.join(dir_path, 'pipes/')):
    imname = os.path.splitext(f)[0]
    images[imname] = pygame.transform.scale(pygame.image.load((os.path.join(dir_path, 'pipes/')+f)).convert_alpha(),
                                                             (10, 10))


class Button:  # Класс для кнопки
    """Class for a button. Anything in the menu is a button"""
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
        """Toggle the button on or off"""
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
        """Draw the button on the screen"""
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
        """Handle what happens when a user clicks the button"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(event.pos):
                if self.action:
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
                        self.finxy[1] //= TILE_SIZE
                        self.grid.place_pipes(self.initialxy[1], self.initialxy[0],
                                              self.finxy[1], self.finxy[0],
                                              preview=False, delete=True)
                        pygame.mixer.Sound.play(place_effect)
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
                        self.finxy[1] //= TILE_SIZE
                        out = self.grid.place_pipes(self.initialxy[1], self.initialxy[0],
                                                    self.finxy[1], self.finxy[0],
                                                    preview=False)
                        if out:
                            pygame.mixer.Sound.play(place_effect)
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
                        out = self.grid.place_rig(self.pos[1], self.pos[0], preview=False, delete=False)
                    elif pygame.mouse.get_pressed()[2]:
                        out = self.grid.place_rig(self.pos[1], self.pos[0], preview=False, delete=True)
                    if out:
                        pygame.mixer.Sound.play(place_effect)

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
                        self.finxy[1] //= TILE_SIZE
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
                        self.finxy[1] //= TILE_SIZE
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
            self.finxy = list(pygame.mouse.get_pos())
            self.finxy[0] -= map_position[0]
            self.finxy[0] //= 10
            self.finxy[1] -= map_position[1]
            self.finxy[1] //= 10
            self.grid.place_pipes(self.initialxy[1], self.initialxy[0],
                                  self.finxy[1], self.finxy[0],
                                  preview=True)

        if self.toggled and self.toggledaction == 'build_rig':
            self.grid.clear_previews()
            self.pos = list(pygame.mouse.get_pos())
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
        """Update the text of informational buttons"""
        self.text = text


class Field:
    """Class for a UI Field"""
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)

    def draw(self, screen):
        """Draw the field"""
        screen.blit(self.surface, (self.rect.x, self.rect.y))


def start_new_game():
    """Prepare everything for a new game"""
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


def how_to_play():
    """Opens the README on github"""
    webbrowser.open('https://github.com/BUSH222/rosneft_simulator/blob/main/README.md')


# Modify the "New Game" button action
start_button = Button(850, 400, 200, 50, "New game", (0, 128, 0),
                      lambda: (start_new_game()) if not started else False)
quit_button = Button(850, 500, 200, 50, "Exit", (128, 0, 0),
                     lambda: ((pygame.quit() or sys.exit()) if not started else False), toggledaction='quit_new_game')


def draw_title(screen, title):
    """Draw the title"""
    title_font = pygame.font.SysFont('Arial', 50)
    title_surface = title_font.render(title, True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(window_size[0] // 2, 50))
    screen.blit(title_surface, title_rect)


# Action buttons
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
action_button6 = Button(window_size[0] - 240, 1000, 130, 90, "HELP", (0, 128, 0),
                        lambda: how_to_play())
action_button7 = Button(window_size[0] - 120, 1000, 130, 90, "Quit", (0, 128, 0),
                        lambda: pygame.quit() or sys.exit(), toggledaction='quit')
# Top bar buttons
button1_field3_1 = Button(0, 10, 160, 85, "%", (0, 128, 0), lambda: None)
button2_field3_2 = Button(150, 10, 160, 85, "$", (0, 128, 0), lambda: None)
button3_field3_3 = Button(300, 10, 160, 85, "m/month", (0, 128, 0), lambda: None)

# Pause buttons
continue_button1 = Button(window_size[0] // 2 - 100, window_size[1] // 2 - 80, 200, 80, "Continue", (0, 128, 0),
                          lambda: paused() if pause else False)
quit_button1 = Button(window_size[0] // 2 - 100, window_size[1] // 2 + 10, 200, 80, "Quit", (128, 0, 0),
                      lambda: ((pygame.quit() or sys.exit()) if pause else False))


def create_pause_surface():
    """Create a surface for the pause menu"""
    pause_surface = pygame.Surface((infoObject.current_w, infoObject.current_h), pygame.SRCALPHA, 32)
    pause_surface.fill((0, 0, 0, 128))
    return pause_surface


def paused():
    """Handle what happens when the game is paused"""
    global pause
    pause_surface = create_pause_surface()
    pause = True
    while pause:
        imagerect = background.get_rect()
        screen.blit(background, imagerect)
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
        # pause_surface.fill((241, 238, 140, 128))  # Clear the surface
        draw_title(pause_surface, "Paused")
        continue_button1.draw(pause_surface)
        quit_button1.draw(pause_surface)
        screen.blit(pause_surface, (0, 0))  # Blit the pause surface on the game screen
        pygame.display.flip()


def win(win=True, score=game.budget):
    pause = True
    win_surf = create_pause_surface()
    while pause:
        imagerect = background.get_rect()
        screen.blit(background, imagerect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button1.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        # pause_surface.fill((241, 238, 140, 128))  # Clear the surface
        if win:
            title_font = pygame.font.SysFont('Arial', 50)

            result_surf = title_font.render("You WON!!!", True, (0, 0, 0))
            res_rect = result_surf.get_rect(center=(window_size[0] // 2, 50))
            screen.blit(result_surf, res_rect)

            score_surf = title_font.render("final score:", True, (0, 0, 0))
            score_rect = score_surf.get_rect(center=(window_size[0] // 2, 150))
            screen.blit(score_surf, score_rect)

            realscore_surf = title_font.render(str(score), True, (0, 0, 0))
            realscore_rect = realscore_surf.get_rect(center=(window_size[0] // 2, 250))
            screen.blit(realscore_surf, realscore_rect)
        else:
            draw_title(win_surf, 'You lost, try again!')

        quit_button1.draw(win_surf)
        screen.blit(win_surf, (0, 0))  # Blit the pause surface on the game screen
        pygame.display.flip()


# MAIN LOOP
running = True
cnt = 0  # Count fps
while running:
    screen.fill((189, 183, 107))
    if not started:
        imagerect = background.get_rect()
        screen.blit(background, imagerect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    if keys[pygame.K_RIGHT]:
        map_position = (map_position[0] - map_speed, map_position[1])
    if keys[pygame.K_LEFT]:
        map_position = (map_position[0] + map_speed, map_position[1])
    if keys[pygame.K_DOWN]:
        map_position = (map_position[0], map_position[1] - map_speed)
    if keys[pygame.K_UP]:
        map_position = (map_position[0], map_position[1] + map_speed)

    if 'field2' in globals():  # Отображение карты
        field2.draw(screen)
        draw_title(screen, "Map")  # Отображение названия
        screen.blit(map_image, (map_position[0], map_position[1]))
        for i, x in enumerate(game.grid):
            for j, y in enumerate(x):
                rect = pygame.Rect(j*TILE_SIZE+map_position[0], i*TILE_SIZE+map_position[1], TILE_SIZE, TILE_SIZE)
                color = y.draw(grid=game)

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
        # Connect the pipes
        game.validate_all()
    elif cnt % 50 == 1:
        # Calculate income
        g = game.calculate_net_income()
        button3_field3_3.updatetext(str(g)+'$/month')
    elif cnt % 50 == 2:
        # Calculate vanishing oil deposits
        oiltext = []
        for rig in game.calculate_connected_rigs():
            centraltile = game.grid[rig.centraltilelocation[0]][rig.centraltilelocation[1]]
            if centraltile not in [i[2] for i in oiltext]:
                oiltext.append([str(centraltile.oilquantity),
                                (centraltile.x*10, centraltile.y*10), centraltile])

            if centraltile.oilquantity > 0:
                centraltile.oilquantity -= 1
        totalpercentage = game.count_oil_percentage()
        button1_field3_1.updatetext(str(totalpercentage)+'%')
    elif cnt % 50 == 3:
        if game.count_oil_percentage() == 0.0 and not pause and started:
            win(win=True, score=game.budget)
        if game.budget < -100000:
            win(win=False, score=0)

    # draw oil quantity
    for text in oiltext:
        text_surface1 = font1.render(text[0], True, (0, 0, 0))
        text_rect1 = text_surface1.get_rect(center=(text[1][0]+map_position[0], text[1][1]+map_position[1]))
        screen.blit(text_surface1, text_rect1)

    button2_field3_2.updatetext(str(game.budget)+'$')
    clock.tick(FPS)
    pygame.display.flip()  # Обновление экрана
    cnt += 1

# Завершение работы с Pygame
pygame.quit()
sys.exit()
