## Project Penney

The purpose of this code is to generate a specified number of decks to simulate Penney's Game, score each combination of the game to determine 
the odds of winning for each combination and display these statistics visually. 

Penney's game is a sequence game commonly played with coins. Player 1 selects any combination of heads and tails with length 3
and then Player 2 does the same. So, for example, Player 1 picks HHT and Player 2 picks THT, and then they flip a coin until
one of their combinations is hit consecutively. The game is replayed for as many times as wanted, with the players tallying up
their wins. At first glance, the game seems to be fair, with each player having almost an equal chance of flipping their
sequence first, but that is not the case. There are combinations that statistically win the majority of the time against
others, so Player 2 always has the advantage over Player 1. To maximize your win percentage, Player 2 must invert Player 1's 
second option, and then repeat Player 1's first two options. So, if Player 1 selects HHT, Player 2 should select THH 
(Player 1 = 123, Player 2 = -212).

However, for our implementation of the game, instead of coins, we are using a deck of cards. The same rules still apply,
Player 1 selects a combination of length 3 followed by Player 2 selecting a combination of length 3, but now they 
choose Red/Black instead of Heads/Tails. For example, Player 1 selects BRB and Player 2, knowing the trick, should select
BBR. Additionally, our game is scored in terms of wins and cards won. For instance, in a shuffled deck of 52 cards, each time 
a selected combination appears consecutively, that player adds one win to their tally, and collects all of the previous cards
leading up to the consecutive combination. 

---

Files included:

`src/` 

- datagen.py: Contains code related to the generation of decks and their storage.

- helpers.py: Contains code with functions and variables needed across various other modules. 

- processing.py: Contains code related to scoring the games. 

- visualization.py: Contains code related to creating visualizations for the scoring. 


---
