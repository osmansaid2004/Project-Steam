from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from io import BytesIO
import numpy as np
from datetime import datetime

# HERINNERING ---- behoud variabele in het engels
API_KEY = 'A3901F53D2D1F26049D9FF8C91E9BB78'


# Call info van de games die de gebruiker speelt
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
                sorted_games = custom_sort(games_list)
                most_played_game = sorted_games[0]

                return {
                    'games': sorted_games,
                    'most_played': most_played_game,
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


# Functie om de gradient descent te berekenen
def gradient_descent(x, y, num_iterations=1000, learning_rate=0.0001):
    coefficients = [0, 0]

    for _ in range(num_iterations):
        for i in range(len(x)):
            prediction = coefficients[0] + coefficients[1] * x[i]
            error = prediction - y[i]
            coefficients[0] -= error * learning_rate
            coefficients[1] -= error * x[i] * learning_rate

    return coefficients


# Hier roepen we de player info op
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
        avatar = player_info['avatar']
        lastlogoff = player_info['lastlogoff']

        lastlogoff_unix = player_info['lastlogoff']
        lastlogoff = datetime.utcfromtimestamp(lastlogoff_unix).strftime('%Y-%m-%d %H:%M')

        if persona_state in range(5):
            persona_states = ["Offline", "Online", "Busy", "Away", "Snooze"]
            persona_state = persona_states[persona_state]

        gameextrainfo = player_info.get('gameextrainfo', 'Nothing')

        return {
            'steam_id': steam_id,
            'persona_name': persona_name,
            'profile_url': profile_url,
            'persona_state': persona_state,
            'avatar': avatar,
            'lastlogoff': lastlogoff,
            'gameextrainfo': gameextrainfo
        }

    else:
        print(f"Error: {response.status_code}")
        return None


def display_player_info_label(steam_id, dashboard_window):
    player_info = api_call_player_info(steam_id)

    if player_info:
        labels = [
            Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('Helvetica', 18, 'bold'),
                  text=f"Status: {player_info['persona_state']}"),
            Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('Helvetica', 18, 'bold'),
                  text=f"Last seen: {player_info['lastlogoff']}")
        ]

        if player_info.get('gameextrainfo'):
            labels.append(Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('NS Sans', 18, 'bold'),
                                text=f"playing: {player_info['gameextrainfo']}"))
        else:
            labels.append(Label(master=dashboard_window, fg='#c7d5e0', bg='#171a21', font=('NS Sans', 18, 'bold'),
                                text="playing: N/A"))

        for index, label in enumerate(labels):
            label.place(y=130 + (index * 40), x=20)

        welcome_label = Label(master=dashboard_window,
                              fg='#c7d5e0',
                              bg='#171a21',
                              font=('Helvetica', 30, 'bold'),
                              text=f"Welcome {player_info['persona_name']}'s Friend!")
        welcome_label.place(y=40, x=140)
        display_avatar(player_info['avatar'], dashboard_window)


