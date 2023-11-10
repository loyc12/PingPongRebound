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

# MASTER LIST
# TODO : implement getData()
# TODO : make a controler class to control call makeMove() and getData()
# TODO : make an ai child class of controler
# TODO : allow racket control through sockets (player child class of controler)
# TODO : add a game start and game over screen


# MINOR LIST
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)
# TODO : add gravity to pingest  (to make it an actua ping game lol)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)


if __name__ == '__main__':

	g = Pong()

	bot = ai( g, "bot" )
	g.addControler( bot )

	player = pl( g, "player" )
	g.addControler( player )

	g.start()

	while g.running:
		g.step()

		# read local inputs
		for event in pg.event.get():
			# quiting the game
			if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
				g.running = False

			# handling key presses
			elif event.type == pg.KEYDOWN:
				player.handleKeyInput(event.key)

		bot.playStep()
		g.clock.tick (g.framerate)

	g.pause()
