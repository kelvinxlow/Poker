# import code
import pygame
import random
import time
from Deck import Deck
from Actions import Actions
from Best import Best
from Money import Money

pygame.init()

# colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 128)
red = (128, 0, 0)
hover_blue = (0, 0, 255)
hover_red = (255, 0, 0)
yellow = (255, 180, 0)
hover_yellow = (255, 255, 0)

# screen size
x = 1000
y = 750
screen = pygame.display.set_mode([x, y])

# window settings
pygame.display.set_caption("Texas Hold'Em")
icon = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\icon.png")
pygame.display.set_icon(icon)
home_screen = True

# left click
left = 1

# images
home = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\home.jpg")
table = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\table.jpg")
monkey = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\monkey.jpg")
rhino = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\rhino.jpg")
penguin = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\penguin.jpg")
croc = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\croc.jpg")
hippo = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\hippo.jpg")
eagle = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\eagle.jpg")

# card images
a, b = 13, 4
card_images = [[0 for x in range(a)] for y in range(b)]
for i in range(0, 13):
    card_images[0][i] = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\PNG\{}D.png".format(i+1))
    card_images[1][i] = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\PNG\{}C.png".format(i+1))
    card_images[2][i] = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\PNG\{}H.png".format(i+1))
    card_images[3][i] = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\PNG\{}S.png".format(i+1))
card_back = pygame.image.load(r"C:\Users\lkelv\PycharmProjects\SimpleGame\PNG\CB.png")

# set up - variables
num_players = 6
button = 0
small_blind = 1
big_blind = 2
current_player = 3
small_post = 5
big_post = 10
money = []
cards = []
player_card_images = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
comm_card_images = [0, 0, 0, 0, 0]
p_cards = []
c_cards = []
best_card = []
best_rank = [0, 0, 0, 0, 0, 0]
fold_con = [False, False, False, False, False, False]
current_stage = "Round Start"
cycle_end = big_blind
amount_raised = 0
round_bet = [0, 5, 10, 0, 0, 0]
total_pot = 15
deck = []

# text and buttons
title_font = pygame.font.Font('freesansbold.ttf', 50)
welcome = title_font.render("Welcome to ", True, white)
texas = title_font.render("Texas Hold'Em", True, white)

title_font_poker = pygame.font.Font('freesansbold.ttf', 100)
poker = title_font_poker.render("Poker", True, white)

button_font = pygame.font.Font('freesansbold.ttf', 20)
play = button_font.render("Play", True, white)
exit = button_font.render("Exit", True, white)
check = button_font.render("Check", True, black)
call = button_font.render("Call", True, black)
fold = button_font.render("Fold", True, white)
raise_txt = button_font.render("Raise", True, white)
raise_min = button_font.render("$10", True, white)
raise_qua = button_font.render("1/4", True, white)
raise_hal = button_font.render("1/2", True, white)
raise_all = button_font.render("All", True, white)

# money and displaying money
for i in range(0, num_players):
    money.append(Money())
money_font = pygame.font.Font('freesansbold.ttf', 30)
display_money = []
for i in range(0, num_players):
    display_money.append(money[i].get_total())
player_money = [0, 0, 0, 0, 0, 0]

# initial small and big blind bets
money[small_blind].bet(small_post)
money[big_blind].bet(big_post)


# to determine a players best card
def reset_best():
    for i in range(0, num_players):
        best_card.append(Best())


# to round the players money to two decimal places and to reduce it to an integer if there is no cents
def get_money():
    for i in range(0, num_players):
        if money[i].get_total() % 1 == 0:
            display_money[i] = int(money[i].get_total())
        else:
            display_money[i] = round(money[i].get_total(), 2)


# to get the string to print the amount of money out to the screen
def show_money():
    for i in range(0, num_players):
        player_money[i] = money_font.render("$"+str(display_money[i]), True, white)


# to determine if the player has bet more money than he has remaining and to determine the amount of money that has to be removed from the pot if they did so
def negative_check(current_player):
    if money[current_player].total < 0:
        overshoot = money[current_player].total
        money[current_player].bet(overshoot)
        return -overshoot
    else:
        return 0


