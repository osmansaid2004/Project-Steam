import requests

def Api_Call_Games(print_all=False):
    steamid = '76561198328287806'
    api_key = 'A3901F53D2D1F26049D9FF8C91E9BB78'
    params = {
        'key': api_key,
        'steamid': steamid,
        'format': 'json',
        'include_appinfo': 1
    }

    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if 'response' in data:
                games_data = data['response'].get('games', [])

                if not games_data:
                    print("No games data available.")
                    return

                sorted_games = sorted(games_data, key=lambda game: game.get('playtime_forever', 0), reverse=True)

                if print_all:
                    print("\nAll Played Games:")
                else:
                    print("\nTop 3 Most Played Games:")

                num_games_to_print = len(sorted_games) if print_all else min(3, len(sorted_games))

                for game in sorted_games[:num_games_to_print]:
                    app_id = game.get('appid', 'N/A')
                    name = game.get('name', 'N/A')
                    playtime = game.get('playtime_forever', 'N/A')

                    print(f"App ID: {app_id}, Name: {name}, Playtime: {int(playtime/60)} Hours")

            else:
                print("Response does not contain 'response' key.")

        else:
            print(f"API request failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")


Api_Call_Games()
Api_Call_Games(print_all=True)
