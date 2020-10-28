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
#	PhysicsSim.py
#	
#	Physics simulator of projectile motion of a bouncy ball subject to gravity, drag, etc.
#
################
# Dependencies #
################
import numpy as np
import time 

################
#  Begin Code  #
################
class PhysicsSim():
	def __init__(self, data_Q, parameters):
		self.data_Q = data_Q
		
		# Run projectile motion simulator
		self.projectile_motion(parameters)


	def projectile_motion(self, parameters):
		""" Creates and plots data """
		y0		= parameters[0] 
		v0 		= parameters[1]
		dt 		= parameters[2]
		total_t = parameters[3]
		drag 	= parameters[4]
		refl 	= parameters[5]
		g 		= parameters[6]

		# Convert string to list
		v0_x, v0_y = v0[1:-1].split(',')
		g_x, g_y   = g[1:-1].split(',')

		# Try to convert everything to a float. No strings allowed.
		try:
			y0 		= float(y0)
			v0_x  	= float(v0_x)
			v0_y  	= float(v0_y)
			dt 		= float(dt)		
			total_t = float(total_t)
			drag 	= float(drag)
			refl 	= float(refl)
			g_x		= float(g_x)
			g_y		= float(g_y)

		except:
			self.data_Q.put(['', 'Please input a number (float or int).'])
			return

		# Total number of plot updates
		self.frames = np.int(np.ceil(total_t/dt))

		# Initialize empty numpy arrays
		s, v, a, f = [np.zeros((self.frames,2)) for i in range(4)]

		# Initial conditions (allowed user to change gravity so we ignore intial acceleration as it can simply be incorporated into the "Gravity" param)
		s[0,:] = [0, y0]
		v[0,:] = [v0_x, v0_y]
		a[0,:] = [g_x, g_y]
		f[0,:] = -drag*np.abs(v[0,:])   # Drag force is linear w.r.t velocity

		# Update positions in the proper timeframe set by the user
		for idx in range(1, self.frames):
			x, y = self.updatePosition(idx, s, v, a, f, drag, refl, dt)
			self.data_Q.put(['_Plot_', x, y])
			time.sleep(dt)

		# Look for some maximum values to print to log
		max_v = self.v.max()
		max_a = self.a.max()
		max_v_idx = np.argmax(self.v)
		max_a_idx = np.argmax(self.a)
		max_v_pos = s[max_v_idx,:].tolist()
		max_a_pos = s[max_a_idx,:].tolist()

		max_v = str(max_v)[:6]
		max_a = str(max_a)[:6]
		max_v_pos = str(max_v_pos[0])[:6]+','+str(max_v_pos[1])[:6]
		max_a_pos = str(max_a_pos[0])[:6]+','+str(max_a_pos[1])[:6]

		# Tell the Gui Controller that the calculations are done
		self.data_Q.put(['DONE', [max_v, max_v_pos, max_a, max_a_pos]])

		return 


	def updatePosition(self, idx, s, v, a, f, drag, refl, dt):
		""" Calculates and updates position of the ball """
		# Apply Euler's Method
		s[idx,:] = s[idx-1,:] + v[idx-1,:]*dt
		v[idx,:] = v[idx-1,:] + a[idx-1,:]*dt
		a[idx,:] = a[idx-1,:] + f[idx-1,:]
		f[idx,:] = -drag*np.abs(v[idx,:])

		# Implement specular reflection as in Lab
		if s[idx,1] <= 0:
			v[idx,:] = -refl*v[idx-1,1]
			s[idx,1] = 0

		# If we are on the last position, take the x,y components of velocity and acceleration and find all the magnitudes
		if idx == self.frames-1:
			self.v = np.sqrt([v[i,0]**2 + v[i,1]**2 for i in range(len(v))])
			self.a = np.sqrt([a[i,0]**2 + a[i,1]**2 for i in range(len(a))])
			self.s = s

		# Return updated positions for this idx
		return s[:idx,0], s[:idx,1]


