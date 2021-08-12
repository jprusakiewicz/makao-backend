import json
import random
import uuid
from typing import List, Union

from .connection import Connection
from .game import Game
from .server_errors import GameIsStarted, ItsNotYourTurn


class Room:
    def __init__(self, room_id):
        self.winners = []  # !use normal id!
        self.id = room_id
        self.active_connections: List[Connection] = []
        self.is_game_on = False
        self.game: Union[None, Game] = None
        self.whos_turn: int = 0
        self.MAX_PLAYERS = 4
        self.MIN_PLAYERS = 4
        self.game_id: str

    async def append_connection(self, connection):
        if len(self.active_connections) <= self.MAX_PLAYERS and self.is_game_on is False:
            connection.player.game_id = self.get_free_player_game_id()
            self.active_connections.append(connection)
            if len(self.active_connections) >= self.MIN_PLAYERS:
                await self.start_game()
        else:
            raise GameIsStarted

    def get_taken_ids(self):
        taken_ids = [connection.player.game_id for connection in self.active_connections]
        return taken_ids

    def get_players_in_game(self):
        players = [connection.player for connection in self.active_connections if
                   connection.player.in_game]
        return players

    def get_players_game_ids_in_game(self):
        players = [connection.player.game_id for connection in self.active_connections if
                   connection.player.in_game]
        return players

    def get_free_player_game_id(self):
        taken_ids = self.get_taken_ids()
        for i in range(1, 5):
            if str(i) not in taken_ids:
                return str(i)

    async def remove_connection(self, connection_with_given_ws):
        await self.remove_player_by_id(connection_with_given_ws.player.id)
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
        self.game = Game(len(self.active_connections))
        self.put_all_players_in_game()
        self.game_id = str(uuid.uuid4().hex)
        await self.broadcast_json()

    async def end_game(self):
        self.is_game_on = False
        self.whos_turn = 0
        self.game = None
        self.put_all_players_out_of_game()
        await self.broadcast_json()

    async def remove_player_by_game_id(self, game_id):
        player = next(
            connection.player for connection in self.active_connections if connection.player.game_id == game_id)
        if self.game:

            self.game.remove_players_cards(player.game_id)
            if self.whos_turn == player.game_id:
                self.next_person_move()
            player.in_game = False

            # await self.broadcast_json()

    async def remove_player_by_id(self, id):
        player = next(
            connection.player for connection in self.active_connections if connection.player.id == id)
        if self.game:
            self.game.remove_players_cards(player.game_id)
            if self.whos_turn == player.game_id:
                self.next_person_move()
            player.in_game = False
            print(f"kicked player {player.id}")
            # await self.broadcast_json()

    def put_all_players_in_game(self):
        for connection in self.active_connections:
            connection.player.in_game = True

    def put_all_players_out_of_game(self):
        for connection in self.active_connections:
            connection.player.in_game = False

    async def handle_players_move(self, client_id, player_move):
        next_person_move = False
        player = next(
            connection.player for connection in self.active_connections if connection.player.id == client_id)
        self.validate_its_players_turn(player.game_id)

        if 'picked_cards' in player_move:
            next_person_move = self.game.handle_players_cards_move(player.game_id, player_move)
            await self.check_and_handle_empty_hand(player)
        elif 'other_move' in player_move:
            next_person_move = self.game.handle_players_other_move(player.game_id, player_move)

        if next_person_move:
            self.next_person_move()

    def next_person_move(self):
        active_players_ids = self.get_players_game_ids_in_game()
        current_idx = active_players_ids.index(self.whos_turn)
        #
        # if current_idx >= len(self.get_players_game_ids_in_game()) - 1:  # todo does it work?
        #     self.whos_turn = active_players_ids[0]
        # else:
        if self.game.reverse is True:
            try:
                self.whos_turn = active_players_ids[current_idx - 1]
            except IndexError:
                self.whos_turn = active_players_ids[-1]
        else:
            try:
                self.whos_turn = active_players_ids[current_idx + 1]
            except IndexError:
                self.whos_turn = active_players_ids[0]
        self.game.reset_parameters()


    def get_game_state(self, client_id) -> str:
        if self.is_game_on:
            player = next(
                connection.player for connection in self.active_connections if connection.player.id == client_id)
            game_state = {
                "is_game_on": self.is_game_on,
                "whos_turn": self.game_id_to_direction(player.game_id, str(self.whos_turn)),
                "game_data": self.game.get_current_state(player.game_id),
                "nicks": self.get_nicks(client_id)
            }
        else:
            game_state = {
                "is_game_on": self.is_game_on
            }

        return json.dumps(game_state)

    def draw_random_player_id(self):
        return random.choice(self.get_taken_ids())

    def get_stats(self):
        return {"is_game_on": self.is_game_on,
                "whos turn": self.whos_turn,
                "number_of_connected_players": len(self.active_connections),
                "pile": self.game.pile}

    def game_id_to_direction(self, player_id: str, enemy_id: str):
        direction = ""
        if player_id == enemy_id:
            direction = "player"

        elif player_id == '1':
            if enemy_id == "4":
                direction = "right"
            elif enemy_id == "3":
                direction = "top"
            elif enemy_id == "2":
                direction = "left"
        elif player_id == '2':
            if enemy_id == "4":
                direction = "top"
            elif enemy_id == "3":
                direction = "left"
            elif enemy_id == "1":
                direction = "right"
        elif player_id == '3':
            if enemy_id == "4":
                direction = "left"
            if enemy_id == "2":
                direction = "right"
            if enemy_id == "1":
                direction = "top"
        elif player_id == '4':
            if enemy_id == "3":
                direction = "right"
            if enemy_id == "2":
                direction = "top"
            if enemy_id == "1":
                direction = "left"
        return direction

    def get_nicks(self, player_id):
        nicks = {}
        for connection in self.active_connections:
            enemy_direction = self.game_id_to_direction(player_id, connection.player.game_id)
            nicks[enemy_direction] = connection.player.nick
        return nicks

    def validate_its_players_turn(self, player_id):
        if player_id != self.whos_turn:
            raise ItsNotYourTurn

    async def kick_player(self, player_id):
        await self.remove_player_by_id(player_id)

    async def check_and_handle_empty_hand(self, player):
        if len(self.game.players[player.game_id]) == 0:
            print(f"player {player.id} has ended")
            self.winners.append(player.id)
            await self.remove_player_by_game_id(player.game_id)

