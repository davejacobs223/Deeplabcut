import csv
import numpy as np
import pandas as pd
import math
from glob import glob

a=glob('Alld/*.csv')

csvall=[]



for row in a:
	data=[]
	with open(row,'r') as csvfile:
		reader=csv.reader(csvfile)#,delimiter='\t')
		for line in reader:
			data.append(line)
		csvfile.close()

	data2=np.array(data)


	protocol=data2[1][2]
	subject='S'+row.split('\\')[1].split('_')[0]  
	session=row.split('\\')[1].split('_')[1].split('.')[0]

	if protocol in ['74','77','79','STS_left_4cycles']:
		takecol=11
	elif protocol in ['76','78','80','STS_right_4cycles']:
		takecol=12

	# B1States=['39','3','4','5','7']
	# B2States=['8','11','10','12','13','9']
	# B3States=['14','17','16','18','19','15']
	# B4States=['21','24','23','25','26','22']
	# B5States=['27','30','29','31','32','28']
	# B6States=['33','36','35','37','38','34']
	# Bends=['20','-1','6']
	b1matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='2')[0].tolist()))
	b2matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='8')[0].tolist()))
	b3matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='16')[0].tolist()))
	b4matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='24')[0].tolist()))
	b5matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='50')[0].tolist()))#not set up for 6 cycle program
	b6matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='50')[0].tolist()))#not set up for 6 cycle program
	totaldis=b1matches+b2matches+b3matches+b4matches+b5matches+b6matches



	# b1matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='39')[0].tolist()))
	# b2matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='8')[0].tolist()))
	# b3matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='14')[0].tolist()))
	# b4matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='21')[0].tolist()))
	# b5matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='27')[0].tolist()))
	# b6matches=len(frozenset(np.where(data2[0:][:,takecol]=='1')[0].tolist()).intersection(np.where(data2[0:][:,8]=='33')[0].tolist()))
	# totaldis=b1matches+b2matches+b3matches+b4matches+b5matches+b6matches

	csvall.append([subject,session,b1matches,b2matches,b3matches,b4matches,b5matches,b6matches,totaldis])


pd.DataFrame(csvall).to_csv('yup.csv', header=['subject','session','1','2','3','4','5','6','sum'])