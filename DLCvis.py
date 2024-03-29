
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


def parseDLCdata(dataset,locations,cameratimes,threshold=0.01,abort_threshold=50,nosepokeloc=np.array((71,84)),fastdrops=[]):
	masterdict={}
	distancedict={}
	secondsdict={}
	dfforjandro=[]
	distanceatend=[]

	abortcamtime=[]


	location=-1
	maxlength=0

	for a in range(len(locations)):

		#implant
		IMactivitydatax=dataset[locations[a][0]:locations[a][1]][:,0]
		IMactivitydatay=dataset[locations[a][0]:locations[a][1]][:,1]
		IMactivityliklihood=dataset[locations[a][0]:locations[a][1]][:,2]
		#left ear
		LEactivitydatax=dataset[locations[a][0]:locations[a][1]][:,3]
		LEactivitydatay=dataset[locations[a][0]:locations[a][1]][:,4]
		LEactivityliklihood=dataset[locations[a][0]:locations[a][1]][:,5]		
		#rightear
		REactivitydatax=dataset[locations[a][0]:locations[a][1]][:,6]
		REactivitydatay=dataset[locations[a][0]:locations[a][1]][:,7]
		REactivityliklihood=dataset[locations[a][0]:locations[a][1]][:,8]
		#body
		BDactivitydatax=dataset[locations[a][0]:locations[a][1]][:,9]
		BDactivitydatay=dataset[locations[a][0]:locations[a][1]][:,10]
		BDactivityliklihood=dataset[locations[a][0]:locations[a][1]][:,11]
		#tail base
		TBactivitydatax=dataset[locations[a][0]:locations[a][1]][:,12]
		TBactivitydatay=dataset[locations[a][0]:locations[a][1]][:,13]
		TBactivityliklihood=dataset[locations[a][0]:locations[a][1]][:,14]
		#trialtime
		seconds=cameratimes[locations[a][0]:locations[a][1]]
		secondsnorm=seconds-seconds[0]



		#concat all of it
		concatarray=np.column_stack((secondsnorm,IMactivitydatax,IMactivitydatay,IMactivityliklihood,LEactivitydatax,LEactivitydatay,LEactivityliklihood,REactivitydatax,REactivitydatay,REactivityliklihood,BDactivitydatax,BDactivitydatay,BDactivityliklihood,TBactivitydatax,TBactivitydatay,TBactivityliklihood,seconds))
		concatarray=concatarray[concatarray[:,3]>threshold]

		# get trial number
		trial=a+1

		#make one dictionary to rule them all
		masterdict.update({trial:{'seconds':concatarray[:,0],
		 'x-implant':concatarray[:,1],
		 'y-implant':concatarray[:,2],
		 'p-implant':concatarray[:,3],
		 'x-leftear':concatarray[:,4],
		 'y-leftear':concatarray[:,5],
		 'p-leftear':concatarray[:,6],
		 'x-rightear':concatarray[:,7],
		 'y-rightear':concatarray[:,8],
		 'p-rightear':concatarray[:,9],
		 'x-body':concatarray[:,10],
		 'y-body':concatarray[:,11],
		 'p-body':concatarray[:,12],
		 'x-tailbase':concatarray[:,13],
		 'y-tailbase':concatarray[:,14],
		 'p-tailbase':concatarray[:,15],
		 'seconds(non-norm)':concatarray[:,16]}})


		#drop out the 'fast' trials to be calulated as NANs
		if len(fastdrops)>0:
			for a in fastdrops:
				masterdict.update({a+1:{'seconds':np.array([]),
				 'x-implant':np.array([]),
				 'y-implant':np.array([]),
				 'p-implant':np.array([]),
				 'x-leftear':np.array([]),
				 'y-leftear':np.array([]),
				 'p-leftear':np.array([]),
				 'x-rightear':np.array([]),
				 'y-rightear':np.array([]),
				 'p-rightear':np.array([]),
				 'x-body':np.array([]),
				 'y-body':np.array([]),
				 'p-body':np.array([]),
				 'x-tailbase':np.array([]),
				 'y-tailbase':np.array([]),
				 'p-tailbase':np.array([]),
				 'seconds(non-norm)':np.array([])}})				


		else:
			pass






   
