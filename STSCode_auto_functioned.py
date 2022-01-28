#!/usr/bin/env python
#7/16 for both GS4 and GS3. Removed a bunch of analyses that are not critical. 
#Activity analysis is optional with y/n and currently is not fixed to work with GS4
#10/18 added in take acition parsing based on shock


#11/4/21 bug fix see line 267

#NOT FOR OPTO



import math
import numpy 
import csv
from glob import glob
from numpy import mean
from numpy import var
import re
import pandas
import sys

psls=['F41','F43','M42','M45','M46','M48','M410','M411','M49']
salswitch=['F42','F44','M47','M412','M413','M43','M44','M41']

##############
#some functions
def autodrop(x):
	if len(x)>1:
		return (mean(x))
	else:
		return 'Nan'
def firsttrial(x):
	if len(x)>0:
		return (x[0])
	else:
		return 'Nan'
def timediffcalc(x,GStype):
	if GStype == 'GS3':
		return x*20*.001
	elif GStype == 'GS4':
		return x
	else:
		print ('error:GS not specified')

def latencies(on,off,dataset,listused,postshocklist,block,takecolumn,dispcount=0):
	n=0
	t=0
	stop=len(dataset)
	while t+1<=stop:
		
		if dataset[n][9] == on:
			first=float(dataset[n][7])
			n=n+1
			t=t+1
		elif dataset[n][9] in off:
			fin=float(dataset[n][7])
			timediff=(fin-first)
			SL=timediffcalc(timediff,program)
			listused.append(SL)


			if block != 1:
				wasshock=dataset[numpy.where(numpy.in1d(dataset[1:n][:,9], off+sb1off+[6]))[0][-1]+1][9]  # the +[6] is to fix a bug for when no trials are completed. need to check if its adding in trials that shouldnt be there....
				if wasshock in shockstates:
					postshocklist.append(SL)
				else:
					pass
			else:
				pass

			# s=s+1
			n=n+1
			t=t+1
		elif dataset[n][8] == on and dataset[n][takecolumn]=='1': # total siplacesments, not per trial
			dispcount=dispcount+1
			n=n+1
			t=t+1			
		else:
			n=n+1
			t=t+1
	n=0
	t=0
	return dispcount

def takelatencies(on,off,priorseek,dataset,listused,postshocklist,block):
	n=0
	t=0
	stop=len(dataset)
	while t+1<=stop:
		
		if dataset[n][9] == on:
			first=float(dataset[n][7])
			n=n+1
			t=t+1
			
		elif dataset[n][9]== off:
			fin=float(dataset[n][7])
			timediff=(fin-first)
			TL= timediffcalc(timediff,program)

			if block != 1:
				wasshock=dataset[numpy.where(numpy.in1d(dataset[1:n][:,9], priorseek))[0][-1]+1][9]
				if wasshock in shockstates:
					postshocklist.append(TL)
				else:
					listused.append(TL)
			else:
				pass
			
			n=n+1
			t=t+1



		else:
			n=n+1
			t=t+1
	n=0
	t=0


def csvout(dataset,filename):
	with open(filename+'.csv','w') as file:
		wr=csv.writer(file,lineterminator='\n')
		wr.writerow(['Subj','0','6','10','18','30','60','session','gender','treatment','dose'])
		for item in dataset:
			wr.writerow(item)

# runs all the data at once
a=glob('DailyData/*.txt')
b=glob('DailyData/*.csv')

bothfiles=a+b
csvseek=[]
csvpseek=[]
csvtake=[]
csvshtake=[]
csvpell=[]
csvfood=[]
csvseekvar=[]
csvfirstshocks=[]
csvfirsttrials=[]
csvIBIpokes=[]
csvfirsttake=[]
seeksall=[]
csvdisp=[]

for row in bothfiles:

	data=[]
	with open(row,'r') as csvfile:
		if row[-3]== 'c':
			program='GS4'
			reader=csv.reader(csvfile)
		else:
			program='GS3'
			reader=csv.reader(csvfile,delimiter='\t')
		for line in reader:
			data.append(line)
		csvfile.close()

	data2=numpy.array(data)
	stop=len(data2)	

