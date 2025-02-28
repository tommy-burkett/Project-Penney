## Project Penney

The purpose of this code is to generate a specified number of decks to simulate Penney's Game, score each combination of the game to determine 
the odds of winning for each combination and display these statistics visually on a heatmap. 

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

- datagen.py: Contains code related to the generation of decks and their storage. The first function `get_decks()` generates a certain number of decks specified by `n_decks` for each `seed`. Then, to store the decks we use `store_data()` which will store the decks we generated from `get_decks()` in a `.npy` file in the `data/` folder.

- helpers.py: Contains code with functions and variables needed across various other modules. 

- processing.py: Contains code related to scoring the games. In order to score the games we must first load a file from the `data/` folder by using the `load_file()` function. Then we convert the numbers in the decks to colors with the `numbers_to_colors()` function. After that, we check to make sure the player combinations exist in the deck with `combination_check()`. Once all of the pre-processing is done, we simulate `penney_game()` with a specified number of simulations `num_simulations` that can be changed by the user within this `processing.py` file. To change the number of simulations, simply open the `processing.py` file and at the top, where the constants are listed, change `NUM_SIMULATIONS` to your desired number. Now that we have the Penney's Game function, we can simulate the game for all 64 - 8 = 56 combinations in the `simulate_games_for_all_combinations()` funciton. Lastly, the `statistics()` function stores all of the data from `simulate_games_for_all_combinations()` by the `scoring_method` (either tricks or total cards) and saves it to a `.npy` file that is used in the next module. 

- visualization.py: Contains code related to creating visualizations for the scoring. Before the visualizations can be created, we load the statistics using our `load_file()` function. Once we have the statistics loaded, we convert the `.npy` file to a `Pandas DataFrame` using the `npy_to_dataframe()` function so that the data will be easily accessible when generating our heatmaps. Finally, once this `DataFrame` is created, we load it into our `generate_heatmap_from_df()` function, which returns our final visualizations for tricks and total cards. 

---

`data/` 

- This folder holds all of the `.npy` files stored from `datagen.py` in an organized manner. The files are named `'decks_{seed}.npy'` and they include the seed used to generate the decks within them. The other files saved to this folder are the `'decks_{seed}_{scoring_method}_probabilities.npy'` files that include our statistics that we generated in the `processing.py` file. 

---

`final_testing.ipynb`

- How to Run this file successfully:
    - This file contains the important tests ran to ensure that the code executes as planned.
    - First, run the imports to load our files from the `src/` folder.
    - Second, store the number of decks and seed.
    - Third, store our data using the `datagen.store_data()` function.
          - Check to make sure data was stored properly
    - Fourth, run the file through the `processing.statistics()` function.
          - The statistics files should now be in the `data/` folder
    - Fifth, load the `'data/decks_{seed}_{scoring_method}_probabilities.npy'` file into `visualizations.load_file()`.
    - Sixth, convert the `'data/decks_{seed}_{scoring_method}_probabilities.npy'` into a DataFrame using `visualizations.npy_to_dataframe()`. 
    - Finally, load the Dataframe into the `visualizations.generate_heatmap_from_df()` function.
          - Output: heatmap for the probability statistics 

---
