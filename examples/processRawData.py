import os
import sys
import argparse
import simSettings as sim

def cropRawFile(filepath,**kwargs):
	timeScale = kwargs.get("timeScale",1)
	savefile = os.path.splitext(os.path.basename(filepath))[0]+"_cropped.txt"
	savefilepath = os.path.join(os.path.dirname(filePath)+"_cropped", savefile)
	print("Loading", filepath)
	print("Savefile", savefile)
	print("Savefilepath", savefilepath)
	if not os.path.exists(os.path.dirname(savefilepath)):
			os.makedirs(os.path.dirname(savefilepath))
	fIn = open(filepath,'r')
	fOut = open(savefilepath,'w')
	for line in fIn:
		lineTime = float(line.split(',')[0])
		if lineTime >= kwargs.get("newStart",0):
			if lineTime <= kwargs.get("newEnd",float('inf')):
				fOut.write(str((lineTime-kwargs.get("newStart",0))/timeScale) +"," + ",".join(line.split(',')[1:]))
	fIn.close()
	fOut.close()


if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	for file in sim.files:
		filePath = os.path.join(sim.loadLocation,os.path.splitext(file)[0],file)
		cropRawFile(filePath, newStart = 100, timeScale = 2, newEnd = 200)