def display_avatar(avatar_url, dashboard_window):
    response = requests.get(avatar_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.resize((80, 80))
        img = ImageTk.PhotoImage(img)

        avatar_label = Label(dashboard_window, image=img)
        avatar_label.image = img
        avatar_label.place(y=20, x=20)
    else:
        print("Failed to fetch the avatar image")


# functie om de meest gespeelde game te krijgen en de tijd
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
        label.place(y=150, x=1030)

        label_2_time = Label(master=dashboard_window,
                             fg='#c7d5e0',
                             bg='#171a21',
                             font=('NS Sans', 18, 'bold'),
                             text=f"Played a total of: {most_played_hours} hours")
        label_2_time.place(y=320, x=1030)

        img_url = f"http://media.steampowered.com/steamcommunity/public/images/apps/{data['most_played']['appid']}/{data['most_played']['img_icon_url']}.jpg"
        display_game_image(img_url, dashboard_window)

        top_3_games = data['games'][:3]
        display_charts(top_3_games, dashboard_window)

        for game in top_3_games:
            app_id = game.get('appid', None)
            if app_id:
                display_game_achievements(steam_id, top_3_games, dashboard_window)


def display_game_image(img_url, dashboard_window):
    response = requests.get(img_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.resize((70, 70))
        img = ImageTk.PhotoImage(img)

        game_image_label = Label(dashboard_window, image=img)
        game_image_label.image = img
        game_image_label.place(x=1100, y=215)
    else:
        print("Failed to fetch the game icon")


# Hier word een cirkeldiagram met percentages gemaakt om te laten zien hoe veel de top 3 games worden gespeeld
def display_charts(games, dashboard_window):
    plt.clf()
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    game_names = [game.get('name', 'N/A') for game in games]
    playtimes = [game.get('playtime_forever', 0) / 60 for game in games]
    label = Label(dashboard_window, text='Top 3 Most played games', bg='#171a21', fg='#c7d5e0',
                  font=('NS Sans', 14, 'bold'))
    label.place(x=140, y=379)

    label_colors = ['#c7d5e0', '#c7d5e0', '#c7d5e0']

    wedges, texts, autotexts = ax.pie(playtimes, labels=game_names, autopct=lambda p: '{:.1f}%'.format(p),
                                      startangle=90,
                                      colors=['#1b2838', 'skyblue', '#2a475e'])

    for text, autotext, color in zip(texts, autotexts, label_colors):
        text.set_color(color)
        text.set_fontsize(8)
        autotext.set_color('white')
        autotext.set_fontsize(8)

    ax.axis('equal')
    fig.patch.set_facecolor('#171a21')

    canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=-20, y=404)

    canvas.draw_idle()


def api_call_game_achievements(steam_id, app_id):
    url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={API_KEY}&steamid={steam_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if 'playerstats' in data and 'achievements' in data['playerstats']:
            return data['playerstats']['achievements']
            return len([achievement for achievement in data['playerstats']['achievements'] if
                        achievement.get('achieved', 0) == 1])

    print(f"Error fetching achievements for app_id {app_id}")
    return None


def sort_by_playtime(game):
    return game.get('playtime_forever', 0)


# Eigen simpele sorteer functie gemaakt voor het sorteren van de games
def custom_sort(games):
    for i in range(len(games)):
        for j in range(i + 1, len(games)):
            if sort_by_playtime(games[j]) > sort_by_playtime(games[i]):
                games[i], games[j] = games[j], games[i]
    return games


# Functie om de aantal achievements te krijgen en te zetten in een staafdiagram
def display_game_achievements(steam_id, games, dashboard_window):
    top_games = custom_sort(games)[:3]

    game_names = [game.get('name', 'N/A') for game in top_games]
    achievements_counts = []

    for game in top_games:
        app_id = game.get('appid', None)
        achievements = api_call_game_achievements(steam_id, app_id) or []
        achievements_count = sum(achievement['achieved'] for achievement in achievements)
        achievements_counts.append(achievements_count)

    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#171a21')

    bars = ax.bar(game_names, achievements_counts, color='skyblue')

    for bar, count in zip(bars, achievements_counts):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, count, ha='center', va='bottom', color='#c7d5e0',
                fontweight='bold')

    ax.set_ylabel('Number of Achievements Earned', color='#c7d5e0')
    ax.set_title('Number of Achievements Earned for Top 3 Games',
                 fontdict={'fontname': 'NS Sans', 'size': 11, 'weight': 'bold'})

    ax.patch.set_facecolor('#171a21')
    ax.tick_params(axis='both', colors='#c7d5e0')
    ax.title.set_color('#c7d5e0')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=970, y=375)

    canvas.draw_idle()


