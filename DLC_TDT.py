from DLCvis import *
from glob import glob

data=[]

subject=input('Subject id:')


os.chdir(r'C:\Users')

os.chdir(subject)


DLCfile=glob('*.csv')[0]#input('file name:')
tdtfile=glob('*st*')[0]#input('TDT file name:')


# get DLC data
#file='FP_mPFCOFC-190626-160523_c4f1-210403-145344_Cam1DLC_resnet50_dave_DLCJul29shuffle1_900000.csv'

with open(DLCfile,'r') as csvfile:
	reader=csv.reader(csvfile)
	for line in reader:
		data.append(line)
	csvfile.close()
data2=np.array(data)
headdata=data2[:, 4:7]#4:7
nosedata=data2[:,1:4]
bodydata=data2[:,16:19]
body2data=data2[:,19:22]


SideDict={'S17_M':'r','S3_M':'l','S427_M':'l','S428_M':'r','S20_M':'r','S18_F':'l','SC4F1_F':'l','SC4F2_F':'r','SC4M1_M':'l','SC4M2_M':'r','S5_F':'l','S15_M':'l','S19_F':'r'}
#get TDT data
tdtdata=tdt.read_block(tdtfile)
camerastamps=tdtdata.epocs.Cam1.onset


if SideDict[subject]=='r':
	seekon=tdtdata.epocs.PC0_.onset
	seekoff=tdtdata.epocs.PC0_.offset
elif SideDict[subject]=='l':	
	seekon=tdtdata.epocs.PC2_.onset
	seekoff=tdtdata.epocs.PC2_.offset


seekstamps=list(map(list, zip(seekon, seekoff)))
itistamps=list(map(list,zip(seekon-15,seekon+2)))



if subject == 'S427_M':
	seekstamps[39][1]=seekstamps[39][1]+.2
else:
	pass




framelocations=[]
itiframelocations=[]

for a in range(len(seekstamps)):
	camerastampon= np.where(seekstamps[a][0]>=camerastamps)[0][-1]
	camerastampoff= np.where(seekstamps[a][1]>=camerastamps)[0][-1]
	framelocations.append([camerastampon,camerastampoff])

	iticamerastampon= np.where(itistamps[a][0]>=camerastamps)[0][-1]
	iticamerastampoff= np.where(itistamps[a][1]>=camerastamps)[0][-1]	
	itiframelocations.append([iticamerastampon,iticamerastampoff])



seekdata=parseDLCdata(headdata,nosedata,framelocations,camerastamps)


x_activitydict=seekdata[0]
y_activitydict=seekdata[1]
distancedict=seekdata[2]
secondsdict=seekdata[3]
aborts=seekdata[5]
x_noseactivitydict=seekdata[6]
y_noseactivitydict=seekdata[7]


bodyfun=parseDLCdata(bodydata,body2data,framelocations,camerastamps)
x_bodyactivitydict=bodyfun[0]
y_bodyactivitydict=bodyfun[1]
x_body2activitydict=bodyfun[6]
y_body2activitydict=bodyfun[7]


itidata=parseDLCdata(headdata,bodydata,itiframelocations,camerastamps)
x_itiactivitydict=itidata[0]
y_itiactivitydict=itidata[1]
itidistancedict=itidata[2]
itisecondsdict=itidata[3]


bodyangles=bodyangle(x_activitydict,y_activitydict,x_body2activitydict,y_body2activitydict)


os.chdir('../')

pd.DataFrame(aborts).set_axis(['Trial', 'Abort Count', 'Abort Time(avg)'], axis=1, inplace=False).to_csv('abortdata.csv')




















#####################################




# x_activitydict={}
# y_activitydict={}
# x_bodyactivitydict={}
# y_bodyactivitydict={}
# distancedict={}
# secondsdict={}
# dfforjandro=[]
# location=-1
# maxlength=0



# for a in range(len(framelocations)):
# 	#print(a)
# 	activitydatax=headdata[framelocations[a][0]+3:framelocations[a][1]+3][:,0]#plus 3 to skip the headers
# 	activitydatay=headdata[framelocations[a][0]+3:framelocations[a][1]+3][:,1]
# 	activityliklihood=headdata[framelocations[a][0]+3:framelocations[a][1]+3][:,2].astype("float64")


