import sys, random, time

import pygame, random
from pygame.math import Vector2
pygame.init()


def chrToNum(char):
    return ord(char.lower()) - 97


def numToChar(num):
    return (chr(num + 97)).lower()


NumOfLettersWord = [0] * 26
yellow_list = [False for i in range(26)]
green_list = [False for i in range(26)]
grey_list = [False for i in range(26)]
NumOfLettersGuess = [0] * 26


def mid(s, offset, amount):
    return s[offset:offset+amount]


title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 60)
letters_font = pygame.font.Font(None, 40)
GREEN = (45, 141, 88)
DARK_GREEN = (43, 51, 24)
GREY = (18,18,19)
LIGHT_GREY = (58, 58, 59)
YELLOW = (227, 182, 36)
LIGHTER_GREY = (128, 131, 131)

cell_size = 50
letter_cell_width = 40
letter_cell_height = 60
number_of_cells = 15

OFFSET = 75
OFFSET_WORDBORDER = 4.6
screen = pygame.display.set_mode((cell_size*number_of_cells,cell_size*number_of_cells))

pygame.display.set_caption("Wordle")
clock = pygame.time.Clock()
letter = ""


class EntryRow:
    def __init__(self, rownum):
        self.row = [Vector2(OFFSET_WORDBORDER, 0.2+(rownum*1.1)), Vector2(OFFSET_WORDBORDER + 1.2, 0.2+(rownum*1.1)), Vector2(OFFSET_WORDBORDER + 2.4, 0.2+(rownum*1.1)), Vector2(OFFSET_WORDBORDER + 3.6, 0.2+(rownum*1.1)), Vector2(OFFSET_WORDBORDER + 4.8, 0.2+(rownum*1.1))]
        self.letter_array = ["", "", "", "", ""]
        self.number_letters = 0
        self.word = ""
        self.indexes_green = []
        self.indexes_yellow = []

    def draw(self):
        for box in self.row:
            box_rect = (box.x*cell_size, box.y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, LIGHT_GREY, box_rect, 2, 0)

    def green_box(self):
        for letter_num in self.indexes_green:
            green_box_rect = (self.row[letter_num].x*cell_size, self.row[letter_num].y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, GREEN, green_box_rect, 0, 0)

    def yellow_box(self):
        for letter_num in self.indexes_yellow:
            yellow_box_rect = (self.row[letter_num].x*cell_size, self.row[letter_num].y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, YELLOW, yellow_box_rect, 0, 0)

    def check_word(self):
        self.record_word()
        WordFound = False
        FillerWords = open("FillerandGuess.txt", "r")
        for x in range(12972):
            temp = FillerWords.readline().strip()
            if self.word == temp:
                WordFound = True
                break
        if not WordFound:
            self.word = ""
        FillerWords.close()
        return WordFound

    def write_letters(self):
        global letter
        for box in range(self.number_letters):
            box_rect = (self.row[box].x*cell_size+5.1, self.row[box].y*cell_size+7, cell_size, cell_size)
            screen.blit(score_font.render(self.letter_array[box], True, "white"), box_rect)

    def record_word(self):
        for i in range(5):
            self.word += self.letter_array[i]
        self.word = self.word.lower()

    def Wordle(self, GuessWord):
        global green_list, yellow_list
        outputword = ""
        GuessWord = GuessWord.lower()
        self.word = self.word.lower()
        NumOfLettersGuess = [0] * 26
        for h in range(5):
            charg = (mid(self.word, h, 1))
            Ixg = chrToNum(charg)
            NumOfLettersGuess[Ixg] += 1
        for i in range(5):
            letterfound = False
            letterguessi = mid(self.word, i, 1)
            for x in range(5):
                letterwordx = mid(GuessWord, x, 1)
                if letterguessi == letterwordx and i == x:
                    self.indexes_green.append(i)
                    green_list[chrToNum(letterguessi)] = True
                    letterfound = True
                    break
                elif letterguessi == letterwordx:
                    if letterguessi == mid(GuessWord, i, 1):
                        self.indexes_green.append(i)
                        green_list[chrToNum(letterguessi)] = True
                        letterfound = True
                        break
                    self.indexes_yellow.append(i)
                    outputword = outputword + letterguessi
                    letterfound = True
                    break
        for f in range(5):
            tempo = mid(self.word, f, 1)
            if NumOfLettersGuess[chrToNum(tempo)] > NumOfLettersWord[chrToNum(tempo)]:
                try:
                    self.indexes_yellow.remove(f)
                except:
                    continue
            else:
                yellow_list[chrToNum(tempo)] = True
                NumOfLettersGuess[chrToNum(tempo)] = NumOfLettersGuess[chrToNum(tempo)] - 1
        if GuessWord.lower() == self.word.lower():
            return True
        else:
            return False


