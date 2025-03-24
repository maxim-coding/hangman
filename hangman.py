import pygame
import math
import random

# Setup display
pygame.init()
WIDTH, HEIGHT = 1300, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
HINT_FONT = pygame.font.SysFont('comicsans', 30)

# Load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)

# Game variables
hangman_status = 0
words = ["APPLE", "BANANA", "MANGO", "RASPBERRY", "GRAPE", "APRICOT", "AVOCADO", "CHERRY", "COCONUT", "CUCUMBER",
         "DURIAN", "EGGPLANT", "FIG", "GUAVA", "KIWI", "LEMON", "LIME", "NECTARINE", "ORANGE", "OLIVE", "PAPAYA",
         "PINEAPPLE", "PLUM", "PUMPKIN", "MELON", "STRAWBERRY", "TANGERINE", "WATERMELON", "POMEGRANATE"]
word = random.choice(words)
guessed = []
hint_displayed = False

def draw():
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("Max's Hangman Game", 1, BLUE)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Draw letter buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw reset button
    reset_text = LETTER_FONT.render("RESET", 1, RED)
    win.blit(reset_text, (WIDTH - 150, 20))

    # Draw hint button
    hint_text = LETTER_FONT.render("Hint ?", 1, RED)
    win.blit(hint_text, (WIDTH - 150, 80))

    # Display hint
    if hint_displayed:
        hint_message = f"Hint: The word starts with '{word[0]}'"
        hint_display = HINT_FONT.render(hint_message, 1, BLACK)
        win.blit(hint_display, (WIDTH / 2 - hint_display.get_width() / 2, 300))

    # Draw hangman image
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def reset_game():
    global hangman_status, guessed, word, letters, hint_displayed
    hangman_status = 0
    guessed = []
    word = random.choice(words)
    hint_displayed = False

    # Reset letter visibility
    for letter in letters:
        letter[3] = True

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    word_text = WORD_FONT.render(f"The word was: {word}", 1, BLACK)
    win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, HEIGHT / 2 + 50))

    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status, hint_displayed

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()

                # Check if reset button is clicked
                reset_rect = pygame.Rect(WIDTH - 150, 20, 130, 40)
                if reset_rect.collidepoint(m_x, m_y):
                    reset_game()

                # Check if hint button is clicked
                hint_rect = pygame.Rect(WIDTH - 150, 80, 130, 40)
                if hint_rect.collidepoint(m_x, m_y):
                    hint_displayed = True

                # Check if letters are clicked
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON!")
            reset_game()
            break

        if hangman_status == 6:
            display_message("You LOST!")
            reset_game()
            break

while True:
    main()
pygame.quit()
