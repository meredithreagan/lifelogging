import itertools as it
import random
import time
import glob


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
                        FD = time.strptime(start_image_path[start_image_path.find("Z")-14:start_image_path.find("Z")], "%Y%m%d%H%M%S")
                        SD = time.strptime(end_image_path[end_image_path.find("Z")-14:end_image_path.find("Z")], "%Y%m%d%H%M%S")
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
                        FD = time.strptime(end_image_path[end_image_path.find("Z")-14:end_image_path.find("Z")], "%Y%m%d%H%M%S")
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
        ## You gotta fix the thing where morning to morning on the same day
        ## Needs to be half the time early then late and half the time late then early
        ## Same for Afternoon to afternoon.
        if (len(start_day[start_time]) > 0) & (len(end_day[end_time]) > 0):
            start_image_path = start_day[start_time].pop()
            end_image_path = end_day[end_time].pop()
            FDate = time.strptime(start_image_path[start_image_path.find("Z")-14:start_image_path.find("Z")], "%Y%m%d%H%M%S")
            SDate = time.strptime(end_image_path[end_image_path.find("Z")-14:end_image_path.find("Z")], "%Y%m%d%H%M%S")
            if FDate < SDate:
                correct = "second"
            else:
                correct = "first"
            if order_counter[i%4] < 4:
                if correct == "first":
                    order = "start_first"
                elif correct == "second":
                    order = "end_first"
            elif order_counter[i%4] >= 4:
                if correct == "first":
                    order = "end_first"
                elif correct == "second":
                    order = "start_first"
            if order == "end_first":
                new_dict = {"first_pres":end_image_path,
                            "first_order":"late",
                            "first_time":end_time,
                            "first_date":end_date,
                            "second_pres":start_image_path,
                            "second_order":"early",
                            "second_time":start_time,
                            "second_date":start_date,
                            "correct":correct}
            elif order == "start_first":
                new_dict = {"first_pres":start_image_path,
                            "first_order":"early",
                            "first_time":start_time,
                            "first_date":start_date,
                            "second_pres":end_image_path,
                            "second_order":"late",
                            "second_time":end_time,
                            "second_date":end_date,
                            "correct":correct}

            stimuli.append(new_dict)
            order_counter[i%4] = order_counter[i%4] + 1
            trying = False
        else:
            test_counter = test_counter + 1
            start=random.randint(0,len(gen)-1)
    if trying:
        temp = 1/0
    return stimuli


bigTrying = True
num_tries = 0
while((bigTrying) & (num_tries < 10000)):
    data_dir = "/Users/meredithreagan/Documents/SMILE_MAIN/my_experiment/pics/*"

    gen = []

    for x in glob.glob(data_dir):
        mp = glob.glob(x+"/morning/*")
        ap = glob.glob(x+"/afternoon/*")
        gen.append({"m":mp,
                    "a":ap})
    print gen


    for x in gen:
        random.shuffle(x['m'])
        random.shuffle(x['a'])



    stimuli = []
    stimuli = stimuli + grab_same_day()
    stimuli = stimuli + grab_stim(7, 7)
    stimuli = stimuli + grab_stim(8,12)
    stimuli = stimuli + grab_stim(1,2)
    stimuli = stimuli + grab_stim(4,6)

    print len(stimuli)
    bigTrying=False