# gets distance per trial of animal from seek nosepoke

	for a in range(len(masterdict)):
		xandy=list(zip(masterdict[a+1]['x-implant'],masterdict[a+1]['y-implant']))
		trial=a+1
		temparray=np.array([])
		for point in range(len(xandy)):
			distance=round(np.linalg.norm(np.array(nosepokeloc) - np.array(xandy[point])),2)
			temparray=np.append(temparray,[distance])
		if len(temparray)>0:
			distanceatend.append(temparray[-1])
		else:
			distanceatend.append(np.nan)

		distancedict.update({trial:temparray.astype("float64")})
	abortlist=[]
	
# get the abort for each trial
	for a in range(len(distancedict)):

		trial=a+1
		abortcount=0
		trip=0
		aborttime=[]
		# minimum distance from nosepoke
		min_closeness=abort_threshold
		
		for spot in range(len(distancedict[trial])):
		
			if distancedict[trial][spot] <=min_closeness and trip==0:
				trip=1
				entersample=masterdict[trial]['seconds'][spot]
				enterrawtime=masterdict[trial]['seconds(non-norm)'][spot]
				spot=spot+1

			elif distancedict[trial][spot] <= min_closeness and trip==1:
				spot=spot+1
			elif distancedict[trial][spot] > min_closeness and trip==1:
				abortcount=abortcount+1
				aborttime.append(masterdict[trial]['seconds'][spot]-entersample)

				#get the raw time to backtrack to tdt trace (dsj 10/11/22)
				rawtime=masterdict[trial]['seconds(non-norm)'][spot]
				abortcamtime.append([trial,rawtime,enterrawtime])

				#carry on....
				trip=0
				spot=spot+1

			elif distancedict[trial][spot] > min_closeness and trip==0:
				trip=0
				spot=spot+1
#path to fix if no samples are above threshold
		if len(distancedict[trial])==0:
			abortcount=np.nan
			aborttime.append(np.nan)
			print('one trial with no valid samples')
		else:
			pass


		abortlist.append([trial,abortcount,mean(aborttime)])


	return (masterdict,distancedict,abortlist,min_closeness,distanceatend,abortcamtime)


#UPDATED note this uses the angle WHEN the nosepoke happens
#bodyangle(maindict,seek location, take location)
def bodyangle(data,SL,TL,side='l'):
	datahold=[]

	for a in range(len(data)):

#patch if there are no valid samples
		if len(data[a+1]['x-implant'])>0:
			l1x1=data[a+1]['x-implant'][-1]#[len(data[a+1]['x-implant'])-2:-1][0]
			l1y1=data[a+1]['y-implant'][-1]#[len(data[a+1])-2:-1][0]
			l1x2=data[a+1]['x-body'][-1]#[len(data[a+1])-2:-1][0]
			l1y2=data[a+1]['y-body'][-1]#[len(data[a+1])-2:-1][0]
			leX=data[a+1]['x-leftear'][-1]
			leY=data[a+1]['y-leftear'][-1]
			reX=data[a+1]['x-rightear'][-1]
			reY=data[a+1]['y-rightear'][-1]

			head=np.array([l1x1,l1x2])
			body=np.array([l1y1,l1y2])
			xpoke=np.array([SL[0],TL[0]])
			ypoke=np.array([SL[1],TL[1]])

			headspot=np.array([l1x1,l1y1])
			bodyspot=np.array([l1x2,l1y2])
			lefte=np.array([leX,leY])
			righte=np.array([reX,reY])

			s1=np.polyfit(head,body,1)[0]
			s2=np.polyfit(xpoke,ypoke,1)[0]

			if (1+s1*s2)==0:
				bodang=90
			else:
				bodang=np.arctan((s1-s2)/(1+s1*s2))
				bodangdeg=np.degrees(bodang)

			if side=='l':
				if bodangdeg>=0:	
					adjustang=180-bodangdeg
				elif bodangdeg<0:
					adjustang=abs(bodangdeg)
				datahold.append(adjustang)
				
			elif side=='r':
				if bodangdeg>=0:	
					adjustang=bodangdeg
				elif bodangdeg<0:
					adjustang=180-abs(bodangdeg)
				datahold.append(adjustang)
		else:
			datahold.append(np.nan)
	return (datahold)