#### CHANGED FOR NEW NAMING SYSTEM
	session=re.findall('.*',row)
	session=session[0]
	session=session.split(".")[0]
	dose=session.split('_')[-1]
	session=session.split("_")[1]
	
	protocol=data2[1][2]
	if protocol in ['74','77','79','STS_left_4cycles','STS_left_4cycles_stim','sts_left_4cyle_stim','52','55','56','61','stsleft_takestim']: #getting there, just need to figure out the GS3 rat take locations...
		takecol=11
	elif protocol in ['76','78','80','STS_right_4cycles','STS_right_4cycles_stim','sts_right_4cyle_stim','53','54','60']:
		takecol=12



	gender=row.split(".")[0].split("\\")[1].split("_")[0][0]
	
	name=data[1][6]
	name=name.split('_')[0]
	#print(name,protocol)

	if name in psls:
		treat='psl'
	elif name in salswitch:
		treat='salswtch'
	else:
		treat='NA'


	if gender == 'M':
		gender='Male'
	elif gender == 'F':
		gender='Female'
	else:
		gender='none'

	##############
	if program == 'GS3':
		sb1on='39'
		sb1off=['7','2']
		tb1on='3'
		tb1off='4'
		fb1on='4'
		fb1off='5'
		fblast='20'

		sb2on='8'
		sb2off=['9','10']
		tb2on='11'
		tb2off='12'
		fb2on='12'
		fb2off='13'

		sb3on='14'
		sb3off=['15','16']
		tb3on='17'
		tb3off='18'
		fb3on='18'
		fb3off='19'

		sb4on='21'
		sb4off=['22','23']
		tb4on='24'
		tb4off='25'
		fb4on='25'
		fb4off='26'

		sb5on='27'
		sb5off=['28','29']
		tb5on='30'
		tb5off='31'
		fb5on='31'
		fb5off='32'

		sb6on='33'
		sb6off=['34','35']
		tb6on='36'
		tb6off='37'
		fb6on='37'
		fb6off='38'

		shockstates=['9','15','22','28','34']


	elif program == 'GS4':
		sb1on='2'
		sb1off=['3']
		tb1on='4'
		tb1off='5'
		fb1on='5'
		fb1off='6'
		fblast='8675309'


		# sb2on='7'
		# sb2off=['8','9']
		# tb2on='11'
		# tb2off='12'
		# fb2on='12'
		# fb2off='13'



		sb2on='8'
		sb2off=['9','10']
		tb2on='12'
		tb2off='13'
		fb2on='14'
		fb2off='15'

		sb3on='16'
		sb3off=['17','18']
		tb3on='20'
		tb3off='21'
		fb3on='22'
		fb3off='23'

		# sb3on='14'
		# sb3off=['15','16']
		# tb3on='18'
		# tb3off='19'
		# fb3on='19'
		# fb3off='20'

		sb4on='24'
		sb4off=['25','26']
		tb4on='28'
		tb4off='29'
		fb4on='30'
		fb4off='31'


		# sb4on='21'
		# sb4off=['22','23']
		# tb4on='25'
		# tb4off='26'
		# fb4on='26'
		# fb4off='27'

		sb5on='28'
		sb5off=['29','30']
		tb5on='32'
		tb5off='33'
		fb5on='33'
		fb5off='34'

		sb6on='35'
		sb6off=['36','37']
		tb6on='40'
		tb6off='41'
		fb6on='41'
		fb6off='42'

		shockstates=['8','15','22','29','36']

	##############
	#######################################################################
	###3
	seekdata=[]
	seek2data=[]
	seek3data=[]
	seek4data=[]
	seek5data=[]
	seek6data=[]

	pshseek1data=[]
	pshseek2data=[]
	pshseek3data=[]
	pshseek4data=[]
	pshseek5data=[]
	pshseek6data=[]


	
	trial2array=[]
	trial3array=[]
	trial4array=[]
	trial5array=[]
	trial6array=[]

	disp1=latencies(sb1on,sb1off,data2,seekdata,pshseek1data,1,takecol)
	disp2=latencies(sb2on,sb2off,data2,seek2data,pshseek2data,2,takecol)
	disp3=latencies(sb3on,sb3off,data2,seek3data,pshseek3data,3,takecol)
	disp4=latencies(sb4on,sb4off,data2,seek4data,pshseek4data,4,takecol)
	disp5=latencies(sb5on,sb5off,data2,seek5data,pshseek5data,5,takecol)
	disp6=latencies(sb6on,sb6off,data2,seek6data,pshseek6data,6,takecol)

	

	subj=data2[1][6][0:3]
	


	
	Se1=autodrop(seekdata)
	Se2=autodrop(seek2data)
	Se3=autodrop(seek3data)
	Se4=autodrop(seek4data)
	Se5=autodrop(seek5data)
	Se6=autodrop(seek6data)

	psk2=mean(pshseek2data)
	psk3=mean(pshseek3data)
	psk4=mean(pshseek4data)
	psk5=mean(pshseek5data)
	psk6=mean(pshseek6data)



	Trial1=firsttrial(seekdata)
	Trial2=firsttrial(seek2data)
	Trial3=firsttrial(seek3data)
	Trial4=firsttrial(seek4data)
	Trial5=firsttrial(seek5data)
	Trial6=firsttrial(seek6data)

	stdse1=var(seekdata)
	stdse2=var(seek2data)
	stdse3=var(seek3data)
	stdse4=var(seek4data)
	stdse5=var(seek5data)
	stdse6=var(seek6data)
        

	Seeks=[subj,Se1,Se2,Se3,Se4,Se5,Se6,session,gender,treat,dose]
	psSeeks=[subj,Se1,psk2,psk3,psk4,psk5,psk6,session,gender,treat,dose]
	Vars=[subj,stdse1,stdse2,stdse3,stdse4,stdse5,stdse6,gender,treat,dose]
	FirstTrials=[subj,Trial1,Trial2,Trial3,Trial4,Trial5,Trial6,session,gender,treat,dose]

	csvseek.append(Seeks)
	csvpseek.append(psSeeks)
	csvseekvar.append(Vars)
	csvfirsttrials.append(FirstTrials)
	seeksall.append([subj,session]+seekdata+seek2data+seek3data+seek4data)


	takedisplacement=[subj,disp1,disp2,disp3,disp4,disp5,disp6,session,gender,treat,dose]
	csvdisp.append(takedisplacement)
	csvout(csvdisp,'Displacements')


	csvout(csvseek,'SeekLatency')
	csvout(csvpseek,'PostshSeekLatency')
	csvout(csvseekvar,'SeekVariance')
	csvout(csvfirsttrials,'FirstTrials')

	#sys.exit("EarlyStop")    
	#########################################################################################################
	# Take Latency cycle 1 calculator
	takedata=[]
	take2data=[]
	take3data=[]
	take4data=[]
	take5data=[]
	take6data=[]
	STL1data=[]
	STL2data=[]
	STL3data=[]
	STL4data=[]
	STL5data=[]
	STL6data=[]



	takelatencies(tb1on,tb1off,sb1off,data2,takedata,STL1data,1)
	takelatencies(tb2on,tb2off,sb2off,data2,take2data,STL2data,2)
	takelatencies(tb3on,tb3off,sb3off,data2,take3data,STL3data,3)
	takelatencies(tb4on,tb4off,sb4off,data2,take4data,STL4data,4)
	takelatencies(tb5on,tb5off,sb5off,data2,take5data,STL5data,5)
	takelatencies(tb6on,tb6off,sb6off,data2,take6data,STL6data,6)


	Trial1=firsttrial(takedata)
	Trial2=firsttrial(take2data)
	Trial3=firsttrial(take3data)
	Trial4=firsttrial(take4data)
	Trial5=firsttrial(take5data)
	Trial6=firsttrial(take6data)


	Ta1=mean(takedata)
	Ta2=mean(take2data)
	Ta3=mean(take3data)
	Ta4=mean(take4data)
	Ta5=mean(take5data)
	Ta6=mean(take6data)
	STL2mean=mean(STL2data)
	STL3mean=mean(STL3data)
	STL4mean=mean(STL4data)
	STL5mean=mean(STL5data)
	STL6mean=mean(STL6data)

	Takes=[subj,Ta1,Ta2,Ta3,Ta4,Ta5,Ta6,session,gender,treat,dose]
	shTakes=[subj,Ta1,STL2mean,STL3mean,STL4mean,STL5mean,STL6mean,session,gender,treat,dose]
	
	csvtake.append(Takes),
	csvshtake.append(shTakes)
	


	csvout(csvtake,'TakeLatency')
	csvout(csvshtake,'TakeShockLatency')




