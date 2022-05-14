import ludopy
import numpy as np
import cv2
from ludopy.player import get_enemy_at_pos, enemy_pos_at_pos
from stateAndActions import StateAndActions

g = ludopy.Game()
there_is_a_winner = False

round = 0
while not there_is_a_winner:

    input_states = StateAndActions()
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
    pieces = enemy_pieces
    pieces = np.append(enemy_pieces, [player_pieces], axis=0)
    if player_i == 1:
        if len(move_pieces):
            states = []
            actions = []
            for i in range(len(player_pieces)):
                pos = player_pieces[i]
                other_pieces = []
                for j in range(len(player_pieces)):
                    if j == i:
                        continue
                    other_pieces.append(player_pieces[j])
                states.append(input_states.get_state(pos, other_pieces, enemy_pieces))
                actions.append(input_states.get_action(states[i], pos, dice, other_pieces, enemy_pieces))
            print(f"state {states}")
            print(f"actions {actions}")
            #print(f"possible rewards {input_states.get_reward(actions[0])} {input_states.get_reward(actions[1])} {input_states.get_reward(actions[2])} {input_states.get_reward(actions[3])}")

            if len(move_pieces) == 4:
                print(f"Availabe pieces to move {move_pieces}, chose one of them")
                img = ludopy.visualizer.make_img_of_board(pieces, dice, 3, round)
                img = cv2.resize(img, (1088,900))
                cv2.imshow("current board", img)
                waitkey = cv2.waitKey(0) 
                cv2.destroyAllWindows()
                piece_to_move = None
                if int(waitkey) == 48:
                    piece_to_move = move_pieces[0]
                elif int(waitkey) == 49:
                    piece_to_move = move_pieces[1]
                elif int(waitkey) == 50:
                    piece_to_move = move_pieces[2]
                elif int(waitkey) == 51:
                    piece_to_move = move_pieces[3]

                if piece_to_move == None:
                    raise Exception("invalid input")
            else:
                print(f"Availabe pieces to move {move_pieces}, chose one of them")
                waitkeys = []
                for i in range(len(move_pieces)):
                    waitkeys.append((i, move_pieces[i] + 48))

                img = ludopy.visualizer.make_img_of_board(pieces, dice, 3, round)
                img = cv2.resize(img, (1088,900))
                cv2.imshow("current board", img)
                waitkey = cv2.waitKey(0) 
                cv2.destroyAllWindows()
                piece_to_move = None
                for i in range(len(waitkeys)):
                    (idx,key) = waitkeys[i]
                    if key == waitkey:
                        piece_to_move = move_pieces[idx]
                        break
                
                if piece_to_move == None:
                    raise Exception("Invalid input")

        else:
            piece_to_move = -1

        dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner = g.answer_observation(piece_to_move)      
    else:
        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1

        _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
    
    round = round + 1


print("Saving history to numpy file")
g.save_hist(f"game_history.npy")
print("Saving game video")
g.save_hist_video(f"game_video.avi")