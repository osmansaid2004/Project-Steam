from tkinter import *
import requests

API_KEY = 'A3901F53D2D1F26049D9FF8C91E9BB78'

# Steam_id = 76561199577191098 Van Soulaiman


def api_call_games(steam_id):
    params = {
        'key': API_KEY,
        'steamid': steam_id,
        'format': 'json',
        'include_appinfo': 1
    }

    url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if 'response' in data and 'games' in data['response']:
                games_list = data['response']['games']
                sorted_games = sorted(games_list, key=lambda game: game.get('playtime_forever', 0), reverse=True)
                most_played_game = sorted_games[0]

                return {
                    'games': sorted_games,
                    'most_played': most_played_game
                }

            else:
                print("No games found for the provided Steam ID.")
                return None

        else:
            print(f"API request failed with status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def api_call_player_info(steam_id):
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={steam_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        player_info = data['response']['players'][0]
        steam_id = player_info['steamid']
        persona_name = player_info['personaname']
        profile_url = player_info['profileurl']
        persona_state = player_info['personastate']

        if persona_state in range(5):
            persona_states = ["Offline", "Online", "Busy", "Away", "Snooze"]
            persona_state = persona_states[persona_state]

        return {
            'steam_id': steam_id,
            'persona_name': persona_name,
            'profile_url': profile_url,
            'persona_state': persona_state
        }

    else:
        print(f"Error: {response.status_code}")
        return None


def display_player_info_label(steam_id, dashboard_window):
    player_info = api_call_player_info(steam_id)

    if player_info:
        labels = [
            Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('NS Sans', 18, 'bold'),
                  text=f"Steam ID: {player_info['steam_id']}\n"),
            Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('NS Sans', 18, 'bold'),
                  text=f"Persona Name: {player_info['persona_name']}"),
            Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('NS Sans', 18, 'bold'),
                  text=f"Status: {player_info['persona_state']}")
        ]

        for index, label in enumerate(labels):
            label.place(y=100 + (index * 40), x=1080)
        label2 = Label(master=dashboard_window,
                       fg='#c7d5e0',
                       bg='#171a21',
                       font=('NS Sans', 40, 'bold'),
                       text=f"Welcome {player_info['persona_name']}'s Friend!")
        label2.place(y=20, x=20)


def naam_eerste_spel(steam_id, dashboard_window):
    data = api_call_games(steam_id)

    if data:
        most_played_name = data['most_played'].get('name', 'N/A')
        most_played_hours = data['most_played'].get('playtime_forever', 0) // 60

        label = Label(master=dashboard_window,
                      fg='#c7d5e0',
                      bg='#171a21',
                      font=('NS Sans', 18, 'bold'),
                      text=f"Most Played Game: {most_played_name}")
        label.place(y=420, x=1050)

        label_2_time = Label(master=dashboard_window,
                             fg='#c7d5e0',
                             bg='#171a21',
                             font=('NS Sans', 18, 'bold'),
                             text=f"Played: {most_played_hours} hours")
        label_2_time.place(y=700, x=1050)


def gui_dashboard(steam_id):
    global persona_name
    global player_info
    dashboard_scherm = Tk()
    dashboard_scherm.geometry("1500x1500")
    dashboard_scherm.title(f"Dashboard Steam friends ")
    dashboard_scherm.config(background='#171a21')




    display_player_info_label(steam_id, dashboard_scherm)
    naam_eerste_spel(steam_id, dashboard_scherm)

    dashboard_scherm.mainloop()


def get_steam_id(entry_widget, window):
    steam_id = entry_widget.get()
    if steam_id:
        window.destroy()
        gui_dashboard(steam_id)


def input_steam_id_window():
    input_window = Tk()
    input_window.title("Enter Steam ID")

    label = Label(input_window, text="Enter Steam ID:")
    label.pack(pady=10)

    entry = Entry(input_window)
    entry.pack(pady=10)

    submit_button = Button(input_window, text="Submit", command=lambda: get_steam_id(entry, input_window))
    submit_button.pack(pady=10)

    input_window.mainloop()


input_steam_id_window()