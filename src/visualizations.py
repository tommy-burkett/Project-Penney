import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


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

    return df


def generate_heatmap_from_df(df, prob_column='prob_player2_win'):
    
    """
        Generate a heatmap using a DataFrame containing combinations and probabilities.
    
        Arguments:
            -df: The DataFrame with player1_comb, player2_comb, and probabilities.
            -prob_column: The column containing the probabilities for Player 2's win.
    
    """
    
    # Pivot the DataFrame so that player1_comb are rows and player2_comb are columns
    # (this essentially creates a correlation matrix)
    heatmap_data = df.pivot(index='player1_comb', columns='player2_comb', values=prob_column)
    
    # Plot the heatmap
    plt.figure(figsize=(10, 8))

    # Change heatmap features for readability and organization 
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt='.2f', cbar=True, annot_kws={'fontsize':12})
    
    # Labels and title
    plt.title(f"Heatmap of Player 2's Win Probability")
    plt.xlabel("Player 2 Combinations")
    plt.ylabel("Player 1 Combinations")
    
    # Show the heatmap
    plt.show()
