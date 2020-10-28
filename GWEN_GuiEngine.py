#   .d8888b.  888       888 8888888888 888b    888 
#  d88P  Y88b 888   o   888 888        8888b   888 
#  888    888 888  d8b  888 888        88888b  888 
#  888        888 d888b 888 8888888    888Y88b 888 
#  888  88888 888d88888b888 888        888 Y88b888 
#  888    888 88888P Y88888 888        888  Y88888 
#  Y88b  d88P 8888P   Y8888 888        888   Y8888 
#   "Y8888P88 888P     Y888 8888888888 888    Y888 
#                                                
# GWEN (Gui Widgets EngiNe)  
#                                                                                           
# GWENGui_Engine.py
#
# Authors: Mundo Guzman, Kyle Kung, Cole Meyers  |   Maintainer: Kyle Kung
#
# https://github.com/krkung/GWEN
#
# Framework built to rapidly created PyQt5 GUI Applications.
# A normal work flow begins with creating a GWENGui() object, followed by a series
# of addWidget() function calls, and ends with a .launch() command.
#
#### Git Commit Identifier ####################################################################
import os
try: 
	from pydriller import RepositoryMining
	path = str(os.getcwd())
	commits = RepositoryMining(path, filepath='GWENGui_Engine.py').traverse_commits()
	commits = [commit.hash for commit in commits]
	commit_tag = commits[-1]

	print('Using Gui Library from commit {}'.format(commit_tag))

except:
	print('Git commit tag cannot be found.')
###############################################################################################

# Gui Library Dependencies
from GWEN_GuiObjects import *
import sys

###########################################################################################################
def _delete_(clean_up):
	""" Function to be called when gui exits. clean_up will run before class goes to garbage """
	try: app.exec_()
	finally: 
		if clean_up != None:
			clean_up()


# Necessary PyQt call
app = QtWidgets.QApplication(sys.argv)