class LettersRow:
    def __init__(self):
        self.row = [Vector2(130, 410), Vector2(180, 410), Vector2(230, 410), Vector2(280, 410), Vector2(330, 410), Vector2(380, 410), Vector2(430, 410), Vector2(480, 410), Vector2(530, 410), Vector2(580, 410), Vector2(155, 478), Vector2(205, 478), Vector2(255, 478), Vector2(305, 478), Vector2(355, 478), Vector2(405, 478), Vector2(455, 478), Vector2(505, 478), Vector2(555, 478), Vector2(205, 546), Vector2(255, 546), Vector2(305, 546), Vector2(355, 546), Vector2(405, 546), Vector2(455, 546), Vector2(505, 546)]
        self.letter_list = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]

    def draw(self):
        global green_list, yellow_list
        box_count = -1
        for letter in self.letter_list:
            box_count += 1
            box = self.row[box_count]
            color = LIGHTER_GREY
            if grey_list[chrToNum(letter)] and not yellow_list[chrToNum(letter)] and not green_list[chrToNum(letter)]:
                color = LIGHT_GREY #DARKEN
            if yellow_list[chrToNum(letter)] and not green_list[chrToNum(letter)]:
                color = YELLOW
            if green_list[chrToNum(letter)]:
                color = GREEN
            letter_rect = (box.x, box.y, letter_cell_width, letter_cell_height)
            pygame.draw.rect(screen, color, letter_rect, 0, 8)
            letters_surface = letters_font.render(letter.upper(), True, "white")
            screen.blit(letters_surface, (box.x + 10, box.y + 15))


class ButtonsRow:
    def __init__(self):
        self.row = [Vector2(105, 546), Vector2(555, 546)]
        image_1 = pygame.image.load("Images/Enter.png")
        image_2 = pygame.image.load("Images/Backspace.png")
        self.button_list = [image_1, image_2]
        self.count_image = 0

    def draw(self):
        for button in self.row:
            if self.count_image == 0:
                diff_x = 21
                diff_y = 23
            elif self.count_image == 1:
                diff_x = 29
                diff_y = 20
            button_rect = (button.x, button.y, 90, letter_cell_height)
            pygame.draw.rect(screen, LIGHTER_GREY, button_rect, 0, 8)
            screen.blit(self.button_list[self.count_image], (button.x + diff_x, button.y + diff_y))
            if self.count_image == 0:
                self.count_image = 1
            else:
                self.count_image = 0


class Errors:
    def __init__(self):
        self.invalid_word_surface = pygame.image.load("Images/Invalid_Word.png")
        self.NEL_surface = pygame.image.load("Images/Not_Enough_Letters.png")
        self.error_rect = pygame.Rect(125, 500, 1, 1)

    def draw_invalid_word(self):
        screen.blit(self.invalid_word_surface, self.error_rect)

    def draw_NEL_surface(self):
        screen.blit(self.NEL_surface, self.error_rect)


def draw_boxes():
    row1.draw()
    row2.draw()
    row3.draw()
    row4.draw()
    row5.draw()
    row6.draw()


