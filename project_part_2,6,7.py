

import os

def get_height(tree, index):
    if index >= len(tree) or tree[index] == "":
        return 0
    left_height = get_height(tree, 2 * index + 1)
    right_height = get_height(tree, 2 * index + 2)
    return 1 + max(left_height, right_height)

def get_balance_factor(tree, index):
    if index >= len(tree) or tree[index] == "":
        return 0
    return get_height(tree, 2 * index + 1) - get_height(tree, 2 * index + 2)

def rotate_right(tree, index):
    left_index = 2 * index + 1
    if left_index >= len(tree) or tree[left_index] == "":
        return tree
    tree[index], tree[left_index] = tree[left_index], tree[index]
    return tree

def rotate_left(tree, index):
    right_index = 2 * index + 2
    if right_index >= len(tree) or tree[right_index] == "":
        return tree
    tree[index], tree[right_index] = tree[right_index], tree[index]
    return tree

def balance_tree(tree, index):
    if index >= len(tree) or tree[index] == "":
        return tree
    
    balance_factor = get_balance_factor(tree, index)
    if balance_factor > 1:
        if get_balance_factor(tree, 2 * index + 1) < 0:
            tree = rotate_left(tree, 2 * index + 1)
        tree = rotate_right(tree, index)
    elif balance_factor < -1:
        if get_balance_factor(tree, 2 * index + 2) > 0:
            tree = rotate_right(tree, 2 * index + 2)
        tree = rotate_left(tree, index)
    
    return tree

def update_structure(file_path, name):
    """Updates the structure.txt file using an AVL tree."""
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(name)
        return
    
    with open(file_path, "r") as f:
        data = f.read().split(",")
    
    while len(data) < 1:
        data.append("")
    
    index = 0
    while index < len(data):
        if data[index] == "":
            break
        if name < data[index]:
            index = 2 * index + 1
        else:
            index = 2 * index + 2
        
        while len(data) <= index:
            data.extend([""] * (index - len(data) + 1))
    
    data[index] = name
    data = balance_tree(data, 0)
    
    with open(file_path, "w") as f:
        f.write(",".join(data))

def search_structure(file_path, name):
    """Searches for a name in the AVL tree stored in structure.txt."""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, "r") as f:
        data = f.read().split(",")
    
    sorted_data = sorted(filter(lambda x: x != "", data))
    return name in sorted_data

def create_playlist(user_folder):
    playlists_folder = os.path.join(user_folder, "playlists")
    os.makedirs(playlists_folder, exist_ok=True)
    playlist_name = input("Enter playlist name: ")
    playlist_path = os.path.join(playlists_folder, f"{playlist_name}.txt")
    
    if os.path.exists(playlist_path):
        print("Playlist already exists.")
    else:
        with open(playlist_path, "w") as f:
            while True:
                song_name = input("Enter song name (or type 'exit' to stop): ")
                if song_name.lower() == "exit":
                    break
                singer_name = input("Enter singer name: ")
                genre = input("Enter genre: ")
                f.write(f"{song_name},{singer_name},{genre}\n")
            print(f"Playlist '{playlist_name}' created successfully.")
    

def add_song_to_playlist(user_folder):
    playlists_folder = os.path.join(user_folder, "playlists")
    if not os.path.exists(playlists_folder):
        print("No playlists found. Please create one first.")
        return
    
    playlist_name = input("Enter playlist name: ")
    playlist_path = os.path.join(playlists_folder, f"{playlist_name}.txt")
    
    if not os.path.exists(playlist_path):
        print("Playlist not found. Please try again.")
        return
    
    song_name = input("Enter song name: ")
    singer_name = input("Enter singer name: ")
    genre = input("Enter genre: ")
    
    with open(playlist_path, "a") as f:
        f.write(f"{song_name},{singer_name},{genre}\n")
    
    print(f"Song '{song_name}' added to playlist '{playlist_name}'.")

def user_dashboard(user_folder):
    os.makedirs(os.path.join(user_folder, "playlists"), exist_ok=True)
    while True:
        print("\n1. Create a Playlist")
        print("2. Add Song to Playlist")
        print("3. Logout")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_playlist(user_folder)
        elif choice == "2":
            add_song_to_playlist(user_folder)
        elif choice == "3":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

def sign_up(user_type):
    base_dir = os.path.join("users", user_type)
    structure_file = os.path.join(base_dir, "structure.txt")
    
    while True:
        name = input("Enter your name: ")
        if search_structure(structure_file, name):
            print("Username already exists. Please choose another.")
        else:
            break
    
    user_folder = os.path.join(base_dir, name)
    os.makedirs(user_folder)
    update_structure(structure_file, name)
    
    cred_file = os.path.join(user_folder, "credentials.txt")
    password = input("Enter your password: ")
    with open(cred_file, "w") as f:
        f.write(f"{name}\n{password}\n")
    print(f"Account created successfully for {name} inside {user_type.capitalize()}s")
    user_dashboard(user_folder)

def sign_in(user_type):
    base_dir = os.path.join("users", user_type)
    structure_file = os.path.join(base_dir, "structure.txt")
    
    name = input("Enter your name: ")
    user_folder = os.path.join(base_dir, name)
    cred_file = os.path.join(user_folder, "credentials.txt")
    
    if not search_structure(structure_file, name) or not os.path.exists(cred_file):
        print("User not found. Please sign up first.")
        return
    
    for attempt in range(3):
        password = input("Enter your password: ")
        with open(cred_file, "r") as f:
            lines = f.readlines()
            if len(lines) > 1 and lines[1].strip() == password:
                print("Login successful!")
                user_dashboard(user_folder)
                return
        print("Incorrect password. Try again.")
    print("Too many failed attempts. Process terminated.")
def listener():
    choice = input("Do you want to sign in or sign up? (1 for Sign In, 2 for Sign Up): ")
    if choice == "1":
        sign_in("listeners")
    elif choice == "2":
        sign_up("listeners")
    else:
        print("Invalid choice.")
def artist():
    choice = input("Do you want to sign in or sign up? (1 for Sign In, 2 for Sign Up): ")
    if choice == "1":
        sign_in("artists")
    elif choice == "2":
        sign_up("artists")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    print("Welcome to our music app")
    
    while True:
        print("If you are a listener, press 1")
        print("If you are an artist, press 2")
        print("To search a name, press 3")
        print("To exit, press -1")
        
        inp = int(input("Enter a number: "))
        
        if inp == 1:
            listener()
        elif inp == 2:
            artist()
        elif inp == 3:
            name = input("Enter name to search: ")
            if search_structure(os.path.join("users", "listeners", "structure.txt"), name) or \
               search_structure(os.path.join("users", "artists", "structure.txt"), name):
                print(f"{name} exists in the structure.")
            else:
                print(f"{name} does not exist.")
        elif inp == -1:
            print("Thank you for using our music app. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

