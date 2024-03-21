import pygame
import sys
import pickle
pygame.init()

# Создание окна
window_size = (1920, 1080)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Rosneft simulator')

# Загрузка изображений
background = pygame.image.load('background.jpg')
map_image = pygame.image.load('map.jpg')

# Класс для кнопки
class Button:
    def __init__(self, x, y, w, h, text, color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the border around the button
        border_width = 2 # Define the width of the border
        border_color = (0, 0, 0) # Define the color of the border (black in this case)
        pygame.draw.rect(screen, border_color, self.rect, border_width)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
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
    global field1, field2, field3_right, field3_top

    screen_size = pygame.display.get_surface().get_size()
    width, height = screen_size
    # Создание полей
    field1 = Field(0, 0, 1920, 100, (200, 200, 200))
    field2 = Field(0, height // 11, width, 1920, (150, 150, 150))
    field3_right = Field(width, 0, 1920 // 5,1920 , (100, 100, 100))
    field3_top = Field(1920 - 1820 // 5, 1000 // 10, width , 1020, (100, 100, 100))

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
start_button = Button(850, 400, 200, 50, "New game", (0, 128, 0), lambda: start_new_game())
quit_button = Button(850, 500, 200, 50, "Exit", (128, 0, 0), lambda: pygame.quit() or sys.exit())
# Функция для отображения названия
def draw_title(screen, title):
    title_font = pygame.font.SysFont('Arial', 50)
    title_surface = title_font.render(title, True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(window_size[0] // 2, 50))
    screen.blit(title_surface, title_rect)

# Создание кнопок действия
action_button1 = Button(window_size[0] - 360, 100, 360, 90, "1.Buy land", (0, 128, 0))
action_button2 = Button(window_size[0] - 360, 180, 360, 90, "2. Sunvey", (0, 128, 0))
action_button3 = Button(window_size[0] - 360, 260, 360, 90, "3. Buld pipe", (0, 128, 0))
action_button4 = Button(window_size[0] - 360, 340, 360, 90, "4. Build oil rig", (0, 128, 0))
action_button5 = Button(window_size[0] - 360, 1000, 130, 90, "||", (0, 128, 0), lambda: paused())
action_button6 = Button(window_size[0] - 240, 1000, 130, 90, "SAVE", (0, 128, 0), lambda: save_game_state(game_state, 'save_game.pickle'))
action_button7 = Button(window_size[0] - 120, 1000, 130, 90, "Quit", (0, 128, 0),lambda: pygame.quit() or sys.exit())
# Создание кнопок для полосы
button1_field3_1 = Button(0, 10, 160, 140, "%", (0, 128, 0),lambda: print("%"))
button2_field3_2 = Button(150, 10, 160, 140, "$", (0, 128, 0),lambda: print("$"))
button3_field3_3 = Button(300, 10, 160, 140, "m/month", (0, 128, 0),lambda: print("m/month"))

# Создание кнопок паузы
continue_button1 = Button(window_size[0] // 2 - 100, window_size[1] // 2 - 80, 200, 80, "Continue", (0, 128, 0), lambda: paused())
quit_button1 = Button(window_size[0] // 2 - 100, window_size[1] // 2 + 10, 200, 80, "Quit", (128, 0, 0), lambda: pygame.quit() or sys.exit())
#создание поверхности паузы
def create_pause_surface():
    pause_surface = pygame.Surface((window_size[0], window_size[1]), pygame.SRCALPHA, 32)
    pause_surface.fill((0, 0, 0, 128)) # Fill with semi-transparent black
    return pause_surface
def paused():
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
        pause_surface.fill((241, 238, 140, 128)) # Clear the surface
        draw_title(pause_surface, "Paused")
        continue_button1.draw(pause_surface)
        quit_button1.draw(pause_surface)
        screen.blit(pause_surface, (0, 0)) # Blit the pause surface on the game screen
        pygame.display.flip()
# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        start_button.handle_event(event)
        quit_button.handle_event(event)
        action_button5.handle_event(event)
        continue_button1.handle_event(event)
        quit_button1.handle_event(event)
        action_button7.handle_event(event)
        action_button6.handle_event(event)
    screen.fill((189, 183, 107)) # Заполнение экрана черным цветом
    draw_title(screen, "Rosneft Simulator") # Отображение названия
    start_button.draw(screen) # Отображение кнопки "Начать игру"
    quit_button.draw(screen) # Отображение кнопки "Выход"
    
    if 'field1' in globals():
        field1.draw(screen)
        button1_field3_1.draw(screen) # Draw buttons in Field3
        button2_field3_2.draw(screen)
        button3_field3_3.draw(screen)
    if 'field2' in globals():
        field2.draw(screen)
        draw_title(screen, "Map") # Отображение названия
        screen.blit(map_image, (100, 500)) # Отображение карты
    if 'field3_right' in globals():
        field3_right.draw(screen)
        
    if 'field3_top' in globals():
        field3_top.draw(screen)
        action_button1.draw(screen) # Draw action buttons
        action_button2.draw(screen)
        action_button3.draw(screen)
        action_button4.draw(screen)
        action_button5.draw(screen)
        action_button6.draw(screen)
        action_button7.draw(screen)
    
    

    pygame.display.flip() # Обновление экрана

# Завершение работы с Pygame
pygame.quit()
sys.exit()