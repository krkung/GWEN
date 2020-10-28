# ______          _           _   _ _       ___  ___      _   _               _____ _                 _       _              
# | ___ \        (_)         | | (_) |      |  \/  |     | | (_)             /  ___(_)               | |     | |             
# | |_/ / __ ___  _  ___  ___| |_ _| | ___  | .  . | ___ | |_ _  ___  _ __   \ `--. _ _ __ ___  _   _| | __ _| |_ ___  _ __  
# |  __/ '__/ _ \| |/ _ \/ __| __| | |/ _ \ | |\/| |/ _ \| __| |/ _ \| '_ \   `--. \ | '_ ` _ \| | | | |/ _` | __/ _ \| '__| 
# | |  | | | (_) | |  __/ (__| |_| | |  __/ | |  | | (_) | |_| | (_) | | | | /\__/ / | | | | | | |_| | | (_| | || (_) | |    
# \_|  |_|  \___/| |\___|\___|\__|_|_|\___| \_|  |_/\___/ \__|_|\___/|_| |_| \____/|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|    
#               _/ |                                                                                                         
#              |__/                                                                                                          
#  _   __      _        _   __                                                                                               
# | | / /     | |      | | / /                                                                                               
# | |/ / _   _| | ___  | |/ / _   _ _ __   __ _                                                                              
# |    \| | | | |/ _ \ |    \| | | | '_ \ / _` |                                                                             
# | |\  \ |_| | |  __/ | |\  \ |_| | | | | (_| |                                                                             
# \_| \_/\__, |_|\___| \_| \_/\__,_|_| |_|\__, |                                                                             
#         __/ |                            __/ |                                                                             
#        |___/                            |___/    
#
#	Projectile_Motion.py
#
#	A physics simulator of a bouncy ball under the force of gravity using custom GUI Library wrapper over PyQt5 (GWEN)
#
################
# Dependencies #
################
from GWEN_GuiEngine  import * 
from Comms		 	 import *
from multiprocessing import Queue
import numpy as np
import time

#############
# Constants #
#############
y0 = 50 #[m]
v0 = (1,1) #[m/s]
g = (0., -9.81) #[m/s^2]
dt = 0.1 #[s]
total_t = 7 
drag = 0.
refl = 0.75 # Hard wall reflection value. v = refl*v0

################
#  Create GUI  #
################

