import pygame as pg
import GameObject as go
import GameInterface as gi

class Astro(gi.Game):
	name = "Astro"
	width = 1024
	height = 1024

	raise NotImplementedError("Unimplemented : Astro")


if __name__ == '__main__':
	g = Astro()
	g.start()
	g.run()