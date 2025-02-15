import os
import csv
from collections import Counter

# Define file paths
data_file = r"C:\\Users\\HP\\OneDrive\\Documents\\Console_Based_Spotify\\console-based-spotify\\data.csv"
artists_dir = r"C:\\Users\\HP\\OneDrive\\Documents\\Console_Based_Spotify\\console-based-spotify\\artist"
genre_dir = r"C:\\Users\\HP\\OneDrive\\Documents\\Console_Based_Spotify\\console-based-spotify\\genere"
users_dir = r"C:\\Users\\HP\\OneDrive\\Documents\\Console_Based_Spotify\\console-based-spotify\\users\\listeners"



def ensure_dir(directory):
    """Ensures the given directory exists."""
    os.makedirs(directory, exist_ok=True)

def update_search_history(user_folder, song_name):
    """Updates the search history file for a user."""
    history_file = os.path.join(user_folder, "history.txt")
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(song_name + "\n")

def get_song_suggestions(user_folder):
    """Suggests songs based on past searches and plays."""
    history_file = os.path.join(user_folder, "history.txt")
    if not os.path.exists(history_file):
        return []
    with open(history_file, "r", encoding="utf-8") as f:
        songs = f.read().splitlines()
    song_counts = Counter(songs)
    suggestions = [song for song, _ in song_counts.most_common(5)]
    return suggestions


