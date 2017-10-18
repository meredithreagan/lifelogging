
"""
Listgen v4
"""

# %%
import os
import numpy as np
import pandas as pd
import itertools as it
from glob import glob
import random
import copy
import pickle
from datetime import datetime, timedelta
from dateutil import tz

# %%

class Listgen:
    def __init__(self):
        subject = 'sub'
        #path = path to folder containing folders of different subjects
        path = os.getcwd() + '/images/*'
        days = glob(path)  # list of days for each subject
        self.gen = [] # list containing a dictionary for every day
        frame_list = []

        for day in days:
            x = glob(day+'/morning/*')  #list of morning images
            y = glob(day+'/afternoon/*')  #list of afternoon images
            # setting 'day' key = 0 for now
            for pic in x:
                frame_list.append(
                    {'subject': subject,
                     'time': 'morning',
                     'path': pic,
                     'used': False}
                )
            for pic in y:
                frame_list.append(
                    {'subject': subject,
                     'time': 'afternoon',
                     'path': pic,
                     'used': False}
                )
        # create a DataFrame in which every row is one image
        self.frame = pd.DataFrame(frame_list)
        '''Use this if you already have the pickle file
        with open('self_frame008.pickle', 'rb') as f:
            frame = pickle.load(f)
        self.frame = pd.DataFrame(frame)'''

        self.list_of_days = []
        # converting zulu time to EST
        self.frame['zulu'] = 0    # create column of filler values
        self.frame['zulu_int'] = 0
        #self.frame['est'] = 0
        self.frame['date'] = 0
        self.frame['used'] = False
        for index, row in self.frame.iterrows():
            first = row['path']
            x = first.split('Z')
            self.frame.loc[index,'zulu'] = x[0][-14:]
            self.frame.loc[index,'zulu_int'] = int(x[0][-14:])
            est = self.convert_to_est(x[0][-14:],'UTC','%Y%m%d%H%M%S')
            self.frame.loc[index,'date'] = est.date()
            if est.date() not in self.list_of_days:
                self.list_of_days.append(est.date())

        # sort the reference frame so that the indices are in chronological
        # order
        self.frame.sort_values('zulu_int')

        # save reference frame
        fl = pd.DataFrame.to_dict(self.frame)
        with open('self_frame.pickle', 'wb') as f:
            pickle.dump(fl, f, pickle.HIGHEST_PROTOCOL)

        # conditions: time ranges between images in pairs
        self.conditions = [[0,0], [1,1], [2,3], [4,6],
                      [7,7], [8,12], [13,18]]
        num_conditions = len(self.conditions)
        time_day_combos = 3 # morningxmorn, afternoonxaft, mornxaft
        pair_balancing = 2
        #self.loop_range = ((self.number_of_images/pair_balancing)/2)/num_conditions
        self.loop_range = 6

    def convert_to_est(self, datetime_, starting_timezone, date_format):
        # Timezone converter, since Unforgettable.me datetimes are in Zulu time.
        # Timezones:
        from_zone = tz.gettz(starting_timezone)
        to_zone = tz.gettz('America/New_York')
        # utc = datetime.utcnow()
        utc = datetime.strptime(datetime_, date_format)
        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone.
        eastern = utc.astimezone(to_zone)
        return eastern

    def pair_selector(self, condition):
        # first check to see if any images are available for the
        #   condition in question
        day_l = self.list_of_days
        random.shuffle(day_l)
        # create a key to determine if we succeeded in finding another
        #   day that contains unused images
        day_mod = 'none'
        new_date = 'none'
        for day in day_l:
            if sum(condition) == 0:
                if len(self.day_frame[(self.day_frame.date==(day))&
                             (self.day_frame.used!=True)]) < 2 and new_date == 'none':
                    break
                else:
                    new_date = day
                    day_mod = day
                    break
            elif sum(condition) != 0:
                if len(self.day_frame[(self.day_frame.date==(day))&
                                 (self.day_frame.used!=True)]) == 0 and new_date == 'none':
                    continue
                elif len(self.day_frame[(self.day_frame.date==(day))&
                                 (self.day_frame.used!=True)]) != 0 and new_date == 'none':
                    # create a list of values based upon the condition that will
                    #   determine how far forward or backward we pick another day
                    time_skip = []
                    for i in range(condition[0],condition[1]+1):
                        time_skip.append(i)
                        time_skip.append(i*-1)
                    random.shuffle(time_skip)
                    # now loop through the list
                    ts_flag = False
                    for ts in time_skip:
                        if ts_flag == False:
                            next_day = timedelta(days=ts) + day
                            if len(self.day_frame[(self.day_frame.date==(next_day))&
                                             (self.day_frame.used!=True)]) != 0:
                                new_date = next_day
                                ts_flag = True
                                day_mod = day
                            else:
                                print 'time_skip',ts
                        else:
                            break
            elif new_date != 'none':
                break
        # now we pick the pair of images, if possible. Otherwise we pick
        #   a different day
        if new_date == 'none':
            pair = ['null']
            return pair
        else:
            # get indices of images for first part of condition
            day_0_inds = self.day_frame[(self.day_frame.date==day_mod)&
                             (self.day_frame.used!=True)].index.values.tolist()
            # pick random image from list of day_frame indices
            image_0 = random.choice(day_0_inds)
            # mark this image as used from the day_frame
            self.day_frame.loc[image_0,'used'] = True

            # get indices of images for second part of condition
            day_1_inds = self.day_frame[(self.day_frame.date==new_date)&
                             (self.day_frame.used!=True)].index.values.tolist()
            # pick random image from list of day_frame indices
            image_1 = random.choice(day_1_inds)
            # mark these images as used from the day_frame
            self.day_frame.loc[image_1,'used'] = True
            # now return the pair always in chronological order. This is
            #   balanced later
            Img0 = self.day_frame['zulu_int'][image_0]
            Img1 = self.day_frame['zulu_int'][image_1]
            if Img0 < Img1:
                img_pair = [self.day_frame['path'][image_0],
                            self.day_frame['path'][image_1]]
                time_in_day = [self.day_frame['time'][image_0],
                               self.day_frame['time'][image_1]]
                zulu_time = [self.day_frame['zulu_int'][image_0],
                               self.day_frame['zulu_int'][image_1]]
                dates = [self.day_frame['date'][image_0],
                               self.day_frame['date'][image_1]]
                correct_key = 'J'
            elif Img1 < Img0:
                img_pair = [self.day_frame['path'][image_1],
                            self.day_frame['path'][image_0]]
                time_in_day = [self.day_frame['time'][image_1],
                               self.day_frame['time'][image_0]]
                zulu_time = [self.day_frame['zulu_int'][image_1],
                               self.day_frame['zulu_int'][image_0]]
                dates = [self.day_frame['date'][image_1],
                               self.day_frame['date'][image_0]]
                correct_key = 'F'

            pair = {'pair': img_pair,
                    'condition': condition,
                    'time': time_in_day,
                    'first_pres': img_pair[0],
                    'second_pres': img_pair[1],
                    'dates': dates,
                    'first_date': dates[0],
                    'second_date': dates[1],
                    'zulu_int': zulu_time,
                    'correct_key': correct_key,
                    'order': 'forward'}
            return pair

    def generate(self):
        # attempt to get a full list 1000 times
        break_point = False
        for attempt in range(1000):
            if break_point == False:
                print 'attempt', attempt
                self.day_frame = copy.deepcopy(self.frame)
                self.stimuli_list = []  # list to which we will append pairs
                for i in range(self.loop_range):
                    conditions = self.conditions
                    random.shuffle(conditions)
                    for condition in conditions:
                        pairs = []
                        for pair_number in range(2):
                            pair = self.pair_selector(condition)
                            if pair == ['null']:
                                continue
                            else:
                                #reverse order of second pair
                                if pair_number == 1:
                                    pair['pair'].reverse()
                                    pair['time'].reverse()
                                    pair['zulu_int'].reverse()
                                    pair['dates'].reverse()
                                    pair['order'] = 'reverse'
                                else:
                                    pass
                                pairs.append(pair)
                        if len(pairs) < 2:
                            # mark image as unused so that it can be used again
                            if len(pairs) == 0:
                                continue
                            else:
                                # Restore images in pair to being unused
                                pic_path_0 = pairs[0]['pair'][0]
                                pic_path_1 = pairs[0]['pair'][1]
                                x = self.day_frame.index[self.day_frame['path'] == pic_path_0].tolist()
                                self.day_frame.loc[x[0],'used'] = False
                                y = self.day_frame.index[self.day_frame['path'] == pic_path_1].tolist()
                                self.day_frame.loc[y[0],'used'] = False
                        else:
                            for pair in pairs:
                                self.stimuli_list.append(pair)
                            if len(self.stimuli_list) == 84:
                                break_point = True

        if len(self.stimuli_list) < 84:
            print 'WARNING: Only {} pairs found'.format(str(len(self.stimuli_list)))
            proceed = input('Proceed with current list? [y] or [n]')
            if proceed == 'y':
                with open('short_list.pickle', 'wb') as f:
                    pickle.dump(self.stimuli_list, f, pickle.HIGHEST_PROTOCOL)
                return self.stimuli_list
            else:
                print 'LISTGEN TERMINATED.'
        else:
            with open('stimuli.pickle', 'wb') as f:
                pickle.dump(self.stimuli_list, f, pickle.HIGHEST_PROTOCOL)
            print 'Success'
            return self.stimuli_list


