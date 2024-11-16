#!/usr/bin/env python

import asyncio
import sys
import json

from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosedOK

# Local imports
from game import Game

URI = "ws://localhost:8001"

async def ainput(string: str) -> str:
    #await asyncio.to_thread(sys.stdout.write, f'{string} ') # needs to flush?
    return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')

async def receive(websocket):

    username = None

    while True:
        try:
            message = await websocket.recv()
            print(f"Received: {message}")

            if message.startswith("WELCOME "):
                username = message.replace("WELCOME ", "")
                continue

            if message.startswith("GAME "):
                #print("New game:", message)
                game_json = message.replace("GAME ", "")
                #print("Game JSON:", game_json)
                game_data = json.loads(game_json)
                game = Game()
                game.import_data(game_data)
                #print("New game:", game)
                print("White:", game.get_white())
                print("Black:", game.get_black())
                print("Turn:", game.get_turn())
                print("Board:")
                game.get_board().print()
                if game.get_white().get_username() == username and game.get_turn() == "white":
                    print("Your turn")
                elif game.get_black().get_username() == username and game.get_turn() == "black":
                    print("Your turn")
                else:
                    print("Opponent's turn")
        except ConnectionClosedOK:
            print("Server disconnected")
            break

async def send(websocket):
    while True:
        try:
            message = await ainput("")
            await websocket.send(message)
            if message.upper() == "QUIT":
                break
        except ConnectionClosedOK:
            print("Server disconnected")
            break

async def hello():
    async with connect(URI) as websocket:
        try:
            print("Connected to server")
            bg_rcv = asyncio.create_task(receive(websocket))
            bg_snd = asyncio.create_task(send(websocket))

            await bg_snd
            await bg_rcv

            #while True:
            #    name = input("\U0001f600 Please choose an username: ")
            #    await websocket.send(f"USERNAME {name}")

                #response = await websocket.recv()

                #if response == "OK":
                #    print(f"\u2713 You are now known as {name}")
                #    break
                #else:
                #    print("Something went wrong.")
                
            #while True:
            #    message = input("Command: ")
            #    await websocket.send(message)
            #    received = await websocket.recv()
            #    print(f"Received: {received}")
        except ConnectionClosedOK:
            print("Server closed connection")

if __name__ == "__main__":
    asyncio.run(hello())