import glob
import numpy as np
import os
from src.helpers import PATH_DATA

# Constants
# Number of cards per deck
NUM_CARDS = 52

# User can change # of simulations 
# Number of times we will run simulation to verify results
NUM_SIMULATIONS = 1000

# List for all possible color combinations 
combinations = [
                'RRR', 'RRB', 'RBR', 'RBB', 'BRR', 'BRB', 'BBR', 'BBB',
               ]


def load_file(filename: str):

    """
        User gives the filename and the function returns 
        the loaded deck if it exists
    """
    
    # If the filename is a pattern (like 'decks_42'), find all matching .npy files
    if '*' in filename:  
        files = glob.glob(filename)
        
        # Check to see if files were found
        if not files:
            print(f'No files matching the pattern "{filename}" found.')
            return None
        
        # Initialize an empty list to store loaded arrays
        combined_data = []
        
        # Iterate over each matching file and load it
        for file in files:
            print(f"Loading file: {file}")
            # Load each .npy file
            data = np.load(file, allow_pickle=True)  
            combined_data.append(data)
        
        # Combine all the data into one numpy array (assuming data is in the correct shape)
        # Concatenate along rows (axis=0)
        combined_data = np.concatenate(combined_data, axis=0)  
        
        return combined_data

    # If it's a single file, just load that file
    else:
        # Check to see if file exists and return it
        if os.path.exists(filename):
            return np.load(filename)

        # If file does not exist, let the user know
        else:
            print(f'File "{filename}" does not exist. Try another file.')
            return None


def numbers_to_colors(deck):
    
    """
        Convert a 2D deck of 0's and 1's to a 2D array 
        of 'R' and 'B' for Red and Black respectively.
    """
    # Create a list to hold the colored decks
    # https://www.w3schools.com/python/python_lists_comprehension.asp
    colored_decks = ["".join(['R' if card == 0 else 'B' for card in deck]) for deck in deck]

    return colored_decks


def combination_check(sequence, combination):

    """
        Now we have to check and make sure that
        Player 1 and Player 2's combinations
        exist in the decks
    """

    return combination in sequence


def penney_game(player1: str,
                player2: str,
                decks,
                num_cards: int=NUM_CARDS,
                num_simulations: int=NUM_SIMULATIONS,
                scoring_method = 'tricks'
               ) -> dict:

    """
        Simulate Penney's game with all possible combinations 
        over multiple decks from file

        Keep track of total wins and total cards won

        Arguments:
            - player1: string of combinations
            - player2: string of combinations
            - decks: decks uploaded from file in data/ folder
            - num_cards: 52 cards in one deck
            - num_simulations: number of simulations user wishes to compute
            - scoring_method: can be 'tricks' or 'total_cards'
        
        Returns:
            dictionary with total tricks and cards won by
            each player, specified by scoring_method in the
            function call
    """

    # Start the number of tricks and cards for each player at 0
    player1_tricks = 0
    player1_total_cards = 0
    player2_tricks = 0
    player2_total_cards = 0
    draw = 0

    # Loop over each 52 card deck in the file
    for deck in decks:
        # Create empty list to hold card combinations
        sequence = []

        # Loop over each individual 52 card deck
        for i, card in enumerate(deck):
            # Convert the card to a string
            card_string = 'R' if card == 0 else 'B'
            # Add the card to the sequence
            sequence.append(card_string)

            # Directly check for Player 1's combinations in the sequence
            if ''.join(sequence[-len(player1):]) == player1:
                # If Player 1 wins, add to their total tricks and cards
                if scoring_method == 'tricks':
                    player1_tricks += 1
                # Add the total cards won by Player 1
                player1_total_cards += i + 1
                break
            # Directly check for Player 2's combinations in the sequence
            elif ''.join(sequence[-len(player2):]) == player2:
                # If Player 2 wins, add to their total tricks and cards
                if scoring_method == 'tricks':
                    player2_tricks += 1
                # Add the total cards won by Player 2
                player2_total_cards += i + 1
                break
        else:
            # If neither player wins, it's a draw
            draw += 1  

    # Now we need Player statistics from the games, based on scoring_method
    if scoring_method == 'tricks':
        total_tricks = player1_tricks + player2_tricks
        player2_win_prob = player2_tricks / total_tricks
        player1_win_prob = player1_tricks / total_tricks
        draw_prob = draw / total_tricks
    elif scoring_method == 'total_cards':
        total_cards = player1_total_cards + player2_total_cards
        player2_win_prob = player2_total_cards / total_cards
        player1_win_prob = player1_total_cards / total_cards
        draw_prob = draw / total_cards

    # Return results as a dictionary
    return {
        'prob_player2_win': player2_win_prob,
        'prob_player1_win': player1_win_prob,
        'prob_draw': draw_prob
    }

    
