__author__ = "Kyle Kung"

#### Dependencies ###############################3
from GWENGui_Engine import *

##################################################
class GWENGui(GWENGui):
	def __init__(self, title='Test Gui'):
		super().__init__(title)
		self.buildGui()
		self.launch()

	def buildGui(self):
		self.addButton('Test1', None)
		self.addButton('Test2', None)
		self.endRow()

##################################################
if __name__ == "__main__":
	GWENGui()