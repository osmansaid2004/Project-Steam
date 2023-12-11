import json
import customtkinter

def Json_bestand():
    try:
        with open('steam.json', 'r') as json_bestand:
            data = json.load(json_bestand)
            return data
    except Exception as e:
        print(f"Fout bij het verwerken van het json bestand: {e}")
        return None

def gesorteerde_namen(data):
    game_namen = [game.get("name", " ") for game in data]

    # Sorteer de spelnamen alfabetisch
    game_namen.sort()

    # Geef de eerste 10 gesorteerde spelnamen terug
    return game_namen[:10]

def GUI_Dashboard():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    Dashboard_Scherm = customtkinter.CTk()
    Dashboard_Scherm.geometry("500x350")



    def naam_eerste_spel():
        data = Json_bestand()

        if data:
            # Haal de naam op van het eerste spel
            naam_eerste_spel = data[0].get("name", " ")

            # Toon de naam in het GUI (veronderstel dat je een label-widget hebt)
            label = customtkinter.CTkLabel(master=Dashboard_Scherm, text=f"Eerste Spel: {naam_eerste_spel}")
            label.pack(pady=20, padx=10)

    # Roep de weergeef_naam_eerste_spel functie aan om de naam weer te geven op het GUI
    naam_eerste_spel()

    def alfabetische_spellen():
        data = Json_bestand()

        if data:
            # Gebruik de gesorteerde_namen functie om de gesorteerde namen te krijgen
            gesorteerde_spellen = gesorteerde_namen(data)

            # Toon de namen in het GUI (veronderstel dat je een label-widget hebt)
            for naam in gesorteerde_spellen:
                label = customtkinter.CTkLabel(master=Dashboard_Scherm, text=f"Afabetische volgorde Spel: {naam}")
                label.pack(pady=10, padx=10)

    # Roep de weergeef_alfabetische_spellen functie aan om de namen weer te geven op het GUI
    alfabetische_spellen()

    # Start de Tkinter-eventloop
    Dashboard_Scherm.mainloop()

# Roep de GUI_Dashboard functie aan om het GUI te maken en weer te geven
GUI_Dashboard()