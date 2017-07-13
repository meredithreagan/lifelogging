import itertools as it
import random
import time
#morningpics
m=[]

#afternoonpics
a=[]


def grab_stim(sr, er, ):
    global gen
    stimuli = []
    order_counter = [0, 0, 0, 0]
    for i in range(16):
        if i%4==0:
            start_time = 'm'
            end_time = 'm'
        elif i%4==1:
            start_time = 'm'
            end_time = 'a'
        elif i%4==2:
            start_time = 'a'
            end_time = 'a'
        elif i%4==3:
            start_time = 'a'
            end_time = 'm'

        start=random.randint(0,len(gen)-1)
        dev = random.randint(sr,er)
        trying = True
        test_counter = 0
        while(trying & (test_counter < 10000)):
            start_day = None
            end_day = None
            if (start - dev < 0) & (start + dev < len(gen)-1):
                end = start + dev
                start_day = gen[start]
                end_day= gen[end]
            elif (start + dev > len(gen)-1) & (start - dev > 0):
                end = start
                start = start - dev
                start_day = gen[start]
                end_day = gen[end]
            elif (start - dev > 0) & (start + dev < len(gen)-1):
                coin = random.randint(0,1)
                if coin == 0:
                    end = start + dev
                    start_day = gen[start]
                    end_day= gen[end]
                elif coin == 1:
                    end = start
                    start = start - dev
                    start_day = gen[start]
                    end_day = gen[end]
            start_date = start_day['date']
            end_date = end_day['date']
            try:
                if (len(start_day[start_time]) > 0) & (len(end_day[end_time]) > 0):
                    start_image_path = start_day[start_time].pop()
                    end_image_path = end_day[end_time].pop()
                    if order_counter[i%4] < 2:
                        FD = time.strptime(start_image_path[start_image_path.find("Z")-14:start_image_path.find("Z")],  "%Y%m%d%H%M%S")
                        SD = time.strptime(end_image_path[end_image_path.find("Z")-14:end_image_path.find("Z")] "%Y%m%d%H%M%S")
                        if FD < SD:
                            correct = "second"
                        else:
                            correct = "first"
                        new_dict = {"first_pres":start_image_path,
                                    "first_order":"early",
                                    "first_time":start_time,
                                    "first_date":start_date,
                                    "second_pres":end_image_path,
                                    "second_order":"late",
                                    "second_time":end_time,
                                    "second_date":end_date,
                                    "correct":correct
                                    }
                    else:
                        SD = time.strptime(start_image_path[start_image_path.find("Z")-14:start_image_path.find("Z")],  "%Y%m%d%H%M%S")
                        FD = time.strptime(end_image_path[end_image_path.find("Z")-14:end_image_path.find("Z")] "%Y%m%d%H%M%S")
                        if FD < SD:
                            correct = "second"
                        else:
                            correct = "first"
                        new_dict = {"first_pres":end_image_path,
                                    "first_order":"late",
                                    "first_time":end_time,
                                    "first_date":end_date,
                                    "second_pres":start_image_path,
                                    "second_order":"early",
                                    "second_time":start_time,
                                    "second_date":start_date,
                                    "correct":correct
                                    }
                    stimuli.append(new_dict)
                    order_counter[i%4] = order_counter[i%4] + 1
                    trying = False
                else:
                    test_counter = test_counter + 1
                    start=random.randint(0,len(gen)-1)
                    dev = random.randint(sr,er)
            except:
                test_counter = test_counter + 1
                start=random.randint(0,len(gen)-1)
                dev = random.randint(sr,er)
        if trying :
            temp = 1/0.
    return stimuli

def grab_same_day():
    global gen
    stimuli = []
    order_counter = [0, 0, 0, 0]
    for i in range(32):
        if i%4==0:
            start_time = 'm'
            end_time = 'm'
        elif i%4==1:
            start_time = 'm'
            end_time = 'a'
        elif i%4==2:
            start_time = 'a'
            end_time = 'm'
        elif i%4==3:
            start_time = 'a'
            end_time = 'm'
    trying = True
    test_counter = 0
    while(trying & (test_counter < 10000)):
        start = random.randint(0,len(gen)-1)
        start_day = gen[start]
        end_day = gen[start]
        ## HEY BEEG ITS YOUR BOY BEEG
        ## You gotta fix the thing where morning to morning on the same day
        ## Needs to be half the time early then late and half the time late then early
        ## Same for Afternoon to afternoon. 
        """if (len(start_day[start_time]) > 0) & (len(end_day[end_time]) > 0):
            start_image_path = start_day[start_time].pop()
            end_image_path = end_day[end_time].pop()
            FD = time.strptime(start_image_path[start_image_path.find("Z")-14:start_image_path.find("Z")],  "%Y%m%d%H%M%S")
            SD = time.strptime(end_image_path[end_image_path.find("Z")-14:end_image_path.find("Z")] "%Y%m%d%H%M%S")
            if FD < SD:
                correct = "second"
            else:
                correct = "first"

            if order_counter[i%4] < 2:

                new_dict = {"first_pres":start_image_path,
                            "first_order":"early",
                            "first_time":start_time,
                            "first_date":start_date,
                            "second_pres":end_image_path,
                            "second_order":"late",
                            "second_time":end_time,
                            "second_date":end_date,
                            "correct":
                            }
            else:
                new_dict = {"first_pres":end_image_path,
                            "first_order":"late",
                            "first_time":end_time,
                            "first_date":end_date,
                            "second_pres":start_image_path,
                            "second_order":"early",
                            "second_time":start_time,
                            "second_date":start_date
                            }
            stimuli.append(new_dict)
            trying = False"""
        else:
            test_counter = test_counter + 1
            start=random.randint(0,len(gen)-1)
    if trying:
        temp = 1/0
    return stimuli

bigTrying = True
while(bigTrying):
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

    for x in gen:
        random.shuffle(x['m'])
        random.shuffle(x['a'])
    print gen

    #start of what Beeg was doing
    #1-2 days
    #need to chose 1-2 day interval


    try:
        stimuli = []
        stimuli = stimuli + grab_same_day()
        stimuli = stimuli + grab_stim(7, 7)
        stimuli = stimuli + grab_stim(8,12)
        stimuli = stimuli + grab_stim(1,2)
        stimuli = stimuli + grab_stim(4,6)

        print stimuli
        bigTrying=False
    except:
        pass
#end of what Beeg was doing