# 	# bodyactivitydatax=bodydata[framelocations[a][0]+3:framelocations[a][1]+3][:,0]#plus 3 to skip the headers
# 	# bodyactivitydatay=bodydata[framelocations[a][0]+3:framelocations[a][1]+3][:,1]
# 	# bodyactivityliklihood=bodydata[framelocations[a][0]+3:framelocations[a][1]+3][:,2].astype("float64")
	
# 	seconds=camerastamps[framelocations[a][0]:framelocations[a][1]]
# 	secondsnorm=seconds-seconds[0]

# 	framestodrop=np.where(activityliklihood <=0.01)[0].tolist()
# 	bodyframestodrop=np.where(bodyactivityliklihood <=0.01)[0].tolist()

# 	activitydatax=np.delete(activitydatax,framestodrop)
# 	activitydatay=np.delete(activitydatay,framestodrop)
# 	bodyactivitydatax=np.delete(bodyactivitydatax,framestodrop)
# 	bodyactivitydatay=np.delete(bodyactivitydatay,framestodrop)

# 	secondsnorm=np.delete(secondsnorm,framestodrop)
# 	trial=a+1
# 	x_activitydict.update({trial:activitydatax.astype("float64")})
# 	y_activitydict.update({trial:activitydatay.astype("float64")})


# 	dfforjandro.append(['time'+str(trial)]+secondsnorm.tolist())
# 	dfforjandro.append(['x'+str(trial)]+activitydatax.tolist())
# 	dfforjandro.append(['y'+str(trial)]+activitydatay.tolist())

# 	if len(['x'+str(trial)]+activitydatax.tolist()) < maxlength:
# 		pass
# 	else:
# 		maxlength=len(['x'+str(trial)]+activitydatax.tolist())      




# 	x_bodyactivitydict.update({trial:bodyactivitydatax.astype("float64")})
# 	y_bodyactivitydict.update({trial:bodyactivitydatay.astype("float64")})
# 	secondsdict.update({trial:secondsnorm.astype("float64")})






# ### get euclid distance from seek nosepoke
# for a in range(len(x_activitydict)):
# 	xandy=list(zip(x_activitydict[a+1],y_activitydict[a+1]))
# 	trial=a+1
# 	temparray=np.array([])
# 	for point in range(len(xandy)):
# 		distance=round(np.linalg.norm(np.array(nosepokeloc) - np.array(xandy[point])),2)
# 		temparray=np.append(temparray,[distance])
# 	distancedict.update({trial:temparray.astype("float64")})







##########################################################################################
# with open('jandroDF.csv','w') as file:
# 	wr=csv.writer(file,lineterminator='\n')
# 	for item in dfforjandro:
# 		wr.writerow(item)

# newDF=pd.read_csv('jandroDF.csv',names = list(range(0,maxlength))).transpose()
# newDF.to_csv('jandroDF.csv')

# os.chdir('../')


# abortcount=0
# trip=0
# aborttime=[]
# for a in range(len(distancedict[43])):

# 	if distancedict[43][a] <=200 and trip==0:
# 		trip=1
# 		entersample=secondsdict[43][a]
# 		a=a+1

# 	elif distancedict[43][a] <=200 and trip==1:
# 		a=a+1
# 	elif distancedict[43][a] > 200 and trip==1:
# 		abortcount=abortcount+1
# 		aborttime.append(secondsdict[43][a]-entersample)
# 		trip=0
# 		a=a+1

# 	elif distancedict[43][a] > 200 and trip==0:
# 		trip=0
# 		a=a+1



# def aniplot(trial,x_activitydict=x_activitydict,y_activitydict=y_activitydict,savefile=False,filename='test.gif', markers=True):
# 	x = x_activitydict[trial]#np.arange(1,len(x_activitydict[trial])+1,1)   secondsdict[trial]
# 	y = y_activitydict[trial]

# 	fig, ax = plt.subplots()
# 	line, = ax.plot(x, y, color='k')
# 	line2, = ax.plot(x_bodyactivitydict[trial], y_bodyactivitydict[trial], color='r')

# 	def update(num, x, y, line):
# 	    line.set_data(x[:num], y[:num])

# 	    line.axes.axis([0, 640,480,0])
# 	    return line,


# 	ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],interval=50, blit=True)
	
# 	if markers == True:
# 		plt.plot(71,84,'r*')
# 		plt.plot(37,365,'mo')
# 		plt.plot(627,167,'bo')
# 		plt.plot(x_activitydict[trial][1],y_activitydict[trial][1],'sg')
# 		plt.plot(x_activitydict[trial][-1],y_activitydict[trial][-1],'sr')
# 	else:
# 		pass
# 	if savefile == True:
# 		ani.save(filename)
# 	else:
# 		pass
# 	plt.show()


