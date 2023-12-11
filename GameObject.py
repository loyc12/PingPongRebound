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

	def __init__( self, _id, _game, _x, _y, _w, _h ):
		self.game = _game
		self.id = _id
		self.setSpeeds( 0, 0 )
		self.setDirs( 0, 0 )
		self.setSize( _w, _h )
		self.setPos( _x, _y )

		if( cfg.DEBUG_MODE ):
			self.box = pg.Rect( _game.width / 2, _game.height / 2, _w, _h )# 	NOTE : DEBUG

	def drawSelf( self ): # 														NOTE : DEBUG
		if( cfg.DEBUG_MODE ):
			self.box.center = ( self.px, self.py )
			pg.draw.rect( self.game.win, df.COL_OBJ, self.box )
		else:
			print( "GameObject.drawSelf()is a DEBUG_MODE function" )

	def getCopy( self ):

		copy = GameObject( self.id, self.game, self.px, self.py, self.sx, self.sy )
		copy.setSpeeds( self.dx, self.dy )
		copy.setDirs( self.fx, self.fy )

		return copy


# ---------------------------------------------- POSITION ---------------------------------------------- #

	def setSize( self, _w, _h ):
		self.sx = int( _w / 2 )
		self.sy = int( _h / 2 )

	def getSize( self ):
		return( int( self.sx ), int( self.sy ))


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


	def updatePos( self, max_speed ):
		# makes sure the dx and dy are positive
		self.clampSpeed()

		# moving on x
		if self.fx != 0:
			if abs( self.dx * self.fx ) > max_speed:
				if self.dx > max_speed:
					self.dx = max_speed
				self.px += max_speed * df.getSign( self.fx )
			else:
				self.px += self.dx * self.fx

		# moving on y
		if self.fy != 0:
			if abs( self.dy * self.fy ) > max_speed:
				if self.dy > max_speed:
					self.dy = max_speed
				self.py += max_speed * df.getSign( self.fy )
			else:
				self.py += self.dy * self.fy

		self.px = int( self.px )
		self.py = int( self.py )


	def clampPos( self ):
		# prevent balls from going off screen
		if self.getLeft() < 0:
			self.setLeft( 0 )
		if self.getRight() > self.game.width:
			self.setRight( self.game.width )
		if self.getTop() < 0:
			self.setTop( 0 )
		if self.getBottom() > self.game.height:
			self.setBottom( self.game.height )

	def isInScreen( self ):
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
		if self.getRight() >= other.getLeft()and self.getLeft() <= other.getRight():
			if self.getBottom() >= other.getTop()and self.getTop() <= other.getBottom():
				return True
		return False

	# NOTE : IS ONLY FOR BALLS
	def bounceOnWall( self, mode ):
		if mode == "stop":
			self.stopDirs()
		elif mode == "x":
			self.fx *= -1
			self.dx *= self.game.factor_wall
		elif mode == "y":
			self.fy *= -1
			self.dy *= self.game.factor_wall

		self.clampSpeed()
		if df.BOT_NO_STUCK:
			self.makeUnstuck( mode )


	# NOTE : IS ONLY FOR BALLS
	def bounceOnRack( self, other, mode ):
		t = time.time() - self.game.start_time
		if mode == "x":
			self.fx *= -1
			self.dx *= self.game.factor_rack
			self.dy += other.getMvY() * self.fy
		elif mode == "y":
			self.fy *= -1
			self.dy *= self.game.factor_rack
			self.dx += other.getMvX() * self.fx

		if cfg.PRINT_COLLISIONS:
			print( f"{self.game.gameID} )  {self.game.name}  \t: {'{:.1f}'.format( t )}s" )# 	NOTE : DEBUG

		self.clampSpeed()
		if df.BOT_NO_STUCK:
			self.makeUnstuck( mode )



	def makeUnstuck( self, mode ):
		if mode == "stop":
			return

		elif mode == "x" and self.dx < 1:
			self.dx = 1

			if self.px < self.game.width / 2:
				self.fx = 1
			else:
				self.fx = -1

		elif mode == "y" and self.dy  < 1:
			self.dy = 1

			if self.py < self.game.height / 2:
				self.fy = 1
			else:
				self.fy = -1


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
		# make sure dy and dx are positive
		if self.dy < 0:
			self.dy *= -1
			self.fy *= -1
		if self.dx < 0:
			self.dx *= -1
			self.fx *= -1


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