# %%
x = Listgen()
x.generate()

# %%
'''
To execute, change the line 16 `path` to the subject's folder containing
the folders for each day
________________________________________________________________________________
Summary:

The listgen operates by referencing a DataFrame called `self.frame`. Every row
in this frame is one image with information about what day and what time of day
the image came from, as well as the image's path. Currently, the listgen will
make 1000 attempts to find a combination of image pairs that meet our criteria,
being the following (listed by highest to lowest priority):
1) Equal number of chronologically ordered and reversed pairs of images
2) TRY to get an equal number of pairs for each time range.
        NOTE: Currently, in the event that the listgen cannot find any suitable
        pairs for a time range, it will move on to another condition that works.
        It will keep making pairs untilthe specified number of pairs has been
        made.
The listgen currently does NOT make any attempt to balance the number of
morningxmorning, afternoonxafternoon, and morningxafternoon pairs.  This can be
added in later, if necessary, but will likely result in many failures, as issues
will arise do to participants having varying amounts of images on each day and
for each time of day.

The listgen makes a deep copy of `self.frame` called `self.day_frame` at the
onset of every attempt.  This is critical for making sure that every attempt has
a blank slate.  It is important to note that the frame also contains a column
called "used": Once an image is used, it's corresponding row in `self.day_frame`
is changed from False to True, and it will not be used again.

This listgen works by first having a list of the different conditions in the
form of pairs, such as [0,0] or [13,18]. These condition pairs represent the
range of days in the condtion, so [0,0] would be a range of 0 days, meaning the
selected pair of images must be from the same day.  The [13,18] means there is a
range of + or - 13 to 18 days away from an image that is selected randomly. In
practice, the listgen scrambles the list of condition ranges, selects a
condition range, then scrambles the list of days. It will loop through every
day, checking to see if that day has any unused images, then loop through a list
of days that are within the specified time range both in the forward and
backwards direction.  The second day that is chosen is randomly selected. In the
event that a second day has unused images, the pair is selected. The listgen
will find two pairs of images for each time range, with one of the pairs being
chronologically forward and the other backwards. In the event that there is only
one pair found for a condition, the listgen will NOT use that single pair and
mark the pair that was selected back to being 'unused'. Then, the listgen will
move on to a different condition.

In the event that 1000 attempts have been made and there is no list of stimuli
with enough pairs, a warning will appear and a prompt will ask if you still want
to save the file, with the file being called 'short_list.pickle' and return
the stimuli_list.

Information about each pair isgathered as well, including each image's time of
day. All this informaiton is saved in the form of a list of dictionaries within
a pickle file. For analysis, run the following lines to load in the pickle file
and interact with it as a DataFrame.
----------
with open('stimuli.pickle', 'rb') as f:
    df = pickle.load(f)
df = pd.DataFrame(df)
----------

'''
