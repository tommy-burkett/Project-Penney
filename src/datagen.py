import numpy as np
import os
import glob
from src.helpers import PATH_DATA

# HALF_DECK_SIZE to simulate black and red cards
HALF_DECK_SIZE = 26

# Maximum number of decks per file (GitHub limit)
MAX_DECKS_PER_FILE = 100000


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

def get_total_decks(filenames: str) -> int:
    
    """
        Retrieve the total number of decks from the saved .npy file.
        Number will be later used in visualizations.py to generate the heatmap.
    """

    # Grab all files that match the pattern
    filenames = glob.glob(filenames)

    # Initialize the total number of decks
    total_decks = 0

    # Loop over all of the files with the pattern
    for file in filenames:
        if os.path.exists(file):
            decks = np.load(file)
            # Return the total number of decks
            total_decks += len(decks)  
        else:
            print(f"File {file} not found.")
    return total_decks


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
    
    # Generate decks
    decks = get_decks(n_decks, seed, half_deck_size)

    # Determine how many files are needed
    num_files = (n_decks // MAX_DECKS_PER_FILE) + (1 if n_decks % MAX_DECKS_PER_FILE != 0 else 0)

    # Create and save the decks in chunks of MAX_DECKS_PER_FILE
    for i in range(num_files):
        # Start and end index for chunks
        start_idx = i * MAX_DECKS_PER_FILE
        end_idx = min((i + 1) * MAX_DECKS_PER_FILE, n_decks)
        
        # Get the chunk
        chunk = decks[start_idx:end_idx]

        # Create the filename based on the chunk number
        filename = f'data/decks_{seed}.{i + 1}.npy'

        # Check if the file already exists
        if os.path.exists(filename):
            # Load existing decks
            existing_decks = np.load(filename)
            # Concatenate new decks with the existing ones
            chunk = np.concatenate((existing_decks, chunk))
        
        # Save the chunk
        np.save(filename, chunk)
        print(f"Saved {filename} with {chunk.shape[0]} decks.")