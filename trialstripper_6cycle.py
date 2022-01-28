#! bin/bash/env
#A code to strip trial by trial latencies and shocks. 
#Need to add disp actions in here... 1/30/20 working on it....

#2: are we counting completed seek action for non-complete trials? No, they are excluded


import csv
import numpy as np
import pandas as pd
import math
from glob import glob

a=glob('DailyRaw/*.txt')

t=0
n=0
triallistcsv=[]

def shocklocation(data,places,shocknum,threshold):
    tlist=[]
    tlist2=[]
    for a in range(len(data[1:][:,9])):
        if data2[a][9] in places:
            tlist.append(data[a][9])
        else:
            pass
    for a in range(len(tlist)):
        if tlist[a] == shocknum:
            tlist2.append(1)
        else:
            tlist2.append(0)    
    tarray=np.array(tlist2)
    if 1 in tarray and len(tarray) > 0:
        if np.where(tarray==1)[0][0] >= threshold:
            
            return ('late')

        else:
            return ('early')
    else:
        return ('NA')




for row in a:

    data=[]
    with open(row,'r') as csvfile:
        reader=csv.reader(csvfile,delimiter='\t')
        for line in reader:
            data.append(line)
        csvfile.close()

    

    data2=np.array(data)
    stop=len(data2) 
    
    #find where the first shock happens
    b1stype='NA'
    b2stype=shocklocation(data2,['9','10'],'9',10)
    b3stype=shocklocation(data2,['15','16'],'15',9)
    b4stype=shocklocation(data2,['22','23'],'22',8)
    b5stype=shocklocation(data2,['28','29'],'28',6)
    b6stype=shocklocation(data2,['34','35'],'34',5)




    Session=row.split('\\')[1]
    Session=Session.split('.')[0]
    Session=Session.split('_')[1]
    IDNum=data2[1][6].split('_')[0]
    Protocol=data2[1][2].split('_')[0]

    if Protocol == 'right':
        se=11
        ta=12
        fd=14
    else:
        se=12
        ta=11
        fd=14

    B1States=['39','3','4','5','7']
    B2States=['8','11','10','12','13','9']
    B3States=['14','17','16','18','19','15']
    B4States=['21','24','23','25','26','22']
    B5States=['27','30','29','31','32','28']
    B6States=['33','36','35','37','38','34']
    Bends=['20','-1','6']