#new function for getting distance of an activity path (9-8-22 - DSJ)
#working on addidng freezing
def distancetraveled(data,velcut=1):
	datahold=[]
	immobhold=[]
	
	for sample in range(len(data)):
		trial=sample+1
		xandydata=list(zip(data[trial]['x-implant'],data[trial]['y-implant']))
		time=list(zip(data[trial]['seconds']))
		distance=0
		immobcount=0
		#allv=[]
		if len(data[trial]['x-implant'])>1:
			for point in range(len(xandydata)-1):
				distance=distance+round(np.linalg.norm(np.array(xandydata[point]) - np.array((xandydata[point+1])),3))
				point_dis=round(np.linalg.norm(np.array(xandydata[point]) - np.array((xandydata[point+1])),3))
				point_time=np.array(time[point+1]) - np.array(time[point])[0]
				velocity=point_dis/point_time
				#allv.append(velocity[0])
				trialsamps=len(xandydata)

				if velocity <= velcut:
					#going to go with total immobile counts b/c of mdropped data from rearing/bad tracking
					immobcount=immobcount+1
				else:
					pass
		
		elif len(data[trial]['x-implant'])==1:
			distance=np.nan
			immobcount=0
			trialsamps=1
		else:
			distance=np.nan
			immobcount=np.nan
			trialsamps=np.nan

		datahold.append(distance)
		immobhold.append([immobcount,immobcount/trialsamps])
	return(datahold,immobhold)



###### Written by ATP
def path_C(x,y):
	C = 0
	p1 = np.array((x[0],y[0]))
	i=1
	while i < len(x):
		p2 = np.array((x[i],y[i]))
		C_ = np.linalg.norm(p2-p1)
		C = C + C_
		p1 = p2
		i+=1
	return C

def path_L(x,y):
	p1 = np.array((x[0],y[0]))
	p2 = np.array((x[-1],y[-1]))
	L = np.linalg.norm(p2-p1)
	return L

def tortuosity(data):
	tempdict={}
	#tweak from DSJ to iterate through all trials and work with dictionaries
	for a in range(len(data)):
		if len(data[a+1]['x-implant'])>0:		
			trial=a+1
			C = path_C(data[trial]['x-implant'],data[trial]['y-implant'])
			L = path_L(data[trial]['x-implant'],data[trial]['y-implant'])
			tau = C / L
			tempdict.update({trial:tau.astype("float64")})
		else:
			trial=a+1
			tempdict.update({trial:np.nan})
	return tempdict

#original function for data already pulled from the dictionaries UPDATED
def tortuosity2(x,y):
	C = path_C(x,y)
	L = path_L(x,y)
	tau = C / L
	return tau





###############

#UPDATED 
#findlastapproach(masterdict,distancedict)
def findlastapproach(data,distancedata,minseek):
	tempdict={}

	for a in range(len(distancedata)):
		trial=a+1
		#print(trial)
		if len(np.where(distancedata[trial]<minseek)[0])==0: # if they never enter the zone (also incomplete)
			xpoints=data[trial]['x-implant']
			ypoints=data[trial]['y-implant']
			lengthofapproach=np.nan#data[trial]['seconds']
			approachtor=np.nan
			vel=np.nan

		elif len(np.where(distancedata[trial]>minseek)[0])==0: # if they are only in the zone
			startfinal=0
			xpoints=data[trial]['x-implant'][startfinal:]
			ypoints=data[trial]['y-implant'][startfinal:]
			secs=data[trial]['seconds'][startfinal:]
			if len(secs) >1:
				lengthofapproach=secs[-1]-secs[0]
				approachtor=tortuosity2(xpoints,ypoints)
				distancetrav=sum(abs(np.diff(distancedata[trial][startfinal:])))
				vel=distancetrav/lengthofapproach
			elif len(secs) ==1:
				lengthofapproach=.06#i.e one camera sample at 16 hz
				approachtor=np.nan			#print(trial,startfinal)
				distancetrav=sum(abs(np.diff(distancedata[trial][startfinal-1:])))
				vel=distancetrav/lengthofapproach	

		elif np.where(distancedata[trial]>minseek)[0][-1]+1==len(data[trial]['seconds']): # if they dont finish near the zone (incomplete trial)
			startfinal=0
			xpoints=data[trial]['x-implant'][startfinal:]
			ypoints=data[trial]['y-implant'][startfinal:]
			lengthofapproach=np.nan#data[trial]['seconds'][startfinal:]
			approachtor=np.nan
			vel=np.nan

		else:			# if they enter the zone from outside
			startfinal=np.where(distancedata[trial]>minseek)[0][-1]+1
			xpoints=data[trial]['x-implant'][startfinal:]
			ypoints=data[trial]['y-implant'][startfinal:]
			secs=data[trial]['seconds'][startfinal:]
			if len(secs) >1:
				lengthofapproach=secs[-1]-secs[0]
				approachtor=tortuosity2(xpoints,ypoints)
				distancetrav=sum(abs(np.diff(distancedata[trial][startfinal:])))
				vel=distancetrav/lengthofapproach
			elif len(secs) ==1:
				lengthofapproach=.06 #i.e one camera sample at 16 hz
				approachtor=np.nan			#print(trial,startfinal)
				distancetrav=sum(abs(np.diff(distancedata[trial][startfinal-1:])))
				vel=distancetrav/lengthofapproach	

		
		#addvellocty here
		both=np.array([approachtor,lengthofapproach,vel])
		tempdict.update({trial:both})
	return(tempdict)






