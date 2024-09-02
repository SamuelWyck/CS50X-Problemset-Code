import pygame
import os
from hand import Hand
from button import Button
pygame.font.init()
pygame.mixer.init()

card_shuffle_sound = pygame.mixer.Sound(os.path.join("Assets", "card_shuffle.mp3"))
button_sound = pygame.mixer.Sound(os.path.join("Assets", "button_click.mp3"))
card_deal_sound = pygame.mixer.Sound(os.path.join("Assets", "card_deal.mp3"))

WIDTH, HEIGHT = 1520, 750
CARD_WIDTH, CARD_HEIGHT = 210, 310
BUTTON_WIDTH, BUTTON_HEIGHT = 178, 46

HITx, HITy = 56, 422
STANDx, STANDy = 56, 522
SPLITx, SPLITy = 56, 622
NEW_GAMEx, NEW_GAMEy = WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - BUTTON_HEIGHT//2 - 50
EXITx, EXITy = WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - BUTTON_HEIGHT//2 + 50
CONTINUEx, CONTINUEy = WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 + 130
EXIT2x, EXIT2y = WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 + 210

PLAYER_CARD_X, PLAYER_CARD_Y = 285, 397
SPLIT_CARD_X, SPLIT_CARD_Y = 285, 572
COMPUTER_CARD_X, COMPUTER_CARD_Y = 285, 42

HIGHLIGHT_PLAYER = pygame.Rect((PLAYER_CARD_X - 7, PLAYER_CARD_Y - 7), (CARD_WIDTH//2 + 15, CARD_HEIGHT//2 + 15))
HIGHLIGHT_SPLIT = pygame.Rect((SPLIT_CARD_X - 7, SPLIT_CARD_Y - 7), (CARD_WIDTH//2 + 15, CARD_HEIGHT//2 + 15))

TEXTBOX = pygame.Rect(((WIDTH//2 - 30), (HEIGHT//2 - BUTTON_HEIGHT//2 - 50)), (BUTTON_WIDTH,  BUTTON_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (131, 0, 179)
YELLOW = (247, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

TABLE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "table.png")), (WIDTH, HEIGHT))
DRAW_PILE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "draw_pile1.png")), (CARD_WIDTH, CARD_HEIGHT))
HIT_BUTTON = pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "hit_button.png")), 180)
STAND_BUTTON = pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "stand_button.png")), 180)
BUTTON_PRESSED = pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "button_pressed.png")), 180)
ICON = pygame.image.load(os.path.join("Assets", "spade.png"))

pygame.display.set_icon(ICON)

BUTTON_FONT = pygame.font.SysFont("Goudy Stout", 20)
BUTTON_FONT2 = pygame.font.SysFont("Goudy Stout", 13)
END_FONT = pygame.font.SysFont("Goudy Stout", 100)
END_FONT2 = pygame.font.SysFont("Goudy Stout", 80)

FPS = 60

player = Hand()
computer = Hand()
split = Hand()

hit_button = Button(HIT_BUTTON, HITx, HITy, BUTTON_PRESSED)
stand_button = Button(STAND_BUTTON, STANDx, STANDy, BUTTON_PRESSED)
exit_button = Button(HIT_BUTTON, EXITx, EXITy, BUTTON_PRESSED)
new_game_button = Button(HIT_BUTTON, NEW_GAMEx, NEW_GAMEy, BUTTON_PRESSED)
split_button = Button(HIT_BUTTON, SPLITx, SPLITy, BUTTON_PRESSED)
continue_button = Button(HIT_BUTTON, CONTINUEx, CONTINUEy, BUTTON_PRESSED)
exit_button2 = Button(HIT_BUTTON, EXIT2x, EXIT2y, BUTTON_PRESSED)

balance = 100


