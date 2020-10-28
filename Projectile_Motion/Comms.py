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
#	Comms.py
#
#	Creates a process to run the Physics Simulator calculations and manage communication to Gui
#
################
# Dependencies #
################
from multiprocessing import Process
from PhysicsSim import *
import time

###############
#   Process   #
###############

class PlotProcess(Process):
	""" Multithreading process which is a separate python process on its own thread """
	def __init__(self, param_Q, data_Q):
		super().__init__()
		self.param_Q = param_Q
		self.data_Q = data_Q
		self.stopflag = False
		self.daemon = True


	def run(self):
		""" While the process is alive check the queue from the Gui and execute calculations """
		while not self.stopflag:
			if not self.param_Q.empty():
				params = self.param_Q.get()
				if type(params) == list:
					# Actual execution of simulator
					exec('PhysicsSim(self.data_Q, params)')
				else:
					self.data_Q.put(['', 'Did not receive parameters.'])

				self.stop()

			else:
				time.sleep(0.05)


	def stop(self):
		self.stopflag = True
