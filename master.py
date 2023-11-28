try:
	import cfg
	if cfg.DEBUG_MODE:
		import pygame as pg
	import GameControler as gc
	import GameObject as go
	import GameInterface as gi

except ModuleNotFoundError:
	import game.PingPongRebound.GameControler as gc
	import game.PingPongRebound.GameObject as go
	import game.PingPongRebound.GameInterface as gi