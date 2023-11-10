import GameControler as gc
import pygame as pg

# controler class
class PlayerControler(gc.GameControler):


	def playStep(self):
		# using ai move instead (if set to auto play)

		self.playMove( self.next_move )

	def handleKeyInput(self, key):
		if key == pg.K_SPACE or key == pg.K_KP0:
			self.playMove( self.game.STOP )
		elif key == pg.K_w or key == pg.K_UP:
			self.playMove( self.game.UP )
		elif key == pg.K_d or key == pg.K_RIGHT:
			self.playMove( self.game.RIGHT )
		elif key == pg.K_s or key == pg.K_DOWN:
			self.playMove( self.game.DOWN )
		elif key == pg.K_a or key == pg.K_LEFT:
			self.playMove( self.game.LEFT )
		elif (key != pg.K_SPACE):
			print("Error: invalid move")
