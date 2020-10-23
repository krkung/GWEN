#   .d8888b.  888       888 8888888888 888b    888 
#  d88P  Y88b 888   o   888 888        8888b   888 
#  888    888 888  d8b  888 888        88888b  888 
#  888        888 d888b 888 8888888    888Y88b 888 
#  888  88888 888d88888b888 888        888 Y88b888 
#  888    888 88888P Y88888 888        888  Y88888 
#  Y88b  d88P 8888P   Y8888 888        888   Y8888 
#   "Y8888P88 888P     Y888 8888888888 888    Y888 
#                                                                 
# GWENGui_Objects.py
#
# Authors: Mundo Guzman, Kyle Kung, Cole Meyers  |   Maintainer: Kyle Kung
#
# Collection of PyQt5 wrapper classes that are used in GWENGui_Engine.py
# Each PyQt widget will have its own GWENGui object class
#
# Dependencies
import sys
import os
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui

##### Operating System Check ##################################################################################

# Detect OS platform
if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	os_type = 'Linux'
	graph_path = sys.path.insert(0, '/usr/lib/python3/dist-packages/')
elif sys.platform.startswith('win'):
	os_type = 'Windows'
elif sys.platform.startswith('darwin'):
	os_type = 'macOS'
else:
	raise EnvironmentError('Unsupported platform.')

print('Detected {} as the default operating system.'.format(os_type))

# OS-Specific Dependencies 
import pyqtgraph as pg
import pyqt_led

###############################################################################################################


class GWENButton(QtWidgets.QPushButton):
	""" Class used to create a normal Qt push button """
	def __init__(self, parent, id, callback, dim, label, width):
		# Call parent constructor
		super().__init__(label,parent)

		self.id = id
		self.dim = dim
		self.label = label
		self.red = False

		# Connect callback to button click
		if callback:
			self.clicked.connect(callback)

		# Otherwise, create a toggle button
		else:
			self.enabled = False
			self.clicked.connect(self.toggle)

		# Default size
		self.setFixedWidth(width)


	def toggle(self):
		""" Function makes PyQt Button work as a toggle switch instead. Will simply 
		return true when enabled and false when disabled. Will turn a neon green
		when enabled. Non callback function will execute.
		"""
		# Flip bool value each time its switched
		self.enabled = not self.enabled

		if self.enabled:
			if not self.red:
				self.setStyleSheet('background-color:rgb(57,255,20)' ';color:black')
			else:
				self.setStyleSheet('background-color:rgb(255,0,0)' ';color:black')
		else:
			self.setStyleSheet('')


	def value(self):
		""" Returns true if toggle is enabled """
		try:
			return self.enabled
		except :
			raise TypeError('GWENButton has no return type.')


class Color():
	""" Class to create colors for LEDs """
	black = np.array([0x00, 0x00, 0x00], dtype=np.uint8)
	white = np.array([0xff, 0xff, 0xff], dtype=np.uint8)
	blue = np.array([0x73, 0xce, 0xf4], dtype=np.uint8)
	green = np.array([0x39, 0xff, 0x14], dtype=np.uint8)
	orange = np.array([0xff, 0xa5, 0x00], dtype=np.uint8)
	purple = np.array([0xaf, 0x00, 0xff], dtype=np.uint8)
	red = np.array([0xff, 0x00, 0x00], dtype=np.uint8)
	yellow = np.array([0xff, 0xff, 0x00], dtype=np.uint8)

class GWENLED(pyqt_led.Led):
	""" Class used to create a PyQt LED """
	def __init__(self, parent, id, dim, label, color, shape):
		# Call parent constructor
		super().__init__(parent, on_color=color, shape=shape)

		self.id = id
		self.dim = dim
		self.label = label

		# Default size
		self.setFixedSize(35,35)


	def toggleOn(self):
		""" Toggle LED on """
		self._toggle_on()


	def toggleOff(self):
		""" Toggle LED off """
		self._toggle_off()


	def value(self):
		""" Returns true if on """
		if self.is_on():
			return True
		else:
			return False


