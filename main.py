#initialize 3 lists with values True corresponding to rows
def initialize_row(number_of_pearls_in_row):
    row = [True] * number_of_pearls_in_row
    return row

def initialize_board():
    breakout_flag = False
    while not breakout_flag:
        try:
            row1_length, row2_length, row3_length = input("what is the password?: ").split()
        except:
            print('Incorrect. try again.\n')
            continue
        try:
            board = [row1_length,row2_length,row3_length]
            for index in range(3):
                board[index] = int(board[index])
                if 3 >= board[index] or board[index] > 8:
                    print('nope. out of bounds.\n')
                    board = []
                    initialize_board()
                else:
                    board[index] = initialize_row(board[index])
                    if index == 2:
                        breakout_flag = True
        except:
            print('nope. try again. \n')
            continue
    return board

#Hello Brandon, would you like to go first?
def is_Brandon_first_player():
    while True:
        go_first_raw = input('Hello, Brandon! Would you like to go first? y/n (you can quit at any prompt) >>>')
        if go_first_raw == 'quit':
            quit()
        if go_first_raw == 'y':
            return True
        if go_first_raw == 'n':
            return False
        else:
            print("\nI didn't quite get that. Let's try again.\n")
            continue

#render pearls
def translate_row(row):
    rendered_row = list()
    for element in row:
        if element:
            rendered_row.append('( *) ')
        else: rendered_row.append('')
    return rendered_row

def print_board(board):
    print('\n  A   ' + ''.join(translate_row(board[0])) + '\n')
    print('  B  ' + ''.join(translate_row(board[1])) + '\n')
    print('  C   ' + ''.join(translate_row(board[2])) + '\n')

#ask PLAYER which row to pick from or quit or help
def your_turn_player_announcement(player):
    if player:
        print('Your turn, Brandon!\n')
    else:
        print("Other Player's turn.\n")

def token_inspect(board, row, index):
    placeholder = board[row]
    return placeholder[index]

#TODO DRY
def which_row_get(board):
    while True:
        row_choice_raw = input("Which row would you like to remove from? (can also 'reprint' board) >>> ")
        if row_choice_raw in ['a','A',1]:
            if not token_inspect(board, 0, 0):
                print("Can't remove from an empty row!\n")
                continue
            return 0
        if row_choice_raw in ['b','B',2]:
            if not token_inspect(board, 1, 0):
                print("Can't remove from an empty row!\n")
                continue
            return 1
        if row_choice_raw in ['c','C',3]:
            if not token_inspect(board, 2, 0):
                print("Can't remove from an empty row!\n")
                continue
            return 2
        if row_choice_raw in ['reprint','r']:
            print_board(board)
            continue
        if row_choice_raw == 'quit': quit()
        else:
            print('Invalid Response. Please try your selection again.')
            continue

#ask how many to remove (silent allow quit) and then flip the correct number of tokens to false

def how_many_get(board, row):
    while True:
        number_to_remove = input("How many pearls would you like to remove?") #TODO: ADD GO BACK OPTION
        if number_to_remove == 'quit': quit()
        #TODO
        # if number_to_remove == 'back': return False or something idk yet
        try:
            number_to_remove = int(number_to_remove)
            total_active_tokens = 0
            for token in row:
                if token:
                    total_active_tokens = total_active_tokens + 1
            if number_to_remove <= 0 or number_to_remove > total_active_tokens:
                print('Invalid number, try again please.')
                continue
            if close_to_victory(board):
                if number_to_remove == total_active_tokens:
                    print('Cannot remove all of last line! (You are close to winning!)')
                    continue
            return number_to_remove
        except:
            print("Invalid character! Try again.\n")
            continue
            # old code
            # if row.count(True) >= number_to_remove > 0:
            #     try:
            #         first_false_pos = row.index(False)
            #         remove_pieces(row, number_to_remove, first_false_pos)
            #     except:
            #         remove_pieces(row, number_to_remove, 0)
            # else:
            #     print('Invalid number - Try again please.\n')
            #     continue

def close_to_victory(board):
    empty_rows = 0
    criteria_met_in_choice_row = False
    for i in range(3):
        if not token_inspect(board, i, 0):
            empty_rows = empty_rows + 1
    if empty_rows == 2: criteria_met_in_choice_row = True
    return criteria_met_in_choice_row

def remove_pieces(row, remove_this_many):
    active_tokens = 0
    for token in row:
        if token:
            active_tokens = active_tokens + 1
    for i in range(remove_this_many):
        row[active_tokens - i - 1] = False
    return row
    #old code
    #for i in range(remove_this_many):
    #     if first_false_pos:
    #         row[(first_false_pos - range(row)) -i] = False
    #     row[-i] = False

def player_move(board):
    row_choice = which_row_get(board)
    how_many_choice = how_many_get(board, board[row_choice])
    board[row_choice] = remove_pieces(board[row_choice], how_many_choice)
    return board

#check if won
#if won, print winner win!
#retry? yes/no?

#OLD CODE FOR RETRY
#input sanitizer function
# def sanitize_raw_retry_game(raw_input):
#     if raw_input == 'y':
#         return False
#     if raw_input in ['n', 'quit']:
#         print('\n===Thanks for playing guys!===\n')
#         quit()
#     print("Nope that won't work. Try again! Retry! It will be fun again!\n")
#     sanitize_raw_retry_game(input("Retry? y/n"))

#Enumeration
# 1) Ongoing
# 2) Restarting
# 3) Exit
# class Gamestate(enumeration)

# def compute_game_state(row..., player)

def did_win(board):
    #fun pattern I logic-ed out - keep it simple stupid
    #if (not row1[0] or not row2[0] or not row3[0]) and (row1[0] ^ row2[0]) ^ row3[0] and (not row1[1] or not row2[1] or not row3[1]) :
    empty_rows = 0
    rows_with_only_one_token = 0
    for row in board:
        if not row[0]:
            empty_rows = empty_rows + 1
        if not row[1] and row[0]:
            rows_with_only_one_token = rows_with_only_one_token + 1
    if empty_rows == 2 and rows_with_only_one_token == 1:
        print_board(board)
        print("You've won!!! Nicely done!!! Congratulations!!!\n")
        quit()
        # TODO ADD RETRY
        # raw_retry_game = input('Would you like to play again? y/n')
        # return sanitize_raw_retry_game(raw_retry_game)
    return False


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
                                                #GAME LOGIC:

def game_app():

    # 1- initialize a board (a list) containing 3 lists with values True corresponding to rows
    master_board = initialize_board()

    # 2- Hello Brandon, would you like to go first?
    player_is_Brandon = is_Brandon_first_player()

    # Main loop
    while not did_win(master_board):

        # 3- render pearls
        print_board(master_board)

        #4 player selection and update game and player

        your_turn_player_announcement(player_is_Brandon)

        master_board = player_move(master_board)

        player_is_Brandon = not player_is_Brandon

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################



#Run game
game_app()
