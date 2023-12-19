import time #				NOTE : DEBUG
try:
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg
	import defs as df
except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	import game.PingPongRebound.defs as df


# ------------------------------------------ GAMEOBJECT CLASS ------------------------------------------ #


# object class
class GameObject:

	( dx, fx, px, sx ) = ( 0, 0, 0, 0 )
	( dy, fy, py, sy ) = ( 0, 0, 0, 0 )

	def __init__( self, _id, _game, _x, _y, _w, _h, _maxSpeed = 160 ): #_type = df.OBJ_BASE ):
		self.game = _game
		self.id = _id
		self.setSize( int( _w ), int ( _h ))
		self.setPos( int( _x ), int( _y ))
		self.maxSpeed = int( _maxSpeed )
		self.setDirs( 0, 0 )
		self.setSpeeds( 0, 0 )
		#self.type = _type

		if cfg.DEBUG_MODE:
			self.box = pg.Rect( _game.width / 2, _game.height / 2, _w, _h )


	def getCopy( self ):

		copy = GameObject( self.id, self.game, self.px, self.py, self.sx, self.sy, self.maxSpeed )
		copy.setSpeeds( self.dx, self.dy )
		copy.setDirs( self.fx, self.fy )

		return copy


	def drawSelf( self ): # 										NOTE : DEBUG
		if cfg.DEBUG_MODE:
			self.box.center = ( self.px, self.py )
			pg.draw.rect( self.game.win, df.COL_OBJ, self.box )
		else:
			print( "GameObject.drawSelf() is a DEBUG_MODE function" )


# ---------------------------------------------- POSITION ---------------------------------------------- #


	def setSize( self, _w, _h ): #		NOTE : .sx and .sy are half lenghts
		self.sx = int( _w / 2 )
		self.sy = int( _h / 2 )

	def getSize( self ):
		return( int( 2 * self.sx ), int( 2 * self.sy ))


	def setLeft( self, _x ):
		self.px = int( _x + self.sx )

	def setRight( self, _x ):
		self.px = int( _x - self.sx )

	def setTop( self, _y ):
		self.py = int( _y + self.sy )

	def setBottom( self, _y ):
		self.py = int( _y - self.sy )


	def getLeft( self ):
		return int( self.px - self.sx )

	def getRight( self ):
		return int( self.px + self.sx )

	def getTop( self ):
		return int( self.py - self.sy )

	def getBottom( self ):
		return int( self.py + self.sy )


	def setPos( self, _x, _y ):
		self.px = int( _x )
		self.py = int( _y )

	def setPosX( self, _x ):
		self.px = int( _x )

	def setPosY( self, _y ):
		self.py = int( _y )


	def getPos( self ):
		return( self.px, self.py )

	def getPosX( self ):
		return self.px

	def getPosY( self ):
		return self.py


	def updatePos( self ):
		self.clampSpeed()

		self.px += self.dx * self.fx
		self.py += self.dy * self.fy

		self.px = int( self.px )
		self.py = int( self.py )


	def clampPos( self ):

		# prevent balls from going off screen
		if self.getLeft() < 0:
			self.setLeft( 0 )
			if cfg.PRINT_DEBUG:
				print( "clamping pos to left" )
		if self.getRight() > self.game.width:
			self.setRight( self.game.width )
			if cfg.PRINT_DEBUG:
				print( "clamping pos to right" )
		if self.getTop() < 0:
			self.setTop( 0 )
			if cfg.PRINT_DEBUG:
				print( "clamping pos to top" )
		if self.getBottom() > self.game.height:
			self.setBottom( self.game.height )
			if cfg.PRINT_DEBUG:
				print( "clamping pos to bottom" )


	def isOnScreen( self ):
		if self.getLeft() < 0 or self.getRight() > self.game.width:
			return False
		if self.getTop() < 0 or self.getBottom() > self.game.height:
			return False
		return True

	def isOnScreenX( self ):
		if self.getLeft() < 0 or self.getRight() > self.game.width:
			return False
		return True

	def isOnScreenY( self ):
		if self.getTop() < 0 or self.getBottom() > self.game.height:
			return False
		return True


