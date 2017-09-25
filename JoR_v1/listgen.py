
import itertools as it
import random
from datetime import datetime
import glob


def generateStimList(num_blocks=4, len_blocks=24, data_dir="images/*"):

    # For each subdirectory, add a dictionary, containing a list of images
    # for each half-day
    dayDicts = []
    for x in glob.glob(data_dir):
        paths_m = glob.glob(x+"/morning/*")
        paths_a = glob.glob(x+"/afternoon/*")
        dayDicts.append({"m": paths_m, "a": paths_a})

    # Shuffle images for each half day
    for x in dayDicts:
        random.shuffle(x['m'])
        random.shuffle(x['a'])

    # Assemble the stimuli lists
    stimuli = []
    stimuli = stimuli + grab_days(dayDicts, True)
    stimuli = stimuli + grab_days(dayDicts, False, 7, 7) + \
                        grab_days(dayDicts, False, 1, 2) + \
                        grab_days(dayDicts, False, 4, 6) + \
                        grab_days(dayDicts, False, 8, 12)
    # Grab any unused stims and collect them into an "odd gap" group
    stimuli = stimuli + grab_days_odd(dayDicts)



    # Qualify the lists to verify balanced

    counter_subDay_mm = 0
    counter_subDay_ma = 0
    counter_subDay_aa = 0
    counter_subDay_am = 0
    counter_multiDay_mm = 0
    counter_multiDay_ma = 0
    counter_multiDay_aa = 0
    counter_multiDay_am = 0
    for i in range(len(stimuli)):
        stim = stimuli[i]
        #print i
        #print stim['first_date'], stim['second_date'], stim['gap'], \
        #      stim['first_halfDay'], stim['second_halfDay']

        if stim['gap'] in range(1, 3):
            gapClass = '1to2'
        if stim['gap'] in range(4, 7):
            gapClass = '4to6'
        if stim['gap'] in range(8, 13):
            gapClass = '8to12'
        if stim['gap'] == 0:
            gapClass = 'LessThan1'
        if stim['gap'] == 7:
            gapClass = '7'

        daysClass = stim['halfDays']
        if gapClass == 'LessThan1':
            if daysClass == 'mm':
                counter_subDay_mm += 1
            if daysClass == 'ma':
                counter_subDay_ma += 1
            if daysClass == 'aa':
                counter_subDay_aa += 1
            if daysClass == 'am':
                counter_subDay_am += 1
        elif gapClass != 'LessThan1':
            if daysClass == 'mm':
                counter_multiDay_mm += 1
            if daysClass == 'ma':
                counter_multiDay_ma += 1
            if daysClass == 'aa':
                counter_multiDay_aa += 1
            if daysClass == 'am':
                counter_multiDay_am += 1

    print '---------------------'
    print 'sub-day mm:', counter_subDay_mm
    print 'sub-day ma:', counter_subDay_ma
    print 'sub-day aa:', counter_subDay_aa
    print 'sub-day am:', counter_subDay_am
    print 'different-day mm:', counter_multiDay_mm
    print 'different-day ma:', counter_multiDay_ma
    print 'different-day aa:', counter_multiDay_aa
    print 'different-day am:', counter_multiDay_am

    random.shuffle(stimuli)
    allBlocks = []
    trialCounter = 0
    for i in range(num_blocks):
        block = []
        for j in range(len_blocks):
            if len(stimuli) == 0:
                print 'RAN OUT OF STIMS'
            else:
                stim = stimuli.pop()
                trialCounter += 1
                stim.update({'block':i+1, 'trial_inBlock': j+1,
                             'trial_absolute':trialCounter})
                block.append(stim)
        allBlocks.append(block)

    return allBlocks


