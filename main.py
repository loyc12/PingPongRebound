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
# TODO : add game sate dicts in gameInterface
# TODO : continue working on the gameManager class
# TODO : implement winning and losing
# TODO : integrate gameManager with sockets
# TODO : add game variables : isRunning, isOver, winnerID
# TODO : add queues for gameManager to receive/send messages (gamesToStart, gameStartInfo, gamesToEnd, gameEndInfo)

# FUNCTION LIST
# TODO : make gm.addGame() take in a game id and player ids, nad map the player ids to racket ids
# TODO : implement get/sendUpdateInfo()
# TODO : implement get/sendStartState()
# TODO : implement get/sendCloseState()

# DEBUG LIST
# TODO : see if you can have multiple windows with pygame (or just switch which game to render)
# TODO : put player 1 and 2 in oposite teams always
# TODO : rework the ball respawn trajectory everywhere
# TODO : check hard difficulty's AI gravity management (imprecise(???))

# MINOR LIST
# TODO : have pygame events be put in a queue, and parse from queue for movements in gameManager
# TODO : add a "mode" argument to game.respawnBall() and use it when initializing the ball
# TODO : add a game start and game over screen ?
# TODO : add double-sided gravity to pingest (so it's an actual ping game lol)
# TODO : add sound effects to collisions (in GameObject class) ?
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)

async def debugTester( Initialiser ):

	game = Initialiser()
	game.debugMode = True
	game.addPlayer( "Tester 1" )
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
			for i in range( len( game.controlers )):
				if game.controlers[i].mode == ad.PLAYER:
					game.controlers[i].handleKeyInput( event.key ) # first game controler, aka player 1


def takeGameStep( game ):
	game.step()

	if game.debugMode:
		debugPlayerControler( game )

	game.clock.tick ( game.framerate )

if __name__ == '__main__':
	#asy.run(debugTester( Pong ))
	asy.run(main())


#
#	GameLoop()
#	{
#		initGame()
#		addPlayers()
#		startGame()
#			sendStartState()
#
#		while (isRunning)
#			stepGame()
#				updateObjects()
#				makeBotsPlay()
#				sendUpdateInfo() 			OR: renderScreen() (debug)
#
#		deleteGame()
#			sendEndState()
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