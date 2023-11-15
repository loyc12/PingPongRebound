from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest
from Pongester import Pongester
from GameInterface import Game

from BotControler import BotControler as ai
from PlayerControler import PlayerControler as pl

import pygame as pg
import asyncio as asy
import Addons as ad

# MASTER LIST
# TODO : integrate playerControler with sockets

# FUNCTION LIST
# TODO : implement game.getInfo()		(awaiting formating for that)
# TODO : implement game.respawnBall()
# TODO : add a key to resawn the ball

# DEBUG LIST
# TODO : make the smart ai better at Pinger (move last minute to throw?)
# TODO : make player 1 and 2 the most inward rackets in pingest
# TODO : review ball respawn in pongest

# MINOR LIST
# TODO : make bots move last second to give a spin to the ball
# TODO : add a game start and game over screen ?
# TODO : add double-sided gravity to pingest (so it's an actual ping game lol)
# TODO : figure out the ball respawn trajectory
# TODO : add sound effects to collisions (in GameObject class)
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)

async def main():

	game = Pong()
	#game.addPlayer( "tester_1" )
	game.start()

	while game.running:
		takeGameStep( game )
		await asy.sleep(0)


def debugPlayerControler( game ):
	# read local player inputs
	for event in pg.event.get():

		# quiting the game
		if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
			game.running = False

		# handling key presses
		elif event.type == pg.KEYDOWN:
			if game.controlers[0].mode == ad.PLAYER:
				game.controlers[0].handleKeyInput(event.key) # first game controler, aka player 1


def takeGameStep( game ):
	game.step()

	debugPlayerControler(game)

	game.clock.tick (game.framerate)


if __name__ == '__main__':
	asy.run(main())