##########################################################################	

	# food cycle 1 calculator
	fooddata=[]
	food2data=[]
	food3data=[]
	food4data=[]
	food5data=[]
	food6data=[]

	food1=0
	food2=0
	food3=0
	food4=0
	food5=0
	food6=0

	n=0
	t=0

	while t+1<=stop:
		
		if data2[n][9] == fb1on:
			first=float(data2[n][7])
			n=n+1
			t=t+1
			food1=food1+1
		elif data2[n][9]== fb1off or data2[n][9]== fblast and data2[n][8] == fb1on:
			fin=float(data2[n][7])
			timediff=(fin-first)
			FL=timediffcalc(timediff,program)
			fooddata.append(FL)
			
			# s=s+1
			n=n+1
			t=t+1
		else:
			n=n+1
			t=t+1
	n=0
	t=0

	# Take Latency cycle 2 calculator
	while t+1<=stop:
		
		if data2[n][9] == fb2on:
			first=float(data2[n][7])
			n=n+1
			t=t+1
			food2=food2+1
		elif data2[n][9]== fb2off or data2[n][9]== fblast and data2[n][8] == fb2on:
			fin=float(data2[n][7])
			timediff=(fin-first)
			TL=timediffcalc(timediff,program)
			food2data.append(TL)
			
			# s=s+1
			n=n+1
			t=t+1
		else:
			n=n+1
			t=t+1

	n=0
	t=0

	# Seek Latency cycle 3 calculator
	while t+1<=stop:
		
		if data2[n][9] == fb3on:
			first=float(data2[n][7])
			n=n+1
			t=t+1
			food3=food3+1
		elif data2[n][9]== fb3off or data2[n][9]== fblast and data2[n][8] == fb3on:
			fin=float(data2[n][7])
			timediff=(fin-first)
			TL=timediffcalc(timediff,program)
			food3data.append(TL)
		
			# s=s+1
			n=n+1
			t=t+1
		else:
			n=n+1
			t=t+1	

	n=0
	t=0

	# Seek Latency cycle 4 calculator
	while t+1<=stop:
		
		if data2[n][9] == fb4on:
			first=float(data2[n][7])
			n=n+1
			t=t+1
			food4=food4+1
		elif data2[n][9]== fb4off or data2[n][9]== fblast and data2[n][8] == fb4on:
			fin=float(data2[n][7])
			timediff=(fin-first)
			TL=timediffcalc(timediff,program)
			food4data.append(TL)
			
			# s=s+1
			n=n+1
			t=t+1
		else:
			n=n+1
			t=t+1
	n=0
	t=0		

	# Seek Latency cycle 5 calculator
	while t+1<=stop:
		
		if data2[n][9] == fb5on:
			first=float(data2[n][7])
			n=n+1
			t=t+1
			food5=food5+1
		elif data2[n][9]== fb5off or data2[n][9]== fblast and data2[n][8] == fb5on:
			fin=float(data2[n][7])
			timediff=(fin-first)
			TL=timediffcalc(timediff,program)
			food5data.append(TL)
			
			# s=s+1
			n=n+1
			t=t+1
		else:
			n=n+1 
			t=t+1
	n=0
	t=0		

	# Seek Latency cycle 6 calculator
	while t+1<=stop:
		
		if data2[n][9] == fb6on:
			first=float(data2[n][7])
			n=n+1
			t=t+1
			food6=food6+1
		elif data2[n][9]== fb6off or data2[n][9]== fblast and data2[n][8] == fb6on:
			fin=float(data2[n][7])
			timediff=(fin-first)
			TL=timediffcalc(timediff,program)
			food6data.append(TL)
			
			# s=s+1
			n=n+1
			t=t+1
		else:
			n=n+1
			t=t+1
	n=0
	t=0		

	Fd1=mean(fooddata)
	Fd2=mean(food2data)
	Fd3=mean(food3data)
	Fd4=mean(food4data)
	Fd5=mean(food5data)
	Fd6=mean(food6data)

	Pell=[subj,food1,food2,food3,food4,food5,food6,session,gender,treat,dose]
	FoodLatency=[subj,Fd1,Fd2,Fd3,Fd4,Fd5,Fd6,session,gender,treat,dose]

	csvpell.append(Pell)
	csvfood.append(FoodLatency)

	csvout(csvpell,'Pellets')
	csvout(csvfood,'FoodLatency')



