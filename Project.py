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

        self.steam_data = load_steam_data('steam.json')

        self.create_widgets()

    def create_widgets(self):

        self.game_label = tk.Label(self.root, text="First Game: " + self.steam_data[0]["game"])
        self.game_label.pack(pady=10)


        sort_button = tk.Button(self.root, text="Sort Data", command=self.sort_and_display)
        sort_button.pack(pady=10)

    def sort_and_display(self):

        sorted_data = sorted(self.steam_data, key=lambda x: x["playtime"], reverse=True)

        sorted_str = "\n".join([f"Game: {item['game']}, Playtime: {item['playtime']}, Friends Online: {item['friends_online']}" for item in sorted_data])

        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sorted Data")

        sorted_label = tk.Label(sort_window, text=sorted_str)
        sorted_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteamApp(root)
    root.mainloop()