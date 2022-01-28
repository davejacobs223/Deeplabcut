
import numpy as np
import tdt
import csv
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm as CM
import pandas as pd
import os
from matplotlib import cm as CM


def parseDLCdata(dataset,dataset2,locations,cameratimes,threshold=0.01,nosepokeloc=np.array((71,84))):
	x_activitydict={}
	y_activitydict={}
	x_bodyactivitydict={}
	y_bodyactivitydict={}
	distancedict={}
	secondsdict={}
	dfforjandro=[]
	location=-1
	maxlength=0

	for a in range(len(locations)):
		#print(a)
		activitydatax=dataset[locations[a][0]+3:locations[a][1]+3][:,0]#plus 3 to skip the headers
		activitydatay=dataset[locations[a][0]+3:locations[a][1]+3][:,1]
		activityliklihood=dataset[locations[a][0]+3:locations[a][1]+3][:,2].astype("float64")


		bodyactivitydatax=dataset2[locations[a][0]+3:locations[a][1]+3][:,0]#plus 3 to skip the headers
		bodyactivitydatay=dataset2[locations[a][0]+3:locations[a][1]+3][:,1]
		bodyactivityliklihood=dataset2[locations[a][0]+3:locations[a][1]+3][:,2].astype("float64")
		
		seconds=cameratimes[locations[a][0]:locations[a][1]]
		secondsnorm=seconds-seconds[0]

		framestodrop=np.where(activityliklihood <=threshold)[0].tolist()
		bodyframestodrop=np.where(bodyactivityliklihood <=threshold)[0].tolist()

		activitydatax=np.delete(activitydatax,framestodrop)
		activitydatay=np.delete(activitydatay,framestodrop)
		bodyactivitydatax=np.delete(bodyactivitydatax,framestodrop)
		bodyactivitydatay=np.delete(bodyactivitydatay,framestodrop)

		secondsnorm=np.delete(secondsnorm,framestodrop)
		trial=a+1
		x_activitydict.update({trial:activitydatax.astype("float64")})
		y_activitydict.update({trial:activitydatay.astype("float64")})


		dfforjandro.append(['time'+str(trial)]+secondsnorm.tolist())
		dfforjandro.append(['x'+str(trial)]+activitydatax.tolist())
		dfforjandro.append(['y'+str(trial)]+activitydatay.tolist())

		if len(['x'+str(trial)]+activitydatax.tolist()) < maxlength:
			pass
		else:
			maxlength=len(['x'+str(trial)]+activitydatax.tolist())      




		x_bodyactivitydict.update({trial:bodyactivitydatax.astype("float64")})
		y_bodyactivitydict.update({trial:bodyactivitydatay.astype("float64")})
		secondsdict.update({trial:secondsnorm.astype("float64")})




	for a in range(len(x_activitydict)):
		xandy=list(zip(x_activitydict[a+1],y_activitydict[a+1]))
		trial=a+1
		temparray=np.array([])
		for point in range(len(xandy)):
			distance=round(np.linalg.norm(np.array(nosepokeloc) - np.array(xandy[point])),2)
			temparray=np.append(temparray,[distance])
		distancedict.update({trial:temparray.astype("float64")})
	abortlist=[]
	

	for a in range(len(distancedict)):

		trial=a+1
		abortcount=0
		trip=0
		aborttime=[]
		for spot in range(len(distancedict[trial])):

			if distancedict[trial][spot] <=200 and trip==0:
				trip=1
				entersample=secondsdict[trial][spot]
				spot=spot+1

			elif distancedict[trial][spot] <=200 and trip==1:
				spot=spot+1
			elif distancedict[trial][spot] > 200 and trip==1:
				abortcount=abortcount+1
				aborttime.append(secondsdict[trial][spot]-entersample)
				trip=0
				spot=spot+1

			elif distancedict[trial][spot] > 200 and trip==0:
				trip=0
				spot=spot+1
		abortlist.append([trial,abortcount,mean(aborttime)])


	return (x_activitydict,y_activitydict,distancedict,secondsdict,dfforjandro,abortlist,x_bodyactivitydict,y_bodyactivitydict)