def letter_assign():
    global letter
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_a) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[10].x < Vector2(event.pos).x < letter_row1.row[10].x + letter_cell_width and letter_row1.row[10].y < Vector2(event.pos).y < letter_row1.row[10].y + letter_cell_height):
        letter = "A"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_b) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[23].x < Vector2(event.pos).x < letter_row1.row[23].x + letter_cell_width and letter_row1.row[23].y < Vector2(event.pos).y < letter_row1.row[23].y + letter_cell_height):
        letter = "B"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_c) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[21].x < Vector2(event.pos).x < letter_row1.row[21].x + letter_cell_width and letter_row1.row[21].y < Vector2(event.pos).y < letter_row1.row[21].y + letter_cell_height):
        letter = "C"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_d) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[12].x < Vector2(event.pos).x < letter_row1.row[12].x + letter_cell_width and letter_row1.row[12].y < Vector2(event.pos).y < letter_row1.row[12].y + letter_cell_height):
        letter = "D"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_e) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[2].x < Vector2(event.pos).x < letter_row1.row[2].x + letter_cell_width and letter_row1.row[2].y < Vector2(event.pos).y < letter_row1.row[2].y + letter_cell_height):
        letter = "E"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_f) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[13].x < Vector2(event.pos).x < letter_row1.row[13].x + letter_cell_width and letter_row1.row[13].y < Vector2(event.pos).y < letter_row1.row[13].y + letter_cell_height):
        letter = "F"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_g) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[14].x < Vector2(event.pos).x < letter_row1.row[14].x + letter_cell_width and letter_row1.row[14].y < Vector2(event.pos).y < letter_row1.row[14].y + letter_cell_height):
        letter = "G"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_h) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[15].x < Vector2(event.pos).x < letter_row1.row[15].x + letter_cell_width and letter_row1.row[15].y < Vector2(event.pos).y < letter_row1.row[15].y + letter_cell_height):
        letter = "H"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_i) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[7].x < Vector2(event.pos).x < letter_row1.row[7].x + letter_cell_width and letter_row1.row[7].y < Vector2(event.pos).y < letter_row1.row[7].y + letter_cell_height):
        letter = "I"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_j) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[16].x < Vector2(event.pos).x < letter_row1.row[16].x + letter_cell_width and letter_row1.row[16].y < Vector2(event.pos).y < letter_row1.row[16].y + letter_cell_height):
        letter = "J"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_k) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[17].x < Vector2(event.pos).x < letter_row1.row[17].x + letter_cell_width and letter_row1.row[17].y < Vector2(event.pos).y < letter_row1.row[17].y + letter_cell_height):
        letter = "K"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_l) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[18].x < Vector2(event.pos).x < letter_row1.row[18].x + letter_cell_width and letter_row1.row[18].y < Vector2(event.pos).y < letter_row1.row[18].y + letter_cell_height):
        letter = "L"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_m) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[25].x < Vector2(event.pos).x < letter_row1.row[25].x + letter_cell_width and letter_row1.row[25].y < Vector2(event.pos).y < letter_row1.row[25].y + letter_cell_height):
        letter = "M"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_n) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[24].x < Vector2(event.pos).x < letter_row1.row[24].x + letter_cell_width and letter_row1.row[24].y < Vector2(event.pos).y < letter_row1.row[24].y + letter_cell_height):
        letter = "N"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_o) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[8].x < Vector2(event.pos).x < letter_row1.row[8].x + letter_cell_width and letter_row1.row[8].y < Vector2(event.pos).y < letter_row1.row[8].y + letter_cell_height):
        letter = "O"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_p) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[9].x < Vector2(event.pos).x < letter_row1.row[9].x + letter_cell_width and letter_row1.row[9].y < Vector2(event.pos).y < letter_row1.row[9].y + letter_cell_height):
        letter = "P"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[0].x < Vector2(event.pos).x < letter_row1.row[0].x + letter_cell_width and letter_row1.row[0].y < Vector2(event.pos).y < letter_row1.row[0].y + letter_cell_height):
        letter = "Q"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_r and not game_ended) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[3].x < Vector2(event.pos).x < letter_row1.row[3].x + letter_cell_width and letter_row1.row[3].y < Vector2(event.pos).y < letter_row1.row[3].y + letter_cell_height):
        letter = "R"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_s) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[11].x < Vector2(event.pos).x < letter_row1.row[11].x + letter_cell_width and letter_row1.row[11].y < Vector2(event.pos).y < letter_row1.row[11].y + letter_cell_height):
        letter = "S"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_t) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[4].x < Vector2(event.pos).x < letter_row1.row[4].x + letter_cell_width and letter_row1.row[4].y < Vector2(event.pos).y < letter_row1.row[4].y + letter_cell_height):
        letter = "T"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_u) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[6].x < Vector2(event.pos).x < letter_row1.row[6].x + letter_cell_width and letter_row1.row[6].y < Vector2(event.pos).y < letter_row1.row[6].y + letter_cell_height):
        letter = "U"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_v) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[22].x < Vector2(event.pos).x < letter_row1.row[22].x + letter_cell_width and letter_row1.row[22].y < Vector2(event.pos).y < letter_row1.row[22].y + letter_cell_height):
        letter = "V"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_w) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[1].x < Vector2(event.pos).x < letter_row1.row[ 1].x + letter_cell_width and letter_row1.row[1].y < Vector2(event.pos).y < letter_row1.row[1].y + letter_cell_height):
        letter = "W"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[20].x < Vector2(event.pos).x < letter_row1.row[20].x + letter_cell_width and letter_row1.row[20].y < Vector2(event.pos).y < letter_row1.row[20].y + letter_cell_height):
        letter = "X"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_y) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[5].x < Vector2(event.pos).x < letter_row1.row[5].x + letter_cell_width and letter_row1.row[5].y < Vector2(event.pos).y < letter_row1.row[5].y + letter_cell_height):
        letter = "Y"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_z) or (event.type == pygame.MOUSEBUTTONDOWN and letter_row1.row[19].x < Vector2(event.pos).x < letter_row1.row[19].x + letter_cell_width and letter_row1.row[19].y < Vector2(event.pos).y < letter_row1.row[19].y + letter_cell_height):
        letter = "Z"
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE) or (event.type == pygame.MOUSEBUTTONDOWN and buttons_row1.row[1].x < Vector2(event.pos).x < buttons_row1.row[1].x + 90 and buttons_row1.row[1].y < Vector2(event.pos).y < buttons_row1.row[1].y + letter_cell_height):
        letter = ""
    else:
        return False
    return True