def grab_days(dayDicts, sameDay, gapRangeStart=None, gapRangeEnd=None):

    print '-'
    stimuli = []
    order_counter = [0, 0, 0, 0]
    timeout_counter = 0
    timeout_tries = 1000000

    # Run in blocks of 32 for same-day, 16 for different-day
    if sameDay == True:
        blockLength = 32
    elif sameDay == False:
        blockLength = 16
    for i in range(blockLength):
        # Choose starting/ending half-days in repeat combos every 4 stim-pairs
        if i%4==0:
            first_halfDay = 'm'
            second_halfDay = 'm'
        elif i%4==1:
            first_halfDay = 'm'
            second_halfDay = 'a'
        elif i%4==2:
            first_halfDay = 'a'
            second_halfDay = 'a'
        elif i%4==3:
            first_halfDay = 'a'
            second_halfDay = 'm'

        stopFlag = False
        while(stopFlag == False and timeout_counter < timeout_tries):

            # Pick random index on days
            index1 = random.randint(0, len(dayDicts) - 1)
            if sameDay == True:
                # Both days are based on the start index
                gap = 0
                dayDict1 = dayDicts[index1]
                dayDict2 = dayDicts[index1]
            elif sameDay == False:
                # Pick a random gap distance within the gap range
                gap = random.randint(gapRangeStart, gapRangeEnd)
                # Decide whether to subtract or add the gap to get the second
                # index, based on which is possible. If both are possible,
                # choose randomly
                if (index1 - gap < 0) & (index1 + gap <= len(dayDicts) - 1):
                    index2 = index1 + gap
                elif (index1 + gap > len(dayDicts) - 1) & (index1 - gap >= 0):
                    index2 = index1 - gap
                elif (index1 - gap >= 0) & (index1 + gap <= len(dayDicts) - 1):
                    coin = random.randint(0, 1)
                    if coin == 0:
                        index2 = index1 + gap
                    elif coin == 1:
                        index2 = index1 - gap
                # Now use the indexes in random order to pick the days
                coin = random.randint(0, 1)
                if coin == 0:
                    dayDict1 = dayDicts[index1]
                    dayDict2= dayDicts[index2]
                elif coin == 1:
                    dayDict1 = dayDicts[index2]
                    dayDict2 = dayDicts[index1]

            # If there AREN'T enough images in the chosen directories, abort,
            # increment the timeout counter and try again
            if sameDay == True:
                minSize = 2
            elif sameDay == False:
                minSize = 1
            if not ((len(dayDict1[first_halfDay]) >= minSize) & \
               (len(dayDict2[second_halfDay]) >= minSize)):
                timeout_counter += 1
                if timeout_counter >= timeout_tries:
                    print 'TIMED OUT!'

            # Otherwise,
            else:

                # Pop out a start and an end image
                firstImage_path = dayDict1[first_halfDay].pop()
                secondImage_path = dayDict2[second_halfDay].pop()

                # Get the datetimes for comparison and for logs
                datetime_forCompare_first = datetime.strptime(firstImage_path[
                                                firstImage_path.find("Z")-
                                                14:firstImage_path.find("Z")],
                                                "%Y%m%d%H%M%S")
                datetime_forCompare_second = datetime.strptime(secondImage_path[
                                                secondImage_path.find("Z")-
                                                14:secondImage_path.find("Z")],
                                                "%Y%m%d%H%M%S")
                datetime_forLog_first = firstImage_path[
                                              firstImage_path.find("Z")-
                                              14:firstImage_path.find("Z")-6]
                datetime_forLog_second = secondImage_path[
                                              secondImage_path.find("Z")-
                                              14:secondImage_path.find("Z")-6]

                start_date_fmt1 = datetime_forCompare_first######################## TODO: Get rid of this, switching out the vocab instead of re-assigning redundantly
                start_date_fmt2 = datetime_forLog_first
                end_date_fmt1 = datetime_forCompare_second
                end_date_fmt2 = datetime_forLog_second

                # Record whether first or second image was actually more recent
                if start_date_fmt1 < end_date_fmt1:
                    correct = "second"
                else:
                    correct = "first"

                # Decide the order shown, so that half of the pairs are
                # shown in correct order and half are shown in reverse
                if sameDay == True:
                    halfwayPoint = 4
                elif sameDay == False:
                    halfwayPoint = 2
                if order_counter[i%4] < halfwayPoint:
                    if correct == "first":
                        order = "start_first"
                    elif correct == "second":
                        order = "end_first"
                elif order_counter[i%4] >= halfwayPoint:
                    if correct == "first":
                        order = "end_first"
                    elif correct == "second":
                        order = "start_first"

                # Construct and append the dictionaries to stim-pair list
                if order == "start_first":
                    new_dict = {"first_pres":firstImage_path,
                                "first_order":"early",
                                "first_halfDay":first_halfDay,
                                "first_date":start_date_fmt2,
                                "second_pres":secondImage_path,
                                "second_order":"late",
                                "second_halfDay":second_halfDay,
                                "second_date":end_date_fmt2,
                                "gap":gap,
                                "halfDays":first_halfDay+second_halfDay,
                                "order":order,
                                "correctKey":'F',
                                'godModeLabel':str(gap)+'-'+first_halfDay+second_halfDay,
                                'oddGapClass':'False'}
                elif order == "end_first":
                    new_dict = {"first_pres":secondImage_path,
                                "first_order":"late",
                                "first_halfDay":second_halfDay,
                                "first_date":end_date_fmt2,
                                "second_pres":firstImage_path,
                                "second_order":"early",
                                "second_halfDay":first_halfDay,
                                "second_date":start_date_fmt2,
                                "gap":gap,
                                "halfDays":first_halfDay+second_halfDay,
                                "order":order,
                                "correctKey":'J',
                                'godModeLabel':str(gap)+'-'+first_halfDay+second_halfDay,
                                'oddGapClass':'False'}
                stimuli.append(new_dict)

                print i+1, first_halfDay, second_halfDay

                # Increment the order-counter to maintain balanced design
                order_counter[i%4] = order_counter[i%4] + 1
                # Set stopFlag to True to proceed to the next stim-pair
                stopFlag = True

    print 'stimuli length:', len(stimuli)
    print 'order counter:', order_counter
    return stimuli


