#!/usr/local/Cellar/python

"""
	This is a final version that uses all cores.
	It creates 325 leading frames, and 325 trailing frames; these are black frames.
	Slice speed is 3 pixels per frame.
	Slice width is 6 pixels


	MARTIN WALCH: 2016_08_20

"""
from __future__ import generators
import glob
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from PIL.ExifTags import TAGS, GPSTAGS
import string, sys, traceback, datetime, time, calendar
from datetime import datetime, date, time
from datetime import timedelta
import EXIF, os, shutil
import dirwalk
from PIL import *
import numpy as np
from multiprocessing import *
from SliceObject_REMASTER import *

#_______________________________________________________________________________________________________
ScreenWidth = 1920		# 1080P = 1920,	4K = 3840
ScreenHeight = 1080 	# 1080P = 1080,	4K = 2160
#	sliceCount 			= 		24,  48,  60,   96,   120,   144,   288,   320,    384, 480, 640, 960
#	hours per screen 	=		2    4 	  5 	8     10 	 12     24     26.66

sliceWidth = sW = 1
sliceSpeed = 1


SliceCount = SC = ScreenWidth/sW # produces a 6 pixel wide band



quality = 100
fileExt = '.jpg'

inputDir = '/Volumes/3TB_DP/Bradys_Lake_20170805-06/Working_Files/P1000806/P1000806_2K_25p_out_frames'
#inputDir = '/Users/marty/Documents/DTLA_Programming/JPG_REFINERY/JPG_PIXEL_TEST/input'
outputDir = '/Volumes/3TB_DP/Bradys_Lake_20170805-06/Working_Files/P1000806/P1000806_2K_25p_1-1_output'

location = 'P10008062K_25p_1-1_'

print
print "Input directory  = ", inputDir
print "Output directory = ", outputDir
print
print
print "Slice count = ", SC
print "Slice width = ", sW
print "Speed       = ", sliceSpeed
print
print "File extension = ", fileExt
print "Quality = ", quality
print

namePaths1 = []
namePaths = []					# a list of the full paths to each file
SliceObjectList = SOL = []		# list of all input files(jpegs) as instances of class SliceObject
SOL1 = []

slicePix=[]
imgSlice=[]

tick = 0


#_______________________________________________________________________________________________________

def renderAB(SliceObject):


	#-----------------------------------------------------------------------------------------------------
	#  SETUP the slices for FRAME A and FRAME B  
	# if screenwidth = 1920
	# & speed = 3
	# & sliceWidth = 6

	# AA Frame slices consists of 320 whole slices
	AA=[]
	AAx1 = 0
	AAx2 = sliceWidth
	for i in range(SC):
		aa = [AAx1,AAx2]
		AA.append(aa)
		AAx1 = AAx2
		AAx2 += sliceWidth
	print
	print


	# B Frame slices have 321 slices, 319 wholes slices, plus a half slice at the beginning and at the end
	B=[]
	Bx1 = 0
	Bx2 = sliceWidth/2
	for i in range(SC):
		b = [Bx1,Bx2]
		B.append(b)
		Bx1 = Bx2
		Bx2 += sliceWidth
	# BxF is the extra half slice we add to the end of the list for Frame B
	BxF = [(ScreenWidth-sliceSpeed), ScreenWidth]
	B.append(BxF)
	print


	print
	#print SliceObject.namePath
	print
	#print "SliceObject.ObjectNumber ", SliceObject.ObjectNumber
	obnum = SliceObject.ObjectNumber


	#-----------------------------------------------------------------------------------------------------
	#  FRAME A

	imgA = Image.new('RGB', (ScreenWidth, ScreenHeight))
	arrayGround = np.array(imgA)
	xx = len(AA)-1
	zz=0
	while xx >= 0:

		ax1 = AA[xx][0]
		ax2 = AA[xx][1]

		img1 = Image.open(SOL[xx+obnum].namePath)
		arrayImg = np.array(img1)

		slicePix1 = arrayImg[0:, ax1:ax2]
		arrayGround[0:, ax1:ax2] = slicePix1
		xx-=1

	# name and save the frame
	outNum1 = (SliceObject.ObjectNumber*2)
	print "outNum1 = ", outNum1
	outpathName = outputDir  + '/' +  str(location) + "_" + str(outNum1).rjust(6).replace(' ','0') + '.jpg'
	imgA = Image.fromarray(arrayGround)
	imgA.save(outpathName, 'jpeg', quality=quality)

	#-----------------------------------------------------------------------------------------------------
	#  FRAME B

	imgB = Image.new('RGB', (ScreenWidth, ScreenHeight))
	arrayGround = np.array(imgB)
	xx=len(B)-1

	while xx >= 0:

		bx1 = B[xx][0]
		bx2 = B[xx][1]

		img3 = Image.open(SOL[xx+obnum].namePath)
		arrayImg = np.array(img3)

		slicePix1 = arrayImg[0:, bx1:bx2]
		arrayGround[0:, bx1:bx2] = slicePix1
		xx-=1

	# name and save the frame
	outNum2 = ((SliceObject.ObjectNumber*2))+1
	print "outNum2 = ", outNum2
	outpathName = outputDir  + '/' +  str(location) + "_" + str(outNum2).rjust(6).replace(' ','0') + '.jpg'
	imgB = Image.fromarray(arrayGround)
	imgB.save(outpathName, 'jpeg', quality=quality)







