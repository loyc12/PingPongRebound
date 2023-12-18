import asyncio as asy

try:
	from games import *
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg

except ModuleNotFoundError:
	from game.PingPongRebound.games import *
	import game.PingPongRebound.cfg as cfg


# MASTER LIST
# TODO : rework ball respawn in pongest
# TODO : have respawn trajectories be stored in an array in game interface

# FUNCTION LIST

# DEBUG LIST

# MINOR LIST
# TODO : swap racket 2 and 3 in pingest (breaks client side for now)
# TODO : make obstacles type GameObjects in the base class( and use them in pongester )
# TODO : add sound effects to collisions( in GameObject class )
# TODO : make an 'asteroids' game( solo )

async def debugTester( Initialiser ):

	if cfg.DEBUG_MODE:
		pg.init()
		g = Initialiser( 1 )

		g.setWindow( pg.display.set_mode(( g.width, g.height )))
		pg.display.set_caption( g.name )

		if cfg.ADD_DEBUG_PLAYER:
			g.addPlayer( "Player 1", 1 )

		g.start()

		await g.run()

	else:
		print( "Cannot run game : debug mode is off" )


if __name__ == '__main__':
	asy.run( debugTester( Pingest ))





# client requests a tournament
# backend adds players to the tournament

# backend instanciates the tournament
# tournament starts

# backend instanciates 2 games
# tournament gets the gameIDs
# games start and close
# tournament gets the results
# tournament sends the results

# backend instanciates 2 games
# tournament gets the gameIDs
# games start and close
# tournament gets the results
# tournament sends the results

# tournament closes



# passive (like matchMaker) ?
# needs:
# 4 players
# 4 games (with connectors)

class tournamentManager:

	players = {
		"player1" : [ "won", "won" ],
		"player2" : [ "won", "lost" ],
		"player3" : [ "lost", "won" ],
		"player4" : [ "lost", "lost" ]}

	games = {
		"game1A" : [ "player1", "player3" ],
		"game1B" : [ "player2", "player4" ],
		"game2A" : [ "player1", "player2" ],
		"game2B" : [ "player3", "player4" ]}

	#games = [ "player1", "player2", "player3", "player4", "winner1", "winner2", "loser1", "loser2" ]

	def __init__( self, _gameManager, _gameType, players ):
		self.gm = _gameManager
		self.gameType = _gameType


	def runTourn( self ):
		pass


	def addTournGame( self, gameID, connector, p1, p2 ):
		self.gm.addGame( self.gameTypem, gameID, connector )

		self.gm.addPlayerToGame( p1.id, p1.name, gameID )
		self.gm.addPlayerrToGame( p2.id, p2.name, gameID )


