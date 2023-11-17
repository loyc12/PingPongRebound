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

class GameManager:

	playerID = 0

	def __init__( self ):
		self.lastGameID = 0
		self.gameCount = 0
		self.keep_going = True
		self.gameDict = {}


	def addGame( self, Initialiser ):

		# reset gameIDs when no game is running
		if (self.gameCount == 0):
			self.lastGameID = 0

		newGame = Initialiser()
		self.lastGameID += 1
		self.gameCount += 1
		self.gameDict[self.lastGameID] = newGame

		return self.lastGameID


	def removeGame( self, key ):
		self.gameDict[key].stop()
		self.gameDict.pop(key)
		self.gameCount -= 1

		# reset gameIDs when no game is running
		if (self.gameCount == 0):
			self.lastGameID = 0


	def startGame( self, key ):
		self.gameDict[key].addPlayer( "Player " + str( key ))
		self.gameDict[key].start()


	async def tickGames(self):
		for game in self.gameDict.values():
			if game.over:
				self.removeGame( game.id )
			elif game.running:
				self.runGameStep( game )

		await asy.sleep(0)


	def runGameStep( self, game ):
		if game.running:

			game.step()
			game.clock.tick (game.framerate) # 	TODO : detach from pygame

			#print ( game.getInfo() )

		else:
			print (" This game is not running")


	def takePlayerInputs( self ): # 								NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				# closes the game # 								NOTE : DEBUG
				if event.key == pg.K_ESCAPE:
					for game in self.gameDict.values():
						game.stop()
					self.keep_going = False

				# switches game to control # 						NOTE : DEBUG
				if event.key == pg.K_0:
					self.playerID = 0
					print ("now playing noody")
				elif event.key == pg.K_1:
					self.playerID = 1
					print ("now playing in game #" + str( self.playerID ))
				elif event.key == pg.K_2:
					self.playerID = 2
					print ("now playing in game #" + str( self.playerID ))
				elif event.key == pg.K_3:
					self.playerID = 3
					print ("now playing in game #" + str( self.playerID ))
				elif event.key == pg.K_4:
					self.playerID = 4
					print ("now playing in game #" + str( self.playerID ))
				elif event.key == pg.K_5:
					self.playerID = 5
					print ("now playing in game #" + str( self.playerID ))

				# handling game movement keys
				else:
					if self.playerID > 0 and self.playerID < 6 and self.gameDict[self.playerID] and self.gameDict[self.playerID].controlers[0].mode == ad.PLAYER:
						self.gameDict[self.playerID].controlers[0].handleKeyInput(event.key)
					else:
						print ("Could not pass input from player for game #" + str( self.playerID ))


def main():
	gm = GameManager()

	gm.startGame( gm.addGame( Ping ))
	gm.startGame( gm.addGame( Pong ))

	print ("select a player (1 to 5)")

	while gm.keep_going:

		gm.takePlayerInputs()

		asy.run( gm.tickGames() ) # ASYNNC IS HERE

if __name__ == '__main__':
	main()