class GWENGui(QtWidgets.QMainWindow):
	""" Wrapper class around a PyQtGui QMainWIndow. Instantiating this class should provide the skeleton
	needed for the GUI window. This will be filled out by various addWidget functions.
	"""
	def __init__(self, title='GWENGui'):
		""" Class Constructor. Calls super constructor """
		super().__init__()
		self.title = title

		# Create central widget
		self.centralWidget = QtWidgets.QWidget(self)
		self.setCentralWidget(self.centralWidget)

		# Create lists to hold Gui Widgets, Plots, Labels, and Divies
		self.widgets    = list()
		self.labels     = list()
		self.divies     = list()

		# Create tabs object in case user wants to include tabs
		self.tabs 		= QtWidgets.QTabWidget()
		self.miniTabs	= QtWidgets.QTabWidget()
		self.groupBox 	= QtWidgets.QGroupBox()

		# Number of objects since last Divie
		self.divieSize = 0
		self.mini = False
		self.is_tab = False
		
		# Call Initialize Function
		self.initializeUI()


	def initializeUI(self):
		""" Setups Window """
		self.setWindowTitle(self.title)
		self.move(0,0)
		self.statusBar().showMessage('Ready.')


	def launch(self, clean_up=None):   
		# Create grid layout
		self.createLayout()
		# Display the GUI
		self.show()
		# System call to execute QApplication
		sys.exit(_delete_(clean_up))


	#################################### Layout Functions ###############################################

	def createLayout(self):
		""" GWEN Gui Layout manager function that is called in the launch function. This function
		will create grid layout by reading in the series of addWidget and divies functions that the user specifies.
		Refer to GWENGui_Documentation for more info on how the Gui is created in rowation to the divies calls.
		"""
		# If there are no divies then add an endCol (Creates a vertical layout)
		if not self.divies:
			self.endCol()

		# Create new widget to hold grid layout
		self.gridLayout = QtWidgets.QGridLayout()

		# Establish variables for grid layout manager
		widgetPtr	= 0	# Pointer to widget in list you are at
		row 		= 0 # Pointer to the row in the grid you are currently at
		col 		= 0 # Pointer to the col in the grid you are currently at
		nextRow		= 0 # Row where a endCol() call would reference you to
		nextCol 	= 0 # Col where a endRow() call would reference you to
		newRow 		= 0 # Row where a newCol() call would reference you to
		newCol 		= 0 # Col where a newRow() call would reference you to
		rowSize		= 0
		colSize		= 0

		# DEBUG MESSAGES
		# print('R:{} C:{}'.format(str(row),str(col)))
		# print('nextRow: {} nextCol: {}'.format(str(nextRow),str(nextCol)))
		# print('newRow: {} newCol: {}'.format(str(newRow),str(newCol)))

		# Begin loop for layout manager
		for divie in self.divies:

			# assign row/col indices
			row = nextRow
			col = nextCol

			# End Row will start grid layout on next available Row
			if divie.type == 'endRow':

				if divie.size == 0:
					pass

				else:
					# DEBUG MESSAGES
					# print('\nendRow has size: ' + str(divie.size))

					# Will loop over all widgets in range from first available widget to dim of divie
					for index,widget in enumerate(self.widgets[widgetPtr:widgetPtr+divie.size]):
						# label exists then 
						if self.labels[index+widgetPtr]:
							# Construct mini Vertical Layout to put label and widget in same grid
							miniVLayout = QtWidgets.QVBoxLayout()
							miniVLayout.addWidget(self.labels[index+widgetPtr],alignment=QtCore.Qt.AlignCenter)
							miniVLayout.addWidget(widget,alignment=QtCore.Qt.AlignCenter)
							# Add newly created vertical layout to grid layout
							self.gridLayout.addLayout(miniVLayout,row,col,widget.dim[0],widget.dim[1],alignment=QtCore.Qt.AlignCenter)

						else:
							# Widgets that don't have any labels
							self.gridLayout.addWidget(widget,row,col,widget.dim[0],widget.dim[1],alignment=QtCore.Qt.AlignCenter)

						# DEBUG MESSAGES
						# print('R:{} C:{}'.format(str(row),str(col)))

						# Update row Row and row Col (should just increment col)
						col += widget.dim[1]
						rowSize = widget.dim[0] if widget.dim[0] > rowSize else rowSize

					# Update row Row and row Col (should just increment row and set col to abs col)
					widgetPtr += divie.size
					nextRow += rowSize
					row += rowSize
					newCol = col if col > newCol else newCol
					newRow = row if row > newRow else newRow

					# DEBUG MESSAGES
					# print('nextRow: {} nextCol: {}'.format(str(nextRow),str(nextCol)))
					# print('newRow: {} newCol: {}'.format(str(newRow),str(newCol)))


			# End Col will start grid layout on next available col
			elif divie.type == 'endCol':

				if divie.size == 0:
					pass

				else:
					# DEBUG MESSAGES
					# print('\nendCol has size: ' + str(divie.size))

					# Will loop over all widgets in range from first available widget to dim of divie
					for index,widget in enumerate(self.widgets[widgetPtr:widgetPtr+divie.size]):
						# label exists then 
						if self.labels[index+widgetPtr]:
							# Construct mini Vertical Layout to put label and widget in same grid
							miniVLayout = QtWidgets.QVBoxLayout()
							miniVLayout.addWidget(self.labels[index+widgetPtr],alignment=QtCore.Qt.AlignCenter)
							miniVLayout.addWidget(widget,alignment=QtCore.Qt.AlignCenter)
							# Add newly created vertical layout to grid layout
							self.gridLayout.addLayout(miniVLayout,row,col,widget.dim[0],widget.dim[1],alignment=QtCore.Qt.AlignCenter)

						else:
							# Widgets that don't have any labels
							self.gridLayout.addWidget(widget,row,col,widget.dim[0],widget.dim[1],alignment=QtCore.Qt.AlignCenter)

						# DEBUG MESSAGES
						# print('R:{} C:{}'.format(str(row),str(col)))

						# Update row Row and row Col (should just increment col)
						row += widget.dim[0]
						colSize = widget.dim[1] if widget.dim[1] > colSize else colSize

					# Update row Row and row Col (should just increment row and set col to abs col)
					widgetPtr += divie.size
					nextCol += colSize
					col += colSize
					newRow = row if row > newRow else newRow
					newCol = col if col > newCol else newCol

					# DEBUG MESSAGES
					# print('nextRow: {} nextCol: {}'.format(str(nextRow),str(nextCol)))
					# print('newRow: {} newCol: {}'.format(str(newRow),str(newCol)))


			# Adjust grid layout to start at new row
			elif divie.type == 'newRow':
				nextCol = 0
				nextRow = newRow

				# DEBUG MESSAGES
				# print('\nR:{} C:{}'.format(str(row),str(col)))
				# print('\tnextRow: {} nextCol: {}'.format(str(nextRow),str(nextCol)))
				# print('\tnewRow: {} newCol: {}'.format(str(newRow),str(newCol)))


			# Adjust grid layout to start at new col
			elif divie.type == 'newCol':
				nextRow = 0
				nextCol = newCol

				# DEBUG MESSAGES
				# print('\nR:{} C:{}'.format(str(row),str(col)))
				# print('\tnextRow: {} nextCol: {}'.format(str(nextRow),str(nextCol)))
				# print('\tnewRow: {} newCol: {}'.format(str(newRow),str(newCol)))


			# Puts current grid layout onto tab and starts on new tab
			elif divie.type == 'makeTab':
				if not self.mini:
					# Create a new widget and current layout
					tab = QtWidgets.QWidget()
					tab.setLayout(self.gridLayout)
					# Add widget as a tab
					self.tabs.addTab(tab,divie.name)

					# Grid Layout must be reset
					self.gridLayout = QtWidgets.QGridLayout()
					row=col=nextRow=nextCol=newRow=newCol=rowSize=colSize = 0
				
				else:
					# Create a new mini widget and current layout
					miniTab = QtWidgets.QWidget()
					miniTab.setLayout(self.gridLayout)
					# Add widget as a tab
					self.miniTabs.addTab(miniTab,divie.name)

					# Grid Layout must be reset
					self.gridLayout = QtWidgets.QGridLayout()
					row=col=nextRow=nextCol=newRow=newCol=rowSize=colSize = 0


			# Creates a new group box. The widgets added after this call will be put into box
			elif divie.type == 'startGroup':
				# Set group name
				self.groupBox.setTitle(divie.name)
				# Store all index variables for later use
				self.masterGridLayout	= self.gridLayout
				self.masterNextRow 		= nextRow
				self.masterNextCol 		= nextCol
				self.masterNewRow 		= newRow
				self.masterNewCol 		= newCol
				self.mini 				= True

				# Reset grid layout for mini grid layout
				row=col=nextRow=nextCol=newRow=newCol=rowSize=colSize = 0
				self.gridLayout = QtWidgets.QGridLayout() 
				self.groupBox.setObjectName('groupBox')
				self.groupBox.setStyleSheet(
     				'QGroupBox#groupBox {border: 2px solid gray;' + 
     				'border-radius: 3px; padding: 10px;}' 
				)


			# Ends the current group box.
			elif divie.type == 'endGroup':
				# DEBUG MESSAGES
				# print('\tnextRow: {} nextCol: {}'.format(str(self.masterNextRow),str(self.masterNextCol)))
				# print('\tnewRow: {} newCol: {}'.format(str(self.masterNewRow),str(self.masterNewCol)))

				# Sets mini grid layout to the groupBox
				if self.miniTabs.count():
					self.gridLayout.addWidget(self.miniTabs)
					self.miniTabs	= QtWidgets.QTabWidget()

				self.groupBox.setLayout(self.gridLayout)

				# Now place groupbox in the grid
				if not divie.size:
					self.masterGridLayout.addWidget(self.groupBox,self.masterNextRow,self.masterNextCol,self.gridLayout.rowCount(),self.gridLayout.columnCount())
					nextCol = self.masterNextCol + self.gridLayout.columnCount()
					newRow = self.gridLayout.rowCount() + self.masterNextRow if self.gridLayout.rowCount() + self.masterNextRow > self.masterNewRow else self.masterNewRow

				else:
					self.masterGridLayout.addWidget(self.groupBox,self.masterNextRow,self.masterNextCol,divie.size[0],divie.size[1])
					nextCol = self.masterNextCol + divie.size[1]
					newRow = divie.size[0] + self.masterNextRow if divie.size[0] + self.masterNextRow > self.masterNewRow else self.masterNewRow

				# Update necessary index values
				newCol = nextCol if nextCol > self.masterNewCol else self.masterNewCol

				if not nextCol >= newCol:
					nextRow = self.masterNextRow

				# Resets grid layout to what it was before group box
				self.gridLayout = self.masterGridLayout
				self.groupBox 	= QtWidgets.QGroupBox()
				self.mini 		= False

				# DEBUG MESSAGES
				# print('\tnextRow: {} nextCol: {}'.format(str(nextRow),str(nextCol)))
				# print('\tnewRow: {} newCol: {}'.format(str(newRow),str(newCol)))


			# Corner Case Fix
			if nextCol >= newCol:
				nextRow = 0
				newCol = nextCol

			if nextRow >= newRow:
				nextCol = 0
				newRow = nextRow


		# Set the layout that you just created
		if self.tabs.count():
			self.is_tab = True
			self.setCentralWidget(self.tabs)
		else:
			self.centralWidget.setLayout(self.gridLayout)

		
	#################################### Available Widgets ##############################################

	def addButton(self, id, callback, dim=[1,1], label=None, horizontalAlign=False, size=[120,25]):
		""" Adds a push button to the Gui """
		if not label: label = id
		self.widgets.append(GWENButton(self.centralWidget, id, callback, dim, label, size))
		if horizontalAlign:
			self.labels.append(GWENLabel(self.centralWidget, ' ', dim))
		else:
			self.labels.append(None)


	def addToggle(self, id, dim=[1,1], label=None, size=[120,20]):
		""" Adds a toggle switch to the Gui """
		if not label: label = id
		self.widgets.append(GWENButton(self.centralWidget, id, None, dim, label, size))
		# Toggles don't get labels
		self.labels.append(None)


	def addLED(self, id, dim=[1,1], label=None, color=pyqt_led.Led.green, shape=pyqt_led.Led.circle):
		""" Adds an LED indicator to the Gui """ 
		if not label: label = id
		self.widgets.append(GWENLED(self.centralWidget, id, dim, label, color, shape))
		self.labels.append(GWENLabel(self.centralWidget, label, dim, id))
		

	def addCheckbox(self, id, dim=[1,1], label=None, width=120):
		""" Adds a checkbox to the Gui """
		if not label: label = id
		self.widgets.append(GWENCheckBox(self.centralWidget, id, dim, label, width))
		self.labels.append(None)


	def addRadioButton(self, id, label=None):
		""" Adds a radio button to the Gui """
		if not label: label = id
		self.widgets.append(GWENRadioButton(self.centralWidget, id, label))
		self.labels.append(None)


	def addIndicator(self, id, default='', dim=[1,1], label=None, width=120):
		""" Adds an indicator to the Gui """
		if not label: label = id
		self.widgets.append(GWENIndicator(self.centralWidget, id, str(default), dim, label, width))
		self.labels.append(GWENLabel(self.centralWidget, label, dim))
	  

	def addLogBox(self, id, dim=[2,2], label=None, size=[200,200]):
		""" Adds a log box to the Gui """
		if not label: label = id
		self.widgets.append(GWENLoggingBox(self.centralWidget, id, dim, label, size))
		self.labels.append(GWENLabel(self.centralWidget, label, dim))


	def addInputBox(self, id, default=None, dim=[1,1], label=None, width=120):
		""" Adds an input box to the Gui """
		if not label: label = id
		try:
			if default != None:
				default = str(default)
		except:
			default = str(default)
		self.widgets.append(GWENUserInput(self.centralWidget, id, default, dim, label, width))
		self.labels.append(GWENLabel(self.centralWidget, label, dim, id))


	def addTextBox(self, id, dim=[1,1], label=None):
		""" Adds a text box to the Gui """
		self.widgets.append(GWENTextBox(self.centralWidget, id, default, dim, label))
		self.labels.append(GWENLabel(self, label, dim))


	def addSpinBox(self, id, default=0, dim=[1,1], label=None):
		""" Adds a spin box to the Gui """
		if not label: label = id
		self.widgets.append(GWENSpinBox(self.centralWidget, id, default, dim, label))
		self.labels.append(GWENLabel(self, label, dim))


	def addSlider(self, id, lower=0, upper=100, dim=[1,1], label=None):
		""" Adds a slider to the Gui """
		self.widgets.append(GWENSlider(self.centralWidget, id, default, dim, label))
		self.labels.append(GWENLabel(self, label, dim))


	def addComboBox(self, id, items, dim=[1,1], label=None, width=120):
		""" Adds a combo box to the Gui """
		if not label: label = id
		self.widgets.append(GWENComboBox(self.centralWidget, id, items, dim, label, width))
		self.labels.append(GWENLabel(self, label, dim))


	def addLabel(self, label=None, dim=[1,1], id=None):
		""" Adds a label to the Gui """
		if not label: label = id
		self.widgets.append(GWENLabel(self.centralWidget, label, dim, id))
		# Labels don't get labels
		self.labels.append(None)


	def addSpace(self):
		""" Adds a blank space to the Gui """
		self.widgets.append(GWENLabel(self.centralWidget, dim=[1,1], label=''))
		# Plots don't get labels
		self.labels.append(None)


	def addFileBox(self, id, filetypes=None, path=None):
		""" Adds file box pop-up functionality """
		if self.is_tab:
			parent = self.tabs
		else:
			parent = self.centralWidget
		self.widgets.append(GWENFileDialog(parent, id, filetypes, path, dim=[1,1]))
		# File Boxs don't get labels
		self.labels.append(None)


	def addTable():
		pass


	def addMenuBar():
		pass


	def addImage(self, id, image, size=[100,100], dim=[1,1]):
		""" Adds an image to the Gui """
		self.widgets.append(GWENImage(self.centralWidget, id, image, size, dim))
		# Images don't get labels
		self.labels.append(None)


	def addPlot(self, id, numCurves, labels, color=None):
		""" Adds a plot to the Gui """
		self.widgets.append(GWENPlot(self.centralWidget, id, numCurves, labels, color)) 
		# Plots don't get labels
		self.labels.append(None)


	def addStackPlot(self, id, numPlots, numCurves, dim, labels):
		""" Adds a stack plot to the Gui """
		self.widgets.append(GWENPlot(self.centralWidget))
		# Plots don't get labels
		self.labels.append(None)


	def addMatPlot(self, id, x_len=100, y_range=[0,100], interval=20):
		# 2. Place the matplotlib figure
		self.widgets.append(MyFigureCanvas(self.centralWidget, id, x_len, y_range, interval))
		# Plots don't get labels
		self.labels.append(None)

	################################### Setter Slot Functions ##########################################

	@QtCore.pyqtSlot()
	def updateIndicator(self, id, output):
		# Searches for Gui Object given an ID
		indicator = self.getWidget(id)
		# Once found, set the Indicator 
		indicator.setText(str(output))


	@QtCore.pyqtSlot()
	def updateLog(self, id, message):
		# Searches for Gui Object given an ID
		logBox = self.getWidget(id)
		# Once found, append the message
		logBox.append(str(message))


	@QtCore.pyqtSlot()
	def updatePlot(self, id, x_data, *y_data):
		# Searches for Gui Object given an ID
		plot = self.getWidget(id)
		# Once found, set the Indicator 
		plot.updatePlot(x_data,*y_data)


	@QtCore.pyqtSlot()
	def updateMatPlot(self, id, y_data):
		# Searches for Gui Object given an ID
		plot = self.getWidget(id)
		# Once found, set the Indicator 
		plot._update_canvas_(y_data)


	@QtCore.pyqtSlot()
	def updateLED(self, id, set=False):
		# Searches for Gui Object given an ID
		led = self.getWidget(id)
		# Once found, set the LED
		if set: led.toggleOn()
		else: led.toggleOff()


	################################### Getter Slot Functions ##########################################
	
	@QtCore.pyqtSlot()
	def getInt(self, id):
		""" Returns an int from text box, spinbox, or slider widget """
		# See if id matches widget in database
		widget = self.getWidget(id)
		try: return int(widget.value())
		except ValueError:
			print('')


	@QtCore.pyqtSlot()
	def getFloat(self, id):
		""" Returns value of Float """
		# See if id matches widget in database
		widget = self.getWidget(id)
		try: return float(widget.value())
		except ValueError:
			print('')


	@QtCore.pyqtSlot()
	def getBool(self, id):
		""" Returns value of Boolean """
		# See if id matches widget in database
		widget = self.getWidget(id)
		try: return widget.value()
		except ValueError:
			print('')


	@QtCore.pyqtSlot()
	def getString(self, id):
		""" Returns a string """
		# See if id matches widget in database
		widget = self.getWidget(id)

		try: return str(widget.value())
		except ValueError:
			print('')


	# @QtCore.pyqtSlot()
	# def getVal(self, id):
	# 	""" Returns any type """
	# 	widget = self.getWidget(id)

	# 	if isinstance(widget.value,str):
	# 		return widget.value()
	# 	elif isinstance(widget.value,int):
	# 		return widget.value()
	# 	elif isinstance(widget.value,bool):
	# 		return widget.value()
	# 	elif isinstance(widget.value,float):
	# 		return widget.value()
	

	def getWidget(self, id):
		for widget in self.widgets:
			if widget.id == id:
				return widget
		else:
			pass
	

	def getLabel(self, id):
		for label in self.labels:
			if label:
				if label.id == id:
					return label
		else:
			pass

	########################################## "Divies" Functions ##################################################

	def endCol(self):
		""" Ends a column in the layout. All widgets added since last divies call
		will be layed out in a vertical manner
		"""
		numWidgets = len(self.widgets)
		# Find number of GUI objects since last divie call
		size = numWidgets - self.divieSize
		self.divies.append(GWENDivies('endCol',size))
		self.divieSize = numWidgets


	def endRow(self):
		""" Ends a row in the layout. All widgets added since last divies call
		will be layed out in a horizontal manner
		"""
		numWidgets = len(self.widgets)
		# Find number of GUI objects since last divie call
		size = numWidgets - self.divieSize
		self.divies.append(GWENDivies('endRow',size))
		self.divieSize = numWidgets


	def newCol(self):
		""" This call will move [row,col] to the proper location [nextRow,0] """ 
		self.divies.append(GWENDivies('newCol'))


	def newRow(self):
		""" This call will move [row,col] to the proper location [0,nextCol] """ 
		self.divies.append(GWENDivies('newRow'))


	def makeTab(self, name):
		""" This call will form all previous widgets into a tab and create a new tab """
		self.divies.append(GWENDivies('makeTab',name=name))


	def startGroup(self, name):
		""" Will create a box around all the widgets added after this call is made.
		Will add widgets in the same layout until the endGroup func is called.
		"""
		self.divies.append(GWENDivies('startGroup',name=name))


	def endGroup(self, size=None):
		""" Closing function of a group box. """
		self.divies.append(GWENDivies('endGroup',size))