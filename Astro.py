import pygame as pg
import GameObject as go
import GameInterface as gi

class Astro(gi.Game):
	name = "Astro"
	width = 1280
	height = 1280


if __name__ == '__main__':
	g = Astro()
	g.start()
	g.run()