def main():
    
    menu = False
    end = False
    end_text = ""
    end2_text = ""
    end_loop = 0
    blackjack = False

    stand_clicked = False
    split_clicked = False
    two_hands = False
    turn1 = True
    bet = handle_menu()
    pygame.mixer.music.load(os.path.join("Assets", "play_music.mp3"))
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1, fade_ms=3000)
    game_setup(end, menu, turn1, two_hands)
    hit_clicked = False
    
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settle_up(bet, end_text, end2_text, blackjack)
                check_highscore()
                run = False
                pygame.quit()


        if hit_button.clicked == True and hit_clicked == False and stand_clicked == False:
            button_sound.play()
            pygame.time.delay(310)
            if turn1 == True:
                if two_hands == True:
                    if player.hand[0]["type"][:1] == "a" and len(player.hand) == 2:
                        pass
                    else:
                        player.hit()
                elif two_hands == False:
                    player.hit()
                hit_clicked = True
            elif turn1 == False:
                if split.hand[0]["type"][:1] == "a" and len(split.hand) == 2:
                    pass
                else:
                    split.hit()
                hit_clicked = True
        if hit_button.clicked == False:
            hit_clicked = False


        if stand_button.clicked == True and stand_clicked == False and end == False:
            button_sound.play()
            pygame.time.delay(310)
            if two_hands == False or turn1 == False:
                computer.logic()
                stand_clicked = True
                end = True
            elif two_hands == True:
                turn1 = False
                stand_clicked = True
        if stand_button.clicked == False and end != True:
            stand_clicked = False
        
            
        if end == True:
            end_text, end2_text = get_end_text(two_hands)

            
        if player.score > 21:
            if two_hands == False:
                end = True
            elif two_hands:
                turn1 = False

        if player.score == 21 and two_hands == False and blackjack == False and len(player.hand) == 2:
            blackjack = True
            end = True

        if computer.score == 21 and len(computer.hand) == 2:
            end = True

        if split.score > 21:
            if player.score > 21:
                end = True
            else:
                computer.logic()
                end = True

        draw_window(end, menu, turn1, two_hands)

        if end_text != "" and menu == False:
            hit_clicked = True
            stand_clicked = True
            if end_loop != 1:
                end_loop += 1
            elif end_loop == 1:
                pygame.time.delay(500)
                draw_end_screen(end_text, end2_text)
                menu = True

        if new_game_button.clicked == True:
            new_game_button.clicked = False
            two_hands = False
            button_sound.play()
            pygame.time.delay(400)
            run = False
        if exit_button.clicked == True:
            button_sound.play()
            pygame.time.delay(400)
            settle_up(bet, end_text, end2_text, blackjack)
            check_highscore()
            run = False
            pygame.quit()

        if split_button.clicked == True and split_clicked == False and two_hands == False:
            split_button.clicked = False
            card_deal_sound.play()
            split_clicked = True
            two_hands = True
            split.hand.append(player.hand[1])
            player.hand.pop()
            player.score = int(player.hand[0]["score"])
            split.score = int(split.hand[0]["score"])

    player.new_game()
    computer.new_game()
    split.new_game()
    Hand.new_deck()
    settle_up(bet, end_text, end2_text, blackjack)
    main()

    