#____1____________________________________________________________________________________________________
#	 walk the directory once and make a list that contains the name and dir path for every jpeg file

for root, dirs, files in os.walk(inputDir):
	for name in files:
		if name.endswith(fileExt):
			namePaths1.append(os.path.join(root,name))

xP = len(namePaths1)
print "total number of jpegs found = ", xP
print


#____2 & 3__________________________________________________________________________________________________
#	 sort the list from loop one according to datetime - then extract firstdatetime and lastdatetime from files.

namePaths1.sort()
"""
print "sorting complete"
firstdatetime = namePaths1[0]
lastdatetime = namePaths1[-1]

print "first file ", firstdatetime
print "last file  ", lastdatetime
print

location = str(namePaths1[0][-31:-24])
print "location ", location
fdt = str(namePaths1[0][-23:-4])
fdt2 = fdt
ldt = str(namePaths1[-1][-23:-4])
ldt2 = ldt
print "firstdatetime ", fdt
print "lastdatetime ", ldt

fdt = datetime.strptime(fdt,"%Y_%m_%d-%H_%M_%S")
ldt = datetime.strptime(ldt,"%Y_%m_%d-%H_%M_%S")

print "fdt ", fdt
print "ldt ", ldt
"""

#____4____________________________________________________________________________________________________
# loop to create and name blank files for beginning
"""
x = SliceCount + 4
newFDT = fdt - timedelta(minutes=5)

while x >= 0:

	img = Image.new('RGB',(ScreenWidth, ScreenHeight))
	FnewDT = datetime.strftime(newFDT, "%Y_%m_%d-%H_%M_%S")

	outpathName = str(location) + "_" + str(FnewDT) + '.jpg'
	img.save(inputDir + "/" + outpathName, 'jpeg', quality=quality)
	newFDT = newFDT - timedelta(minutes=5)

	x-=1

print
print "Start files added "
print
"""
#____5____________________________________________________________________________________________________
# loop to create and name blank files at the end
"""
xx = 0
newLDT = ldt + timedelta(minutes=5)

while xx < (SliceCount+30):

	img = Image.new('RGB',(ScreenWidth, ScreenHeight))
	FnewDT = datetime.strftime(newLDT, "%Y_%m_%d-%H_%M_%S")

	outpathName = str(location) + "_" + str(FnewDT) + '.jpg'
	img.save(inputDir + "/" + outpathName, 'jpeg', quality=quality)
	newLDT = newLDT + timedelta(minutes=5)

	xx+=1

print
print "End files added "
print 
"""
#____6____________________________________________________________________________________________________
#	 walk the expanded directory that now contains the additional frames 
#	 and re-make the list that contains the name and dir path for every jpeg file

for root, dirs, files in os.walk(inputDir):
	for name in files:
		if name.endswith(fileExt):
			namePaths.append(os.path.join(root,name))

zP = len(namePaths)
print "total number of jpegs now = ", zP

#_____7___________________________________________________________________________________________________
#	iterate over the list of all namePaths - creating a SliceObject for every element
#	and a SOL SLiceObjectList that contains them all

z = 0
for name in namePaths:
	SO = SliceObject(name)
	SOL.append(SO)
	
	#print SOL[z].namePath
	z+= 1

SOL_total = len(SOL)

print
print "SliceObjectList_total : ", SOL_total
print
print

#____8____________________________________________________________________________________________________
# XC is the amount we want to trim off SOL when we make our render list

XC = SliceCount+4
SOL2 = SOL[:-XC]


#______9__________________________________________________________________________________________________
# SOL2 is now the original list minus 324 black frames at the end
# this way the render completes when the active frames + 1 black frame have left the screen

print "Rendering "

pool = Pool()
pool.map(renderAB, SOL2)
pool.close() 
pool.join()

print
print "*__________________*___________________*_____________________* "
print
print 'all done'















