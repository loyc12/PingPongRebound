import pygame as pg
import GameObject as go
from Pong import rack_1, rack_2 #	set to the game you are using this with

# ----------------------------------------- GAMEINTERFACE CLASS ---------------------------------------- #

def moveRack(target_id, move ):
	global rack_1, rack_2

	print(f" > base factors == {rack_1.fx}:{rack_2.fy}")

	if (target_id <= 0):
		print("Error: no target selected")
		return
	for rack in [rack_1, rack_2]:
		if (rack.id == target_id):
			if (move == "LEFT"):
				if (go.hard_break and rack.fx > 0):
					rack.fx = 0
				else:
					rack.fx -= 1
			elif (move == "RIGHT"):
				if (go.hard_break and rack.fx < 0):
					rack.fx = 0
				else:
					rack.fx += 1
			elif (move == "UP"):
				if (go.hard_break and rack.fy > 0):
					rack.fy = 0
				else:
					rack.fy -= 1
			elif (move == "DOWN"):
				if (go.hard_break and rack.fy < 0):
					rack.fy = 0
				else:
					rack.fy += 1
			elif (move == "STOP"):
				rack.fx == 0
				rack.fy == 0
			else:
				print("Error: invalid move")
				return
			print(f"Moved rack_{target_id} {move} successfully")
			print(f" > speed factors == {rack.fx}:{rack.fy}")

# 	TODO : make a function that sends the state of the game (rackets + balls + points)