#MRBA696
   
    ###
    ofoodlist=[]
    typeoflist=[]

    #foodon
    for a in range(len(data2)):
        if data2[a][9]=='39' and data2[a][8]=='1':
            ofoodlist.append(a)
            #typeoflist.append(1)
    for a in range(len(data2)):
        if data2[a][9]=='5' or data2[a][9] in Bends and data2[a][8] in B1States:
            ofoodlist.append(a)
            typeoflist.append(1)
        elif data2[a][9]=='13' or data2[a][9] in Bends and data2[a][8] in B2States:
            ofoodlist.append(a)
            typeoflist.append(2)
        elif data2[a][9]=='19' or data2[a][9] in Bends and data2[a][8] in B3States:
            ofoodlist.append(a)
            typeoflist.append(3)
        elif data2[a][9]=='26' or data2[a][9] in Bends and data2[a][8] in B4States:
            ofoodlist.append(a)
            typeoflist.append(4)  
        elif data2[a][9]=='32' or data2[a][9] in Bends and data2[a][8] in B5States:
            ofoodlist.append(a)
            typeoflist.append(5)
        elif data2[a][9]=='38' or data2[a][9] in Bends and data2[a][8] in B6States:
            ofoodlist.append(a)
            typeoflist.append(6)

    starts=ofoodlist[0:90]
    ends=ofoodlist[1:]

    new=list(zip(starts,ends,typeoflist))
    new=np.array(new)


    seekcues=['39','8','14','21','27','33']
    takecues=['3','11','17','24','30','36']
    seekstates=['7','10','16','23','29','35','9','15','22','28','34']
    takestates=['4','12','18','25','31','37']
    foodstates=['5','13','19','26','32','38','20'] # also take state and 20
    shockstates=['9','15','22','28','34']
    count1=0
    count2=0
    count3=0
    count4=0
    count5=0
    count6=0
    posttrig=0
    over='no'
    for a in range(len(new)):
        start=new[a][0]
        end=(new[a][1])+1
        CurrBlock=new[a][2]
        if CurrBlock != 6: #make 5 for 5 cycle
            NextBlock=new[a+1][2]
        if a == len(new)-1:
            over='yes'
        data=data2[start:end]
        seekactiontime='NA'
        takeactiontime='NA'
        takecuetime='NA'
        foodactiontime='NA'
        DispCount=0
        shock=0
        for b in range(len(data)):

            if data[b][9] in seekcues:
                seekcuetime=(float(data[b][7])*20*.001)
                if data[b][9] == '39':
                    Btype=1
                    count1=count1+1

                elif data[b][9] == '8':
                    Btype=2
                    count2=count2+1

                elif data[b][9] == '14':
                    Btype=3
                    count3=count3+1

                elif data[b][9] == '21':
                    Btype=4
                    count4=count4+1
                elif data[b][9] == '27':
                    Btype=5
                    count5=count5+1                    
                elif data[b][9] == '33':
                    Btype=6
                    count6=count6+1
            


            elif data[b][9] in seekstates:
                seekactiontime=(float(data[b][7])*20*.001)
                if data[b][9] in shockstates:
                    shock=1
                    if posttrig ==5309:
                        pshock=1
                    else:    
                        posttrig=5309
                        pshock=0
                elif posttrig==5309:
                    shock=0
                    pshock=1
                    posttrig=0
                else:
                    shock=0
                    pshock=0
                    posttrig=0

            elif data[b][9] in takecues:
                takecuetime=(float(data[b][7])*20*.001)
            elif data[b][9] in takestates:
                takeactiontime=(float(data[b][7])*20*.001)
            # elif data[b][9]=='4':
            #     foodcuetime=(float(data[b][7])*20*.001)
            elif data[b][9] in foodstates:
                foodactiontime=(float(data[b][7])*20*.001)
        if seekactiontime != 'NA': #and seekactiontime > seekcuetime:
            seeklat=seekactiontime-seekcuetime
        else:
            seeklat='NA'
            pshock=0

        if takeactiontime != 'NA' and takeactiontime > takecuetime:
            takelat=takeactiontime-takecuetime
        else:
            takelat='NA'
            pshock=0
       
        if foodactiontime != 'NA' and takeactiontime != 'NA':
            foodlat=foodactiontime-takeactiontime
        else:
            foodlat='NA'
            pshock=0

            

        Trial=a+1
        #Total=count1+count2+count3+count4+count5+count6
        if Btype == 1:
            ShTime =b1stype
            Total=count1
        elif Btype == 2:
            ShTime = b2stype
            Total=count2
        elif Btype == 3:
            ShTime = b3stype
            Total=count3
        elif Btype == 4:
            ShTime = b4stype
            Total=count4
        elif Btype == 5:
            ShTime = b5stype
            Total=count5
        elif Btype == 6:
            ShTime = b6stype
            Total=count6


        triallist=[Session,IDNum,seeklat,takelat,foodlat,shock,pshock,Trial,Btype,Total,ShTime]
        triallistcsv.append(triallist)

        # if CurrBlock < NextBlock or over == 'yes':
        #     if Btype == 1:
        #         while count1 < 15:
        #             count1=count1+1
        #             DispCount=0
        #             Total=count1+count2+count3+count4+count5+count6
        #             triallist=[Session,IDNum,'NA','NA','NA','NA','NA','NA','NA',Total]
        #             triallistcsv.append(triallist)
        #         trig=0 
        #     elif Btype == 2:
        #         while count2 < 15:
        #             count2=count2+1
        #             DispCount=0
        #             Total=count1+count2+count3+count4+count5+count6
        #             triallist=[Session,IDNum,'NA','NA','NA','NA','NA','NA','NA',Total]
        #             triallistcsv.append(triallist)
        #         trig=0             
        #     elif Btype == 3:
        #         while count3 < 15:
        #             count3=count3+1
        #             DispCount=0
        #             Total=count1+count2+count3+count4+count5+count6
        #             triallist=[Session,IDNum,'NA','NA','NA','NA','NA','NA','NA',Total]
        #             triallistcsv.append(triallist)
        #         trig=0             
        #     elif Btype == 4:
        #         while count4 < 15:
        #             count4=count4+1
        #             DispCount=0
        #             Total=count1+count2+count3+count4+count5+count6
        #             triallist=[Session,IDNum,'NA','NA','NA','NA','NA','NA','NA',Total]
        #             triallistcsv.append(triallist)
        #         trig=0


with open('All_Data.csv','w') as file:
    wr=csv.writer(file,lineterminator='\n')
    wr.writerow(['Session','Subject','SL','TL','FL','Sh','PostShock','Trial','Block','Total'])

    for item in triallistcsv:
        wr.writerow(item)

        
DF=pd.read_csv('All_Data.csv')
DF=DF.groupby(by=['Sh','Session','Subject','Block']).mean()
DF.unstack().transpose().to_csv('bob2.csv')