from datetime import datetime

def calculate_true_shooting(fg2_attempted, fg2_made, fg3_attempted, fg3_made, ft_attempted, ft_made):
    # True Shooting % formula
    points = 2 * fg2_made + 3 * fg3_made + ft_made
    total_shots = 2 * fg2_attempted + fg3_attempted + 0.44 * ft_attempted
    if total_shots == 0:
        return 0
    return (points / (2 * total_shots)) * 100

def find_qualified_games(game_data: list[dict], true_shooting_cutoff: int, player_count: int) -> list[int]:
    qualified_games = {}

    for game in game_data:
        gameID = game['gameID']
        ts_percentage = calculate_true_shooting(
            game['fieldGoal2Attempted'], game['fieldGoal2Made'],
            game['fieldGoal3Attempted'], game['fieldGoal3Made'],
            game['freeThrowAttempted'], game['freeThrowMade']
        )
        if ts_percentage >= true_shooting_cutoff:
            if gameID not in qualified_games:
                qualified_games[gameID] = 0
            qualified_games[gameID] += 1
    
    result = [
        gameID for gameID, count in qualified_games.items() 
        if count >= player_count
    ]

    # Sort by gameDate in descending order
    result.sort(key=lambda gameID: max(
        datetime.strptime(game['gameDate'], '%m/%d/%Y') 
        for game in game_data if game['gameID'] == gameID
    ), reverse=True)

    return result