def draw_window(end, menu, turn1, two_hands):
    WINDOW.blit(TABLE, (0, 0))
    WINDOW.blit(DRAW_PILE, (40, 42))

    hit_button.draw(WINDOW)
    hit_text = BUTTON_FONT.render("HIT", 1, WHITE)
    WINDOW.blit(hit_text, (
    (HITx + BUTTON_WIDTH//2 - hit_text.get_width()//2),(HITy + BUTTON_HEIGHT//2 - hit_text.get_height()//2 + 1)))

    stand_button.draw(WINDOW)
    stand_text = BUTTON_FONT.render("STAND", 1, WHITE)
    WINDOW.blit(stand_text, (
    (STANDx + BUTTON_WIDTH//2 - stand_text.get_width()//2), (STANDy + BUTTON_HEIGHT//2 - stand_text.get_height()//2 + 1)))

    if two_hands == False and len(player.hand) > 5:
        player.draw(WINDOW, CARD_WIDTH//2, CARD_HEIGHT//2, PLAYER_CARD_X, PLAYER_CARD_Y)
    elif two_hands == False:
        player.draw(WINDOW, CARD_WIDTH, CARD_HEIGHT, PLAYER_CARD_X, PLAYER_CARD_Y)
    elif two_hands == True:
        if turn1 == True:
            pygame.draw.rect(WINDOW, YELLOW, HIGHLIGHT_PLAYER, border_radius=10)
        elif turn1 == False:
            pygame.draw.rect(WINDOW, YELLOW, HIGHLIGHT_SPLIT, border_radius=10)
        player.draw(WINDOW, CARD_WIDTH//2, CARD_HEIGHT//2, PLAYER_CARD_X, PLAYER_CARD_Y)
        split.draw(WINDOW, CARD_WIDTH//2, CARD_HEIGHT//2, SPLIT_CARD_X, SPLIT_CARD_Y)

    if len(computer.hand) <= 5:    
        computer.draw(WINDOW, CARD_WIDTH, CARD_HEIGHT, COMPUTER_CARD_X, COMPUTER_CARD_Y)
    elif len(computer.hand) > 5:
        computer.draw(WINDOW, CARD_WIDTH//2, CARD_HEIGHT//2, COMPUTER_CARD_X, COMPUTER_CARD_Y)


    if len(computer.hand) == 2 and (computer.hand[0]["type"][0:1] != "a") and (
        computer.hand[0]["type"][0:1] != "1") and (computer.hand[0]["type"][0:1] != "k") and (
        computer.hand[0]["type"][0:1] != "q") and (computer.hand[0]["type"][0:1] != "j") and end == False:
        WINDOW.blit(DRAW_PILE, ((285*2) - 40, 42))

    if len(player.hand) == 2 and player.hand[0]["type"][0:1] == player.hand[1]["type"][0:1] and two_hands == False:
        split_button.draw(WINDOW)
        split_text = BUTTON_FONT.render("SPLIT", 1, WHITE)
        WINDOW.blit(split_text, (
        (SPLITx + BUTTON_WIDTH//2 - split_text.get_width()//2), (SPLITy + BUTTON_HEIGHT//2 - split_text.get_height()//2 + 2)))


    if menu:
        new_game_button.draw(WINDOW)
        new_game_text = BUTTON_FONT2.render("DEAL AGAIN", 1, WHITE)
        WINDOW.blit(new_game_text, (
        (NEW_GAMEx + BUTTON_WIDTH//2 - new_game_text.get_width()//2), (NEW_GAMEy + BUTTON_HEIGHT//2 - new_game_text.get_height()//2)))

        exit_button.draw(WINDOW)
        exit_text = BUTTON_FONT.render("EXIT", 1, WHITE)
        WINDOW.blit(exit_text, (
        (EXITx + BUTTON_WIDTH//2 - exit_text.get_width()//2), (EXITy + BUTTON_HEIGHT//2 - exit_text.get_height()//2 + 1)))

    pygame.display.update()


def game_setup(end, menu, turn1, two_hands):
    draw_window(end, menu, turn1, two_hands)
    card_shuffle_sound.play()
    pygame.time.delay(4000)

    STARTING_CARDS = 2
    cards = 0
    while cards < STARTING_CARDS:
        draw_window(end, menu, turn1, two_hands)
        pygame.time.delay(500)
        player.hit()
        draw_window(end, menu, turn1, two_hands)
        pygame.time.delay(500)
        computer.hit()
        cards += 1
    

def draw_end_screen(end_text, end2_text):
    if end2_text == "":
        if end_text == "COMPUTER WINS!":
            text = END_FONT2.render(end_text, 1, PURPLE)
        else:
            text = END_FONT.render(end_text, 1, PURPLE)
        WINDOW.blit(text, ((WIDTH/2 - text.get_width()/2), (HEIGHT/2 - text.get_height()/2)))
    
    else:
        text1 = END_FONT2.render(end_text, 1, PURPLE)
        WINDOW.blit(text1, ((WIDTH/2 - text1.get_width()/2), (HEIGHT/2 - text1.get_height()/2) - 100))
        text2 = END_FONT2.render(end2_text, 1, PURPLE)
        WINDOW.blit(text2, ((WIDTH/2 - text2.get_width()/2), (HEIGHT/2 - text2.get_height()/2) + 100))
    
    pygame.display.update()
    if end2_text == "":
        pygame.time.delay(3000)
    else:
        pygame.time.delay(5000)


def get_end_text(two_hands):
    if two_hands == False:
        end2_text = ""
        if player.score > 21:
            end_text = "BUST!"
        elif player.score > computer.score and player.score <= 21:
            end_text = "PLAYER WINS!"
        elif player.score == computer.score and computer.score <= 21:
            end_text = "TIE!"
        elif player.score < computer.score and computer.score <= 21:
            end_text = "COMPUTER WINS!"
        elif computer.score > 21:
            end_text = "PLAYER WINS!"
            

    elif two_hands == True:
        if player.score > 21:
            end_text = "FIRST HAND: BUST!"
        elif computer.score > 21:
            end_text = "FIRST HAND: WIN!"
        elif player.score < computer.score and computer.score <= 21:
            end_text = "FIRST HAND: LOSS!"
        elif player.score <= 21 and player.score > computer.score:
            end_text = "FIRST HAND: WIN!"
        elif player.score == computer.score and computer.score <= 21:
            end_text = "FIRST HAND: TIE!"
        if split.score > 21:
            end2_text = "SECOND HAND: BUST!"
        elif split.score < computer.score and computer.score <= 21:
            end2_text = "SECOND HAND: LOSS!"
        elif split.score <= 21 and split.score > computer.score:
            end2_text = "SECOND HAND: WIN!"
        elif split.score == computer.score and computer.score <= 21:
            end2_text = "SECOND HAND: TIE!"
        elif computer.score > 21 and split.score <= 21:
            end2_text = "SECOND HAND: WIN!"
    
    return end_text, end2_text


def handle_menu():
    pygame.key.set_repeat(200)
    text = ""
    tick = pygame.time.Clock()
    MENU = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "menu_background.png")), (WIDTH, HEIGHT))
    TITLE_BACK = pygame.image.load(os.path.join("Assets", "title.png"))
    LIGHTBOX = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "lightbox.png")), (500, 150))


    pygame.mixer.music.load(os.path.join("Assets", "menu_music.mp3"))
    pygame.mixer.music.set_volume(.4)
    pygame.mixer.music.play(-1, fade_ms=500)
    

    with open("highscore.txt") as file:
        highscore = file.read()
    highscore_text = BUTTON_FONT.render(f"HIGHSCORE: ${highscore}", 1, GOLD)

    continue_clicked = False

    run = True
    while run:
        tick.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_highscore()
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN and text.isdigit():
                    if int(text) > 0 and int(text) <= balance:
                        pygame.time.delay(310)
                        run = False
                        break
                elif event.key != pygame.K_RETURN:
                    text += event.unicode

        if continue_button.clicked == True and continue_clicked == False:
            continue_clicked = True
            button_sound.play()
            if text.isdigit():
                if int(text) > 0 and int(text) <= balance:
                    continue_button.clicked = False
                    pygame.time.delay(310)
                    break
        if continue_button.clicked == False:
            continue_clicked = False

        if exit_button2.clicked == True:
            button_sound.play()
            pygame.time.delay(400)
            check_highscore()
            run = False
            pygame.quit()

        WINDOW.blit(MENU, (0, 0))
        title = END_FONT.render("BLACKJACK", 1, GOLD)
        WINDOW.blit(TITLE_BACK, ((WIDTH//2 - title.get_width()/2 - 100), (HEIGHT//2 - 334)))
        WINDOW.blit(title, ((WIDTH//2 - title.get_width()/2), (HEIGHT//2 - 300)))

        WINDOW.blit(LIGHTBOX, ((WIDTH//2 - LIGHTBOX.get_width()/2), (238)))
        WINDOW.blit(highscore_text, ((WIDTH//2 - highscore_text.get_width()/2), (298)))

        prompt = BUTTON_FONT.render(f"ENTER YOUR BET. BALANCE: ${balance}", 1, GOLD)
        WINDOW.blit(prompt, ((WIDTH//2 - prompt.get_width()/2), (HEIGHT//2 + 80)))

        pygame.draw.rect(WINDOW, WHITE, TEXTBOX, border_radius=20)
        text_render = BUTTON_FONT2.render(text, 1, BLACK)
        WINDOW.blit(text_render, ((TEXTBOX.x + 5), (TEXTBOX.y + 15)))
        TEXTBOX.w=max(100, text_render.get_width() + 10)
        TEXTBOX.topleft=((WIDTH//2 - TEXTBOX.w//2), (HEIGHT//2 + 15))

        continue_button.draw(WINDOW)
        continue_text = BUTTON_FONT2.render("CONTINUE", 1, WHITE)
        WINDOW.blit(continue_text, (
        (CONTINUEx + BUTTON_WIDTH//2 - continue_text.get_width()//2), (CONTINUEy + BUTTON_HEIGHT//2 - continue_text.get_height()//2)))

        exit_button2.draw(WINDOW)
        exit_text = BUTTON_FONT.render("EXIT", 1, WHITE)
        WINDOW.blit(exit_text, (
        (EXIT2x + BUTTON_WIDTH//2 - exit_text.get_width()//2), (EXIT2y + BUTTON_HEIGHT//2 - exit_text.get_height()//2 + 1)))
        
        pygame.display.update()
    
    pygame.mixer.music.stop()
    pygame.key.set_repeat()
    return int(text)


def settle_up(bet, end_text, end2_text, blackjack):
    if end_text == "PLAYER WINS!" and blackjack == True:
        global balance
        balance = balance + bet + (round(bet/2))
    if end_text == "PLAYER WINS!" and blackjack == False:
        balance += bet
    if end_text == "COMPUTER WINS!" or end_text == "BUST!":
        balance -= bet
    if end_text == "FIRST HAND: WIN!":
        balance += bet
    if end_text == "FIRST HAND: LOSS!" or end_text == "FIRST HAND: BUST!":
        balance -= bet
    if end2_text == "SECOND HAND: WIN!":
        balance += bet
    if end2_text == "SECOND HAND: LOSS!" or end2_text == "SECOND HAND: BUST!":
        balance -= bet
    if balance <= 0:
        balance = 100


def check_highscore():
    global balance
    with open("highscore.txt") as file:
        highscore = file.read()

    if balance > int(highscore):
        with open("highscore.txt", "w") as file:
            file.write(str(balance))


if __name__ == "__main__":
    main()