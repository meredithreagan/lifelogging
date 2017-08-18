
"""
Listgen v2
"""


import random
import glob
import itertools as it
from datetime import datetime


def generate_stim_list(num_blocks=4, len_blocks=24, data_dir="images/*"):
    # Generates a list of dictionaries, each of which contains the info for
    # one stimulus (image pair), organized into blocks.

    # For each subdirectory (representing a day of collection), add a dictionary
    # containing a list of images for each half-day.
    day_dicts = []
    for x in glob.glob(data_dir):
        paths_m = glob.glob(x+"/morning/*")
        paths_a = glob.glob(x+"/afternoon/*")
        day_dicts.append({'morning': paths_m, 'afternoon': paths_a})

    # Shuffle images within each half-day.
    for day_dict in day_dicts:
        random.shuffle(day_dict['morning'])
        random.shuffle(day_dict['afternoon'])

    # Assemble the stimuli lists.
    stimuli = []
    stimuli = stimuli + grab_days(day_dicts, 'same-day')
    stimuli = stimuli + grab_days(day_dicts, 'different-day', 7, 7) + \
                        grab_days(day_dicts, 'different-day', 1, 2) + \
                        grab_days(day_dicts, 'different-day', 4, 6) + \
                        grab_days(day_dicts, 'different-day', 8, 12) + \
                        grab_days(day_dicts, 'odd')


    # Qualify the lists to verify balance.

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
            if daysClass == 'morning-morning':
                counter_subDay_mm += 1
            if daysClass == 'morning-afternoon':
                counter_subDay_ma += 1
            if daysClass == 'afternoon-afternoon':
                counter_subDay_aa += 1
            if daysClass == 'afternoon-morning':
                counter_subDay_am += 1
        elif gapClass != 'LessThan1':
            if daysClass == 'morning-morning':
                counter_multiDay_mm += 1
            if daysClass == 'morning-afternoon':
                counter_multiDay_ma += 1
            if daysClass == 'afternoon-afternoon':
                counter_multiDay_aa += 1
            if daysClass == 'afternoon-morning':
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

    # Return the stimulus dictionaries.
    return allBlocks


