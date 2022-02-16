# player_Q_Values = {} #*! key: player_value, show_card, usable_ace; actions: hit or stick
# for i in range(12, 22):
#     for j in range(1, 11):
#         for k in [True, False]:
#             player_Q_Values[(i, j, k)] = {}
#             for a in [1, 0]: #*! 1: HIT  0: STAND
#                 if (i == 21) and (a == 0):
#                     player_Q_Values[(i, j, k)][a] = 1
#                 else:
#                     player_Q_Values[(i, j, k)][a] = 0
                    
# print((player_Q_Values))


import gym
from gym import envs

env = gym.make('Blackjack-v1')
print(env.observation_space)

env.action_space.n