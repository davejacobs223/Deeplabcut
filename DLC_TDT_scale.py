# written by DSJ

#for DLC-TDT data interactions uses functions housed in the DLCvis script

# required files: DLC csv of poses, tdt data block, trial file


#NOTE TOSELF NEED TO PUT A MARKER FOR INCOMPLETE VERSUS COMPLETE TRIALS.SHOULD BED DETERMINABLE THROUHGGH BEHAVIOR FILE

from DLCvis import *
from glob import glob
from matplotlib import interactive
interactive(True)



#GET ALL THE SUBJECTS
Subjects=glob('S*')
Subjects=Subjects[0:8]
#Subjects=Subjects



abortcountdf=pd.DataFrame()
abortcountdf_all=pd.DataFrame()

######################################
#DONT MESS WITH THIS
SideDict={'S17_M':'r','S3_M':'l','S427_M':'l','S428_M':'r','S20_M':'r','S18_F':'l','SC4F1_F':'l','SC4F2_F':'r','SC4M1_M':'l','SC4M2_M':'r','S5_F':'l','S15_M':'l','S19_F':'r'}

#for loop to start iteerating through each subject
for subjecta in Subjects:
	os.chdir(subjecta)
	print (subjecta)
	sidechoice=SideDict[subjecta]#input("Right or left take action side? (r/l)    ")
	print ('Side:'+sidechoice)
	#doesnt matter until we build in the neural data
	OFCdata='y'
	
	# and for each subject find all the sessions (for now jsut the STSPre which is a shock day)
	sessions=glob('STS*')+glob('STPr*')+glob('STE*')+glob('STN*')#?=ST*




	for sessarino in sessions:


	#get timestamp data and load files
		os.chdir(sessarino)
		hasstamps=len(glob('tdtseek.csv')+glob('tdtiti.csv')+glob('tdtcam.csv'))==3
		print ('Analyzing '+sessarino)  

		if hasstamps == True:
			seekstamps=pd.read_csv('tdtseek.csv')[['0','1']].to_numpy().tolist()
			itistamps=pd.read_csv('tdtiti.csv')[['0','1']].to_numpy().tolist()
			camerastamps=pd.read_csv('tdtcam.csv',header=None)[0]
			camerastamps=np.array(camerastamps)
		else:      
			tdtfile =glob('ST*')+glob('RD*')
			tdtfile=tdtfile[0]
			tdtdata = tdt.read_block(tdtfile)
			camerastamps=tdtdata.epocs.Cam1.onset
			if SideDict[subjectname]=='r':
				seekon=tdtdata.epocs.PC0_.onset
				seekoff=tdtdata.epocs.PC0_.offset
			elif SideDict[subjectname]=='l':	
				seekon=tdtdata.epocs.PC2_.onset
				seekoff=tdtdata.epocs.PC2_.offset
			seekstamps=list(map(list, zip(seekon, seekoff)))
			itistamps=list(map(list,zip(seekon-15,seekon+2)))
			pd.DataFrame(seekstamps).to_csv('tdtseek.csv')
			pd.DataFrame(itistamps).to_csv('tdtiti.csv')	
			savetxt('tdtcam.csv', camerastamps, delimiter=',')	



		DLCfile=glob('*DLC*.csv')[0]
		trialnumbs=pd.read_csv(glob('*_Trials.csv')[0],header=None)

	#get subject name, sex
		spd=sessarino
		sex=subjecta.split('_')[1]
		subjectname=subjecta


	#read the DLC csv
	# set up an empty DF
		data=[]
		with open(DLCfile,'r') as csvfile:
			reader=csv.reader(csvfile)
			for line in reader:
				data.append(line)
			csvfile.close()
		data2=np.array(data)
		headers=data2[1:3][:,4:19]
		bodydata=np.asarray(data2[3:][:,4:19],dtype=float)



		#lets reconstuct the NP and feeder and get their locations in the video file
		if SideDict[subjectname]=='l':
			# go into DLCfile and get NP and feeder coords
			seeknpdata=np.asarray(data2[3:][:,22:25],dtype=float)
			#filter for only high confidence
			seeknpdata=seeknpdata[seeknpdata[:,2]>.98]
			#take average of all points
			sxmean=mean(seeknpdata[:,0])
			symean=mean(seeknpdata[:,1])
			takenpdata=np.asarray(data2[3:][:,19:22],dtype=float)
			takenpdata=takenpdata[takenpdata[:,2]>.98]
			txmean=mean(takenpdata[:,0])
			tymean=mean(takenpdata[:,1])
			feederdata=np.asarray(data2[3:][:,25:28],dtype=float)
			feederdata=feederdata[feederdata[:,2]>.98]
			fxmean=mean(feederdata[:,0])
			fymean=mean(feederdata[:,1])
			seeklocation=np.array((sxmean,symean))	
			takelocation=np.array((txmean,tymean))	
			feederlocation=np.array((fxmean,fymean))

			sTf=round(np.linalg.norm(np.array(seeklocation) - np.array(feederlocation)),2)	
			normthresh=(sTf/12)*3.5
			
		elif SideDict[subjectname]=='r':
			seeknpdata=np.asarray(data2[3:][:,19:22],dtype=float)
			seeknpdata=seeknpdata[seeknpdata[:,2]>.98]
			sxmean=mean(seeknpdata[:,0])
			symean=mean(seeknpdata[:,1])
			takenpdata=np.asarray(data2[3:][:,22:25],dtype=float)
			takenpdata=takenpdata[takenpdata[:,2]>.98]
			txmean=mean(takenpdata[:,0])
			tymean=mean(takenpdata[:,1])
			feederdata=np.asarray(data2[3:][:,25:28],dtype=float)
			feederdata=feederdata[feederdata[:,2]>.98]
			fxmean=mean(feederdata[:,0])
			fymean=mean(feederdata[:,1])
			seeklocation=np.array((sxmean,symean))	
			takelocation=np.array((txmean,tymean))
			feederlocation=np.array((fxmean,fymean))	

			sTf=round(np.linalg.norm(np.array(seeklocation) - np.array(feederlocation)),2)	
			normthresh=(sTf/12)*3.5



		# gets seek latencies
		seektimes=np.array(seekstamps)
		seektimes=seektimes[:,1]-seektimes[:,0]




		# open lists for relevant camera frames based on seek nosepoke
		framelocations=[]
		itiframelocations=[]

		# what frames in DLC file need to be pulled for each trial
		for a in range(len(seekstamps)):
			camerastampon= np.where(seekstamps[a][0]>=camerastamps)[0][-1]
			camerastampoff= np.where(seekstamps[a][1]>=camerastamps)[0][-1]
			framelocations.append([camerastampon,camerastampoff])

			iticamerastampon= np.where(itistamps[a][0]>=camerastamps)[0][-1]
			iticamerastampoff= np.where(itistamps[a][1]>=camerastamps)[0][-1]	
			itiframelocations.append([iticamerastampon,iticamerastampoff])

