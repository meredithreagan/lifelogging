from smile.common import *
import itertools as it
import random
#morningpics
m=[]

#afternoonpics
a=[]

gen=[{'date': 612,'m':['1','2','3','4'],'a':['5','6','7','8']},
{'date': 613,'m':['9','10','11','12'],'a':['13','14','15','16']},
{'date': 614,'m':['17','18','19','20'],'a':['21','22','23','24']},
{'date': 615,'m':['25','26','27','28'],'a':['29','30','31','32']},
{'date': 616,'m':['33','34','35','36'],'a':['37','38','39','40']},
{'date': 617,'m':['41','42','43','44'],'a':['45','46','47','48']},
{'date': 618,'m':['49','50','51','52'],'a':['53','54','55','56']},
{'date': 619,'m':['57','58','59','60'],'a':['61','62','63','64']},
{'date': 620,'m':['65','66','67','68'],'a':['69','70','71','72']},
{'date': 621,'m':['73','74','75','76'],'a':['77','78','79','80']},
{'date': 622,'m':['81','82','83','84'],'a':['85','86','87','88']},
{'date': 623,'m':['89','90','91','92'],'a':['93','94','95','96']},
{'date': 624,'m':['97','98','99','100'],'a':['101','102','103','104']},
{'date': 625,'m':['105','106','107','108'],'a':['109','110','111','112']},
{'date': 626,'m':['113','114','115','116'],'a':['117','118','119','120']},
{'date': 627,'m':['121','122','123','124'],'a':['125','126','127','128']},
{'date': 628,'m':['129','130','131','132'],'a':['133','134','135','136']},
{'date': 629,'m':['137','138','139','140'],'a':['141','142','143','144']},
{'date': 630,'m':['145','146','147','148'],'a':['149','150','151','152']},
{'date': 701,'m':['153','154','155','156'],'a':['157','158','159','160']},
{'date': 702,'m':['161','162','163','164'],'a':['165','166','167','168']}]




same_day_m=[]
for day in gen:
    sdm=[]
    x=day['m']
    z = list(it.combinations(x,2))    #Get every combination of pics
    for i in z:
        same_day_m.append(i)    #add each pair to storage
#print same_day_m



same_day_a=[]
for day in gen:
    sda=[]
    x=day['a']
    z = list(it.combinations(x,2))    #Get every combination of pics
    for i in z:
        same_day_a.append(i)
#print same_day_a



same_day_ma=[]
for day in gen:
    ma=[]
    m=day['m']
    a=day['a']
    z = [[x,y] for x in m for y in a]   #Generate every combo
    for i in z:
        same_day_ma.append(i)
#print same_day_ma



different_day_m_1to2=[]
for ind in range(len(gen)-1):
    coin0=random.randint(0,1)
    coin1=random.randint(0,1)
    coin2=random.randint(0,1)
    if coin0 == 0:
        halfDayKey0 = 'm'
    else:
        halfDayKey0= 'a'

    if coin1 == 0:
        halfDayKey1 = 'm'
    else:
        halfDayKey1= 'a'

    if coin2 == 0:
        halfDayKey2='m'
    else:
        halfDayKey2='a'

    day_0=gen[ind][halfDayKey0]
    day_1=gen[ind+1][halfDayKey1]
    try:
        day_2=gen[ind+2][halfDayKey2]
        next_day=[day_1,day_2]
    except:
        next_day=[day_1]
    for day in next_day:
        z = [[x,y] for x in day_0 for y in day]  #Get all combos
        for i in z:
          different_day_m_1to2.append(i)
random.shuffle(different_day_m_1to2)
#print different_day_m_1to2




#this works!!!!
different_day_m_4to6=[]
for ind in range(len(gen)-4):
    coin0=random.randint(0,1)
    coin4=random.randint(0,1)
    coin5=random.randint(0,1)
    coin6=random.randint(0,1)
    if coin0 == 0:
        halfDayKey0 = 'm'
    else:
        halfDayKey0= 'a'

    if coin4 == 0:
        halfDayKey4 = 'm'
    else:
        halfDayKey4= 'a'

    if coin5 == 0:
        halfDayKey5='m'
    else:
        halfDayKey6='a'

    if coin6==0:
        halfDayKey6='m'
    else:
        halfDayKey6='a'

    day_0=gen[ind][halfDayKey0]
    day_4=gen[ind+4][halfDayKey4]
    try:
        day_5=gen[ind+5][halfDayKey5]
        day_6=gen[ind+6][halfDayKey6]
        next_day=[day_4, day_5, day_6]
    except:
        next_day=[day_4]
    for day in next_day:
        z=[[x,y] for x in day_0 for y in day]
        for i in z:
           different_day_m_4to6.append(i)
#print different_day_m_4to6





different_day_m_8to12=[]
for ind in range(len(gen)-8):
    coin0=random.randint(0,1)
    coin8=random.randint(0,1)
    coin9=random.randint(0,1)
    coin10=random.randint(0,1)
    coin11=random.randint(0,1)
    coin12=random.randint(0,1)
    if coin0 == 0:
        halfDayKey0 = 'm'
    else:
        halfDayKey0= 'a'

    if coin8 == 0:
        halfDayKey8 = 'm'
    else:
        halfDayKey8= 'a'

    if coin9 == 0:
        halfDayKey9='m'
    else:
        halfDayKey9='a'

    if coin10==0:
        halfDayKey10='m'
    else:
        halfDayKey10='a'

    if coin11 == 0:
        halfDayKey11 = 'm'
    else:
        halfDayKey11= 'a'

    if coin12 == 0:
        halfDayKey12 = 'm'
    else:
        halfDayKey12= 'a'


    day_0=gen[ind][halfDayKey0]
    day_8=gen[ind+8][halfDayKey8]
    try:
        day_9=gen[ind+9][halfDayKey9]
        day_10=gen[ind+10][halfDayKey10]
        day_11=gen[ind+11][halfDayKey11]
        day_12=gen[ind+12][halfDayKey12]
        next_day=[day_8,day_9,day_10,day_11,day_12]
    except:
        next_day=[day_8]
    for day in next_day:
        z=[[x,y] for x in day_0 for y in day]
        for i in z:
            different_day_m_8to12.append(i)
#print different_day_m_8to12




different_day_m_7=[]
for ind in range(len(gen)-7):
    coin0=random.randint(0,1)
    coin7=random.randint(0,1)
    if coin0==0:
        halfDayKey0='m'
    else:
        halfDayKey0='a'
    if coin7==0:
        halfDayKey7='m'
    else:
        halfDayKey7='a'
    day_0=gen[ind][halfDayKey0]
    day_7=gen[ind+7][halfDayKey7]
    next_day=[day_7]
    for day in next_day:
        z=[[x,y] for x in day_0 for y in day]
        for i in z:
            different_day_m_7.append(i)
#print different_day_m_7