def dicttolist(dicti,columns=1):

	

	store1=[]
	store2=[]
	store3=[]


	for a in range(len(dicti)):
		tkey=a+1
		
		if columns ==1:
			store1.append(dicti[tkey])

		elif columns==2:
			store1.append(dicti[tkey][0])
			store2.append(dicti[tkey][1])
		elif columns==3: 
			store2.append(dicti[tkey][1])
			store3.append(dicti[tkey][2])
		elif columns >= 4:
			pass

	return(store1,store2,store3)



#function added so that trial numbres are turned into corresponding block (10/11/22-dsj). input is the trial number file

def decodetrials(tdata,abortdata):
	outlist=[]

	b1=tdata[1][0]
	b2=tdata[1][0]+tdata[2][0]
	b3=tdata[1][0]+tdata[2][0]+tdata[3][0]
	b4=tdata[1][0]+tdata[2][0]+tdata[3][0]+tdata[4][0]

	for item in range(len(abortdata)): 
		if abortdata[0][item] <= b1:
			outlist.append(1)
		elif abortdata[0][item] > b1 and abortdata[0][item] <= b2:
			outlist.append(2)
		elif abortdata[0][item] > b2 and abortdata[0][item] <= b3:
			outlist.append(3)
		elif abortdata[0][item] > b3 and abortdata[0][item] <= b4:
			outlist.append(4)
	return (outlist)










###############################
#plotting functions



#UPDATED
def aniplot(trial,data,SL,savefile=False,filename='test.gif', markers=True):
	x = data[trial]['x-implant']#np.arange(1,len(x_activitydict[trial])+1,1)   secondsdict[trial]
	y = data[trial]['y-implant']

	#x = np.arange(1,len(data[trial])+1,1)
	#y = data[trial]

	fig, ax = plt.subplots()
	line, = ax.plot(x, y, color='k')
	#line2, = ax.plot(x_bodyactivitydict[trial], y_bodyactivitydict[trial], color='r')

	def update(num, x, y, line):
		line.set_data(x[:num], y[:num])

		line.axes.axis([0, 640,480,0]) # flip axes?
		return line,


	ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],interval=50, blit=True)
	
	if markers == True:
		plt.plot(SL[0],SL[1],'r*')
		#plt.plot(37,365,'mo')
		#plt.plot(627,167,'bo')
		plt.plot(data[trial]['x-implant'][1],data[trial]['y-implant'][1],'sg')
		plt.plot(data[trial]['x-implant'][-1],data[trial]['y-implant'][-1],'sr')
	else:
		pass
	if savefile == True:
		ani.save(filename)
	else:
		pass
	plt.show()

