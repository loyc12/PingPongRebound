from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest
from Pongester import Pongester
from GameInterface import Game
from GameManager import main

import pygame as pg
import asyncio as asy
import Addons as ad

# MASTER LIST
# TODO : add a player array in gameInterface for player ID
# TODO : add game state dicts in gameInterface
# TODO : implement winning and losing
# TODO : integrate gameManager with sockets
# TODO : add game variable : winnerID
# TODO : add queues for gameManager to receive/send messages (gamesToStart, gameStartInfo, gamesToEnd, gameEndInfo)

# FUNCTION LIST
# TODO : make gm.addGame() take in player ids, and map them to racket ids
# TODO : implement get/sendUpdateInfo()
# TODO : implement get/sendStartState()
# TODO : implement get/sendCloseState()

# DEBUG LIST
# TODO : make sure to always put player 1 and 2 in oposite teams
# TODO : rework the ball respawn trajectory everywhere

# MINOR LIST
# TODO : have pygame events be put in a queue, and parse from queue for movements in gameManager
# TODO : add a "mode" argument to game.respawnBall() and use it when initializing the ball
# TODO : add a game start and game over screen ?
# TODO : add double-sided gravity to pingest (so it's an actual ping game lol)
# TODO : add sound effects to collisions (in GameObject class) ?
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)

async def debugTester( Initialiser ):

	pg.init() # 										NOTE : DEBUG
	win = pg.display.set_mode((2048, 1280)) # 			NOTE : ...

	game = Initialiser( win, pg.time.Clock(), True )
	pg.display.set_caption("DEBUG") # 					NOTE : ...

	game.addPlayer( "Tester 1", 1 )
	game.start()

	while game.isRunning:
		takeGameStep( game )
		game.refreshScreen()
		await asy.sleep(0)


def debugPlayerControler( game ):
	# read local player inputs
	for event in pg.event.get():

		# quiting the game
		if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
			game.isRunning = False

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
#			while (keepGoing)
#			{
#				if (isRunning)
#					stepGame()
#						updateObjects()
#						makeBotsPlay()
#						sendUpdateInfo()
#				elif (isOver)
#					deleteGame()
#						sendEndState()
# 			}
#		}
#