#check for super fast trials,add a few seconds to allow the functions to work. THESE TRIALS ARE DROPPED IN ANALYSIS AND RETURN AS NANS NOW (dsj 9/2/22)
		if len(np.where(np.array(framelocations)[:,1]-np.array(framelocations)[:,0]==0)[0])>0:
			fastones=np.where(np.array(framelocations)[:,1]-np.array(framelocations)[:,0]==0)[0]
			for item in fastones:
				framelocations[item][1]=framelocations[item][1]+5
			#print('fast ones: '+ str(len(fastones))) will print one trial with no valid samples now if fast one or no x,y data above the threshold for confidence
		else:
			fastones=np.array([])


		# GET DATA
		seekdata=parseDLCdata(bodydata,framelocations,camerastamps,threshold=.1,nosepokeloc=seeklocation,abort_threshold=normthresh,fastdrops=fastones)
		#get data specifically for each trial
		maindict=seekdata[0]
		distancedict=seekdata[1]
		aborts=seekdata[2]
		abortthreshold=seekdata[3]
		headatpoke=seekdata[4]

		# get iti data
		itidata=parseDLCdata(bodydata,itiframelocations,camerastamps,threshold=.01,nosepokeloc=seeklocation)
		itimaindict=itidata[0]
		itidistancedict=itidata[1]
		itiaborts=itidata[2]


		# some other metrics
		bodyangles=bodyangle(maindict,SL=seeklocation,TL=takelocation)
		Tortuositydata=tortuosity(maindict)
		finalapproachdata=findlastapproach(maindict,distancedict,minseek=abortthreshold)





		#analyze the behavioral abort and final approach data
		aborts=np.array(aborts)
		trialnumbs=pd.read_csv(glob('*_Trials.csv')[0],header=None)
		newcol=[]

		if sessarino == 'STS1B':
			for item in trialnumbs.columns[1:]:
				newcol=newcol+[trialnumbs.columns[item]+2]*trialnumbs[item][0]	
				sessionout='STS1'
		else:		
			for item in trialnumbs.columns[1:]:
				newcol=newcol+[trialnumbs.columns[item]]*trialnumbs[item][0]
				sessionout=sessarino
		
		aborts_update=np.c_[aborts,newcol]

		newcol=[]
		newcol2=[]
		for item in finalapproachdata:
			newcol.append(finalapproachdata[item][1])
			newcol2.append(finalapproachdata[item][0])
		aborts_update=np.c_[aborts_update,newcol]
		aborts_update=np.c_[aborts_update,newcol2]
		aborts_update=np.c_[aborts_update,headatpoke]
		aborts_update=np.c_[aborts_update,bodyangles]

		# make a new DF with the analysis to writeout to csv
		abortbyblock=pd.DataFrame(aborts_update).groupby(by=3).mean().drop(0,1).rename(columns={1: "Abort#", 2: "abortTime",4:"FinalApprTime",5:"Tort",6:'Distatpoke',7:'BodyAngle'})
		sumbyblock=pd.DataFrame(aborts_update).groupby(by=3).sum().drop(0,1).rename(columns={1: "Abort#(Sum)", 2: "abortTime",4:"FinalApprTime",5:"Tort",6:'Distatpoke',7:'BodyAngle'})


		abortbyblock_all=pd.DataFrame(aborts_update).drop(0,1).rename(columns={1: "Abort#", 2: "abortTime",4:"FinalApprTime",5:"Tort",6:'Distatpoke',7:'BodyAngle'})
		sumbyblock_all=pd.DataFrame(aborts_update).drop(0,1).rename(columns={1: "Abort#(Sum)", 2: "abortTime",4:"FinalApprTime",5:"Tort",6:'Distatpoke',7:'BodyAngle'})
		#kick in the subject and session
		abortbyblock['Subject']=subjectname
		abortbyblock['Session']=sessionout
		abortbyblock.insert(0, 'Abort#(Sum)', sumbyblock['Abort#(Sum)'])

		abortbyblock_all['Subject']=subjectname
		abortbyblock_all['Session']=sessionout
		abortbyblock_all.insert(0, 'Abort#(Sum)', sumbyblock_all['Abort#(Sum)'])



		##3
		abortcountdf=abortcountdf.append(abortbyblock)
		abortcountdf_all=abortcountdf_all.append(abortbyblock_all)


#show plots if you want
		showplot='True'
		if showplot == 'Nah':
			figure, axes = plt.subplots() 
			plot(seeknpdata[:,0],seeknpdata[:,1],'o')
			plot(takenpdata[:,0],takenpdata[:,1],'o')
			plot(feederdata[:,0],feederdata[:,1],'o')
			plot(sxmean,symean,'o',color='r')
			plot(txmean,tymean,'o',color='g')
			plot(fxmean,fymean,'o',color='r')
			chamber=plt.Circle((sxmean,symean), normthresh,alpha=.1)
			axes.add_artist(chamber)
			plt.xlim(0, 640)
			plt.ylim(480,0)
			plt.title(subjecta+sessarino)
			plt.show()
		else: 
			pass
		os.chdir('../')
	os.chdir('../')

#to csv we go
abortcountdf.reset_index().rename(columns={3:'Block'}).to_csv('abortdata.csv')
abortcountdf_all.reset_index().rename(columns={3:'Block'}).to_csv('abortdataalltrials.csv')
















