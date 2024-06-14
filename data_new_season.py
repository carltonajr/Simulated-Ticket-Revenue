import pandas as pd
import numpy as np
import os
import time
# importing Tkinter
import tkinter as tk
# importing Themed Tkinter
from tkinter import ttk

pd.set_option('display.max_columns', None)


def authenticate():
    # Define your secure username and PIN
    logins = pd.read_csv("C:/Users/E4D User/Documents/GitHub/Original/Charlotte Talons Data/db files/logins.csv",
                         index_col='ID')
    secure_pin = 2564
    run = True
    count = 0
    while run:
        # Ask the user for username
        username_input = input("Please enter your username: ")
        username_results = logins[logins['user'] == username_input]
        usernames = list(username_results['user'])

        if len(usernames) == 1:
            password = usernames = list(username_results['password'])
            password_input = input("Please enter your password: ")
            if password_input != password[0]:
                print("Unable to login, please see try again or admin for assistance.")
            else:
                print("Access granted! Welcome, {}.".format(username_input))
                break
        else:
            print("Username not found, please input again")
    #     print("Please input a value to continue to the next step:\n\n"
    #           "1 - New Data Entry\n"
    #           "2 - Season Analysis\n"
    #           "3 - Sample Predictions")
    #     while run:
    #         next_task = int(input("Input: "))
    #
    #         if isinstance(next_task, int):
    #             print(next_task)
    #             break
    #         else:
    #             print("Answer provided was not acceptable.\n")


# Example usage:
authenticate()


# Function for adding to the dataset
def new_season_ingestion():
    # Read the Opponents CSV
    opponents = pd.read_csv(
        f"")
    # Update the 'opponent' column to string values
    opponents['opponent'] = opponents['opponent'].astype('string')
    # Split the values in the 'opponent' column, creating a new column
    change_team_names = opponents['opponent'].str.split(' ', expand=True)
    # Rename columns in to 'opp_id' and 'opp_name'
    change_team_names.columns = ['opp_id', 'opp_name']
    # Create a dataframe then add 'change_team_names' and drop the 'opponent' and 'id' columns
    change_team_names = pd.DataFrame(change_team_names)
    opponents = pd.concat([change_team_names, opponents], axis=1).drop(['opponent', 'id'], axis=1)

    # Create 'new_row' for each row we add and 'new_season' for a complete dataframe to merge with existing data
    new_row = []
    new_season = pd.DataFrame()
    # Columns for new_season
    columns = ['season', 'game', 'opp_id', 'opp_name', 'home_away', 'talons_score', 'opp_score', 'conference',
               'division', 'city', 'state']
    # Data Path
    data_path = f""
    # "DataFrame that contains the most current data file"
    current_data = pd.read_csv(data_path)
    # Pulls the last row from 'current_data'
    last_game = current_data.tail(1)
    # Pulls specifically the 'game' number from the last row of 'current_data'
    last_game_num = current_data['game'].iloc[-1]
    # Adds one to the last game number selected
    next_game = last_game_num + 1
    # While statement to pull the next file needing to be updated
    while True:
        if last_game_num == 82:
            # if last_game_num is 82, pull the season of the data file selected and print message
            last_season = int(current_data['season'].unique())
            season = last_season + 1
            print(f"All 82 games for the {last_season} season have been added. Loading data for the {season} season.")
            data_path = f""
            # "Pulls the next most current data file based on the season
            # continue process until 'last_game_num' is not 82"
            current_data = pd.read_csv(data_path)
            last_game = current_data.tail(1)
            last_game_num = current_data['game'].iloc[-1]
            next_game = last_game_num + 1
            continue

        else:
            # Break from while statement once 'last_game_num' is not 82
            break
    # Calculate how many games are left in the selected season
    remaining = 82 - last_game_num

    # Verify you are about to update data in the correct season
    season = int(input("Please enter the season your are updating: "))
    print(f"Games remaining: {remaining}")

    # Prints the last row of data from the selected file
    print(last_game)
    # Print out the last time the file was updated.
    modification_time = os.path.getmtime(data_path)
    print(f"This dataset was last updated: {time.ctime(modification_time)}")

    while True:
        # if the amount of games to be added is more than 82 (the games in the regular season) do not continue
        games = int(input("How many games are you inputting? "))
        game_index = np.arange(next_game, games + next_game)
        if game_index[-1] > 82 or games > 82:
            print(f"Based on number of games being added, the season will be {game_index[-1]} games\n"
                  f"which is longer than 82 games.\nPlease adjust the amount of games being added.")
        else:
            print(f"Last game to be input: {game_index[-1]}")
            break

    for i in game_index:
        # 1st input for the opponent information
        print(f"Game {i}")
        input_opponent = input("Opponent Abbreviation: ").upper()

        # Search for opponent's data using the above user input
        def search(value):
            results = opponents[opponents['opp_id'].str.contains(value, case=False)]
            name = list(results['opp_name'])
            if len(name) == 0:
                raise ValueError("Did not find anything with that title.")
            elif len(name) > 1:
                raise ValueError("Found more than one opponent with that input.")
            return results

        # Pull data from found opponent data and plug in appropriate slots
        opp_name = search(input_opponent)
        opp_name = opp_name.reset_index().drop('index', axis=1)
        opp_id = opp_name.at[0, columns[2]]
        opp_mascot = opp_name.at[0, columns[3]]
        conference = opp_name.at[0, columns[7]]
        division = opp_name.at[0, columns[8]]
        city = opp_name.at[0, columns[9]]
        state = opp_name.at[0, columns[10]]

        while True:
            # Game location input home or away game
            home = "H"
            away = "A"
            home_away = input("Input H for Home game / A for Away: ").upper()
            if home_away == home or home_away == away:
                break
            else:
                # Do not advance until the input fulfills the break above
                print("Invalid input. Please enter H for Home game or A for Away game.")

        while True:
            # Game score input
            print("Paladins Score: ")
            talons_score = int(input())
            print("Opponent Score: ")
            opp_score = int(input())
            # Conditionals for scores
            if opp_score == talons_score:
                print("Opponent score cannot be the same as the Talons Score")
            # if both 'talons_score' and 'opp_score' is within range, break to the next portion
            elif 300 > talons_score > 1 and 300 > opp_score > 1:
                break
            else:
                print("Invalid final scores. Please input scores for each team.")
        # if the user team is the home team set to a specific location
        if home_away == "H":
            city = "Nashville"
            state = "Tennessee"
        # insert the data into 'new_row'
        new_row.append([season, i, opp_id, opp_mascot, home_away, talons_score, opp_score, conference, division,
                        city, state])
        # insert all the new_row inputs into DataFrame 'new_season'
        new_season = pd.DataFrame(new_row, columns=columns)
    # return the dataframe
    return new_season


