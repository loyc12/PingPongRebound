from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest
from Pongester import Pongester

from AiControler import AiControler as ai
from PlayerControler import PlayerControler as pl

import pygame as pg
import asyncio as asy

# MASTER LIST
# TODO : implement getData()
# TODO : test with sockets
# TODO : allow racket control through sockets (player child class of controler)

# FUNCTION LIST
# TODO : gameIsFull()
# TODO : gameHasPlayer()
# TODO : __contains__()

# DEBUG LIST


# MINOR LIST
# TODO : add a game start and game over screen
# TODO : add gravity to pingest  (to make it an actua ping game lol)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)

async def main():

	game = Pong()

	bot = ai( game, "bot" )
	game.addControler( bot )

	player = pl( game, "player" )
	game.addControler( player )

	game.start()
	while game.running:

		takeGameStep( game, player, bot )
		await asy.sleep(0)


def takeGameStep( game, player, bot ):
	game.step()

	# read local inputs
	for event in pg.event.get():
		# quiting the game
		if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
			game.running = False

		# handling key presses
		elif event.type == pg.KEYDOWN:
			player.handleKeyInput(event.key)

	bot.playStep()

	game.clock.tick (game.framerate)


if __name__ == '__main__':
	asy.run(main())