###############################3

def transposer(x):
	DF=pandas.read_csv(x)
	tpose=DF.sort_values(by=['gender'])
	tpose=tpose.transpose()
	tpose.to_csv(x)

def transposer(x):
	DF=pandas.read_csv(x)
	tpose=DF.sort_values(by=['gender'])
	tpose=tpose.transpose()
	tpose.to_csv(x)
# DF=pandas.read_csv('Pellets.csv')
# tpose=DF.sort_values(by=['session','gender'])PostshSeekLatency
# tpose=tpose.transpose()
# tpose.to_csv('Pellets.csv')
transposer('Pellets.csv')
transposer('SeekLatency.csv')
transposer('PostshSeekLatency.csv')
transposer('FirstTrials.csv')
transposer('TakeLatency.csv')
transposer('TakeShockLatency.csv')
transposer('FoodLatency.csv')
pandas.read_csv('Pellets.csv').transpose().sort_values(by=[9,7,0]).to_csv('Pellets.csv')
pandas.read_csv('SeekLatency.csv').transpose().sort_values(by=[9,7,0]).to_csv('SeekLatency.csv')
pandas.read_csv('PostshSeekLatency.csv').transpose().sort_values(by=[9,7,0]).to_csv('PostshSeekLatency.csv')
pandas.read_csv('FirstTrials.csv').transpose().sort_values(by=[9,7,0]).to_csv('FirstTrials.csv')
pandas.read_csv('TakeLatency.csv').transpose().sort_values(by=[9,7,0]).to_csv('TakeLatency.csv')
pandas.read_csv('TakeShockLatency.csv').transpose().sort_values(by=[9,7,0]).to_csv('TakeShockLatency.csv')
pandas.read_csv('FoodLatency.csv').transpose().sort_values(by=[9,7,0]).to_csv('FoodLatency.csv')
###############################################################33

