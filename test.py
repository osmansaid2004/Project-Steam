import tkinter as tk
from tkinter import ttk
import json

def load_steam_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON in '{file_path}'.")
        return None

class SteamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Dashboard")

        # Load data from steam.json
        self.steam_data = self.load_steam_data('steam.json')

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Label to display the name of the first game
        self.game_label = tk.Label(self.root, text="First Game: " + self.steam_data[0]["name"])
        self.game_label.pack(pady=10)

        # Button to sort and display data
        sort_button = tk.Button(self.root, text="Sort Data", command=self.sort_and_display)
        sort_button.pack(pady=10)

    def load_steam_data(self, file_path):
        data = load_steam_data(file_path)
        return data.get("games", []) if data else []

    def sort_and_display(self):
        # Sort data based on playtime
        sorted_data = sorted(self.steam_data, key=lambda x: x.get("playtime", 0), reverse=True)

        # Display sorted data
        sorted_str = "\n".join([f"Game: {item['name']}, Playtime: {item['playtime']}, Friends Online: {item.get('friends_online', 0)}" for item in sorted_data])

        # Create a new window to display sorted data
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sorted Data")

        # Label to display sorted data
        sorted_label = tk.Label(sort_window, text=sorted_str)
        sorted_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteamApp(root)
    root.mainloop()