class GWENCheckBox(QtWidgets.QCheckBox):
	""" Class used to create a Qt check box """
	def __init__(self, parent, id, dim, label, width):
		# Call parent constructor
		super().__init__(label, parent)

		self.id = id
		self.dim = dim
		self.label = label

		# Default size
		self.setFixedWidth(width)


	def value(self):
		""" Returns True if checked otherwise false """
		return self.isChecked()


class GWENRadioButton(QtWidgets.QRadioButton):
	""" Class used to create a Qt option button """
	def __init__(self, parent, id, label):
		# Call parent constructor
		super().__init__(label, parent)

		self.id = id
		self.dim = [1,1]
		self.label = label

		# Disables default state that only allows one option to be checked
		self.setAutoExclusive(False)


	def value(self):
		""" Returns True if checked otherwise false """
		return self.isChecked()


class GWENIndicator(QtWidgets.QLineEdit):
	""" Class used to create a Qt indicator """
	def __init__(self, parent, id, default, dim, label, width):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = dim
		self.label = label

		# Set defaut readout
		self.setText(default)

		# Users do not have permission to alter indicators
		self.setReadOnly(True)
		self.setStyleSheet('background-color:rgb(103, 111, 112)' ';color:white')
		self.setFixedWidth(width)
		self.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

	def value(self):
		""" Returns a string with indicator value """
		return self.text()


class GWENUserInput(QtWidgets.QLineEdit):
	""" Class used to create a Qt user input box """
	def __init__(self, parent, id, default, dim, label, width):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = dim
		self.label = label

		if default: self.setText(default)
		self.setFixedWidth(width)
		self.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)


	def value(self):
		""" Returns a string with user input """
		return self.text()


class GWENTextBox(QtWidgets.QTextEdit):
	""" Class used to create a Qt text box """
	def __init__(self, parent, id, default, dim, label):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = [1,1]
		self.label = label

		if default: self.setText(default)


class GWENSpinBox(QtWidgets.QDoubleSpinBox):
	""" Class used to create a Qt spin box """
	def __init__(self, parent, id, default, dim, label):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = dim
		self.label = label

		self.setFixedWidth(120)

		self.setDecimals(2)
		self.setSingleStep(1)
		self.setRange(0,1000)
		self.setValue(default)

	# Note: value obtained by using gui.getString(label) instead of gui.getWidget(label)


class GWENSlider(QtWidgets.QSlider):
	""" Class used to create a Qt slider """
	def __init__(self, parent, id, default, dim, label):
		# Call parent constructor
		self.id = id
		self.dim = [1,1]
		self.label = label


	def value(self):
		""" Returns the current value the slider is set to """
		return self.value()


class GWENComboBox(QtWidgets.QComboBox):
	""" Class used to create a Qt combo box """
	def __init__(self, parent, id, items, dim, label, width):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = dim
		self.label = label

		for item in items:
			self.addItem(item)

		self.setFixedWidth(width)


	def value(self):
		""" Returns the string of the item that is currently selected """
		return self.currentText()
			

class GWENLoggingBox(QtWidgets.QTextBrowser):
	""" Class used to create a empty Qt text box which can log actions/messages in real time """
	def __init__(self, parent, label, dim, id=None, size=[200,200]):
		# Call parent constructor
		super().__init__(parent)
		# Labels do not require an ID
		self.dim = dim
		self.id = id
		self.label = label

		self.setFixedWidth(size[0])
		self.setFixedHeight(size[1])


class GWENLabel(QtWidgets.QLabel):
	""" Class used to create a normal Qt label """
	def __init__(self, parent, label, dim, id=None):
		# Call parent constructor
		super().__init__(parent)
		# Labels do not require an ID
		self.dim = dim
		self.id = id
		self.label = label

		self.setText(label)