actdecide=input('Analyze Activity?: (y/n)')

if actdecide== 'n':
	pass
elif actdecide == 'y':
	t=0
	tot=0
	n=0
	csvITIact=[]
	csvShockact=[]



	for row in a:

		data=[]
		with open(row,'r') as csvfile:
			reader=csv.reader(csvfile,delimiter='\t')
			for line in reader:
				data.append(line)
			csvfile.close()

		

		data2=numpy.array(data)
		stop=len(data2)	

		session=re.findall('.*',row)
		session=session[0]
		name=data[1][6]

		if name[0] == 'M':
			gender='Male'
		elif name[0] == 'F':
			gender='Female'
		else:
			gender='none'
		



		#######################################################################

		ICIactivity=0
		activity1=0
		activity2=0
		activity3=0
		activity4=0
		activity5=0
		activity6=0

		# Seek Latency cycle 1 calculator
		while t+1<=stop:
			
			if data2[n][8] == '6' and data2[n][13]== '1':
				ICIactivity=ICIactivity+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1
		n=0
		t=0




		# Seek Latency cycle 1 calculator
		while t+1<=stop:
			
			if data2[n][8] == '5' and data2[n][13]== '1':
				activity1=activity1+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1
		n=0
		t=0

		# Seek Latency cycle 2 calculator
		while t+1<=stop:
			
			if data2[n][8] == '13' and data2[n][13]== '1':
				activity2=activity2+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1

		n=0
		t=0

		# Seek Latency cycle 3 calculator
		while t+1<=stop:
			
			if data2[n][8] == '19' and data2[n][13]== '1':
				activity3=activity3+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1	

		n=0
		t=0

		# Seek Latency cycle 4 calculator
		while t+1<=stop:
			
			if data2[n][8] == '26' and  data2[n][13]== '1':
				activity4=activity4+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1
		n=0
		t=0		

		# Seek Latency cycle 5 calculator
		while t+1<=stop:
			
			if data2[n][8] == '32' and data2[n][13]== '1':
				activity5=activity5+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1
		n=0
		t=0		

		# Seek Latency cycle 6 calculator
		while t+1<=stop:
			
			if data2[n][8] == '38' and data2[n][13]== '1':
				activity6=activity6+1
				n=n+1
				t=t+1
			else:
				n=n+1
				t=t+1
		n=0
		t=0		


		subj=data2[1][6][0:3]
		

		ITIactivity=[subj,activity1,activity2,activity3,activity4,activity5,activity6,ICIactivity,session]

		csvITIact.append(ITIactivity)
		

		with open('ITIact.csv','w') as file:
			wr=csv.writer(file,lineterminator='\n')

			wr.writerow(['Subj','1','2','3','c4','c5','c6','ICITotal','session'])

			for item in csvITIact:
				wr.writerow(item)

	########################################################################
		shockactivity1=0
		shockactivity2=0
		shockactivity3=0
		shockactivity4=0
		shockactivity5=0
		shockactivity6=0

		shockcount1=0
		shockcount2=0
		shockcount3=0
		shockcount4=0
		shockcount5=0
		shockcount6=0



		# Seek Latency cycle 1 calculator
		while t+1<=stop:
				
			if data2[n][9] == '2':
				time=float(data2[n][7])
				stoptime=time+38
				s=n
				n=n+1
				t=t+1
				shockcount1=shockcount1+1
				currtime=float(data2[s][13])

				while currtime<stoptime:
					
					if data2[s][13] == '1':
						shockactivity1=shockactivity1+1
						currtime=float(data2[s][7])
						s=s+1	
					else:
						currtime=float(data2[s][7])
						s=s+1
								
			else: 	
				n=n+1
				t=t+1
		n=0
		t=0

		# Seek Latency cycle 2 calculator
		while t+1<=stop:
				
			if data2[n][9] == '9':
				time=float(data2[n][7])
				stoptime=time+38
				s=n
				n=n+1
				t=t+1
				shockcount2=shockcount2+1
				currtime=float(data2[s][13])

				while currtime<stoptime:
					
					if data2[s][13] == '1':
						shockactivity2=shockactivity2+1
						currtime=float(data2[s][7])
						s=s+1	
					else:
						currtime=float(data2[s][7])
						s=s+1
								
			else: 	
				n=n+1
				t=t+1
		n=0
		t=0


		# Seek Latency cycle 3 calculator
		while t+1<=stop:
				
			if data2[n][9] == '15':
				time=float(data2[n][7])
				stoptime=time+38
				s=n
				n=n+1
				t=t+1
				shockcount3=shockcount3+1
				currtime=float(data2[s][13])

				while currtime<stoptime:
					
					if data2[s][13] == '1':
						shockactivity3=shockactivity3+1
						currtime=float(data2[s][7])
						s=s+1	
					else:
						currtime=float(data2[s][7])
						s=s+1
								
			else: 	
				n=n+1
				t=t+1
		n=0
		t=0

		# Seek Latency cycle 4 calculator
		while t+1<=stop:
				
			if data2[n][9] == '22':
				time=float(data2[n][7])
				stoptime=time+38
				s=n
				n=n+1
				t=t+1
				shockcount4=shockcount4+1
				currtime=float(data2[s][13])

				while currtime<stoptime:
					
					if data2[s][13] == '1':
						shockactivity4=shockactivity4+1
						currtime=float(data2[s][7])
						s=s+1	
					else:
						currtime=float(data2[s][7])
						s=s+1
								
			else: 	
				n=n+1
				t=t+1
		n=0
		t=0	

		# Seek Latency cycle 5 calculator
		while t+1<=stop:
				
			if data2[n][9] == '28':
				time=float(data2[n][7])
				stoptime=time+38
				s=n
				n=n+1
				t=t+1
				shockcount5=shockcount5+1
				currtime=float(data2[s][13])

				while currtime<stoptime:
					
					if data2[s][13] == '1':
						shockactivity5=shockactivity5+1
						currtime=float(data2[s][7])
						s=s+1	
					else:
						currtime=float(data2[s][7])
						s=s+1
								
			else: 	
				n=n+1
				t=t+1
		n=0
		t=0	

		# Seek Latency cycle 6 calculator
		while t+1<=stop:
				
			if data2[n][9] == '34':
				time=float(data2[n][7])
				stoptime=time+38
				s=n
				n=n+1
				t=t+1
				shockcount6=shockcount6+1
				currtime=float(data2[s][13])

				while currtime<stoptime:
					
					if data2[s][13] == '1':
						shockactivity6=shockactivity6+1
						currtime=float(data2[s][7])
						s=s+1	
					else:
						currtime=float(data2[s][7])
						s=s+1
								
			else: 	
				n=n+1
				t=t+1
		n=0
		t=0		


		subj=data2[1][6][0:3]
		

		overall=shockactivity2+shockactivity3+shockactivity4+shockactivity5+shockactivity6
		totalshock=shockcount2+shockcount3+shockcount4+shockcount5+shockcount6

		overallmean="nan"





		Shockactivity=[subj,shockactivity1,shockactivity2,shockactivity3,shockactivity4,shockactivity5,shockactivity6,shockcount1,shockcount2,shockcount3,shockcount4,shockcount5,shockcount6,overallmean,session]

		csvShockact.append(Shockactivity)
		

		with open('Shockact.csv','w') as file:
			wr=csv.writer(file,lineterminator='\n')

			wr.writerow(['Subj','1','2','3','4','5','6','count1','count2','count3','count4','count5','count6', 'overallmean','session'])

			for item in csvShockact:
				wr.writerow(item)
	else:
		pass