class ProjectileGui(GWENGui):
	def __init__(self,title: str = "Projectile Motion Simulator"):
		# Initialize parent GWENGUI class
		super().__init__(title)
		# Create communication queues
		self.param_Q = Queue()	# To calculation
		self.data_Q = Queue()	# From calculation
		self.linked = False

		self.buildGUI()
		self.launch()


	def buildGUI(self):
		""" Set up display UI """
		self.startGroup('Initial Conditions')
		self.addInputBox('Initial Height [m]', y0)
		self.addInputBox('  Initial Velocity\n(V_x, V_y) [m/s]', v0)
		self.endRow()
		self.endGroup()

		self.newRow()
		self.startGroup('Parameters')
		self.addInputBox('Timestep dt [s]', dt)
		self.addInputBox('Total time [s]', total_t)
		self.endRow()
		self.addInputBox('Drag', drag)
		self.addInputBox('Reflection coefficient', refl)
		self.endRow()
		self.addSpace()
		self.endRow()
		self.addLabel('Ever wanted to try side gravity? --->\n   format: (side, -9.81)')
		self.addInputBox('Gravity [m/s^2]', g)
		self.endRow()
		self.endGroup()

		self.newRow()
		self.addToggle('PLOT', dim=[1,2], size=[150, 90])
		self.getWidget('PLOT').clicked.connect(self.plot)
		self.endRow()

		self.newCol()
		self.addPlot('_Plot_', 1, labels=['', 'x (distance) [m]', 'y (height) [m]'], color='g')
		self.addLogBox('', dim=[2,4], size=[300,200])
		self.endCol()

		# Set up Gui Controller and its communication thread
		self.link()


	def link(self):
		""" Creates GUi_Controller instance and moves it to its own thread. Signals & Slots connected. """
		self.controller = Gui_Controller(self.data_Q)
		self.ctrl_thread = QtCore.QThread()
		self.controller.moveToThread(self.ctrl_thread)
		self.ctrl_thread.started.connect(self.controller.update)
		self.controller.updatePlotSig.connect(self.update_plot)
		self.controller.updateLogSig.connect(self.update_log)
		self.ctrl_thread.start()
		self.linked = True


	def plot(self):
		""" Gathers parameters from Gui and opens a separate python process to handle calculation"""
		if self.getBool('PLOT'):
			self.getWidget('PLOT').setText('Plotting...')
			self.PlotProcess = PlotProcess(self.param_Q, self.data_Q) # Cant pass in gui (or objects) to a process
			time.sleep(0.5)
			self.getParameters()
			self.PlotProcess.start()
		else:
			self.PlotProcess.stop()
			self.getWidget('PLOT').setText('PLOT')
			self.getWidget('PLOT').toggle()
			

	def getParameters(self):
		""" Retrieves parameters from gui for calculation """
		y0		= self.getWidget('Initial Height [m]').value()
		v0 		= self.getWidget('  Initial Velocity\n(V_x, V_y) [m/s]').value()
		dt 		= self.getWidget('Timestep dt [s]').value()
		total_t = self.getWidget('Total time [s]').value()
		drag 	= self.getWidget('Drag').value()
		refl 	= self.getWidget('Reflection coefficient').value()
		g 		= self.getWidget('Gravity [m/s^2]').value()

		self.param_Q.put([y0, v0, dt, total_t, drag, refl, g])


	def __del__(self):
		""" Called when Gui instance goes to the garbage """
		self.controller = Gui_Controller(self.data_Q)
		self.controller.active = False

		if self.linked:
			self.ctrl_thread.terminate()

#### Slot Functions ###############################################################################

	@QtCore.pyqtSlot(str, np.ndarray, np.ndarray)
	def update_plot(self,label,x_vals,y_vals):
		""" PyQt Slot Function (to Gui_Controller signal) to handle Plot Updates """
		try:
			self.updatePlot(label,x_vals,y_vals)
		except AttributeError:
			pass


	@QtCore.pyqtSlot(str, str)
	def update_log(self,label,message):
		""" PyQt Slot Function to handle Logbox Updates """
		if label == 'DONE':
			self.getWidget('PLOT').setText('PLOT')
			self.getWidget('PLOT').toggle()
			label = ''
		try:
			self.updateLog(label, message)
		except AttributeError:
			pass

###################################################################################################




###################################################################################################

class Gui_Controller(QtCore.QObject):
	# Signals
	updatePlotSig = QtCore.pyqtSignal(str, np.ndarray, np.ndarray)
	updateLogSig = QtCore.pyqtSignal(str, str)

	def __init__(self, data_Q):
		# Call parent
		super().__init__()
		self.data_Q = data_Q
		self.active = True


	def update(self):
		""" Loop that will continuously check a queue for data/messages for the Gui """
		while self.active:
			if not self.data_Q.empty():
				data = self.data_Q.get()
				label = data[0]

				# If finished plotting
				if label == 'DONE':
					message = """Magnitude Max Velocity of {} m/s occurred at (x,y) = ({}) meters\nMagnitude of Max Acceleration of {} m/s^2 occured at (x,y) = ({}) meters\n""".format(data[1][0],data[1][1],data[1][2],data[1][3])
					self.updateLogSig.emit(label, message)
					
				# If we want to update the log
				elif label == '':
					self.updateLogSig.emit(label, data[1])

				# It's plot data so uh, plot it :)
				else:
					x_vals = data[1]
					y_vals = data[2]
					self.updatePlotSig.emit(label, x_vals, y_vals)
			# Sleep so that the queue can be accessed elsewhere
			time.sleep(0.05)		
		

#####################################################################################################

if __name__ == "__main__":
	ProjectileGui()