# actions to do at the start of a new round
def round_start():
    # resets all the players best hand values
    reset_best()

    # to generate the deck
    global deck
    deck_obj = Deck()
    deck_obj.generate_deck()
    deck_obj.shuffle_deck()
    deck = deck_obj.get_deck()

    # to deal the players their cards
    for i in range(0, num_players):
        cards.append(Actions(deck))
        cards[i].initial_deal()
        deck = cards[i].get_deck()

    # to get the images corresponding to the players cards
    for i in range(0, num_players):
        p_cards = cards[i].get_player_cards()
        for j in range(0, 2):
            if p_cards[j][-1] == 'D':
                player_card_images[i][j] = card_images[0][int(p_cards[j][:-1])-1]
            elif p_cards[j][-1] == 'C':
                player_card_images[i][j] = card_images[1][int(p_cards[j][:-1])-1]
            elif p_cards[j][-1] == 'H':
                player_card_images[i][j] = card_images[2][int(p_cards[j][:-1])-1]
            else:
                player_card_images[i][j] = card_images[3][int(p_cards[j][:-1])-1]


# betting proceedure for all pre_flop betting
def pre_flop(current_player, amount_raised):
    global total_pot
    # determine if the player needs to make an action
    if fold_con[current_player] is False and money[current_player].total > 0:
        # the rng in their decision
        decision = get_move()
        # determine the best hand available to help decide what they will do
        best_card[current_player].get_player_hand(cards[current_player].get_player_cards())
        best_card[current_player].get_player_cards()
        get_best(current_player)
        # their move will vary based on whether or not someone has already raised the pot this round
        if amount_raised == 0:
            # their move will also vary based on what hand they have
            if best_rank == 2:
                # in this case there is a 50% chance they raise 50% chance they check 0% chance they fold
                if decision > 50:
                    amount_raised += 10
                    total_pot += betting_pre_flop(amount_raised, current_player)
                else:
                    total_pot += betting_pre_flop(amount_raised, current_player)
            else:
                if big_blind == current_player:
                    pass
                elif decision > 80:
                    amount_raised += 10
                    total_pot += betting_pre_flop(amount_raised, current_player)
                elif decision > 20:
                    total_pot += betting_pre_flop(amount_raised, current_player)
                else:
                    fold_con[current_player] = True
        else:
            if best_rank == 2:
                if decision > 90:
                    amount_raised += 10
                    total_pot += betting_pre_flop(amount_raised, current_player)
                elif decision > 20:
                    total_pot += betting_pre_flop(amount_raised, current_player)
                else:
                    fold_con[current_player] = True
            else:
                if decision > 80:
                    total_pot += betting_pre_flop(amount_raised, current_player)
                else:
                    fold_con[current_player] = True
        # this determines if they bet more than they could
        overshoot = negative_check(current_player)
        # if they did over bet the money they didn't have is removed from the pot
        if overshoot != 0:
            total_pot -= overshoot
    return amount_raised