# def traceplot(xdata,ydata):
# 	fig, axs = plt.subplots(8,10,sharex=True,sharey=True)
# 	for a in range(0,len(x_activitydict)):
# 		if a > 9 and a <20:
# 			rowspot=1
# 			colspot=a-10
# 		elif a >19 and a<30:
# 			rowspot=2
# 			colspot=a-20
# 		elif a>29  and a<40:
# 			rowspot=3
# 			colspot=a-30
# 		elif a >39 and a <50:
# 			rowspot=4
# 			colspot=a-40
# 		elif a >49 and a<60:
# 			rowspot=5
# 			colspot=a-50

# 		elif a >59 and a<70: 
# 			rowspot=6
# 			colspot=a-60
# 		elif a >69 and a<80: 
# 			rowspot=7
# 			colspot=a-70			
# 		elif a >79 and a<89:
# 			rowspot=8
# 			colspot=a-80
# 		elif a<10:
# 			rowspot=0
# 			colspot=a
		

# 		axs[rowspot,colspot].plot(xdata[a+1],ydata[a+1])
# 		#axs[rowspot,colspot].plot(x_bodyactivitydict[a+1],y_bodyactivitydict[a+1])
# 		axs[rowspot,colspot].plot(82,66,'r*')
# 		axs[rowspot,colspot].plot(62,336,'mo')
# 		axs[rowspot,colspot].plot(606,163,'bo')
# 		axs[rowspot,colspot].plot(xdata[a+1][0],ydata[a+1][0],'sg')
# 		axs[rowspot,colspot].plot(xdata[a+1][-1],ydata[a+1][-1],'sr')


# 	plt.xlim(0, 640)
# 	plt.ylim(480,0)

# 	plt.show()



#c4f1NP=71,84, take=37,365,'mo' feeder=627,167,'bo'
# def distanceplot(xdata=secondsdict,ydata=distancedict):
# 	fig, axs = plt.subplots(5,10,sharex=False,sharey=True)
# 	for a in range(0,50):
# 		if a > 9 and a <20:
# 			rowspot=1
# 			colspot=a-10
# 		elif a >19 and a<30:
# 			rowspot=2
# 			colspot=a-20
# 		elif a>29  and a<40:
# 			rowspot=3
# 			colspot=a-30
# 		elif a >39 and a <50:
# 			rowspot=4
# 			colspot=a-40
# 		elif a<10:
# 			rowspot=0
# 			colspot=a
		

# 		axs[rowspot,colspot].plot(xdata[a+1],ydata[a+1])
# 		# axs[rowspot,colspot].plot(71,84,'r*')
# 		# axs[rowspot,colspot].plot(37,365,'mo')
# 		# axs[rowspot,colspot].plot(627,167,'mo')
# 		# axs[rowspot,colspot].plot(x_activitydict[a+1][0],y_activitydict[a+1][0],'sg')
# 		# axs[rowspot,colspot].plot(x_activitydict[a+1][-1],y_activitydict[a+1][-1],'sr')


# 	# plt.xlim(0, 640)
# 	# plt.ylim(480,0)

# 	plt.show()







# trial=43
# fig = plt.figure()
# ax1 = plt.axes(xlim=(0, 640), ylim=(480,0))
# line, = ax1.plot([], [], lw=2)
# plt.xlabel('x')
# plt.ylabel('y')

# plotlays, plotcols = [2], ["black","red"]
# lines = []
# for index in range(2):
#     lobj = ax1.plot([],[],marker='o',linestyle='',lw=2,color=plotcols[index])[0]
#     lines.append(lobj)


# def init():
#     for line in lines:
#         line.set_data([],[])
#     return lines

# x1,y1 = [],[]
# x2,y2 = [],[]




# def animate(i):



#     x = x_bodyactivitydict[trial][i]
#     y = y_bodyactivitydict[trial][i]
#     x1.append(x)
#     y1.append(y)

#     x = x_activitydict[trial][i]
#     y = y_activitydict[trial][i]
#     x2.append(x)
#     y2.append(y)

#     xlist = [x1, x2]
#     ylist = [y1, y2]


#     #for index in range(0,1):
#     for lnum,line in enumerate(lines):
#         line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 




