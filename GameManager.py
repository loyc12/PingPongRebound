from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest
from Pongester import Pongester
from GameInterface import Game

import pygame as pg
import asyncio as asy
import Addons as ad
import sys

class GameManager:

	playerID = 0 #							NOTE : DEBUG
	debugMode = True #						NOTE : DEBUG

	def __init__( self ):
		self.lastGameID = 0
		self.gameCount = 0
		self.runGames = True
		self.gameDict = {}


	def addGame( self, Initialiser, GameID):

		newGame = Initialiser( self.win, pg.time.Clock(), self.debugMode ) # 	TODO : detach from pygame
		self.gameDict[GameID] = newGame
		self.gameCount += 1

		self.addPlayer( GameID, "Player " + str( GameID ), GameID ) #			NOTE : DEBUG

		return GameID


	def addPlayer( self, key, name, _playerID ):
		try:
			self.gameDict.get(key).addPlayer( name, _playerID )
		except:
			print ("Could not add player #" + str( _playerID ) + " to game #" + str( key ))


	def removePlayer( self, key, _playerID ):
		#try:
		#	self.gameDict.get(key).removePlayer( _playerID )
		#except:
		#	print ("Could not remove player #" + str( _playerID ) + " from game #" + str( key ))
		pass


	def startGame( self, key ):
		#self.gameDict.get(key).addPlayer( "Player " + str( key ))
		self.gameDict.get(key).start()


	def pauseGame( self, key ):
		#self.gameDict.get(key).addPlayer( "Player " + str( key ))
		self.gameDict.get(key).pause()


	def removeGame( self, key ):
		self.gameDict.get(key).close()
		self.gameDict.pop(key)
		self.gameCount -= 1



	def tickGames(self):
		for key in self.gameDict.keys():
			game = self.gameDict.get(key)

			if game.isOver:
				self.removeGame( game.id )
			elif game.isRunning:
				self.runGameStep( game )

				if self.debugMode: #				NOTE : DEBUG
					if key == self.playerID:
						self.displayGame( game )


	def runGameStep( self, game ):
		if game.isRunning:

			game.moveObjects()
			game.makeBotsPlay()
			game.clock.tick (game.framerate) # 	TODO : detach from pygame

			#print ( game.getInfo() )

		else:
			print (" This game is not running")

	def displayGame( self, game ): # 			NOTE : DEBUG
		if game.isRunning:
			if game.width != self.win.get_width() or game.height != self.win.get_height(): # 		TODO : detach from pygame
				self.win = pg.display.set_mode( (game.width, game.height) )
				pg.display.set_caption( game.name ) #

			game.refreshScreen()
		else:
			self.win.fill( self.col_bgr )
			print (" This game is not running")


	def takePlayerInputs( self ): # 			NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				k = event.key

				# closes the game
				if k == pg.K_ESCAPE:
					for game in self.gameDict.values():
						game.close()
					self.runGames = False
					sys.exit()

				# respawns the ball
				elif k == pg.K_RETURN:
					try:
						game = self.gameDict.get(self.playerID)
						game.respawnAllBalls()
						#game.respawnBall( game.balls[0] )
					except:
						print ( "coud not respawn the ball" )

				# switches game to control
				elif k == pg.K_0:
					print ("please select a valid game (1-8)")
					self.playerID = 0
					self.emptyDisplay()

				# switches game to control
				elif k == pg.K_1 or k == pg.K_2 or k == pg.K_3 or k == pg.K_4 or k == pg.K_5 or k == pg.K_6 or k == pg.K_7 or k == pg.K_8 or k == pg.K_9:
					if k == pg.K_1:
						self.playerID = 1
					elif k == pg.K_2:
						self.playerID = 2
					elif k == pg.K_3:
						self.playerID = 3
					elif k == pg.K_4:
						self.playerID = 4
					elif k == pg.K_5:
						self.playerID = 5
					elif k == pg.K_6:
						self.playerID = 6
					elif k == pg.K_7:
						self.playerID = 7
					elif k == pg.K_8:
						self.playerID = 8
					elif k == pg.K_9:
						self.playerID = 9
					print ("now playing in game #" + str( self.playerID ))

					try:
						self.gameDict.get(self.playerID).controlerCount += 0
					except:
						print ("Could not switch to game #" + str( self.playerID ))
						print ("no longer playing in any game")
						self.playerID = 0
						self.emptyDisplay()

				# handling game movement keys
				else:
					try:
						controler = self.gameDict.get(self.playerID).controlers[0]
						if controler.mode == ad.PLAYER:
							controler.handleKeyInput(k)
						else:
							print ("rack 1 is a bot")
					except:
						print ("Could not pass input from player for game #" + str( self.playerID ))


	def emptyDisplay( self ):
		pg.display.set_caption("Game Manager") # 			NOTE : DEBUG
		self.win = pg.display.set_mode((2048, 1280)) # 		NOTE : ...
		self.win.fill( pg.Color('black') ) # 				NOTE : ...


async def main():  # ASYNC IS HERE

	gm = GameManager()

	if (gm.debugMode):
		pg.init() # 										NOTE : DEBUG
		pg.display.set_caption("Game Manager") # 			NOTE : ...
		gm.win = pg.display.set_mode((2048, 1280)) # 		NOTE : ...
		gm.win.fill( pg.Color('black') ) # 					NOTE : ...

	addAllGames( gm )

	while gm.runGames:

		if gm.debugMode:
			gm.takePlayerInputs()

		gm.tickGames()

	await asy.sleep(0)


def addAllGames( gm ):
	gameID = 1

	gm.startGame( gm.addGame( Game, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Ping, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pinger, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pingest, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pong, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Ponger, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pongest, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pongester, gameID ))
	gameID += 1

	print ("select a player (1-8)")

if __name__ == '__main__':
	asy.run( main())