def grab_days_odd(dayDicts):

    leftovers = []
    leftoverHalfDayLength = 0
    for dayDict in dayDicts:
        if not ((len(dayDict['m']) == 0 & len(dayDict['a']) == 0)):
            leftovers.append(dayDict)
        leftoverHalfDayLength += len(dayDict['m'])
        leftoverHalfDayLength += len(dayDict['a'])

    print '-odd-'
    stimuli = []
    order_counter = [0, 0, 0, 0]
    timeout_counter = 0
    timeout_tries = 1000000
    halfwayPoint = leftoverHalfDayLength/4

    for i in range(leftoverHalfDayLength/2):

        stopFlag = False
        while(stopFlag == False and timeout_counter < timeout_tries):

            # Choose starting/ending half-days randomly
            coin = random.randint(0, 1)
            if coin == 0:
                first_halfDay = 'm'
            elif coin == 1:
                first_halfDay = 'a'

            coin = random.randint(0, 1)
            if coin == 0:
                second_halfDay = 'm'
            elif coin == 1:
                second_halfDay = 'a'

            # Pick random indexes on days
            index1 = random.randint(0, len(dayDicts) - 1)
            index2 = random.randint(0, len(dayDicts) - 1)
            if index1 == index2:
                sameDay = True
            else:
                sameDay = False
            gap = abs(index1 - index2)
            # Now use the indexes in random order to pick the days
            coin = random.randint(0, 1)
            if coin == 0:
                dayDict1 = dayDicts[index1]
                dayDict2= dayDicts[index2]
            elif coin == 1:
                dayDict1 = dayDicts[index2]
                dayDict2 = dayDicts[index1]

            # If there AREN'T enough images in the chosen directories, abort,
            # increment the timeout counter and try again
            if sameDay == True:
                minSize = 2
            elif sameDay == False:
                minSize = 1
            if not ((len(dayDict1[first_halfDay]) >= minSize) & \
               (len(dayDict2[second_halfDay]) >= minSize)):
                timeout_counter += 1
                if timeout_counter >= timeout_tries:
                    print 'TIMED OUT!', dayDicts

            # Otherwise,
            else:

                # Pop out a start and an end image
                firstImage_path = dayDict1[first_halfDay].pop()
                secondImage_path = dayDict2[second_halfDay].pop()

                # Get the datetimes for comparison and for logs
                datetime_forCompare_first = datetime.strptime(firstImage_path[
                                                firstImage_path.find("Z")-
                                                14:firstImage_path.find("Z")],
                                                "%Y%m%d%H%M%S")
                datetime_forCompare_second = datetime.strptime(secondImage_path[
                                                secondImage_path.find("Z")-
                                                14:secondImage_path.find("Z")],
                                                "%Y%m%d%H%M%S")
                datetime_forLog_first = firstImage_path[
                                              firstImage_path.find("Z")-
                                              14:firstImage_path.find("Z")-6]
                datetime_forLog_second = secondImage_path[
                                              secondImage_path.find("Z")-
                                              14:secondImage_path.find("Z")-6]

                start_date_fmt1 = datetime_forCompare_first######################## TODO: Get rid of this, switching out the vocab instead of re-assigning redundantly
                start_date_fmt2 = datetime_forLog_first
                end_date_fmt1 = datetime_forCompare_second
                end_date_fmt2 = datetime_forLog_second

                # Record whether first or second image was actually more recent
                if start_date_fmt1 < end_date_fmt1:
                    correct = "second"
                else:
                    correct = "first"

                # Decide the order shown, so that half of the pairs are
                # shown in correct order and half are shown in reverse
                if order_counter[i%4] < halfwayPoint:
                    if correct == "first":
                        order = "start_first"
                    elif correct == "second":
                        order = "end_first"
                elif order_counter[i%4] >= halfwayPoint:
                    if correct == "first":
                        order = "end_first"
                    elif correct == "second":
                        order = "start_first"

                # Construct and append the dictionaries to stim-pair list
                if order == "start_first":
                    new_dict = {"first_pres":firstImage_path,
                                "first_order":"early",
                                "first_halfDay":first_halfDay,
                                "first_date":start_date_fmt2,
                                "second_pres":secondImage_path,
                                "second_order":"late",
                                "second_halfDay":second_halfDay,
                                "second_date":end_date_fmt2,
                                "gap":gap,
                                "halfDays":first_halfDay+second_halfDay,
                                "order":order,
                                "correctKey":'F',
                                'godModeLabel':str(gap)+'-'+first_halfDay+second_halfDay,
                                'oddGapClass':'True'}
                elif order == "end_first":
                    new_dict = {"first_pres":secondImage_path,
                                "first_order":"late",
                                "first_halfDay":second_halfDay,
                                "first_date":end_date_fmt2,
                                "second_pres":firstImage_path,
                                "second_order":"early",
                                "second_halfDay":first_halfDay,
                                "second_date":start_date_fmt2,
                                "gap":gap,
                                "halfDays":first_halfDay+second_halfDay,
                                "order":order,
                                "correctKey":'J',
                                'godModeLabel':str(gap)+'-'+first_halfDay+second_halfDay,
                                'oddGapClass':'True'}
                stimuli.append(new_dict)

                print i+1, first_halfDay, second_halfDay

                # Increment the order-counter to maintain balanced design
                order_counter[i%4] = order_counter[i%4] + 1
                # Set stopFlag to True to proceed to the next stim-pair
                stopFlag = True

    print 'stimuli length:', len(stimuli)
    print 'order counter:', order_counter
    return stimuli


if __name__ == "__main__":

    generateStimList()
