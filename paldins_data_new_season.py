import pandas as pd
import numpy as np
import os
import time

pd.set_option('display.max_columns', None)


def new_season_ingestion():
    opponents = pd.read_csv(
        f"C:/Users/E4D User/Documents/GitHub/Original/Nashville Paladins Data/extra_files/Opponents.csv")
    opponents['opponent'] = opponents['opponent'].astype('string')
    change_team_names = opponents['opponent'].str.split(' ', expand=True)
    change_team_names.columns = ['opp_id', 'opp_name']
    change_team_names = pd.DataFrame(change_team_names)
    opponents = pd.concat([change_team_names, opponents], axis=1).drop(['opponent', 'id'], axis=1)
    new_row = []
    new_season = pd.DataFrame()
    columns = ['season', 'game', 'opp_id', 'opp_name', 'home_away', 'talons_score', 'opp_score', 'conference',
               'division', 'city', 'state']

    data_path = f"C:/Users/E4D User/Documents/GitHub/Original/Nashville Paladins Data/" \
                f"Nashville Paladins 2020 Season.csv"
    modification_time = os.path.getmtime(data_path)
    print(f"This dataset was last updated: {time.ctime(modification_time)}")
    current_data = pd.read_csv(data_path)
    last_game = current_data.tail(1)
    last_game_num = current_data['game'].iloc[-1]
    next_game = last_game_num + 1
    print(last_game)
    print(last_game_num)
    remaining = 82 - last_game_num
    print(f"Games remaining: {remaining}")

    while True:
        # if the amount of games to be added is more than 82 (the games in the regular season)
        games = int(input("How many games are you inputting? "))
        game_index = np.arange(next_game, games + next_game)
        if game_index[-1] > 82 or games > 82:
            print(f"Based on number of games being added, the season will be {game_index[-1]} games\n"
                  f"which is longer than 82 games.\nPlease adjust the amount of games being added.")
        else:
            print(f"Last game to be input: {game_index[-1]}")
            break

    for i in game_index:
        print(f"Game {i}")
        input_opponent = input("Opponent Abbreviation: ").upper()

        def search(value):
            results = opponents[opponents['opp_id'].str.contains(value, case=False)]
            name = list(results['opp_name'])
            if len(name) == 0:
                raise ValueError("Did not find anything with that title.")
            elif len(name) > 1:
                raise ValueError("Found more than one opponent with that input.")
            return results

        opp_name = search(input_opponent)
        opp_name = opp_name.reset_index().drop('index', axis=1)
        opp_id = opp_name.at[0, columns[2]]
        opp_mascot = opp_name.at[0, columns[3]]
        conference = opp_name.at[0, columns[7]]
        division = opp_name.at[0, columns[8]]
        city = opp_name.at[0, columns[9]]
        state = opp_name.at[0, columns[10]]
        while True:
            home = "H"
            away = "A"
            home_away = input("Input H for Home game / A for Away: ").upper()
            if home_away == home or home_away == away:
                break
            else:
                print("Invalid input. Please enter H for Home game or A for Away game.")

        while True:
            print("Paladins Score: ")
            talons_score = int(input())
            print("Opponent Score: ")
            opp_score = int(input())
            if opp_score == talons_score:
                print("Opponent score cannot be the same oas the Talons Score")
            elif 300 > talons_score > 1 and 300 > opp_score > 1:
                break
            else:
                print("Invalid final scores. Please input scores for each team.")
        if home_away == "H":
            city = "Nashville"
            state = "Tennessee"
        new_row.append([2020, i, opp_id, opp_mascot, home_away, talons_score, opp_score, conference, division,
                        city, state])
        new_season = pd.DataFrame(new_row, columns=columns)

    return new_season


update_data = new_season_ingestion()
print(update_data)
while True:
    current_season = update_data['season'].unique()
    year = int(input("Please confirm the the year: "))
    if current_season == year:
        break
    else:
        print(f"The existing data has the season as: {current_season}.\n"
              f"Please verify the season before continuing.\n")

path = f"C:/Users/E4D User/Documents/GitHub/Original/Nashville Paladins Data/Nashville Paladins " \
       f"{year} Season.csv"

data = pd.read_csv(path)
data = pd.concat([data, update_data])
data.to_csv(path, index=False)

updated_time = os.path.getmtime(path)
print(f"File saved as Nashville Paladins {year} Season.csv was last updated: {time.ctime(updated_time)}")

save_correctly = pd.read_csv(path, index_col='season')
print(save_correctly.tail())
