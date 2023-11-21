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

	playerID = 0 #									NOTE : DEBUG

	def __init__( self ):
		self.lastGameID = 0
		self.gameCount = 0
		self.runGames = True
		self.gameDict = {}


	def addGame( self, Initialiser, GameID): #		TODO : take game id as argument instead

		newGame = Initialiser()
		newGame.debugMode = True #					NOTE : DEBUG

		self.gameDict[GameID] = newGame
		self.gameCount += 1

		return GameID



	def removeGame( self, key ):
		self.gameDict[key].stop()
		self.gameDict.pop(key)
		self.gameCount -= 1


	def startGame( self, key ):
		#self.gameDict[key].addPlayer( "Player " + str( key ))
		self.gameDict[key].start()


	async def tickGames(self):
		for key in self.gameDict.keys():
			game = self.gameDict[key]
			if game.over:
				self.removeGame( game.id )
			elif game.running:
				self.runGameStep( game )
				if key == self.playerID:
					self.displayGame( game )

		await asy.sleep(0)


	def runGameStep( self, game ):
		if game.running:

			game.moveObjects()
			game.makeBotsPlay()
			game.clock.tick (game.framerate) # 	TODO : detach from pygame

			#print ( game.getInfo() )

		else:
			print (" This game is not running")

	def displayGame( self, game ): # 			TODO : detach from pygame
		if game.running:
			game.refreshScreen()
		else:
			print (" This game is not running")


	def takePlayerInputs( self ): # 			NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				# closes the game # 						NOTE : DEBUG
				if event.key == pg.K_ESCAPE:
					for game in self.gameDict.values():
						game.stop()
					self.runGames = False
					sys.exit()

				# switches game to control # 						NOTE : DEBUG
				if event.key == pg.K_0:
					print ("please select a valid game (1-8)")

				# switches game to control # 						NOTE : DEBUG
				elif event.key == pg.K_1 or event.key == pg.K_2 or event.key == pg.K_3 or event.key == pg.K_4 or event.key == pg.K_5 or event.key == pg.K_6 or event.key == pg.K_7 or event.key == pg.K_8 or event.key == pg.K_9:
					if event.key == pg.K_1:
						self.playerID = 1
					elif event.key == pg.K_2:
						self.playerID = 2
					elif event.key == pg.K_3:
						self.playerID = 3
					elif event.key == pg.K_4:
						self.playerID = 4
					elif event.key == pg.K_5:
						self.playerID = 5
					elif event.key == pg.K_6:
						self.playerID = 6
					elif event.key == pg.K_7:
						self.playerID = 7
					elif event.key == pg.K_8:
						self.playerID = 8
					elif event.key == pg.K_9:
						self.playerID = 9
					print ("now playing in game #" + str( self.playerID ))


					try:
						game = self.gameDict[self.playerID]
						game.win = pg.display.set_mode((game.width, game.height)) # 	TODO : detach from pygame
					except:
						print ("Could not switch to game #" + str( self.playerID ))
						print ("now playing nobody")
						self.playerID = 0

				# handling game movement keys
				else:
					if self.playerID > 0 and self.playerID < 6 and self.gameDict[self.playerID] and self.gameDict[self.playerID].controlers[0].mode == ad.PLAYER:
						self.gameDict[self.playerID].controlers[0].handleKeyInput(event.key)
					else:
						print ("Could not pass input from player for game #" + str( self.playerID ))


def main():
	gm = GameManager()

	addAllGames( gm )

	while gm.runGames:

		gm.takePlayerInputs()

		asy.run( gm.tickGames() ) # ASYNNC IS HERE

if __name__ == '__main__':
	main()


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