def grab_days(day_dicts, type_, gapRangeStart=None, gapRangeEnd=None):
    # Get a set of dictionaries for stimuli of a given between-image gap.

    # Set timeout setting.
    timeout_tries = 1000000

    # If the gap-type is odd, construct a list of the day-dictionaries that
    # remain to be pulled from, along with a length of that list (in half-days).
    if type_ == 'odd':
        leftovers = []
        leftoverHalfDayLength = 0
        for dayDict in day_dicts:
            if not (
                    (len(dayDict['morning']) == 0
                    and len(dayDict['afternoon']) == 0)
                    ):
                leftovers.append(dayDict)
            leftoverHalfDayLength += len(dayDict['morning'])
            leftoverHalfDayLength += len(dayDict['afternoon'])

    # Set starting values for method constructs.
    stimuli = []
    order_counter = [0, 0, 0, 0]
    timeout_counter = 0

    # Run in blocks of 32 for same-day, 16 for different-day, and however long
    # you can grab pairs for odd.
    if type_ == 'same-day':
        blockLength = 32
    elif type_ == 'different-day':
        blockLength = 16
    elif type_ == 'odd':
        blockLength = leftoverHalfDayLength/2

    for i in range(blockLength):

        # For same-day and different-day types, choose starting/ending half-days
        # in repeat combos every 4 stimuli.
        if type_ == 'same-day' or type_ == 'different-day':
            half_day_assignments = {
                                    0: ['morning', 'morning'],
                                    1: ['morning', 'afternoon'],
                                    2: ['afternoon', 'afternoon'],
                                    3: ['afternoon', 'morning'],
                                    }
            half_day_A = half_day_assignments[i%4][0]
            half_day_B = half_day_assignments[i%4][1]
        # For odd type, choose starting/ending half-days randomly.
        elif type_ == 'odd':
            half_day_possibilities = ['morning', 'afternoon']
            half_day_A = half_day_possibilities[random.randint(0, 1)]
            half_day_B = half_day_possibilities[random.randint(0, 1)]

        # Keep trying to pull a pair as long as you haven't reached the
        # timeout limit and the method hasn't cleared you to proceed to the
        # next stimulus.
        stopFlag = False
        while(stopFlag == False and timeout_counter < timeout_tries):

            # Pick random index on first day.
            index1 = random.randint(0, len(day_dicts) - 1)

            # If type is same-day,
            if type_ == 'same-day':
                # Both days are based on the start index.
                gap = 0
                index2 = index1
            # If type is different-day,
            elif type_ == 'different-day':
                # Pick a random gap distance within the gap range.
                gap = random.randint(gapRangeStart, gapRangeEnd)
                # Decide whether to subtract or add the gap to get the second
                # index, based on which is possible. If both are possible,
                # choose randomly.
                if (index1 - gap < 0) & (index1 + gap <= len(day_dicts) - 1):
                    index2 = index1 + gap
                elif (index1 + gap > len(day_dicts) - 1) & (index1 - gap >= 0):
                    index2 = index1 - gap
                elif (index1 - gap >= 0) & (index1 + gap <= len(day_dicts) - 1):
                    coin = random.randint(0, 1)
                    if coin == 0:
                        index2 = index1 + gap
                    elif coin == 1:
                        index2 = index1 - gap
            # If type is odd, pick random (but distinct) second index.
            elif type_ == 'odd':
                index2 = random.randint(0, len(day_dicts) - 1)
                gap = abs(index1 - index2)

            # Now use the indexes in random order to pick the days.
            index_set_possibilities = [[index1, index2], [index2, index1]]
            index_set = index_set_possibilities[random.randint(0, 1)]
            daydict_A = day_dicts[index_set[0]]
            daydict_B = day_dicts[index_set[1]]

            # If there AREN'T enough images in the chosen directories, abort,
            # increment the timeout counter and try again
            if type_ == 'same-day':
                minSize = 2
            elif type_ == 'different-day':
                minSize = 1
            elif type_ == 'odd':
                if index1 == index2:
                    minSize = 2
                else:
                    minSize = 1
            if not (
                    (len(daydict_A[half_day_A]) >= minSize)
                    & (len(daydict_B[half_day_B]) >= minSize)
                    ):
                timeout_counter += 1
                if timeout_counter >= timeout_tries:
                    print 'TIMED OUT!'

            # Otherwise,
            else:

                # Pop out a start and an end image.
                image_A_path = daydict_A[half_day_A].pop()
                image_B_path = daydict_B[half_day_B].pop()

                # Get the datetimes for comparison and for logs.
                datetime_for_compare_A = datetime.strptime(image_A_path[
                                                image_A_path.find("Z")-
                                                14:image_A_path.find("Z")],
                                                "%Y%m%d%H%M%S")
                datetime_for_compare_B = datetime.strptime(image_B_path[
                                                image_B_path.find("Z")-
                                                14:image_B_path.find("Z")],
                                                "%Y%m%d%H%M%S")
                datetime_for_log_A = image_A_path[
                                              image_A_path.find("Z")-
                                              14:image_A_path.find("Z")-6]
                datetime_for_log_B = image_B_path[
                                              image_B_path.find("Z")-
                                              14:image_B_path.find("Z")-6]


                # Determine which image was actually more recent
                if datetime_for_compare_A < datetime_for_compare_B:
                    AB_in_forward_order = True
                else:
                    AB_in_forward_order = False

                # Determine what the halfway point is for balancing morning/
                # afternoon bins.
                if type_ == 'same-day':
                    halfwayPoint = 4
                elif type_ == 'different-day':
                    halfwayPoint = 2
                elif type_ == 'odd':
                    halfwayPoint = leftoverHalfDayLength/4

                # Decide the order of display, so that half of the pairs are
                # shown in correct order and half are shown in reverse
                if order_counter[i%4] < halfwayPoint:
                    order = "earlier_shown_first"
                    correct = "second"
                    slog_correct_key = 'J'
                elif order_counter[i%4] >= halfwayPoint:
                    order = "later_shown_first"
                    correct = "first"
                    slog_correct_key = 'F'

                # Decide which image (A or B) is actually displayed first, based
                # on the order-shown condition and the true order of the
                # images in time.
                AB_info = {
                           'A': [image_A_path, datetime_for_log_A, half_day_A],
                           'B': [image_B_path, datetime_for_log_B, half_day_B]
                           }

                if (
                        (order == 'earlier_shown_first'
                         and AB_in_forward_order == True)
                        or
                        (order == 'later_shown_first'
                         and AB_in_forward_order == False)
                        ):

                    first_info = AB_info['A']
                    second_info = AB_info['B']

                elif (
                          (order == 'later_shown_first'
                           and AB_in_forward_order == True)
                          or
                          (order == 'earlier_shown_first'
                           and AB_in_forward_order == False)
                          ):

                    first_info = AB_info['B']
                    second_info = AB_info['A']


                # Create the dictionary for this stimulus and append it to list.
                new_dict = {
                            "first_pres":first_info[0],
                            "first_date":first_info[1],
                            "first_halfDay":first_info[2],

                            "second_pres":second_info[0],
                            "second_date":second_info[1],
                            "second_halfDay":second_info[2],

                            "gap":gap,
                            "halfDays":half_day_A+'-'+half_day_B,

                            "order":order,
                            'correct':correct,
                            "correctKey":slog_correct_key,

                            'listgen_type':type_,
                            'godModeLabel':str(gap)+'-'+half_day_A+half_day_B,
                            }
                stimuli.append(new_dict)

                # Increment the order-counter to maintain balanced design.
                order_counter[i%4] = order_counter[i%4] + 1
                # Set stopFlag to True to proceed to the next stim-pair.
                stopFlag = True

    # Report block info to the user.
    print '-', type_, '-'
    print 'stimuli length:', len(stimuli)
    print 'order counter:', order_counter

    # Return the stimuli.
    return stimuli


if __name__ == "__main__":

    generate_stim_list()
