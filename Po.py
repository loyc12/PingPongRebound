import pygame as pg
import GameObject as go
import GameInterface as gi

class Po(gi.Game):
	name = "Po"

	width = 1280
	height = 1280

	factor_rack = 1.2
	factor_wall = 0.9

	score_mode = gi.ad.HITS



if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Po(1, True)

	g.setWindow(pg.display.set_mode((1280, 1280)))
	pg.display.set_caption(g.name)

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()