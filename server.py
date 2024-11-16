#!/usr/bin/env python

import asyncio
import json

from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK

# Local imports
#from chess import Board
from chess import InvalidMove
from game import Game, User

SERVER_PORT = 8001

users = {}

async def handler(websocket: ServerConnection):
    print("Client connected")
    print("Client remote address:", websocket.remote_address)
    print("Client local address:", websocket.local_address)
    print("ID: ", websocket.id)

    user_id = str(websocket.id)

    # Ask the client to choose a username
    while True:
        await websocket.send("Welcome! Please use the command USERNAME to choose a username.")
        response = await websocket.recv()
        if response.upper().startswith("USERNAME "):
            username = response.split(" ")[1]
            # TODO validate username
            users[user_id] = User(user_id, username)
            await websocket.send("WELCOME " + username)
            break
        else:
            await websocket.send("Invalid command. Please use the command USERNAME to choose a username.")

    user = users[user_id]
    user.set_websocket(websocket)

    while True:
        try:
            message = await websocket.recv()
        except ConnectionClosedOK:
            print("Client disconnected")
            break

        print(f"Received message: {message}")

        if message == "QUIT":
            print("Client requested to quit")
            await websocket.close()
            break
        
        if message == "LIST":
            await websocket.send(json.dumps([u.export_data() for u in users.values()]))
            continue
        
        if message == "NEWGAME":
            if user.is_in_a_game():
                await websocket.send("You are already in a game")
                continue
            
            # Search for an opponent
            opponent = None
            for id, other_user in users.items():
                if id == user_id:
                    continue
                if other_user.is_in_a_game():
                    continue
                opponent = other_user

            if opponent is None:
                await websocket.send("No opponent found")
                continue
            
            user.set_in_a_game(True)
            opponent.set_in_a_game(True)
            game = Game(user, opponent)

            user.set_game(game)
            opponent.set_game(game)

            game_msg = "GAME " + json.dumps(game.export_data())
            await websocket.send(game_msg)
            await opponent.get_websocket().send(game_msg)
            continue

        if message.startswith("MOVE "):
            
            move = message.replace("MOVE ", "").upper().replace(" ","")
            
            if move[0] not in "ABCDEFGH" or move[1] not in "12345678" or move[2] not in "ABCDEFGH" or move[3] not in "12345678":
                await websocket.send("ERROR Invalid move format - Example: MOVE E2 E4")
                continue

            source = [8 - int(move[1]), ord(move[0]) - 65]
            dest = [8 - int(move[3]), ord(move[2]) - 65]
            print("move:", source, dest)

            game = user.get_game()

            try:
                game.move(source, dest)
            except InvalidMove as e:
                print(e)
                await websocket.send("ERROR Invalid move")
                continue

            opponent = game.get_white() if game.get_white().get_id() != user.get_id() else game.get_black()
            game_msg = "GAME " + json.dumps(game.export_data())
            await websocket.send(game_msg)
            await opponent.get_websocket().send(game_msg)
            continue

        # Unknown command
        await websocket.send("UNKNOWN COMMAND")

    del users[user_id]

async def main():
    async with serve(handler, "", SERVER_PORT):
        print("Server started on port", SERVER_PORT)
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