# determines their actions post-flop
def flop(current_player, amount_raised):
    global total_pot
    decision = get_move()
    best_card[current_player].get_community_card(c_cards)
    best_card[current_player].get_player_cards()
    best_card[current_player].sort_hand()
    get_best(current_player)
    if fold_con[current_player] is False and money[current_player].total > 0:
        if amount_raised == 0:
            if best_rank[current_player] >= 5: # if they have a straight or better
                if decision > 70:
                    amount_raised += 20
                    total_pot += betting(amount_raised, current_player)
                elif decision > 20:
                    amount_raised += 10
                    total_pot += betting(amount_raised, current_player)
                else:# placeholder in case i need to do something with check
                    pass
            elif best_rank[current_player] > 2:
                if decision > 95:
                    amount_raised += 20
                    total_pot += betting(amount_raised, current_player)
                elif decision > 40:
                    amount_raised += 10
                    total_pot += betting(amount_raised, current_player)
                else:# placeholder for check
                    pass
            elif best_rank[current_player] == 2:
                if decision > 80:
                    amount_raised += 10
                    total_pot += betting(amount_raised, current_player)
                else:
                    pass
            elif best_card[current_player].high >= 12:
                if decision > 95:
                    amount_raised += 10
                    total_pot += betting(amount_raised, current_player)
                else:
                    pass
            else:
                pass
        else:
            if best_rank[current_player] >= 5:  # if they have a straight or better
                if decision > 90:
                    amount_raised += 20
                    total_pot += betting(amount_raised, current_player)
                elif decision > 50:
                    amount_raised += 10
                    total_pot += betting(amount_raised, current_player)
                else:
                    total_pot += betting(amount_raised, current_player)
            elif best_rank[current_player] > 2:
                if decision > 90:
                    amount_raised += 10
                    total_pot += betting(amount_raised, current_player)
                elif decision > 20:
                    total_pot += betting(amount_raised, current_player)
                else:
                    fold_con[current_player] = True
            elif best_rank[current_player] == 2:
                if decision > 60:
                    total_pot += betting(amount_raised, current_player)
                else:
                    fold_con[current_player] = True
            else:
                if decision > 90:
                    total_pot += betting(amount_raised, current_player)
                else:
                    fold_con[current_player] = True
        overshoot = negative_check(current_player)
        if overshoot != 0:
            total_pot -= overshoot
    return amount_raised


# determines the amount of money they have to bet to stay in the round
# varies from betting post-flop because it must account for the big post and small post
def betting_pre_flop(amount_raised, current_player):
    bet_amount = big_post + amount_raised - round_bet[current_player]
    money[current_player].bet(bet_amount)
    round_bet[current_player] += bet_amount
    return bet_amount


# determines the amount of money they have to bet to stay in the round post-flop
def betting(amount_raised, current_player):
    bet_amount = amount_raised - round_bet[current_player]
    money[current_player].bet(bet_amount)
    round_bet[current_player] += bet_amount
    return bet_amount


# the rng factor, generates a random number that adds a hint of randomness and unpredictability to the computer
def get_move():
    return random.randint(1, 101)


# determines what the players best hand is
def get_best(current_player):
    best_card[current_player].reset_best()
    best_card[current_player].royal_flush()
    if best_card[current_player].player_best is None:
        best_card[current_player].straight_flush()
        if best_card[current_player].player_best is None:
            best_card[current_player].four_oak()
            if best_card[current_player].player_best is None:
                best_card[current_player].full_house()
                if best_card[current_player].player_best is None:
                    best_card[current_player].flush()
                    if best_card[current_player].player_best is None:
                        best_card[current_player].straight()
                        if best_card[current_player].player_best is None:
                            best_card[current_player].three_oak()
                            if best_card[current_player].player_best is None:
                                best_card[current_player].two_pair()
                                if best_card[current_player].player_best is None:
                                    best_card[current_player].one_pair()
                                    if best_card[current_player].player_best is None:
                                        best_card[current_player].high_card()
                                        best_rank[current_player] = 1
                                    else:
                                        best_rank[current_player] = 2
                                else:
                                    best_rank[current_player] = 3
                            else:
                                best_rank[current_player] = 4
                        else:
                            best_rank[current_player] = 5
                    else:
                        best_rank[current_player] = 6
                else:
                    best_rank[current_player] = 7
            else:
                best_rank[current_player] = 8
        else:
            best_rank[current_player] = 9
    else:
        best_rank[current_player] = 10


# determines the number of players that have folded to see
def get_total_fold():
    total_fold = 0
    for i in range(0, num_players):
        if fold_con[i] is True:
            total_fold += 1
    return total_fold


# determines the number of players that are still in the game
def get_players_left():
    players_left = num_players
    for i in range(0, num_players):
        if money[i].get_total() == 0:
            players_left -= 1
    return players_left


