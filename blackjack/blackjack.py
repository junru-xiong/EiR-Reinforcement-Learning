import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import random

# actions: hit or stand
ACTION_HIT = 0
ACTION_STICK = 1
ACTIONS = [ACTION_HIT, ACTION_STICK]
ALPHA = 0.1
T = 0.2

AVAILABLE_CARDS = [x for x in range(1, 11)] * 4 + (12 * [10])


# get a new card
def get_card(cards_left):
    return np.random.choice(cards_left)


def card_value(card_id):
    return 11 if card_id == 1 else card_id


# policy for dealer
def dealer_policy(sum_dealer_cards):
    if sum_dealer_cards > 16:
        return ACTION_STICK
    else:
        return ACTION_HIT


# policy for player:
def player_policy(q, t):
    # p = np.array([v/t for v in q.values()])
    p = np.array([q[(2, 7, 10), 0], q[(2, 7, 10), 1]])/t  #*! why (2,7,10) why not random?
    prob_actions = np.exp(p) / np.sum(np.exp(p))
    #*! why not just argmax below?
    cumulative_probability = 0.0
    choice = random.uniform(0, 1)
    for a, pr in enumerate(prob_actions):
        cumulative_probability += pr
        if cumulative_probability > choice:
            return a
    # return len(prob_actions) - 1

# def play(player_sum, dealer_sum, usable_ace_dealer, left_cards, player_action):
def play(player_sum, left_cards, player_action):
    if player_action == ACTION_HIT:
        player_card = get_card(left_cards)
        left_cards.remove(player_card)
        player_sum += card_value(player_card)
        if player_card == 1: #player draws an ace       #*! ace can also be 11
            player_sum -= 10
        if player_sum > 21:
            return True, -1, player_sum
        else:
            return True, 1, player_sum
    else:
        return True, 1, player_sum
    # Dealer's turn
    # while True:
    #     dealer_action = dealer_policy(dealer_sum)
    #     if dealer_action == ACTION_STICK:
    #         break
    #     new_card = get_card(left_cards)
    #     left_cards.remove(new_card)
    #     ace_count = int(usable_ace_dealer)
    #     if new_card == 1:
    #         ace_count += 1
    #     dealer_sum += card_value(new_card)
    #     while dealer_sum > 21 and ace_count:
    #         dealer_sum -= 10
    #         ace_count -= 1
    #     if dealer_sum > 21:
    #         return True, 1, player_sum, dealer_sum
    #     usable_ace_dealer = (ace_count == 1)

    # if player_sum > dealer_sum:
    #     return True, 1, player_sum, dealer_sum
    # elif player_sum == dealer_sum:
    #     return True, 0, player_sum, dealer_sum
    # else:
    #     return True, -1, player_sum, dealer_sum

if __name__ == '__main__':
    # initialize Q
    Q = {}
    state = (2, 7, 10)
    for action in ACTIONS:
        Q[state, action] = 0

    action_counts = {}
    reward_counts = {}
    reward_per_episode = []
    episodes = 100
    for episode in range(episodes):
        print("*" * 100)
        print(f"Episode: {episode + 1}")
        print("*" * 100)
        # Set initial state of the game
        left_cards = AVAILABLE_CARDS.copy()
        player_initial_cards = [2, 7, 10]
        player_sum = 2 + 7 + 10
        for card in player_initial_cards:
            left_cards.remove(card)
        state = (2, 7, 10)
        action = player_policy(Q, T)
        print(f"Player Action: {action}")
        action_counts[action] = action_counts.get(action, 0) + 1
        # Set dealer initial state
        # dealer_card1 = get_card(left_cards)
        # left_cards.remove(dealer_card1)
        # dealer_card2 = get_card(left_cards)
        # left_cards.remove(dealer_card2)
        # print(f"Dealer's Cards: {dealer_card1} and {dealer_card2}")
        # dealer_sum = card_value(dealer_card1) + card_value(dealer_card2)
        # usable_ace_dealer = 1 in (dealer_card1, dealer_card2)
        # if dealer_sum > 21:
        #     dealer_sum -= 10
        reward = 0
        game_over = False
        while not game_over:
            # print(f"Play Games with player sum: {player_sum} and dealer sum: {dealer_sum}")
            print(f"Play Games with player sum: {player_sum} and player action: {action}")
            # game_over, reward, player_sum, dealer_sum = play(player_sum, dealer_sum, usable_ace_dealer,
            #                                                  left_cards, action)
            game_over, reward, player_sum = play(player_sum, left_cards, action)

            reward_counts[reward] = reward_counts.get(reward, 0) + 1
            print(f"Reward in episode-{episode + 1} is: {reward}")
            # s2 = state
            # a2 = player_policy(Q, T)
            # Q[state, action] = Q[state, action] + ALPHA * (reward + Q[s2, a2] - Q[state, action])
            #*! TD algorithm?
            Q[state, action] = Q[state, action] + ALPHA * (reward - Q[state, action])
            # print(f"Player Sum: {player_sum} and Dealer Sum: {dealer_sum}")
            print(f"Reward in episode# {episode+1}: {reward} for player's action: {action}")
        reward_per_episode.append(reward)
        print(Q)
        print(f"Action Counts: {action_counts}")
        print(f"Reward Counts: {reward_counts}")
    # for reward in reward_per_episode:
    #     print(f"Reward: {reward}")
    # plt.plot(reward_per_episode)
    # plt.title("reward_per_episode")
    # plt.show()