sound = "unmuted"
TIMER_POPUP = pygame.USEREVENT
pygame.time.set_timer(TIMER_POPUP, 1500)


def row_brain(local_num):
    global row1, row2, row3, row4, row5, row6, current_row, game_ended, word_found, sound, grey_list, invalid_word, NEL, inv_flag_timer, NEL_flag_timer
    type_sound = pygame.mixer.Sound("Sounds/ChangeSelection.mp3")
    backspace_sound = pygame.mixer.Sound("Sounds/Backspace.mp3")
    enter_sound = pygame.mixer.Sound("Sounds/Enter.mp3")
    win_sound = pygame.mixer.Sound("Sounds/Bright Popup.mp3")
    lose_sound = pygame.mixer.Sound("Sounds/Lose.mp3")
    error_sound = pygame.mixer.Sound("Sounds/Error.mp3")
    if local_num == 1:
        row_num = row1
    elif local_num == 2:
        row_num = row2
    elif local_num == 3:
        row_num = row3
    elif local_num == 4:
        row_num = row4
    elif local_num == 5:
        row_num = row5
    elif local_num == 6:
        row_num = row6
    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        valid = letter_assign()
        # SPACE
        if row_num.number_letters != 5 and letter != "" and valid:
            row_num.letter_array[row_num.number_letters] = letter
            row_num.number_letters += 1
            if sound != "muted":
                type_sound.play()
        elif letter == "" and valid:
            if row_num.number_letters != 0:
                row_num.number_letters -= 1
                row_num.letter_array[row_num.number_letters] = letter
                if sound != "muted":
                    backspace_sound.play()
        elif row_num.number_letters == 5 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER) or (event.type == pygame.MOUSEBUTTONDOWN and buttons_row1.row[0].x < Vector2(event.pos).x < buttons_row1.row[0].x + 90 and buttons_row1.row[0].y < Vector2(event.pos).y < buttons_row1.row[0].y + letter_cell_height)) and current_row <= 6 and row_num.check_word():
            for char in range(5):
                grey_list[chrToNum(row_num.word[char])] = True
            if not row_num.Wordle(GuessWord):
                current_row += 1
                if sound != "muted" and current_row != 7:
                    enter_sound.play()
                if current_row == 7:
                    word_found = False
                    game_ended = True
                    if sound != "muted":
                        lose_sound.play()

            else:
                word_found = True
                game_ended = True
                if sound != "muted":
                    win_sound.play()
        elif row_num.number_letters == 5 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER) or (event.type == pygame.MOUSEBUTTONDOWN and buttons_row1.row[0].x < Vector2(event.pos).x < buttons_row1.row[0].x + 90 and buttons_row1.row[0].y < Vector2(event.pos).y < buttons_row1.row[0].y + letter_cell_height)) and current_row <= 6 and not row_num.check_word():
            if sound != "muted":
                error_sound.play()
            invalid_word = True
            inv_flag_timer = True
        elif row_num.number_letters != 5 and ((event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER) or (event.type == pygame.MOUSEBUTTONDOWN and buttons_row1.row[0].x < Vector2(event.pos).x < buttons_row1.row[0].x + 90 and buttons_row1.row[0].y < Vector2(event.pos).y < buttons_row1.row[0].y + letter_cell_height)) and current_row <= 6:
            if sound != "muted":
                error_sound.play()
            NEL = True
            NEL_flag_timer = True


restart_game = True