# gets input for what the player wants to do
def get_player_action(left):
    while True:
        # options
        pygame.draw.rect(screen, yellow, (320, 610, 100, 49))
        pygame.draw.rect(screen, red, (320, 665, 100, 49))
        pygame.draw.rect(screen, blue, (580, 610, 100, 32))
        pygame.draw.rect(screen, blue, (580, 647, 49, 32))
        pygame.draw.rect(screen, blue, (580, 681, 49, 32))
        pygame.draw.rect(screen, blue, (631, 647, 49, 32))
        pygame.draw.rect(screen, blue, (631, 681, 49, 32))
        # options text
        screen.blit(check, (338, 625))
        screen.blit(fold, (348, 680))
        screen.blit(raise_txt, (600, 617))
        screen.blit(raise_min, (588, 654))
        screen.blit(raise_qua, (640, 654))
        screen.blit(raise_hal, (588, 688))
        screen.blit(raise_all, (640, 688))
        # determines what button the player clicks
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if 420 > mouse[0] > 320 and 659 > mouse[1] > 610:
                pygame.draw.rect(screen, hover_yellow, (320, 610, 100, 49))
                screen.blit(check, (338, 625))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    return "check"
            elif 420 > mouse[0] > 320 and 714 > mouse[1] > 665:
                pygame.draw.rect(screen, hover_red, (320, 665, 100, 49))
                screen.blit(fold, (348, 680))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    return "fold"
            elif 629 > mouse[0] > 580 and 679 > mouse[1] > 647:
                pygame.draw.rect(screen, hover_blue, (580, 647, 49, 32))
                screen.blit(raise_min, (588, 654))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    return "raise 10"
            elif 680 > mouse[0] > 631 and 679 > mouse[1] > 647:
                pygame.draw.rect(screen, hover_blue, (631, 647, 49, 32))
                screen.blit(raise_qua, (640, 654))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    return "raise 1/4"
            elif 629 > mouse[0] > 580 and 713 > mouse[1] > 681:
                pygame.draw.rect(screen, hover_blue, (580, 681, 49, 32))
                screen.blit(raise_hal, (588, 688))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    return "raise 1/2"
            elif 680 > mouse[0] > 631 and 713 > mouse[1] > 681:
                pygame.draw.rect(screen, hover_blue, (631, 681, 49, 32))
                screen.blit(raise_all, (640, 688))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    return "raise all"
        pygame.display.update()


# executes the players actions, runs in place of pre_flop() since the user can control their actions
def execute_player_action_pre_flop(player_action, amount_raised):
    global total_pot
    if player_action == "fold":
        fold_con[0] = True
    elif player_action == "check":
        total_pot += betting_pre_flop(amount_raised, 0)
    elif player_action == "raise 10":
        amount_raised += 10
        total_pot += betting_pre_flop(amount_raised, 0)
    elif player_action == "raise 1/4":
        amount_raised += int(money[0].get_total()/4)
        total_pot += betting_pre_flop(amount_raised, 0)
    elif player_action == "raise 1/2":
        amount_raised += int(money[0].get_total()/2)
        total_pot += betting_pre_flop(amount_raised, 0)
    elif player_action == "raise all":
        amount_raised += money[0].get_total()
        total_pot += betting_pre_flop(amount_raised, 0)
    overshoot = negative_check(0)
    if overshoot != 0:
        total_pot -= overshoot
    return amount_raised


# executes the players actions post_flop
def execute_player_action(player_action, amount_raised):
    global total_pot
    if player_action == "fold":
        fold_con[0] = True
    elif player_action == "check":
        total_pot += betting(amount_raised, 0)
    elif player_action == "raise 10":
        amount_raised += 10
        total_pot += betting(amount_raised, 0)
        overshoot = negative_check(0)
        if overshoot != 0:
            total_pot -= overshoot
    elif player_action == "raise 1/4":
        amount_raised += int(money[0].get_total()/4)
        total_pot += betting(amount_raised, 0)
        overshoot = negative_check(0)
        if overshoot != 0:
            total_pot -= overshoot
    elif player_action == "raise 1/2":
        amount_raised += int(money[0].get_total()/2)
        total_pot += betting(amount_raised, 0)
        overshoot = negative_check(0)
        if overshoot != 0:
            total_pot -= overshoot
    elif player_action == "raise all":
        amount_raised += money[0].get_total()
        total_pot += betting(amount_raised, 0)
        overshoot = negative_check(0)
        if overshoot != 0:
            total_pot -= overshoot
    return amount_raised