#     return lines


# # call the animator.  blit=True means only re-draw the parts that have changed.
# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=len(x_activitydict[trial]), interval=100, blit=True,repeat=False)


# plt.show()



# import numpy as np
# import numpy.random
# import matplotlib.pyplot as plt
# from matplotlib import cm as CM

# # Generate some test data
# x = x_activitydict[43]
# y = y_activitydict[43]

# heatmap, xedges, yedges = np.histogram2d(x, y, bins=(10,20))
# extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# plt.clf()
# plt.imshow(heatmap.T, extent=extent, origin='lower',cmap=cm.jet)
# plt.show()


# from matplotlib import pyplot as PLT
# from matplotlib import cm as CM
# from matplotlib import mlab as ML
# import numpy as NP

# n = 1e5
# x = y = NP.linspace(-5, 5, 100)
# X, Y = NP.meshgrid(x, y)
# Z1 = ML.bivariate_normal(X, Y, 2, 2, 0, 0)
# Z2 = ML.bivariate_normal(X, Y, 4, 1, 1, 1)
# ZD = Z2 - Z1
# x = X.ravel()
# y = Y.ravel()
# z = ZD.ravel()
# gridsize=30
# PLT.subplot(111)

# # if 'bins=None', then color of each hexagon corresponds directly to its count
# # 'C' is optional--it maps values to x-y coordinates; if 'C' is None (default) then 
# # the result is a pure 2D histogram 

# PLT.hexbin(x, y, C=z, gridsize=gridsize, cmap=CM.jet, bins=None)
# PLT.axis([x.min(), x.max(), y.min(), y.max()])

# cb = PLT.colorbar()
# cb.set_label('mean value')
# PLT.show()   



# def hexplots(xdata,ydata,showtrace=False,colmin=0,colmax=20):
# 	fig, axs = plt.subplots(8,10,sharex=True,sharey=True)
# 	for a in range(0,len(x_activitydict)): #50
# 		if a > 9 and a <20:
# 			rowspot=1
# 			colspot=a-10
# 		elif a >19 and a<30:
# 			rowspot=2
# 			colspot=a-20
# 		elif a>29  and a<40:
# 			rowspot=3
# 			colspot=a-30
# 		elif a >39 and a <50:
# 			rowspot=4
# 			colspot=a-40
# 		elif a >49 and a<60:
# 			rowspot=5
# 			colspot=a-50

# 		elif a >59 and a<70: 
# 			rowspot=6
# 			colspot=a-60
# 		elif a >69 and a<80: 
# 			rowspot=7
# 			colspot=a-70			
# 		elif a >79 and a<89:
# 			rowspot=8
# 			colspot=a-80
# 		elif a<10:
# 			rowspot=0
# 			colspot=a
		

# 		axs[rowspot,colspot].hexbin(xdata[a+1],ydata[a+1],gridsize=(8,8),cmap=CM.jet,vmin=colmin,vmax=colmax,extent=(0, 640,480,0))
# 		#axs[rowspot,colspot].legend(loc='upper center')
# 		if showtrace == True:
# 			axs[rowspot,colspot].plot(xdata[a+1],ydata[a+1])
# 		else:
# 			pass 
		
# 		#fig.colorbar(axs[0,1].hexbin(xdata[1],ydata[1],gridsize=(8,8),cmap=CM.jet,vmin=colmin,vmax=colmax,extent=(0, 640,480,0)), cax=cbar_ax)
# 		#axs[rowspot,colspot].hexbin(x_bodyactivitydict[a+1],y_bodyactivitydict[a+1])
# 		#axs[rowspot,colspot].plot(71,84,'r*')
# 		#axs[rowspot,colspot].plot(37,365,'mo')
# 		#axs[rowspot,colspot].plot(627,167,'bo') vmin=-2,vmax=10
# 		#axs[rowspot,colspot].plot(x_activitydict[a+1][0],y_activitydict[a+1][0],'sg')
# 		#axs[rowspot,colspot].plot(x_activitydict[a+1][-1],y_activitydict[a+1][-1],'sr')


# 	plt.xlim(0, 640)
# 	plt.ylim(480,0)
# 	cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
# 	fig.colorbar(hexbin(x_activitydict[a],y_activitydict[a],cmap=CM.jet,vmin=colmin,vmax=colmax),cax=cbar_ax)	

# 	plt.show()