# Api call van de meest recente gespeelde games
def api_call_recently_played(steam_id):
    API_KEY = 'A3901F53D2D1F26049D9FF8C91E9BB78'
    url = f'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={API_KEY}&steamid={steam_id}'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            if games:
                most_recent_game = games[0]
                app_id = most_recent_game['appid']
                name = most_recent_game['name']
                icon_hash = most_recent_game['img_icon_url']
                icon_url = f'http://media.steampowered.com/steamcommunity/public/images/apps/{app_id}/{icon_hash}.jpg'
                return name, icon_url
            else:
                return "No recently played games found."
        else:
            print("Failed to fetch recently played games.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def display_recently_played_game(steam_id, dashboard_window):
    game_info = api_call_recently_played(steam_id)

    if game_info:
        game_name, game_icon_url = game_info

        game_label = Label(dashboard_window, text=f"Recently Played: {game_name}", bg='#171a21', fg='#c7d5e0',
                           font=('NS Sans', 18, 'bold'))
        game_label.place(x=20, y=250)

        display_game_icon(game_icon_url, game_name, dashboard_window)


def display_game_icon(icon_url, game_name, dashboard_window):
    response = requests.get(icon_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.resize((30, 30))
        img = ImageTk.PhotoImage(img)
        # Formule voor het berekenen van de coördinaten gebaseerd op de lengte van de naam van het spel
        x_coordinaat = 335 + (len(game_name) - 8) * 15

        icon_label = Label(dashboard_window, image=img)
        icon_label.image = img
        icon_label.place(x=x_coordinaat, y=250)
    else:
        print("Failed to get the game icon")


# Hier word de functie gradient descent gebruik om de aantal behaalde achievements en uren in een statistiek te zetten
def display_linear_regression(steam_id, dashboard_window):
    data = api_call_games(steam_id)
    # Hier maak ik een lege lijst van de playtimes en achievements
    if data:
        playtime_list = []
        achievements_list = []

        for game in data['games']:
            playtime_hours = game.get('playtime_forever', 0) / 60
            achievements_data = api_call_game_achievements(steam_id, game.get('appid', None)) or []
            achieved_achievements = [achievement for achievement in achievements_data if
                                     achievement.get('achieved', 0) == 1]
            achievements_count = len(achieved_achievements)

            playtime_list.append(playtime_hours)
            achievements_list.append(achievements_count)

        coefficients = gradient_descent(playtime_list, achievements_list)

        fig, ax = plt.subplots(figsize=(4.5, 4))

        scatter = ax.scatter(playtime_list, achievements_list, color='#c7d5e0', label='Games', edgecolor='#171a21',
                             marker='o')

        # Hier worden de puntjes en lijn gemaakt
        ax.plot(playtime_list, [coefficients[0] + coefficients[1] * hours for hours in playtime_list], color='#171a21',
                linewidth=2,
                label='Linear Regression')

        ax.set_title('Linear Regression: Playtime vs Achievements', color='#c7d5e0',
                     fontdict={'fontname': 'NS Sans', 'size': 11, 'weight': 'bold'})
        ax.set_xlabel('Playtime (hours)', color='#c7d5e0')
        ax.set_ylabel('Number of Achievements', color='#c7d5e0')
        ax.legend()

        fig.set_facecolor('#171a21')

        ax.tick_params(axis='both', colors='#c7d5e0')

        canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
        canvas_widget = canvas.get_tk_widget()

        canvas_widget.place(x=750, y=561, anchor=CENTER)

        canvas.draw_idle()


from tkinter import Toplevel


# Functie op een pokemon en de info ervan apart op een scherm te zetten
def display_pokemon_info_window(pokemon_info):
    pokemon_window = Toplevel()
    pokemon_window.title("Pokémon Info")
    pokemon_window.geometry("400x400")
    pokemon_window.config(background='#171a21')

    name_label = Label(pokemon_window, text=f"Name: {pokemon_info['name']}", bg='#171a21', fg='white')
    name_label.pack()

    # Hier worden de pokemon moves gezet
    moves_label = Label(pokemon_window, text=f"Moves: {', '.join(pokemon_info['moves'])}", bg='#171a21', fg='white')
    moves_label.pack()

    # Hier worden de pokemon types gezet
    types_label = Label(pokemon_window, text=f"Types: {', '.join(pokemon_info['types'])}", bg='#171a21', fg='white')
    types_label.pack()

    number_label = Label(pokemon_window, text=f"Number: {pokemon_info['number']}", bg='#171a21', fg='white')
    number_label.pack()

    description_label = Label(pokemon_window, text=f"Description: {pokemon_info['description']}", bg='#171a21',
                              fg='white')
    description_label.pack()

    artwork_img = Image.open(requests.get(pokemon_info['artwork'], stream=True).raw)
    artwork_photo = ImageTk.PhotoImage(artwork_img)
    artwork_label = Label(pokemon_window, image=artwork_photo, bg='#171a21')
    artwork_label.image = artwork_photo
    artwork_label.pack()
    # Gebaseerd op de playtime weergeeft die de pokemon info van het aantal uur. Daarnaast laat die ook weten of het aantal gespeelde uren gezond is of niet.
    if 1 <= pokemon_info['number'] <= 25:
        playing_level_label = Label(pokemon_window,
                                    text=f"You played: {pokemon_info['number']} hours in the last 2 weeks \nA Healty amount of hours! ",
                                    fg="green", font=('Arial', 12, 'bold'), bg='#171a21')
        playing_level_label.pack()
    elif 26 <= pokemon_info['number'] <= 50:
        playing_level_label = Label(pokemon_window,
                                    text=f"You played: {pokemon_info['number']} hours in the last 2 weeks \nA average amount of hours!",
                                    fg="#D5B60A", bg='#171a21',
                                    font=('Arial', 12, 'bold'))
        playing_level_label.pack()
    elif 51 <= pokemon_info['number'] <= 90:
        playing_level_label = Label(pokemon_window,
                                    text=f"You played: {pokemon_info['number']} hours in the last 2 weeks \nTake care of yourself!",
                                    fg="orange", bg='#171a21',
                                    font=('Arial', 12, 'bold'))
        playing_level_label.pack()
    elif 91 <= pokemon_info['number'] <= 151:
        playing_level_label = Label(pokemon_window,
                                    text=f"You played: {pokemon_info['number']} hours in the last 2 weeks \nPlease don't neglect your health!",
                                    fg="red", bg='#171a21',
                                    font=('Arial', 12, 'bold'))
        playing_level_label.pack()
    else:
        playing_level_label = Label(pokemon_window,
                                    text=f"You played: {pokemon_info['number']} hours in the last 2 weeks \nPlaying level: Touch grass...",
                                    font=('Arial', 12, 'bold'), bg='#171a21')
        playing_level_label.pack()


def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            'name': data['name'].capitalize(),
            'artwork': data['sprites']['front_default'],
            'moves': [move['move']['name'].capitalize() for move in data['moves'][:4]],
            'types': [type['type']['name'].capitalize() for type in data['types']],
            'number': data['id'],
        }
        description_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"
        description_response = requests.get(description_url)
        if description_response.status_code == 200:
            description_data = description_response.json()
            for entry in description_data['flavor_text_entries']:
                if entry['language']['name'] == 'en':
                    pokemon_info['description'] = entry['flavor_text']
                    break
        else:
            print(f"Failed to get {pokemon_name} from Pokémon API.")
        return pokemon_info
    else:
        print(f"Failed to get Pokémon info for {pokemon_name}")
        return None


def get_recent_playtime(steam_id):
    API_KEY = 'A3901F53D2D1F26049D9FF8C91E9BB78'
    url = f'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={API_KEY}&steamid={steam_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'games' in data['response']:
                playtime_2weeks = sum(game['playtime_2weeks'] // 60 for game in data['response']['games'])
                return playtime_2weeks
            else:
                print("No recent playtime  found.")
        else:
            print("Failed to fetch recent playtime data.")
    except Exception as e:
        print(f"Error: {e}")
    return None


def display_pokemon_info(steam_id, dashboard_window):
    playtime_2weeks = get_recent_playtime(steam_id)
    if playtime_2weeks is not None:
        pokemon_name = int(playtime_2weeks)
        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:

            display_pokemon_info_window(pokemon_info)
        else:
            print(f"Failed to fetch Pokémon info for {pokemon_name}")

    else:
        print("Failed to fetch recent playtime data. Cannot display Pokémon info.")


# Dit is het main dashboard van de GUI
def gui_dashboard(steam_id):
    dashboard_scherm = Tk()
    dashboard_scherm.geometry("1500x1500")
    dashboard_scherm.title(f"Dashboard Steam friends ")
    dashboard_scherm.config(background='#171a21')

    img = Image.open("breed.png")
    img = img.resize((300, 80))
    img = ImageTk.PhotoImage(img)
    logo = Label(dashboard_scherm, image=img)
    logo.image = img
    logo.place(x=1060, y=20)

    response = requests.get("https://avatars.steamstatic.com/d691cc17a95f18fb80b21945bb940ccce8cb7bdc.jpg")
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.resize((80, 80))
        img = ImageTk.PhotoImage(img)

        logo = Label(dashboard_scherm, image=img)
        logo.image = img
        logo.place(x=20, y=20)
    else:
        print("Failed to fetch the image")

    display_player_info_label(steam_id, dashboard_scherm)
    naam_eerste_spel(steam_id, dashboard_scherm)
    display_recently_played_game(steam_id, dashboard_scherm)
    display_linear_regression(steam_id, dashboard_scherm)

    pokemon_button = Button(dashboard_scherm, text="Show Pokémon Info",
                            command=lambda: display_pokemon_info(steam_id, dashboard_scherm))
    pokemon_button.place(x=20, y=300)

    dashboard_scherm.mainloop()


def get_steam_id(entry_widget, window):
    steam_id = entry_widget.get()
    if steam_id:
        window.destroy()
        gui_dashboard(steam_id)


# De gebruiker moet hier zijn steamid invoeren
def input_steam_id_window():
    input_window = Tk()
    input_window.title("Enter Steam ID")
    input_window.geometry('2500x2500')
    input_window.config(bg='#171a21')

    label = Label(input_window, text="Enter your friend's Steam ID:", bg='#171a21', fg='#c7d5e0',
                  font=('NS Sans', 24, 'bold'))
    label.pack(pady=80)

    entry = Entry(input_window)
    entry.pack(pady=80)

    img = Image.open("breed.png")
    img = img.resize((300, 100))
    img = ImageTk.PhotoImage(img)
    logo = Label(input_window, image=img)
    logo.image = img
    logo.place(x=10, y=10)

    submit_button = Button(input_window, text="Submit", command=lambda: get_steam_id(entry, input_window),
                           bg='#1b2838', fg='#c7d5e0', font=('NS Sans', 18, 'bold'))
    submit_button.pack(pady=20)

    input_window.mainloop()


input_steam_id_window()