# visuals
while True:
    if home_screen:
        # displays text and buttons on the homescreen
        screen.blit(home, (0, 0))
        screen.blit(welcome, (650, 250))
        screen.blit(texas, (620, 325))
        screen.blit(poker, (650, 400))
        pygame.draw.rect(screen, blue, (600, 550, 150, 100))
        pygame.draw.rect(screen, red, (800, 550, 150, 100))
        screen.blit(play, (655, 590))
        screen.blit(exit, (855, 590))

        # gives the use the option to play or quit
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if 750 > mouse[0] > 600 and 650 > mouse[1] > 550:
                pygame.draw.rect(screen, hover_blue, (600, 550, 150, 100))
                screen.blit(play, (655, 590))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    home_screen = False
            if 900 > mouse[0] > 800 and 650 > mouse[1] > 550:
                pygame.draw.rect(screen, hover_red, (800, 550, 150, 100))
                screen.blit(exit, (855, 590))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
                    pygame.quit()
                    quit()
            pygame.display.update()
    else:
        if get_players_left() == 1:# game ends when there is only one player
            current_stage = "Game Over"
        if current_stage == "Round Start":
            round_start()
            current_stage = "Pre-Flop"
        elif current_stage == "Pre-Flop":
            total_fold = get_total_fold()  # determines if there is more than one player left
            if total_fold < num_players - 1:
                time.sleep(2)
                if current_player == 0 and fold_con[current_player] is False:  # if its the users turn
                    player_action = get_player_action(left)
                    amount_raised_temp = execute_player_action_pre_flop(player_action, amount_raised)
                else:
                    amount_raised_temp = pre_flop(current_player, amount_raised)
                if amount_raised_temp > amount_raised:  # if someone raises then all the other players must complete their turn again
                    amount_raised = amount_raised_temp
                    if current_player != 0:  # shifts the last player to the player before the current player without going out of bounds
                            cycle_end = current_player - 1
                    else:
                            cycle_end = num_players - 1
                elif current_player == cycle_end:  # moves on to the next stage if everyone has had their turn
                    total_fold = get_total_fold()
                    if total_fold < num_players - 1:
                        current_stage = "Flop"
                    else:
                        current_stage = "Round End"
                if current_player < num_players - 1:  # shifts action to next player
                        current_player += 1
                else:
                    current_player = 0
            else:
                current_stage = "Round End"
        elif current_stage == "Flop":
            # getting the first three community cards and their images
            cards[0].update_deck(deck)
            cards[0].get_community()
            deck = cards[0].get_deck()
            c_cards = cards[0].get_community_cards()
            for j in range(0, 3):
                if c_cards[j][-1] == 'D':
                    comm_card_images[j] = card_images[0][int(c_cards[j][:-1]) - 1]
                elif c_cards[j][-1] == 'C':
                    comm_card_images[j] = card_images[1][int(c_cards[j][:-1]) - 1]
                elif c_cards[j][-1] == 'H':
                    comm_card_images[j] = card_images[2][int(c_cards[j][:-1]) - 1]
                else:
                    comm_card_images[j] = card_images[3][int(c_cards[j][:-1]) - 1]
            # makes the cards deal 1 by 1
            time.sleep(2)
            screen.blit(comm_card_images[0], (355, 345))
            pygame.display.update()
            time.sleep(2)
            screen.blit(comm_card_images[1], (415, 345))
            pygame.display.update()
            time.sleep(2)
            screen.blit(comm_card_images[2], (475, 345))
            current_stage = "Post-Flop"
            # resets everyones bet for the given turn to 0
            for i in range(0, 6):
                round_bet[i] = 0
            current_player = small_blind
            cycle_end = button
            amount_raised = 0
        elif current_stage == "Post-Flop":
            if get_total_fold() < num_players - 1:
                if fold_con[current_player] is True:
                    if current_player == cycle_end:
                        current_stage = "The Turn"

                    if current_player < num_players - 1:
                        current_player += 1
                    else:
                        current_player = 0
                else:
                    time.sleep(2)
                    if current_player == 0 and fold_con[current_player] is False:
                        player_action = get_player_action(left)
                        amount_raised_temp = execute_player_action(player_action, amount_raised)
                    else:
                        amount_raised_temp = flop(current_player, amount_raised)
                    if amount_raised_temp > amount_raised:
                        amount_raised = amount_raised_temp
                        if current_player != 0:
                            cycle_end = current_player - 1
                        else:
                            cycle_end = num_players - 1
                    elif current_player == cycle_end:
                        current_stage = "The Turn"

                    if current_player < num_players - 1:
                        current_player += 1
                    else:
                        current_player = 0
            else:
                current_stage = "Round End"
        elif current_stage == "The Turn":
            # gets the next commmunity card
            cards[0].update_deck(deck)
            cards[0].get_next_community()
            deck = cards[0].get_deck()
            c_cards = cards[0].get_community_cards()
            if c_cards[3][-1] == 'D':
                comm_card_images[3] = card_images[0][int(c_cards[3][:-1]) - 1]
            elif c_cards[3][-1] == 'C':
                comm_card_images[3] = card_images[1][int(c_cards[3][:-1]) - 1]
            elif c_cards[3][-1] == 'H':
                comm_card_images[3] = card_images[2][int(c_cards[3][:-1]) - 1]
            else:
                comm_card_images[3] = card_images[3][int(c_cards[3][:-1]) - 1]
            current_stage = "Turn Bet"
            for i in range(0, 6):
                round_bet[i] = 0
            current_player = small_blind
            cycle_end = button
            amount_raised = 0
        elif current_stage == "Turn Bet":
            if get_total_fold() < num_players - 1:
                if fold_con[current_player] is True:
                    if current_player == cycle_end:
                        current_stage = "The River"
                    if current_player < num_players - 1:
                        current_player += 1
                    else:
                        current_player = 0
                else:
                    time.sleep(2)
                    if current_player == 0 and fold_con[current_player] is False:
                        player_action = get_player_action(left)
                        amount_raised_temp = execute_player_action(player_action, amount_raised)
                    else:
                        amount_raised_temp = flop(current_player, amount_raised) #need to make new betting algorithm
                    if amount_raised_temp > amount_raised:
                        amount_raised = amount_raised_temp
                        if current_player != 0:
                            cycle_end = current_player - 1
                        else:
                            cycle_end = num_players - 1
                    elif current_player == cycle_end:
                        current_stage = "The River"
                    if current_player < num_players - 1:
                        current_player += 1
                    else:
                        current_player = 0
            else:
                current_stage = "Round End"
        elif current_stage == "The River":
            cards[0].update_deck(deck)
            cards[0].get_next_community()
            deck = cards[0].get_deck()
            c_cards = cards[0].get_community_cards()
            if c_cards[4][-1] == 'D':
                comm_card_images[4] = card_images[0][int(c_cards[4][:-1]) - 1]
            elif c_cards[4][-1] == 'C':
                comm_card_images[4] = card_images[1][int(c_cards[4][:-1]) - 1]
            elif c_cards[4][-1] == 'H':
                comm_card_images[4] = card_images[2][int(c_cards[4][:-1]) - 1]
            else:
                comm_card_images[4] = card_images[3][int(c_cards[4][:-1]) - 1]
            current_stage = "Showdown"
            for i in range(0, 6):
                round_bet[i] = 0
            current_player = small_blind
            cycle_end = button
            amount_raised = 0
        elif current_stage == "Showdown":
            if get_total_fold() < num_players - 1:
                if fold_con[current_player] is True:
                    if current_player == cycle_end:
                        current_stage = "Round End"
                    if current_player < num_players - 1:
                        current_player += 1
                    else:
                        current_player = 0
                else:
                    time.sleep(2)
                    if current_player == 0 and fold_con[current_player] is False:
                        player_action = get_player_action(left)
                        amount_raised_temp = execute_player_action(player_action, amount_raised)
                    else:
                        amount_raised_temp = flop(current_player, amount_raised) #need to make new betting algorithm
                    if amount_raised_temp > amount_raised:
                        amount_raised = amount_raised_temp
                        if current_player != 0:
                            cycle_end = current_player - 1
                        else:
                            cycle_end = num_players - 1
                    elif current_player == cycle_end:
                        current_stage = "Round End"
                    if current_player < num_players - 1:
                        current_player += 1
                    else:
                        current_player = 0
            else:
                current_stage = "Round End"
        elif current_stage == "Round End":
            # if the player has not yet folded reveal their cards to the user so they can see what their opponent had
            if fold_con[1] is False:
                screen.blit(player_card_images[1][0], (255, 455))
                screen.blit(player_card_images[1][1], (315, 455))
            if fold_con[2] is False:
                screen.blit(player_card_images[2][0], (255, 225))
                screen.blit(player_card_images[2][1], (315, 225))
            if fold_con[3] is False:
                screen.blit(player_card_images[3][0], (445, 200))
                screen.blit(player_card_images[3][1], (505, 200))
            if fold_con[4] is False:
                screen.blit(player_card_images[4][0], (640, 225))
                screen.blit(player_card_images[4][1], (700, 225))
            if fold_con[5] is False:
                screen.blit(player_card_images[5][0], (640, 455))
                screen.blit(player_card_images[5][1], (700, 455))
            pygame.display.update()
            time.sleep(4)
            # if the player has not folded his best card must be determined to compare to the computers
            if fold_con[0] is False:
                best_card[0].get_community_card(c_cards)
                best_card[0].get_player_hand(cards[0].get_player_cards())
                best_card[0].get_player_cards()
                best_card[0].sort_hand()
                print(best_card[0].player_cards)
                get_best(0)
            best_hand_left = -1
            best_hand_owner = -1 
            other_winners = []
            num_winners = 1
            # to determine the player with the best hand
            for player in range(0, 6):  # to run through all the players
                if fold_con[player] is False:  # if the player has not folded
                    if best_rank[player] > best_hand_left:  # if their best hand is higher than the current best hand
                        best_hand_left = best_rank[player]
                        best_hand_owner = player
                    elif best_rank[player] == best_hand_left:  # if their best hand is equal (in terms of hand, example both players have a full house)
                        # goes to tiebreakers (example who has the higher pair)
                        if best_card[player].tie_break_one > best_card[int(best_hand_owner)].tie_break_one:
                            best_hand_left = best_rank[player]
                            best_hand_owner = player
                        elif best_card[player].tie_break_one == best_card[int(best_hand_owner)].tie_break_one:
                            if best_card[player].tie_break_two is not None:
                                if best_card[player].tie_break_two > best_card[int(best_hand_owner)].tie_break_two:
                                    best_hand_left = best_rank[player]
                                    best_hand_owner = player
                                elif best_card[player].tie_break_two == best_card[int(best_hand_owner)].tie_break_two:
                                    other_winners.append(player)
                                    num_winners += 1
                            else:  # if no player has the better hand then there are multiple winners this round which will split the pot
                                other_winners.append(player)
                                num_winners += 1
            split = num_winners
            # if there is a pot split
            if num_winners > 1:
                money_won = round(total_pot/split, 2)
                while num_winners > 1:
                    money[other_winners[num_winners - 2]].win(money_won)
                    num_winners -= 1
                money[best_hand_owner].win(money_won)
            else:
                money[best_hand_owner].win(total_pot)
            current_stage = "Reset"
        elif current_stage == "Reset":  # resets all the necessary values and shifts the button, small blind and big blind
            reset_best()
            button += 1
            small_blind += 1
            big_blind += 1

            # to ensure that the big and small blind belong to players still in this match
            if button == 6:
                button = 0
            if small_blind == 6:
                small_blind = 0
            if big_blind == 6:
                big_blind = 0

            while money[small_blind].get_total() == 0:
                small_blind += 1
                big_blind += 1
                if small_blind == 6:
                    small_blind = 0
                if big_blind == 6:
                    big_blind = 0

            while money[big_blind].get_total() == 0:
                big_blind += 1
                if big_blind == 6:
                    big_blind = 0

            # to determine the player who will call the shot first in the next pre-flop
            current_player = big_blind + 1
            if current_player == 6:
                current_player = 0

            # reset variables
            cards = []
            player_card_images = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            comm_card_images = [0, 0, 0, 0, 0]
            p_cards = []
            best_card = []
            best_rank = [0, 0, 0, 0, 0, 0]
            fold_con = [False, False, False, False, False, False]
            current_stage = "Round Start"
            cycle_end = big_blind
            amount_raised = 0
            round_bet = [0, 0, 0, 0, 0, 0]
            total_pot = 0
            print(str(money[0].get_total() + money[1].get_total() + money[2].get_total() + money[3].get_total() + money[4].get_total() + money[5].get_total()))

            # to do the small and big bets and ensure
            if money[small_blind].get_total() >= 5:
                money[small_blind].bet(small_post)
                round_bet[small_blind] = small_post
                total_pot += small_post
            else:
                round_bet[small_blind] = money[small_blind].get_total()
                money[small_blind].bet(money[small_blind].get_total())
                total_pot += round_bet[small_blind]

            if money[big_blind].get_total() >= 10:
                money[big_blind].bet(big_post)
                round_bet[big_blind] = big_post
                total_pot += big_post
            else:
                round_bet[big_blind] = money[big_blind].get_total()
                money[big_blind].bet(money[big_blind].get_total())
                total_pot += round_bet[big_blind]

            # to take the players who have no money out
            for i in range(0, 6):
                if money[i].total == 0:
                    fold_con[i] = True
        # when all but one player is left
        elif current_stage == "Game Over":
            winner_declaration = None
            end_font = pygame.font.Font('freesansbold.ttf', 100)
            for i in fold_con:
                if fold_con[i] is False:
                    if i == 0:
                        winner_declaration = "You Win"
                    else:
                        winner_declaration = "Player " + str(i) +" Wins"
            winner_txt = end_font.render(winner_declaration, True, white)
            print(winner_txt)
            screen.blit(winner_txt, (300, 300))
            pygame.display.update()
            time.sleep(5)
            current_stage = "Round Start"
            home_screen = True
            continue

        # draw backdrop
        screen.fill(black)
        screen.blit(table, (50, 75))
        # show player money
        get_money()
        show_money()
        screen.blit(hippo, (50, 50))
        screen.blit(player_money[2], (90, 160))
        screen.blit(eagle, (800, 50))
        screen.blit(player_money[4], (840, 160))
        screen.blit(rhino, (50, 550))
        screen.blit(player_money[1], (90, 660))
        screen.blit(croc, (800, 550))
        screen.blit(player_money[5], (840, 660))
        screen.blit(penguin, (425, 610))
        screen.blit(player_money[0], (465, 720))
        screen.blit(monkey, (425, 10))
        screen.blit(player_money[3], (465, 115))
        pot_display = money_font.render("Pot: $" + str(total_pot), True, white)
        screen.blit(pot_display, (435, 300))
        # show cards
        if current_stage != "Round Start":
            if fold_con[0] is False:
                screen.blit(player_card_images[0][0], (445, 480))
                screen.blit(player_card_images[0][1], (505, 480))
            if fold_con[1] is False:
                screen.blit(card_back, (255, 455))
                screen.blit(card_back, (315, 455))
            if fold_con[2] is False:
                screen.blit(card_back, (255, 225))
                screen.blit(card_back, (315, 225))
            if fold_con[3] is False:
                screen.blit(card_back, (445, 200))
                screen.blit(card_back, (505, 200))
            if fold_con[4] is False:
                screen.blit(card_back, (640, 225))
                screen.blit(card_back, (700, 225))
            if fold_con[5] is False:
                screen.blit(card_back, (640, 455))
                screen.blit(card_back, (700, 455))
        # show community cards
        if comm_card_images[0] != 0:
            screen.blit(comm_card_images[0], (355, 345))
            screen.blit(comm_card_images[1], (415, 345))
            screen.blit(comm_card_images[2], (475, 345))
        if comm_card_images[3] != 0:
            screen.blit(comm_card_images[3], (535, 345))
        if comm_card_images[4] != 0:
            screen.blit(comm_card_images[4], (595, 345))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                home_screen = True
            pygame.display.update()
        pygame.display.update()