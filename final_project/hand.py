import random
import pygame
import os
pygame.mixer.init()

card_deal_sound = pygame.mixer.Sound(os.path.join("Assets", "card_deal.mp3"))

class Hand:

    BACKUP_DECK = (
    {"type": "king_of_hearts", "score": "10"}, { "type": "queen_of_hearts", "score": "10"}, 
    {"type": "jack_of_hearts", "score": "10"}, {"type": "10_of_hearts", "score": "10"},
    {"type": "9_of_hearts", "score": "9"}, {"type": "8_of_hearts", "score": "8"}, {"type": "7_of_hearts", "score": "7"}, 
    {"type": "6_of_hearts", "score": "6"}, {"type": "5_of_hearts", "score": "5"}, {"type": "4_of_hearts", "score": "4"}, 
    {"type": "3_of_hearts", "score": "3"}, {"type": "2_of_hearts", "score": "2"}, 
    {"type": "ace_of_hearts", "score": "1"},
    {"type": "king_of_spades", "score": "10"}, {"type": "queen_of_spades", "score": "10"}, 
    {"type": "jack_of_spades", "score": "10"}, {"type": "10_of_spades", "score": "10"},
    {"type": "9_of_spades", "score": "9"}, {"type": "8_of_spades", "score": "8"}, {"type": "7_of_spades", "score": "7"}, 
    {"type": "6_of_spades", "score": "6"}, {"type": "5_of_spades", "score": "5"}, {"type": "4_of_spades", "score": "4"}, 
    {"type": "3_of_spades", "score": "3"}, {"type": "2_of_spades", "score": "2"}, 
    {"type": "ace_of_spades", "score": "1"},
    {"type": "king_of_diamonds", "score": "10"}, {"type": "queen_of_diamonds", "score": "10"}, 
    {"type": "jack_of_diamonds", "score": "10"}, {"type": "10_of_diamonds", "score": "10"},
    {"type": "9_of_diamonds", "score": "9"}, {"type": "8_of_diamonds", "score": "8"}, {"type": "7_of_diamonds", "score": "7"}, 
    {"type": "6_of_diamonds", "score": "6"}, {"type": "5_of_diamonds", "score": "5"}, {"type": "4_of_diamonds", "score": "4"}, 
    {"type": "3_of_diamonds", "score": "3"}, {"type": "2_of_diamonds", "score": "2"}, 
    {"type": "ace_of_diamonds", "score": "1"},
    {"type": "king_of_clubs", "score": "10"}, {"type": "queen_of_clubs", "score": "10"}, 
    {"type": "jack_of_clubs", "score": "10"}, {"type": "10_of_clubs", "score": "10"},
    {"type": "9_of_clubs", "score": "9"}, {"type": "8_of_clubs", "score": "8"}, {"type": "7_of_clubs", "score": "7"}, 
    {"type": "6_of_clubs", "score": "6"}, {"type": "5_of_clubs", "score": "5"}, {"type": "4_of_clubs", "score": "4"}, 
    {"type": "3_of_clubs", "score": "3"}, {"type": "2_of_clubs", "score": "2"}, 
    {"type": "ace_of_clubs", "score": "1"})


    card_deck = list(BACKUP_DECK)

    
    def __init__(self):
        self.hand = []
        self.split_hand = []
        self.score = 0
        self.spilt = False


    def hit(self):
        card = random.choice(Hand.card_deck)
        self.hand.append(card)
        Hand.card_deck.remove(card)
        self.score = self.points()
        card_deal_sound.play()


    def points(self):
        score = [card["score"] for card in self.hand]
        score.append("0")
        score = eval("+".join(score))

        ace_hearts_counter = 0
        ace_spades_counter = 0
        ace_clubs_counter = 0
        ace_diamonds_counter = 0
        for card in self.hand:
            if card["type"] == "ace_of_clubs":
                ace_clubs_counter += 1
            elif card["type"] == "ace_of_hearts":
                ace_hearts_counter += 1
            elif card["type"] == "ace_of_spades":
                ace_spades_counter += 1
            elif card["type"] == "ace_of_diamonds":
                ace_diamonds_counter += 1

        if ace_hearts_counter == 1:
            if score + 10 <= 21:
                score = score + 10
                
        if ace_clubs_counter == 1:
            if score + 10 <= 21:
                score = score + 10

        if ace_diamonds_counter == 1:
            if score + 10 <= 21:
                score = score + 10

        if ace_spades_counter == 1:
            if score + 10 <= 21:
                score = score + 10

        return score
    

    def draw(self, surface, width, height, local_x, local_y):
        index = 0
        space = 40
        small_space = 164
        for card in self.hand:
            png = f"{card["type"]}.png"
            png = str(png)
            image = pygame.image.load(os.path.join("Assets", png))
            image = pygame.transform.scale(image, (width, height))
            if height < 310:
                surface.blit(image, ((local_x + ((local_x - small_space) * index)), local_y))
            else:
                surface.blit(image, ((local_x + ((local_x - space) * index)), local_y))
            index += 1


    def logic(self):
        if self.score < 17:
            self.hit()
            self.logic()


    def new_game(self):
        self.hand = []
        self.score = 0
    

    @classmethod
    def new_deck(cls):
        Hand.card_deck = list(Hand.BACKUP_DECK)