def search_song(song_name):
    """
    Searches for a song in data.csv, artist files, and genre files.
    Returns a list of found song details if found; otherwise, returns "Not Found".
    """
    found_songs = []
    
  
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and song_name.lower() in row[0].lower():
                    found_songs.append(f"{row[0]} (from data.csv)")
    
 
    if os.path.exists(artists_dir):
        for artist in os.listdir(artists_dir):
            artist_file = os.path.join(artists_dir, artist, f"{artist}.txt")
            if os.path.exists(artist_file):
                with open(artist_file, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    for song in lines:
                        if song_name.lower() in song.lower():
                            found_songs.append(f"{song} (from artist: {artist})")
    

    if os.path.exists(genre_dir):
        for genre in os.listdir(genre_dir):
            genre_file = os.path.join(genre_dir, genre, f"{genre}.txt")
            if os.path.exists(genre_file):
                with open(genre_file, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    for song in lines:
                        if song_name.lower() in song.lower():
                            found_songs.append(f"{song} (from genre: {genre})")
    
    return found_songs if found_songs else "Not Found"

def search_song_menu(user_folder):
    """Prompts the user to search for a song, prints results, and updates history if found."""
    song_name = input("Enter song name to search: ").strip()
    if not song_name:
        print("No song name entered.")
        return

    result = search_song(song_name)
    if result == "Not Found":
        print("Not Found")
    else:
        print("\nFound:")
        for song in result:
            print(f"- {song}")
        update_search_history(user_folder, song_name)



def add_song_to_playlist(user_folder, song_name):
    """
    Adds a song to a playlist.
    User is prompted to either use an existing playlist or create a new one.
    """
    option = input("Do you want to add to an (e)xisting playlist or create a (n)ew one? [e/n]: ").strip().lower()
    
    if option == "e":
      
        available = [f for f in os.listdir(user_folder) if f.endswith(".txt") and f not in ("history.txt", "credentials.txt")]
        if not available:
            print("No existing playlists found. Creating a new one.")
            option = "n"
        else:
            print("Existing playlists:")
            for idx, pl in enumerate(available, 1):
                print(f"{idx}. {pl.replace('.txt', '')}")
            choice = input("Enter the playlist name from above: ").strip()
            playlist_file = os.path.join(user_folder, f"{choice}.txt")
    if option == "n":
        new_playlist = input("Enter a new playlist name: ").strip()
        playlist_file = os.path.join(user_folder, f"{new_playlist}.txt")
    
    with open(playlist_file, "a", encoding="utf-8") as f:
        f.write(song_name + "\n")
    print(f"'{song_name}' added to playlist '{os.path.basename(playlist_file).replace('.txt','')}'.")


def artist_add_song(artist_folder):
    """Artist uploads a new song."""
    song_name = input("Enter song name to upload: ").strip()
    artist_file = os.path.join(artist_folder, f"{os.path.basename(artist_folder)}.txt")
    with open(artist_file, "a", encoding="utf-8") as f:
        f.write(song_name + "\n")
    print(f"'{song_name}' uploaded successfully.")

def artist_delete_song(artist_folder):
    """Artist deletes an uploaded song."""
    artist_file = os.path.join(artist_folder, f"{os.path.basename(artist_folder)}.txt")
    if not os.path.exists(artist_file):
        print("No songs found for this artist.")
        return
    with open(artist_file, "r", encoding="utf-8") as f:
        songs = f.read().splitlines()
    if not songs:
        print("No songs available to delete.")
        return
    print("Available songs:")
    for idx, song in enumerate(songs, 1):
        print(f"{idx}. {song}")
    try:
        choice = int(input("Enter song number to delete: ").strip()) - 1
        if 0 <= choice < len(songs):
            del songs[choice]
            with open(artist_file, "w", encoding="utf-8") as f:
                f.write("\n".join(songs) + "\n")
            print("Song deleted successfully.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def artist_dashboard(artist_folder):
    """Dashboard for an artist."""
    ensure_dir(artist_folder)
    while True:
        print("\n--- Artist Dashboard ---")
        print("1. Add a Song")
        print("2. Delete a Song")
        print("3. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            artist_add_song(artist_folder)
        elif choice == "2":
            artist_delete_song(artist_folder)
        elif choice == "3":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice.")



def user_dashboard(user_folder):
    """Dashboard for a listener."""
    ensure_dir(user_folder)
    while True:
        print("\n--- User Dashboard ---")
        print("1. Search for a Song")
        print("2. Add Song to Playlist")
        print("3. View Song Recommendations")
        print("4. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            search_song_menu(user_folder)
        elif choice == "2":
            song_name = input("Enter song name to add to playlist: ").strip()
            if song_name:
                add_song_to_playlist(user_folder, song_name)
        elif choice == "3":
            suggestions = get_song_suggestions(user_folder)
            if suggestions:
                print("\n🎵 Based on your history, you might like:")
                for song in suggestions:
                    print(f"- {song}")
            else:
                print("\nNo recommendations available yet. Start searching for songs!")
        elif choice == "4":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice.")



def sign_in(user_type):
    """Handles user login."""
    base_dir = os.path.join(users_dir if user_type == "listeners" else artists_dir)
    name = input("Enter your name: ").strip()
    user_folder = os.path.join(base_dir, name)
    if not os.path.exists(user_folder):
        print("User not found. Please sign up first.")
        return
    password = input("Enter your password: ").strip()
    try:
        with open(os.path.join(user_folder, "credentials.txt"), "r", encoding="utf-8") as f:
            stored_name, stored_password = f.read().splitlines()
        if stored_password == password:
            print("Login successful!")
            if user_type == "listeners":
                user_dashboard(user_folder)
            else:
                artist_dashboard(user_folder)
        else:
            print("Incorrect password.")
    except Exception as e:
        print("Error reading credentials file.", e)

def sign_up(user_type):
    """Registers a new user and creates necessary directories."""
    base_dir = os.path.join(users_dir if user_type == "listeners" else artists_dir)
    ensure_dir(base_dir)
    name = input("Enter your name: ").strip()
    user_folder = os.path.join(base_dir, name)
    if os.path.exists(user_folder):
        print("User already exists. Please sign in.")
        return
    ensure_dir(user_folder)
    password = input("Enter your password: ").strip()
    with open(os.path.join(user_folder, "credentials.txt"), "w", encoding="utf-8") as f:
        f.write(f"{name}\n{password}\n")
    print(f"Account created successfully for {name}.")
    if user_type == "listeners":
        user_dashboard(user_folder)
    else:
        artist_dashboard(user_folder)



def main():
    print("🎵 Welcome to Console-Based Spotify 🎵")
    while True:
        print("\nMain Menu:")
        print("1. Listener Login/Sign-up")
        print("2. Artist Login/Sign-up")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            action = input("Enter 1 for Sign In, 2 for Sign Up: ").strip()
            if action == "1":
                sign_in("listeners")
            elif action == "2":
                sign_up("listeners")
            else:
                print("Invalid option.")
        elif choice == "2":
            action = input("Enter 1 for Sign In, 2 for Sign Up: ").strip()
            if action == "1":
                sign_in("artists")
            elif action == "2":
                sign_up("artists")
            else:
                print("Invalid option.")
        elif choice == "3":
            print("Thank you for using our music app. Goodbye! 👋")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
