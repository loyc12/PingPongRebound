class Adder:

	# ------------------------------------------- INITIALIZATION ------------------------------------------- #

	def __init__(self):

		self.valueToAdd = 0
		self.currentValue = 0
		self.running = False

	def reset(self):

		self.running = False
		self.valueToAdd = 0
		self.currentValue = 0

	# ---------------------------------------------- INTERFACE --------------------------------------------- #

	def giveInput(self, value):
		self.valueToAdd = value

	# ---------------------------------------------- CORE CMDS --------------------------------------------- #

	def start(self):
		self.running = True
		print("Starting adder " + self.name)

	def stop(self):
		self.running = False
		print("Stopping adder " + self.name)

	def run(self):

		if self.running == False:
			print("Adder is not running")
			return

		# main loop
		while self.running:
			self.step()

		print("Adder is finished")

	def getState(self):
		return ( self.currentValue, self.valueToAdd)

	def step(self):

		print(f"Adding : {self.nextValue} + {self.currentValue}")

		self.currentValue += self.nextValue
		self.next_value = 0

		print(f"Result : {self.currentValue}")
		print(f" ")

		self.clock.tick ()