def simulate_games_for_all_combinations(decks: np.ndarray,
                   num_simulations: int = NUM_SIMULATIONS,
                   num_cards: int = NUM_CARDS
                  ):

    """
        We want to be able to simulate n number of games to
        verify our results and ensure that statistics for
        Penney's game are accurate for each 64-8=56 combinations

        Arguments:
            - decks: decks uploaded from file in data/ folder
            - num_simulations: number of simulations user wishes to compute
            - num_cards: 52 cards in one deck
    """
    
    # Create an empty dictionary to store scoring_method results from simulation
    results_tricks = {}
    results_total_cards = {}

    # Loop over Player1 and Player2's combinations
    for player1 in combinations:
        for player2 in combinations:
            # Make sure combinations are not the same
            if player1 != player2:
                # Create a key for the results dict, keep it consistent 
                key = f'{player1}_{player2}'
                
                # Track results from Penney_game() 'tricks'
                result_tricks = penney_game(player1, player2, decks, num_cards, num_simulations, scoring_method='tricks')
                results_tricks[key] = result_tricks
                
                # Track results from Penney_game() 'total_cards'
                result_total_cards = penney_game(player1, player2, decks, num_cards, num_simulations, scoring_method='total_cards')
                results_total_cards[key] = result_total_cards

    return results_tricks, results_total_cards


def statistics(filename: str,
               seed: int,
               num_simulations: int = NUM_SIMULATIONS, 
               num_cards: int = NUM_CARDS,
               scoring_method: str = 'tricks'
              ):
    
    """
        Now that we have n number of simulations for Penney's Game
        let's look at the statistics for the possible combinations
        of Player 2

        Arguments:
            - filename: filename in data/ folder with decks
            - seed: seed used for generating decks
            - num_simulations: number of simulations user wishes to compute
            - num_cards: 52 cards in one deck
            - scoring_method: can be 'tricks' or 'total_cards'
        
        Saves 
            - .npy file with Player statistics and seed in filename
    """

    # Load decks from file
    decks = load_file(filename)
    
    # Load the dictionaries from simulate_games_for_all_combinations
    results_tricks, results_total_cards = simulate_games_for_all_combinations(decks, num_simulations, num_cards)
    
    # Empty dictionary to hold statistics 
    stats_dict = {}

    # Select the correct results dictionary based on the scoring method
    if scoring_method == 'tricks':
        results = results_tricks
    elif scoring_method == 'total_cards':
        results = results_total_cards

    # Print a line for user to see probability statistics 
    # and how many simulations of which file
    print(f"Generating probabilities for {num_simulations} simulations of Penney's Game using '{filename}'")
   
    
    # Loop over Player1 and Player2's combinations
    for player1_comb in combinations:
        for player2_comb in combinations:
            # Avoid identical combinations
            if player1_comb == player2_comb: 
                continue

            key = f'{player1_comb}_{player2_comb}'
            # Player 2's win probability
            prob_p2_win = results[key]["prob_player2_win"]
            # Player 1's win probability
            prob_p1_win = results[key]["prob_player1_win"] 
            # Draw probability
            prob_draw = results[key]["prob_draw"] 

            # Store the statistics as a dictionary
            stats_dict[key] = {
                'prob_player2_win': prob_p2_win,
                'prob_player1_win': prob_p1_win,
                'prob_draw': prob_draw
            }

    # Create filename for statistics 
    stats_filename = f'data/decks_{seed}_{scoring_method}_probabilities.npy'

    # Save the file to the data/ folder
    np.save(stats_filename, stats_dict)

    # Alert the user that the statistics have been saved
    print(f"Statistics for seed {seed} have been saved to '{stats_filename}'")
