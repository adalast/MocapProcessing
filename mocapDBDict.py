#------------------------------------
#  Motion capture file processing objects.   The mocapMarkerDict object is used to manage the data for 
#  marker in the data.  The mocapDBDict manages and holds all of the markers for easier use.
#------------------------------------

import collections

#Motion Capture marker processing object
class mocapMarkerDict:
	ERROR = -9999.99
	SCALE = 1.0
	def __init__(self):
		self.marker = collections.OrderedDict()
		
	def append(self, x, y, z, f):
		if (x == mocapMarkerDict.ERROR or y == mocapMarkerDict.ERROR or z == mocapMarkerDict.ERROR):
			self.marker[f] = []
		else:
			self.marker[f] = [x*mocapMarkerDict.SCALE, z*mocapMarkerDict.SCALE, y*mocapMarkerDict.SCALE]
		
	def zip(list1, list2):
		self.marker = zip(list1, list2)
		
	def delPoint(self, f):
		if f in self.marker:
			del self.marker[f]
		else:
			print("Frame " + str(f) + " is missing!")
			
	def getData(self, f):
		if f in self.marker:
			return self.marker[f]
		else:
			False
			
    #Return the bounding box for the marker data
	def getBbox(self):
		x = []
		y = []
		z = []
		for f in self.marker:
			if len(self.marker[f]):
				x.append(self.marker[f][0])
				y.append(self.marker[f][1])
				z.append(self.marker[f][2])
		if len(x) and len(y) and len(z):
			hold = dict()
			hold["min"] = [min(x), min(y), min(z)]
			hold["max"] = [max(x), max(y), max(z)]
			return hold


#----------------------------------------------------------  

#Object for processing motion capture file
class mocapDBDict:
	def __init__(self, datafile, scaling):
		mocapMarkerDict.SCALE = scaling
		#read file
		f = open(datafile, 'r')
		data_in = f.readlines()
		f.close()
		
		self.mocap = collections.OrderedDict()
		text = data_in.pop(0)
		self.frames = len(data_in)
		items = text.split()[2:]
		for n in range(0, len(items), 3):
			self.mocap[items[n][0:-2]] = mocapMarkerDict()

		self.parseData(data_in)
		self.bbox = self.getBbox()
		
    #Process the file into a memory buffer
	def parseData(self, source):
		keys = self.mocap.keys()
		frame = 0
		for row in source:
			hold = row.split()[2:]
			for n in range(0,len(hold), 3):
				self.mocap[keys[(n/3)%len(keys)]].append(float(hold[n]), float(hold[n+1]), float(hold[n+2]), frame)
			frame += 1
			
	def getFrameData(self, frame):
		out = []
		for m in self.mocap:
			if frame in self.mocap[m]:
				out.append(self.mocap[m][frame])
		return out
		
	def getMarkerData(self, name, begin, end, step):
		out = []
		for i in range(begin, end, step):
			a = self.mocap[name].getData(i)
			if a:
				out.append(a)
			else:
				print("Missing Frame Number: " + str(i))
		return out
	
	def getNames(self):
		return self.mocap.keys()
		
	def numMarkers(self):
		len(self.mocap)
	
	def getBbox(self):
		mins = [[],[],[]]
		maxs = [[],[],[]]
		bbox = dict()
		for i in self.mocap:
			hold = self.mocap[i].getBbox()
			if hold is not None:
				for j in range(3):
					mins[j].append(hold["min"][j])
					maxs[j].append(hold["max"][j])
		bbox["min"] = [min(mins[0]), min(mins[1]), min(mins[2])]
		bbox["max"] = [max(maxs[0]), max(maxs[1]), max(maxs[2])]
		return bbox
