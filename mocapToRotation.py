#----------------------------------------------------------------------
#  This file is designed to convert the motion capture data from an ASCII file into a sequence of rotational
#  animations.  Three different methods are included for the same concept.
#----------------------------------------------------------------------

from mocapDBDict import mocapDBDict
import collections as collect
import math

class mocapToRotation:
	def __init__(self, mocapData):
		self.mocapData = mocapData
	
    #This function converts a componant of each point's position data directly into an 
    #angle by using the sin of the position, then the asin to convert the result into a 
    #corresponding angle.
	def sinRot(self, thetaLimit, variable):
		angles = collect.OrderedDict()
		for key in self.mocapData:
			keyAngles = dict()
			for frame in range(0,len(self.mocapData[key].marker)):
				value = self.mocapData[key].marker[frame]
				if len(value) > 0:
					value = value[variable]
				else:
					angles[key]=None
					continue
				keyAngleValue = math.asin(math.sin(value))
				keyAngleValue = (keyAngleValue)*(thetaLimit)/(2*math.pi)
				keyAngles[frame]=(keyAngleValue)				
			angles[key] = keyAngles
		return angles
		
    #This function converts the the marker's velocity into and angle measure.  The velocity 
    #is derived from the length of the difference between the current point and next point's 
    #positions.  The first and last frames have the angles duplicated from the next and 
    #previous, respectively.  The angles are calculated via the same sin then asin method as 
    #was used on the coordinate method.
	def velocityRot(self, thetaLimit):
		angles = collect.OrderedDict()
		for key in self.mocapData:
			keyAngles = []
			for frame in range(1,len(self.mocapData[key].marker)):
				if len(self.mocapData[key].marker[frame])==0:
					break
				current = self.mocapData[key].marker[frame]
				if frame != len(self.mocapData[key].marker)-1:
					if len(self.mocapData[key].marker[frame+1])==0:
						continue
					nextFrame = frame+1
					next = self.mocapData[key].marker[nextFrame]
				else:
					if len(self.mocapData[key].marker[frame-1])==0:
						continue
					next = self.mocapData[key].marker[frame-1]
				
				testVec = [current[0]-next[0], current[1]-next[1], current[2]-next[2]]
				mag = math.sqrt(pow(testVec[0],2) + pow(testVec[1], 2) + pow(testVec[2],2))
				keyAngleValue = math.asin(math.sin(mag))
				keyAngleValue = (keyAngleValue)*(thetaLimit)/(2*math.pi)
				keyAngles.append(keyAngleValue)
			angles[key] = keyAngles
		return angles
	
    #This function retrieves the angle for each frame directly from the angle change over 3 
    #frames of motion.  The two vectors, previous -> current and current -> next are calculated,
    #then the angle between those vectors is retrieved from the dot product of the vectors and 
    #is stored.
	def dotRot(self):
		angles = collect.OrderedDict()
		for key in self.mocapData:
			keyAngles = dict()
			for frame in range(1, len(self.mocapData[key].marker)-1):
				p1 = self.mocapData[key].marker[frame-1]
				p2 = self.mocapData[key].marker[frame]
				p3 = self.mocapData[key].marker[frame+1]
				if len(p1) == 0 or len(p2) == 0 or len(p3) ==0:
					continue
				v1 = [p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2]]
				v2 = [p2[0]-p3[0], p2[1]-p3[1], p2[2]-p2[2]]
				v1Mag = math.sqrt(pow(v1[0],2) + pow(v1[1],2) + pow(v1[2],2))
				v2Mag = math.sqrt(pow(v2[0],2) + pow(v2[1],2) + pow(v2[2],2))
				if v1Mag == 0 or v2Mag == 0:
					continue
				cosAngle = (v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])/(v1Mag*v2Mag)
				if cosAngle > 1 or cosAngle < -1:
					continue
				angle = math.acos(cosAngle)
				output = self.normalizeVector(self.crossProduct(v1, v2))
				output = [output[0]*angle, output[1]*angle, output[2]*angle]
				if frame == 1:
					keyAngles[frame] = output
				if frame == len(self.mocapData[key].marker)-1:
					keyAngles[frame] = output
				keyAngles[frame] = output
			angles[key] = keyAngles
		return angles
		
    #I was unable to use libraries like numpy, so I had to write my own cross product
    #and normalization functions.  They ended up being quite simple and fast to work with.
	def crossProduct(self, v1, v2):
		return [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]
		
	def normalizeVector(self, v1):
		mag = math.sqrt( pow(v1[0],2) + pow(v1[1],2) + pow(v1[2],2) )
		if mag == 0:
			return [0,0,0]
		return [v1[0]/mag, v1[1]/mag, v1[2]/mag]