# A GUI to view the new data in a separate window:
# function for when user clicks the button on the pop-up window
def on_button_click(new_data):
    # message in the original pop-up window once the button is clicked
    label.config(text="Data Loaded!")

    # Upload the DataFrame
    df = new_data

    # Create a new window to display the DataFrame
    df_window = tk.Toplevel(run_it)
    # give the new window a title to display
    df_window.title("Sample DataFrame")

    # Create a Treeview widget to display the DataFrame
    tree = ttk.Treeview(df_window, columns=list(df.columns), show='headings')

    # Add columns to the Treeview
    for col in df.columns:
        # set the column heading text for the specified column
        tree.heading(col, text=col)
        # centering the text in each column
        tree.column(col, anchor='center')

    # Insert data into the Treeview
    for i, row in df.iterrows():
        # insert a new row at the end of values of list 'row'
        tree.insert("", "end", values=list(row))

    # create a vertical scrollbar widget
    vsb = ttk.Scrollbar(df_window, orient="vertical", command=tree.yview)
    # Enable the scrollbar, positioned above the data here to ensure the
    # scrollbar will be at the side of the data shown
    tree.configure(yscrollcommand=vsb.set)

    # display the scrollbar
    vsb.pack(side="right", fill="y")
    # display the Treeview
    tree.pack(fill='y', expand=True, padx=5, pady=10)


# Run the function to create and populate the variable 'update_data'
update_data = new_season_ingestion()

# while statement to verify the season being updated is the season input.
while True:
    current_season = update_data['season'].unique()
    year = int(input("Please confirm the the year: "))
    if current_season == year:
        break
    else:
        print(f"The existing data has the season as: {current_season}.\n"
              f"Please verify the season before continuing.\n")


path = f""


# Initialize the GUI should the user want to see the complete additions
# Create the main window
run_it = tk.Tk()
# Title for main window
run_it.title("Recent Updates")

# Create a label
label = tk.Label(run_it, text="Data Window")
# display the label with 10 pixels of padding
label2 = tk.Label(run_it, text=f"\nLast Updated - {time.ctime(os.path.getmtime(path))}")
label.pack(pady=10)
label2.pack(pady=15)

# Create a button to open the stored data
button = tk.Button(run_it, text="Click to Show DataFrame", command=f"{on_button_click(update_data)}")
# display the button with 10 pixels of padding
button.pack(pady=10)

# Start the Tkinter event loop
# run_it.mainloop()

# Complete the update by loading the current data file and concatenate the new data and save the one complete file
data = pd.read_csv(path)
data = pd.concat([data, update_data])
data.to_csv(path, index=False)

# Verify the save occurred correctly by viewing the message with the most recent 'Time Modified' for the file
updated_time = os.path.getmtime(path)
print(f"File saved as Nashville Paladins {year} Season.csv was last updated: {time.ctime(updated_time)}")

# View the newly updated file, having 'season' as the index column
save_correctly = pd.read_csv(path, index_col='season')
print(save_correctly.tail())