def bodyangle(xdata,ydata,xbdata,ybdata):
	datahold=[]
	for a in range(len(xdata)):
		l1x1=xdata[a+1][len(xdata[a+1])-2:-1][0]
		l1y1=ydata[a+1][len(ydata[a+1])-2:-1][0]
		l1x2=xbdata[a+1][len(xbdata[a+1])-2:-1][0]
		l1y2=ybdata[a+1][len(ybdata[a+1])-2:-1][0]

		head=np.array([l1x1,l1x2])
		body=np.array([l1y1,l1y2])

		l2x1=71
		l2y1=84
		l2x2=62
		l2y2=336

		spoke=np.array([l2x1,l2x2])
		tpoke=np.array([l2y1,l2y2])

		s1=np.polyfit(head,body,1)[0]
		s2=np.polyfit(spoke,tpoke,1)[0]


		datahold.append((np.degrees(np.arctan(s1))-np.degrees(np.arctan(s2))))
	return (datahold)





def aniplot(trial,xdata,ydata,savefile=False,filename='test.gif', markers=True):
	x = xdata[trial]#np.arange(1,len(x_activitydict[trial])+1,1)   secondsdict[trial]
	y = ydata[trial]

	fig, ax = plt.subplots()
	line, = ax.plot(x, y, color='k')
	#line2, = ax.plot(x_bodyactivitydict[trial], y_bodyactivitydict[trial], color='r')

	def update(num, x, y, line):
	    line.set_data(x[:num], y[:num])

	    line.axes.axis([0, 640,480,0])
	    return line,


	ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],interval=50, blit=True)
	
	if markers == True:
		plt.plot(71,84,'r*')
		plt.plot(37,365,'mo')
		plt.plot(627,167,'bo')
		plt.plot(xdata[trial][1],ydata[trial][1],'sg')
		plt.plot(xdata[trial][-1],ydata[trial][-1],'sr')
	else:
		pass
	if savefile == True:
		ani.save(filename)
	else:
		pass
	plt.show()


def traceplot(xdata,ydata,xdata2,ydata2,xdata3,ydata3):
	fig, axs = plt.subplots(8,10,sharex=True,sharey=True)
	for a in range(0,len(xdata)):
		if a > 9 and a <20:
			rowspot=1
			colspot=a-10
		elif a >19 and a<30:
			rowspot=2
			colspot=a-20
		elif a>29  and a<40:
			rowspot=3
			colspot=a-30
		elif a >39 and a <50:
			rowspot=4
			colspot=a-40
		elif a >49 and a<60:
			rowspot=5
			colspot=a-50

		elif a >59 and a<70: 
			rowspot=6
			colspot=a-60
		elif a >69 and a<80: 
			rowspot=7
			colspot=a-70			
		elif a >79 and a<89:
			rowspot=8
			colspot=a-80
		elif a<10:
			rowspot=0
			colspot=a
		

		axs[rowspot,colspot].plot(xdata[a+1][len(xdata[a+1])-2:-1],ydata[a+1][len(ydata[a+1])-2:-1],'bo')#(xdata[a+1],ydata[a+1])
		axs[rowspot,colspot].plot(xdata2[a+1][len(xdata2[a+1])-2:-1],ydata2[a+1][len(ydata2[a+1])-2:-1],'ro')#(x_bodyactivitydict[a+1],y_bodyactivitydict[a+1])
		axs[rowspot,colspot].plot(xdata3[a+1][len(xdata3[a+1])-2:-1],ydata3[a+1][len(ydata3[a+1])-2:-1],'rs')
		axs[rowspot,colspot].plot(xdata[a+1],ydata[a+1])
		axs[rowspot,colspot].plot([xdata[a+1][len(xdata[a+1])-2:-1],xdata3[a+1][len(xdata3[a+1])-2:-1]],[ydata[a+1][len(ydata[a+1])-2:-1],ydata3[a+1][len(ydata3[a+1])-2:-1]],color='green',linewidth=5,marker='<')
		axs[rowspot,colspot].plot(82,66,'r*')
		axs[rowspot,colspot].plot(62,336,'mo')
		axs[rowspot,colspot].plot(606,163,'bo')
		#axs[rowspot,colspot].plot(xdata[a+1][0],ydata[a+1][0],'sg')
		#axs[rowspot,colspot].plot(xdata[a+1][-1],ydata[a+1][-1],'sr')


	plt.xlim(0, 640)
	plt.ylim(480,0)

	plt.show()



