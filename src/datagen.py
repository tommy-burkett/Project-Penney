import numpy as np
import os
from src.helpers import PATH_DATA

# half_deck_size to simulate black and red cards
HALF_DECK_SIZE = 26


def get_decks(n_decks: int, 
              seed: int,
              half_deck_size: int = HALF_DECK_SIZE
             ) -> tuple[np.ndarray, np.ndarray]:
    
    """
        Efficiently generate `n_decks` shuffled decks using NumPy.
    
        Returns:
            decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
            each row is a shuffled deck.

    """
    
    init_deck = [0]*half_deck_size + [1]*half_deck_size  # Base deck
    decks = np.tile(init_deck, (n_decks, 1))
    rng = np.random.default_rng(seed)
    rng.permuted(decks, axis=1, out=decks)
    
    return decks


def store_data(n_decks: int,
               seed: int,
               half_deck_size: int = HALF_DECK_SIZE, 
              ):
    """
        Generate decks from get_decks() and store 
        generated decks in a .npy file with their seed

        Have to check and see if that file already
        exists so we can append the new decks, or
        create the new file with a new seed and decks
    """
    
    # Generating decks to store
    decks = get_decks(n_decks, 
                      seed,
                      half_deck_size, 
                      )
    
    # Create the filename
    filename = f'data/decks_{seed}.npy'

    # Check to see if the file exists already in order to generate more decks
    if os.path.exists(filename):
        # load file with decks
        load_decks = np.load(filename)
        
        # add new decks to existing file
        # documentation for np.concatenate
        #https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html
        add_decks = np.concatenate((load_decks, decks))

        # save file with new decks
        np.save(filename, add_decks)

    # Save the filename and decks if filename does not exist yet
    else:
        np.save(filename, decks)

