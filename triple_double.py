import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

def get_player_triple_double_report(player_name, season, season_type):
    # Find the ID of the player in the NBA API
    player_dict = players.get_players()
    players_df = pd.DataFrame(player_dict)
    try:
        player_id = players_df.loc[players_df['full_name'] == player_name, 'id'].item()
        # Create an instance of the PlayerGameLog object
        player_game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season,
            season_type_all_star=season_type
        )
        games_data = player_game_log.get_data_frames()[0]
        
        # Create a boolean column to check if there was a triple double
        stats = ['REB', 'AST', 'STL', 'BLK', 'PTS']
        games_data['TRIP_DOUB'] = (games_data[stats] >= 10).sum(1) == 3

        # Generate the report
        report = "-----------TRIPLE-DOUBLE REPORT " + player_name.upper() + "-----------\n\n"
        report += "Total of Triple-Doubles: " + str(games_data['TRIP_DOUB'].sum()) + "\n"
        report += "Total of games: " + str(len(games_data)) + "\n"
        report += "Percentage of Triple-Doubles: " + str(round(games_data['TRIP_DOUB'].sum()*100 / len(games_data), 2)) + "%\n"
        report += "Avg of Points: " + str(round(games_data['PTS'].mean(), 2)) + "\n"
        report += "Avg of Rebounds: " + str(round(games_data['REB'].mean(), 2)) + "\n"
        report += "Avg of Assists: " + str(round(games_data['AST'].mean(), 2)) + "\n"
        report += "Avg of Steals: " + str(round(games_data['STL'].mean(), 2)) + "\n"
        report += "Avg of Blocks: " + str(round(games_data['BLK'].mean(), 2)) + "\n"
        return print(report)
    except:
        return print("Invalid Parameters\
            (Player or Season or Season_Type).Please try again!")
        
