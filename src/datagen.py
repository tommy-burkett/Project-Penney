'''
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

def get_total_decks(filename: str) -> int:
    """
        Retrieve the total number of decks from the saved .npy file.
        Number will be later used in visualizations.py 
    """
    if os.path.exists(filename):
        decks = np.load(filename)
        return len(decks)  # Return the total number of decks
    else:
        print(f"File {filename} not found.")
        return 0


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
'''
import numpy as np
import os

# Constants
HALF_DECK_SIZE = 26
MAX_DECKS_PER_FILE = 100000  # Maximum decks per .npy file

def get_decks(n_decks: int, seed: int, half_deck_size: int = HALF_DECK_SIZE) -> np.ndarray:
    """
    Efficiently generate `n_decks` shuffled decks using NumPy.
    
    Returns:
        decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
        each row is a shuffled deck.
    """
    init_deck = [0] * half_deck_size + [1] * half_deck_size  # Base deck
    decks = np.tile(init_deck, (n_decks, 1))
    rng = np.random.default_rng(seed)
    rng.permuted(decks, axis=1, out=decks)
    return decks

def store_data(n_decks: int, seed: int, half_deck_size: int = HALF_DECK_SIZE):
    """
    Generate decks from get_decks() and store them in .npy files, ensuring each file has no more than 
    MAX_DECKS_PER_FILE decks.

    If the file already exists, new decks are appended to the existing file.
    """
    # Generate decks
    decks = get_decks(n_decks, seed, half_deck_size)

    # Determine how many files are needed
    num_files = (n_decks // MAX_DECKS_PER_FILE) + (1 if n_decks % MAX_DECKS_PER_FILE != 0 else 0)

    # Create and save the decks in chunks of MAX_DECKS_PER_FILE
    for i in range(num_files):
        start_idx = i * MAX_DECKS_PER_FILE
        end_idx = min((i + 1) * MAX_DECKS_PER_FILE, n_decks)
        
        chunk = decks[start_idx:end_idx]

        # Create the filename based on the chunk number
        filename = f'data/decks_{seed}_{i + 1}.npy'

        if os.path.exists(filename):
            # Load existing decks
            existing_decks = np.load(filename)
            # Concatenate new decks with the existing ones
            chunk = np.concatenate((existing_decks, chunk))
        
        # Save the chunk
        np.save(filename, chunk)
        print(f"Saved {filename} with {chunk.shape[0]} decks.")

def get_total_decks(filename: str) -> int:
    """
    Retrieve the total number of decks from the saved .npy file.
    """
    if os.path.exists(filename):
        decks = np.load(filename)
        return len(decks)  # Return the total number of decks
    else:
        print(f"File {filename} not found.")
        return 0
