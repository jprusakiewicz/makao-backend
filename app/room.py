import json
import random
from typing import List, Union

from .connection import Connection
from .deck import Deck
from .server_errors import GameIsStarted


class Room:
    def __init__(self, room_id):
        self.id = room_id
        self.active_connections: List[Connection] = []
        self.is_game_on = False
        self.deck: Union[None, Deck] = None
        self.whos_turn: int = 0
        self.MAX_PLAYERS = 4

    async def append_connection(self, connection):
        if len(self.active_connections) < self.MAX_PLAYERS and self.is_game_on is False:
            connection.player.game_id = self.get_free_player_game_id()  # todo here
            self.active_connections.append(connection)
            if len(self.active_connections) > 1:  # todo change to 4
                await self.start_game()
        else:
            raise GameIsStarted

    def get_taken_ids(self):
        taken_ids = [connection.player.game_id for connection in self.active_connections]
        return taken_ids

    def get_free_player_game_id(self):
        taken_ids = self.get_taken_ids()
        for i in range(1, 4):
            if i not in taken_ids:
                return str(i)

    async def remove_connection(self, connection_with_given_ws):
        self.active_connections.remove(connection_with_given_ws)
        if len(self.active_connections) <= 1:
            await self.end_game()

    async def broadcast_json(self):
        for connection in self.active_connections:
            gs = self.get_game_state(connection.player.id)
            await connection.ws.send_text(gs)

    async def restart_game(self):
        await self.start_game()

    async def start_game(self):
        self.is_game_on = True
        self.whos_turn = self.draw_random_player_id()  # todo
        self.deck = Deck(len(self.active_connections))
        await self.broadcast_json()

    async def end_game(self):
        self.is_game_on = False
        self.whos_turn = 0
        self.deck = None
        await self.broadcast_json()

    def handle_players_move(self, player_id, picked_cards):
        self.deck.handle_players_move(player_id, picked_cards)
        self.next_person_move()

    def next_person_move(self):
        if int(self.whos_turn) > len(self.get_taken_ids()):
            self.whos_turn = str(1)
        else:
            self.whos_turn = str(int(self.whos_turn) + 1)

    def get_game_state(self, client_id) -> str:
        if self.is_game_on:
            player = next(
                connection.player for connection in self.active_connections if connection.player.id == client_id)
            game_state = {
                "is_game_on": self.is_game_on,
                "whos_turn": self.whos_turn,
                "game_data": self.deck.get_current_state(player.game_id),
            }
        else:
            game_state = {
                "is_game_on": self.is_game_on
            }

        return json.dumps(game_state)

    def draw_random_player_id(self):
        return random.choice(
            [connection.player.id for connection in self.active_connections])

    def get_stats(self):
        return {"is_game_on": self.is_game_on,
                "whos turn": self.whos_turn,
                "number_of_connected_players": len(self.active_connections),
                "pile": self.deck.pile}