# GAME LOOP
while True:
    if restart_game:
        WordNum = int(random.randrange(1, 2316))
        GuessWords = open("GuessWords.txt", "r")
        for i in range(WordNum):
            GuessWord = GuessWords.readline().strip()
        GuessWords.close()

        NumOfLettersWord = [0] * 26

        GuessWord = GuessWord.lower()
        for i in range(5):
            char = (mid(GuessWord, i, 1))
            Ix = chrToNum(char)
            NumOfLettersWord[Ix] += 1

        letters_selected = [False for i in range(26)]

        error_board = Errors()
        row1 = EntryRow(1)
        row2 = EntryRow(2)
        row3 = EntryRow(3)
        row4 = EntryRow(4)
        row5 = EntryRow(5)
        row6 = EntryRow(6)

        letter_row1 = LettersRow()

        buttons_row1 = ButtonsRow()

        valid_word = True
        game_ended = False
        word_found = False

        invalid_word = False
        NEL = False
        inv_flag_timer = False
        NEL_flag_timer = False

        yellow_list = [False for i in range(26)]
        green_list = [False for i in range(26)]
        grey_list = [False for i in range(26)]
        NumOfLettersGuess = [0] * 26

        current_row = 1
        restart_game = False
    # 1. Event Handling
    for event in pygame.event.get():
        if game_ended and ((event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and 35 < Vector2(event.pos).x < 115 and 640 < Vector2(event.pos).y < 725)):
            restart_game = True
            break
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN and 30 < Vector2(event.pos).x < 115 and 30 < Vector2(event.pos).y < 115):
            pygame.quit()
            sys.exit()
        row_brain(current_row)
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_0) or (event.type == pygame.MOUSEBUTTONDOWN and 640 < Vector2(event.pos).x < 725 and 45 < Vector2(event.pos).y < 105):
            if sound == "muted":
                sound = "unmuted"
            elif sound == "unmuted":
                sound = "muted"


    screen.fill(GREY)
    if not game_ended:

        letter_row1.draw()
        buttons_row1.draw()
        draw_boxes()
        row1.yellow_box()
        row1.green_box()
        row1.write_letters()

        row2.yellow_box()
        row2.green_box()
        row2.write_letters()

        row3.yellow_box()
        row3.green_box()
        row3.write_letters()

        row4.yellow_box()
        row4.green_box()
        row4.write_letters()

        row5.yellow_box()
        row5.green_box()
        row5.write_letters()

        row6.yellow_box()
        row6.green_box()
        row6.write_letters()

        if invalid_word:
            error_board.draw_invalid_word()
            if inv_flag_timer:
                start_timer1 = pygame.time.get_ticks()
                inv_flag_timer = False
            if pygame.time.get_ticks() >= (start_timer1 + 1500):
                invalid_word = False
        if NEL:
            error_board.draw_NEL_surface()
            if NEL_flag_timer:
                start_timer2 = pygame.time.get_ticks()
                NEL_flag_timer = False
            if pygame.time.get_ticks() >= (start_timer2 + 1500):
                NEL = False
    else:
        outcome_rect = pygame.Rect(175, 150, 1, 1)
        if word_found:
            screen.fill(pygame.Color("turquoise"))
            win_surface = pygame.image.load("Images/Win.png")
            screen.blit(win_surface, outcome_rect)
            details_surface1_win = title_font.render(f"You Correctly Guessed the Word", True, DARK_GREEN)
            screen.blit(details_surface1_win, (50, 500))
            details_surface2_win = title_font.render(f" {GuessWord.title()} in {current_row} guesses.", True, DARK_GREEN)
            screen.blit(details_surface2_win, (172, 542))
        elif not word_found:
            screen.fill(pygame.Color("orange"))
            lose_surface = pygame.image.load("Images/Lose.png")
            screen.blit(lose_surface, outcome_rect)
            details_surface1_lose = title_font.render(f"You Were Unable to Guess ", True, DARK_GREEN)
            screen.blit(details_surface1_lose, (100, 500))
            details_surface2_lose = title_font.render(f"the Word {GuessWord.title()}", True, DARK_GREEN)
            screen.blit(details_surface2_lose, (225, 542))
        restart_rect = pygame.Rect(30, 625, 1, 1)
        restart_surface = pygame.image.load("Images/Restart.png")
        screen.blit(restart_surface, restart_rect)
    sound_rect = pygame.Rect((640, 30, 85, 85))
    sound_on_surface = pygame.image.load("Images/SoundOn.png")
    sound_off_surface = pygame.image.load("Images/SoundOff.png")
    logo_rect = pygame.Rect((125, 3, 1, 1))
    logo_surface = pygame.image.load("Images/Wordle_Logo.png")
    screen.blit(logo_surface, logo_rect)
    if sound == "muted":
        screen.blit(sound_off_surface, sound_rect)
    elif sound == "unmuted":
        screen.blit(sound_on_surface, sound_rect)
    exit_rect = pygame.Rect(30, 30, 1, 1)
    exit_surface = pygame.image.load("Images/Exit.png")
    screen.blit(exit_surface, exit_rect)
    pygame.display.update()
    clock.tick(60)