#c4f1NP=71,84, take=37,365,'mo' feeder=627,167,'bo'
def distanceplot(xdata,ydata):
	fig, axs = plt.subplots(8,10,sharex=False,sharey=True)
	for a in range(0,len(xdata)):
		if a > 9 and a <20:
			rowspot=1
			colspot=a-10
		elif a >19 and a<30:
			rowspot=2
			colspot=a-20
		elif a>29  and a<40:
			rowspot=3
			colspot=a-30
		elif a >39 and a <50:
			rowspot=4
			colspot=a-40
		elif a >49 and a<60:
			rowspot=5
			colspot=a-50

		elif a >59 and a<70: 
			rowspot=6
			colspot=a-60
		elif a >69 and a<80: 
			rowspot=7
			colspot=a-70			
		elif a >79 and a<89:
			rowspot=8
			colspot=a-80
		elif a<10:
			rowspot=0
			colspot=a
		

		axs[rowspot,colspot].plot(xdata[a+1],ydata[a+1])
		# axs[rowspot,colspot].plot(71,84,'r*')
		# axs[rowspot,colspot].plot(37,365,'mo')
		# axs[rowspot,colspot].plot(627,167,'mo')
		# axs[rowspot,colspot].plot(x_activitydict[a+1][0],y_activitydict[a+1][0],'sg')
		# axs[rowspot,colspot].plot(x_activitydict[a+1][-1],y_activitydict[a+1][-1],'sr')


	# plt.xlim(0, 640)
	# plt.ylim(480,0)

	plt.show()













def hexplots(xdata,ydata,showtrace=False,colmin=0,colmax=20):
	fig, axs = plt.subplots(8,10,sharex=True,sharey=True)
	for a in range(0,len(xdata)): #50
		if a > 9 and a <20:
			rowspot=1
			colspot=a-10
		elif a >19 and a<30:
			rowspot=2
			colspot=a-20
		elif a>29  and a<40:
			rowspot=3
			colspot=a-30
		elif a >39 and a <50:
			rowspot=4
			colspot=a-40
		elif a >49 and a<60:
			rowspot=5
			colspot=a-50

		elif a >59 and a<70: 
			rowspot=6
			colspot=a-60
		elif a >69 and a<80: 
			rowspot=7
			colspot=a-70			
		elif a >79 and a<89:
			rowspot=8
			colspot=a-80
		elif a<10:
			rowspot=0
			colspot=a
		

		axs[rowspot,colspot].hexbin(xdata[a+1],ydata[a+1],gridsize=(8,8),cmap=CM.jet,vmin=colmin,vmax=colmax,extent=(0, 640,480,0))
		#axs[rowspot,colspot].legend(loc='upper center')
		if showtrace == True:
			axs[rowspot,colspot].plot(xdata[a+1],ydata[a+1])
		else:
			pass 
		
		#fig.colorbar(axs[0,1].hexbin(xdata[1],ydata[1],gridsize=(8,8),cmap=CM.jet,vmin=colmin,vmax=colmax,extent=(0, 640,480,0)), cax=cbar_ax)
		#axs[rowspot,colspot].hexbin(x_bodyactivitydict[a+1],y_bodyactivitydict[a+1])
		#axs[rowspot,colspot].plot(71,84,'r*')
		#axs[rowspot,colspot].plot(37,365,'mo')
		#axs[rowspot,colspot].plot(627,167,'bo') vmin=-2,vmax=10
		#axs[rowspot,colspot].plot(x_activitydict[a+1][0],y_activitydict[a+1][0],'sg')
		#axs[rowspot,colspot].plot(x_activitydict[a+1][-1],y_activitydict[a+1][-1],'sr')


	plt.xlim(0, 640)
	plt.ylim(480,0)
	cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
	fig.colorbar(hexbin(xdata[a],ydata[a],cmap=CM.jet,vmin=colmin,vmax=colmax),cax=cbar_ax)	

	plt.show()