class GWENFileDialog(QtWidgets.QFileDialog):
	""" Class used to create a Qt file dialog window """
	def __init__(self, parent, id, filetypes, path, dim):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = dim
		self.filetypes = filetypes

		file_dict = {'*.txt':'Text Files (*.txt)', '*.csv': 'CSV files (*.csv)',
					 '*.xlsx':'Excel files (*.xlsx)','*.png':'Images (*.png *.xpm *.jpg)',
					 '*.jpg':'Images (*.png *.xpm *.jpg)'}

		try:
			self.filetypes = [file_dict[i] for i in self.filetypes]
		except:
			print('Wrong file type found.')
		self.filetypes = ';;'.join(self.filetypes)
		
		if filetypes != None:
			self.selectNameFilter(self.filetypes)

		if path != None:
			self.setDirectory(path)

		self.options = self.Options()
		self.options |= self.DontUseNativeDialog

		# Default size
		self.setFixedWidth(1200)


	def value(self,type_='OPEN'):
		""" Returns the string of the item that is selected in file dialog box"""
		self.type_ = type_
		box_title = self.id
		'''Can open a single folder (returns string of path), 
		   open file(s) (returns list of file path strings), 
		   or save to a file (returns string of path)'''
		if type_.upper() == 'FOLDER':
			output_path = self.getExistingDirectory()
		elif type_.upper() == 'OPEN':
			output_path = self.getOpenFileNames(self,box_title,os.getcwd(),self.filetypes)[0]
		elif type_.upper() == 'SAVE':
		 	output_path = self.getSaveFileName(self,box_title,os.getcwd(),self.filetypes,options=self.options)[0]
		return output_path


class GWENImage(QtWidgets.QLabel):
	""" Class used to create a Qt label of an image """
	def __init__(self, parent, id, image, size, dim):
		# Call parent constructor
		super().__init__(parent)
		# Labels do not require an ID
		self.id = id
		self.dim = dim

		self.setPixmap(QtGui.QPixmap(image).scaled(size[0], size[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
		#self.setFixedSize(size[0],size[1])


class GWENPlot(pg.GraphicsLayoutWidget):
	""" Class used to create a Qt plot """
	def __init__(self, parent, id, numCurves, labels):
		# Call parent constructor
		super().__init__(parent)

		self.id = id
		self.dim = [4,4]
		# List that holds curves in a plot
		self.curves = []

		# Available colors for plot (up to 8 colors)
		colors = ['w','b','g','r','c','m','y','w']

		# Create plot object
		self.axe = self.addPlot()

		# Create a list to contain all curves
		for curve in range(0,numCurves):
			self.curves.append(self.axe.plot(pen=colors[curve]))

		# Set title and axis labels
		self.axe.setTitle(labels[0])
		self.axe.setLabel('bottom',labels[1])
		self.axe.setLabel('left',labels[2])

		# Set Fixed Size 
		self.setFixedSize(350,350)


	def updatePlot(self, x, *y):
		""" Update Plot Object. Will take up to "n" number of arguments.
		Will plot as many items specified against one x axis only
		"""
		for index,_y in enumerate(y):
			self.curves[index].setData(x,_y)
		

class GWENStackPlot(pg.GraphicsLayoutWidget):

	def __init__():
		# Call parent constructor
		# Set dim and id
		pass


class GWENDivies():
	""" Class used to create a normal Qt push button """
	def __init__(self, type, size=None, name=None):

		self.type = type
		self.size = size
		self.name = name


def showDialog(title, message, icontype):
	""" """
	if isinstance(icontype,str):
		if icontype.lower() == 'critical':
			icontype = 3
		elif icontype.lower() == 'warning':
			icontype = 2
		elif icontype.lower() == 'information':
			icontype = 1

	msgBox = QtWidgets.QMessageBox()
	msgBox.setIcon(icontype)
	msgBox.setText(message)
	msgBox.setFixedWidth(300)
	msgBox.setWindowTitle(title)
	msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
	msgBox.setWindowModality(True)
	#msgBox.buttonClicked.connect(msgButtonClick)

	returnValue = msgBox.exec()
	if returnValue == QtWidgets.QMessageBox.Ok:
		msgBox.close()