# ---------------------------------------------- COLLISION --------------------------------------------- #


	def isOverlaping( self, other ):
		if self.getRight() >= other.getLeft() and self.getLeft() <= other.getRight():
			if self.getBottom() >= other.getTop() and self.getTop() <= other.getBottom():
				return True
		return False


	def bounceOnWall( self, mode ):
		if mode == "stop":
			self.stopDirs()
			return

		# vertical surface bounces ( | )
		elif mode == "x":
			self.fx *= -1
			self.dx *= self.game.factor_wall
			if cfg.PRINT_DEBUG:
				print ( "bouncing on x" )

		# horizontal surface bounces ( -- )
		elif mode == "y":
			self.fy *= -1
			self.dy *= self.game.factor_wall
			if cfg.PRINT_DEBUG:
				print ( "bouncing on y" )

		self.clampSpeed()
		if df.NO_STUCK_BALLS:
			self.makeUnstuck()


	# NOTE : IS ONLY FOR BALLS
	def bounceOnRack( self, other, mode ):

		# vertical surface bounces ( | )
		if mode == "x":
			self.fx *= -1
			self.dx *= self.game.factor_rack
			self.dy = int( self.dy + ( other.getMvY() * df.KICK_FACTOR * df.getSign( self.fy )))

		# horizontal surface bounces ( -- )
		elif mode == "y":
			self.fy *= -1
			self.dy *= self.game.factor_rack
			self.dx = int( self.dx + ( other.getMvX() * df.KICK_FACTOR * df.getSign( self.fx )))

		if cfg.PRINT_COLLISIONS:
			t = time.time() - self.game.start_time
			print( f"{self.game.gameID} )  {self.game.name}  \t: racket bounce at {'{:.1f}'.format( t )}s" )# 	NOTE : DEBUG

		self.clampSpeed()
		if df.NO_STUCK_BALLS:
			self.makeUnstuck()


	def makeUnstuck( self ):

		if self.dy < 1:
			self.dy = 1

			if self.py < self.game.height / 2:
				self.fy = 1
			else:
				self.fy = -1

			if cfg.PRINT_DEBUG:
				print( "unstuck on x" )

		if  self.dx < 1:
			self.dx = 1

			if self.px < self.game.width / 2:
				self.fx = 1
			else:
				self.fx = -1

			if cfg.PRINT_DEBUG:
				print( "unstuck on y" )


# ---------------------------------------------- MOVEMENT ---------------------------------------------- #


	def setSpeeds( self, _dx, _dy ):
		self.dx = _dx
		self.dy = _dy
		self.clampSpeed()

	def getSpeeds( self ):
		return( self.dx, self.dy )


	def setDirs( self, _fx, _fy ):
		self.fx = _fx
		self.fy = _fy

	def getDirs( self ):
		return( self.fx, self.fy )


	def getMove( self ):
		return( self.fx * self.dx, self.fy * self.dy )

	def getMvX( self ):
		return( self.fx * self.dx )

	def getMvY( self ):
		return( self.fy * self.dy )


	def stopSpeeds( self ):
		self.dx = 0
		self.dy = 0

	def stopDirs( self ):
		self.fx = 0
		self.fy = 0


	def clampSpeed( self ):
		# making sure dx is positive
		if self.dy < 0:
			self.dy *= -1
			self.fy *= -1

		# making sure dy is positive
		if self.dx < 0:
			self.dx *= -1
			self.fx *= -1

		self.checkMaxSpeed()


	def checkMaxSpeed( self ):
		# checking on x
		if abs( self.dx * self.fx ) > self.maxSpeed:
			if self.dx > self.maxSpeed: # 				NOTE : handling for balls (variable dx/dy)
				self.dx = self.maxSpeed

			else: # 									NOTE : handling for rackets (variable fx/fy)
				while abs( self.dx * self.fx ) > self.maxSpeed:
					self.fx -= df.getSign( self.fx )

			if cfg.PRINT_DEBUG:
				print( "clamping speed on x" )

		# checking on y
		if abs( self.dy * self.fy ) > self.maxSpeed:
			if self.dy > self.maxSpeed: # 				NOTE : handling for balls (variable dx/dy)
				self.dy = self.maxSpeed

			else: # 									NOTE : handling for rackets (variable fx/fy)
				while abs( self.dy * self.fy ) > self.maxSpeed:
					self.fy -= df.getSign( self.fy )

			if cfg.PRINT_DEBUG:
				print( "clamping speed on y" )


# ---------------------------------------------- DIRECTION --------------------------------------------- #

	def isGoingLeft( self ):
		if self.fx < 0:
			return True
		return False

	def isGoingRight( self ):
		if self.fx > 0:
			return True
		return False

	def isGoingUp( self ):
		if self.fy < 0:
			return True
		return False

	def isGoingDown( self ):
		if self.fy > 0:
			return True
		return False


	def isLeftOfX( self, X ):
		if self.getRight() < X:
			return True
		return False

	def isRightOfX( self, X ):
		if self.getLeft() > X:
			return True
		return False

	def isAboveY( self, Y ):
		if self.getBottom() < Y:
			return True
		return False

	def isBelowY( self, Y ):
		if self.getTop() > Y:
			return True
		return False


	def isLeftOf( self, other ):
		return self.isLeftOfX( other.getLeft() )

	def isRightOf( self, other ):
		return self.isRightOfX( other.getRight() )

	def isAbove( self, other ):
		return self.isAboveY( other.getTop() )

	def isBelow( self, other ):
		return self.isBelowY( other.getBottom() )