# traceplot(masterdict) UPDATED
def traceplot(data,SL,TL,xdata2=None,ydata2=None,xdata3=None,ydata3=None,saveplot=False, savefile=False, savedir=None):
	fig, axs = plt.subplots(8,10,sharex=True,sharey=True)
	for a in range(0,len(data)):
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
		

		axs[rowspot,colspot].plot(data[a+1]['x-implant'][len(data[a+1]['x-implant'])-2:-1],data[a+1]['y-implant'][len(data[a+1]['y-implant'])-2:-1],'go')#(xdata[a+1],ydata[a+1])
		axs[rowspot,colspot].plot(data[a+1]['x-body'][len(data[a+1]['x-body'])-2:-1],data[a+1]['y-body'][len(data[a+1]['y-body'])-2:-1],'rs')
		#axs[rowspot,colspot].plot(xdata2[a+1][len(xdata2[a+1])-2:-1],ydata2[a+1][len(ydata2[a+1])-2:-1],'ro')#(x_bodyactivitydict[a+1],y_bodyactivitydict[a+1])
		#axs[rowspot,colspot].plot(xdata3[a+1][len(xdata3[a+1])-2:-1],ydata3[a+1][len(ydata3[a+1])-2:-1],'rs')
		axs[rowspot,colspot].plot(data[a+1]['x-implant'],data[a+1]['y-implant'])
		#axs[rowspot,colspot].plot([xdata[a+1][len(xdata[a+1])-2:-1],xdata3[a+1][len(xdata3[a+1])-2:-1]],[ydata[a+1][len(ydata[a+1])-2:-1],ydata3[a+1][len(ydata3[a+1])-2:-1]],color='green',linewidth=5,marker='<')
		axs[rowspot,colspot].plot(SL[0],SL[1],'r*')
		#axs[rowspot,colspot].plot([xdata[a+1][len(xdata[a+1])-2:-1],xdata3[a+1][len(xdata3[a+1])-2:-1]],[ydata[a+1][len(ydata[a+1])-2:-1],ydata3[a+1][len(ydata3[a+1])-2:-1]],color='green',linewidth=5,marker='<')
		axs[rowspot,colspot].plot(TL[0],TL[1],'r*')
		axs[rowspot,colspot].plot(62,336,'mo')
		axs[rowspot,colspot].plot(606,163,'bo')
		#axs[rowspot,colspot].Circle((SL[0],SL[1]), normthresh,alpha=.1)
		#axs[rowspot,colspot].plot(xdata[a+1][0],ydata[a+1][0],'sg')
		#axs[rowspot,colspot].plot(xdata[a+1][-1],ydata[a+1][-1],'sr')

	plt.xlim(0, 640)
	plt.ylim(480,0)

	if saveplot:
		plt.savefig(os.getcwd() + '\\traceplot')

	plt.show()



#distanceplot(masterdict,distancedict,abortthreshold) UPDATED

def distanceplot(data,data2,limit):
	fig, axs = plt.subplots(8,10,sharex=False,sharey=True)
	for a in range(0,len(data)):
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
		

		axs[rowspot,colspot].plot(data[a+1]['seconds'],data2[a+1])
		axs[rowspot,colspot].axhline(y=limit, color='r')
		# axs[rowspot,colspot].plot(71,84,'r*')
		# axs[rowspot,colspot].plot(37,365,'mo')
		# axs[rowspot,colspot].plot(627,167,'mo')
		# axs[rowspot,colspot].plot(x_activitydict[a+1][0],y_activitydict[a+1][0],'sg')
		# axs[rowspot,colspot].plot(x_activitydict[a+1][-1],y_activitydict[a+1][-1],'sr')


	# plt.xlim(0, 640)
	# plt.ylim(480,0)

	plt.show()











# hexplots(masterdict) UPDATED

def hexplots(data,showtrace=False,colmin=0,colmax=20):
	fig, axs = plt.subplots(8,10,sharex=True,sharey=True)
	for a in range(0,len(data)):
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
		

		axs[rowspot,colspot].hexbin(data[a+1]['x-implant'],data[a+1]['y-implant'],gridsize=(8,8),cmap=CM.jet,vmin=colmin,vmax=colmax,extent=(0, 640,480,0))
		#axs[rowspot,colspot].legend(loc='upper center')
		if showtrace == True:
			axs[rowspot,colspot].plot(data[a+1]['x-implant'],data[a+1]['y-implant'])
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
	fig.colorbar(hexbin(data[a]['x-implant'],data[a]['y-implant'],cmap=CM.jet,vmin=colmin,vmax=colmax),cax=cbar_ax)	

	plt.show()