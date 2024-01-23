import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_games_data():
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
                return data['response'].get('games', [])

            else:
                print("Response does not contain 'response' key.")

        else:
            print(f"API request failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
    return []

def calculate_statistics(data):
    sorted_games = sorted(data, key=lambda game: game.get('playtime_forever', 0), reverse=True)
    top_3_games = sorted_games[:3]

    return top_3_games

def display_statistics():
    games_data = get_games_data()

    if not games_data:
        print("No games data available.")
        return

    top_3_games = calculate_statistics(games_data)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Steam Games Statistics")

    chart_frame = ttk.Frame(root)
    chart_frame.pack(side=tk.TOP, padx=10, pady=10)

    # Display top 3 games as a bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    game_names = [game.get('name', 'N/A') for game in top_3_games]
    playtimes = [game.get('playtime_forever', 0) / 60 for game in top_3_games]

    ax.bar(game_names, playtimes, color='skyblue')
    ax.set_ylabel('Playtime (hours)')
    ax.set_title('Top 3 Played Games')

    # Embed the Matplotlib chart in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(padx=5, pady=5)

    # Button to close the GUI
    close_button = ttk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=5)

    # Run the Tkinter main loop
    root.mainloop()

# Call the function to display statistics in a GUI
display_statistics()
