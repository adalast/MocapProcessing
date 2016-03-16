#---------------------------------------------------------------
#  Uses the motion capture DB objects to process the data from a file given in the mocapDBDict function call.
#  The data is then used to create a sequence of rib file that creates a line for each point.
#---------------------------------------------------------------

from mocapDBDict import mocapDBDict
  
scene_scale = 0.01
db = mocapDBDict('../mocap_data/swagger.txt', scene_scale)
  
markerID = 2
start = 1
end = db.frames
step = 1
curve_width = 0.1
coords = db.getMarkerData("CLAV", start, end, step)

rib = open('../archives/marker4.rib', 'w')
rib.write('#bbox: {} {} {} {} {} {}\n'.format(db.bbox["min"][0], db.bbox["min"][1], db.bbox["min"][2], db.bbox["max"][0], db.bbox["max"][1], db.bbox["max"][2]))
rib.write('Attribute "dice" "int roundcurve" [1]\n')
rib.write('Basis "catmull-rom" 1 "catmull-rom" 1\n')
rib.write('Curves "cubic" [%d] "nonperiodic"\n' % int(len(coords)))
rib.write('"P" [\n')

for n in range(0,len(coords)):
	x = coords[n][0]
	y = coords[n][1]
	z = coords[n][2]
	rib.write('\t%1.3f %1.3f %1.3f\n' % (x,y,z))
	
rib.write('\t] "constantwidth" [%1.3f]\n' % curve_width)
rib.close()
