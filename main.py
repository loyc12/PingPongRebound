from Pi import Pi
from Po import Po
from Ping import Ping
from Pong import Pong
from Pinger import Pinger
from Ponger import Ponger
from Pingest import Pingest
from Pongest import Pongest
from GameInterface import Game
from GameManager import main

import pygame as pg
import asyncio as asy
import Addons as ad

# MASTER LIST
# TODO : only add bots to game on start
# TODO : allow removing players from games via GameManager
# TODO : implement gamesToEnd queue to avoid issue with deleting games while iterating over gameDict
# TODO : add game state dicts in gameManager or gameInterface to be return with getInfo
# TODO : add queues for gameManager to receive/send messages (gamesToStart, gameStartInfo, gamesToEnd, gameEndInfo, playerEvents)
# TODO : integrate gameManager with sockets

# FUNCTION LIST
# TODO : make gm.addGame() take in player ids, and map them to racket ids
# TODO : implement get/sendUpdateInfo()
# TODO : implement get/sendStartState()
# TODO : implement get/sendCloseState()

# DEBUG LIST
# TODO : make sure to always put player 1 and 2 in oposite teams
# TODO : add a "mode" argument to game.respawnBall() and use it when initializing the ball
# TODO : rework the ball respawn trajectory everywhere

# MINOR LIST
# TODO : turn ping into pi and turn game into po
# TODO : add double-sided gravity to pingest (so it's an actual ping game lol)
# TODO : add sound effects to collisions (in GameObject class) ?
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)

async def debugTester( Initialiser ):

	pg.init()
	g = Initialiser(1, True)

	g.setWindow(pg.display.set_mode((g.width, g.height)))
	pg.display.set_caption(g.name)

	g.printControlers()
	g.addPlayer( "Player 1", 1 )
	g.printControlers()
	g.start()
	g.printControlers()
	g.run()


def debugPlayerControler( game ):
	# read local player inputs
	for event in pg.event.get():

		# quiting the game
		if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
			game.state = ad.ENDING

		# handling key presses
		elif event.type == pg.KEYDOWN:
			for i in range( len( game.controlers )):
				if game.controlers[i].mode == ad.PLAYER:
					game.controlers[i].handleKeyInput( event.key ) # first game controler, aka player 1


def takeGameStep( game ):
	game.step()

	if game.debugMode:
		debugPlayerControler( game )

	game.clock.tick ( game.framerate )

if __name__ == '__main__':
	asy.run(debugTester( Pong ))


#
#	GameLoop()
#	{
#		initGame()
#			sendStartState()
#
#		addPlayers()
#		startGame()
#			game.start()
#
#		while (isRunning)
#			stepGame()
#				updateObjects()
#				makeBotsPlay()
#				sendUpdateInfo() 			OR: renderScreen() (debug)
#
#		deleteGame()
#			sendEndState()
#			game.close()
#	}
#
#	ManagerLoop()
#	{
#		addGames()
#			initGame()
#			addPlayers()
#			sendStartState()
#
#		startGames()
#
#		tickGames()
#			while (runGames)
#			{
#				for game in gameDict
#					{
#					if (isRunning)
#						stepGame()
#							updateObjects()
#							makeBotsPlay()
#					elif (isOver)
#						deleteGame()
#							sendEndState()
#							game.close()
# 					}
# 			}

#			sendUpdateInfo() (sends the dictionary of game states)
#		}
#