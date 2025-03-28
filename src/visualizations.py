import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Import get_total_decks from datagen.py
from src.datagen import get_total_decks


def load_file(filename: str):

    """
        User gives the filename and the function returns 
        the loaded probabilities if they exist
    """
    
    # Check to see if file exists and return it
    if os.path.exists(filename):
        return np.load(filename, allow_pickle = True).item()

    # If file does not exist, let the user know
    else:
        print(f'File "{filename}" does not exist. Try another file.')


def npy_to_dataframe(filename) -> pd.DataFrame:
    
    """
        Load a .npy file and convert it into a Pandas DataFrame
        so that the data can be easily uploaded into the heatmap
    
        Arguments:
            -filename (str): The path to the .npy file to be loaded

        Returns:
            -pd.DataFrame: A DataFrame containing the data from the 
            decks_seed_probabilities.npy file
    """
    
    # Load the .npy file
    data = load_file(filename)
    
    # Create an empty list to hold the data for the DataFrame
    data_list = []

    # Loop through the dictionary to convert it to a DataFrame
    for key, value in data.items():
        row = {
               'key': key,
               'prob_player2_win': value.get('prob_player2_win', 0),
               'prob_player1_win': value.get('prob_player1_win', 0),
               'prob_draw': value.get('prob_draw', 0)
              }
        # Append the rows to the list
        data_list.append(row)

    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(data_list)

    # Split the key, key currently in (player1_comb, player2_comb) format
    df[['player1_comb', 'player2_comb']] = df['key'].str.split('_', expand=True)

    # Drop the key, since we have player1_comb and player2_comb column 
    df = df.drop('key', axis=1)

    # Convert the statistical columns to percentages
    df[['prob_player1_win', 'prob_player2_win', 'prob_draw']] = (df[['prob_player1_win', 'prob_player2_win', 'prob_draw']] * 100).astype(int)

    # Add the draw probabilities to the player1 and player2 win probabilities
    df['prob_player1_win_(draw)'] = df['prob_player1_win'].astype(str) + '(' + df['prob_draw'].astype(str) + ')'
    df['prob_player2_win_(draw)'] = df['prob_player2_win'].astype(str) + '(' + df['prob_draw'].astype(str) + ')'


    return df

def generate_heatmap_from_df(df, decks_filename: str, heatmap_filename: str):
    
    """
        Generate a heatmap using a DataFrame containing combinations and probabilities.
    
        Arguments:
            -df: The DataFrame with player1_comb, player2_comb, and probabilities.
            -decks_filename (str): The filename of the .npy file containing the decks.
            -heatmap_filename (str): The filename to save the heatmap image as.
    
    """

    # Create pivot tables for Player 1 and Player 2 win probabilities
    heatmap_data_player2 = df.pivot(index='player1_comb', 
                                    columns='player2_comb', 
                                    values='prob_player2_win')
    heatmap_data_player1 = df.pivot(index='player2_comb', 
                                    columns='player1_comb', 
                                    values='prob_player1_win')
  
    # Annotations for the heatmap
    annot_data = df.pivot(index='player1_comb', 
                          columns='player2_comb', 
                          values='prob_player2_win_(draw)'
                          )

    # Create a combined matrix for Player 1 and Player 2 probabilities
    num_rows = len(heatmap_data_player2.index)
    num_cols = len(heatmap_data_player2.columns)

    # Create a zero matrix of the same size as the heatmap data
    combined_matrix = np.zeros((num_rows, num_cols))

    # Loop through the lower triangle and fill with Player 2's probabilities
    for i in range(num_rows):
        # Include the diagonal 
        for j in range(i+1):  
            # Fill the lower triangle with Player 2's probabilities
            combined_matrix[i, j] = heatmap_data_player2.iloc[i, j]

    # Loop through the upper triangle and fill with Player 1's probabilities
    for i in range(num_rows):
        # Start from above the diagonal 
        for j in range(i+1, num_cols):  
            # Fill the upper triangle with Player 1's probabilities
            combined_matrix[i, j] = heatmap_data_player1.iloc[i, j]

    # Create a DataFrame from the combined matrix
    combined_matrix_df = pd.DataFrame(combined_matrix, 
                                      index=heatmap_data_player2.index, 
                                      columns=heatmap_data_player2.columns)

    # Count the number of decks used to add to heatmap title
    num_decks = get_total_decks(decks_filename)

    # Plot the heatmap
    plt.figure(figsize=(10, 8))

    # Change heatmap features for readability and organization 
    sns.heatmap(combined_matrix_df, 
                annot=annot_data, 
                cmap='Blues', 
                fmt='', 
                cbar=False, 
                annot_kws={'fontsize':12})

    # Labels and title
    plt.title(f"My Chance of Win(Draw)\n({num_decks} Decks)", fontsize=16)
    plt.xlabel("My Choice")
    plt.ylabel("Opponent Choice")
    plt.yticks(rotation=0)
    
    # Save the heatmap image in the 'figures' folder
    save_path = os.path.join('figures', heatmap_filename)
        
    # Save the figure automatically to the figures folder
    plt.savefig(save_path)
    print(f"Heatmap saved as {save_path}")

    # Show the heatmap
    plt.show()
