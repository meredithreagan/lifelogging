#randomly presenting the images from the directory (196 - sae that we used for the Judgment of Recency)
#present the picture on the top of hte screen
import glob
import random
from smile.common import *




#need to change this directory to the directory on cmlab with the photos for each participant
data_dir = "/Users/meredithreagan/Documents/SMILE_MAIN/my_experiment/pics/*"



#put the pictures form the directory into a list
gen = []
for x in glob.glob(data_dir):
    m = glob.glob(x+"/morning/*")
    for i in m:
        gen.append(i)
    a= glob.glob(x+"/afternoon/*")
    for i in a:
        gen.append(i)


#create the stimuli from the lsit
imgstim=[]
random.shuffle(gen)
for i in range(0,len(gen)):
    imgstim.append({'stim':gen[i-1],'dur':30,'trial_num':i+1})
print imgstim

#read in the instructions
instruct_text = open('timelineinstructions.rst', 'r').read()


#length of the slider
slider_width=1320


exp=Experiment()

#open the instructions
init_text = RstDocument(text=instruct_text, width=900, font_size=50, top=exp.screen.top, height=exp.screen.height)
with UntilDone():
    KeyPress(keys=['ENTER'])


Wait(2)
with Loop(imgstim) as trial:
    with Parallel():
        img = Image(source=trial.current['stim'], duration=trial.current['dur'], top=exp.screen.top+5, trial_num=trial.current['trial_num'])

    with UntilDone():
        with Serial():
            with Parallel():

                MouseCursor()
                s1 = Slider(min=0, max=3, value=1.5, width=slider_width, top=400, padding=0)
                week0=Rectangle(color='white', top=375, width=1, height=50, center_x=s1.left)
                week1 = Rectangle(color='white', top=375, width=1, height=50, center_x=week0.center_x+(slider_width/(3)))
                week2 = Rectangle(color='white', top=375, width=1, height=50, center_x=week1.center_x+(slider_width/(3)))
                week3 = Rectangle(color="white", top=375, width=1, height=50, center_x=week2.center_x+(slider_width/3))
                lblw1 = Label(text="Week 1", center_x=(s1.left)+slider_width/(6), top=340)
                lblw2 = Label(text="Week 2", center_x=((lblw1.center_x)+slider_width/(3)), top=340)
                lblw3 = Label (text="Week 3", center_x=((lblw2.center_x)+slider_width/(3)), top=340)
                mbs1=MouseButton(widget=s1)
            with UntilDone():
                Wait(until=mbs1)
                s1.disabled = True

                with Parallel():
                    line1=Rectangle(color='red', top=350, width=slider_width, height=1, center_x=s1.center_x,)
                    MouseCursor()
                    s2 = Slider(min=0, max=7, value=3.5, width=slider_width, top=300,padding=0)
                    day0=Rectangle(color='white', top=275, width=1, height=50, center_x=s2.left)
                    day1=Rectangle(color='white', top=275, width=1, height=50, center_x=day0.center_x+(slider_width/(7)))
                    day2=Rectangle(color='white', top=275, width=1, height=50, center_x=day1.center_x+(slider_width/(7)))
                    day3=Rectangle(color='white', top=275, width=1, height=50, center_x=day2.center_x+(slider_width/(7)))
                    day4=Rectangle(color='white', top=275, width=1, height=50, center_x=day3.center_x+(slider_width/(7)))
                    day5=Rectangle(color='white', top=275, width=1, height=50, center_x=day4.center_x+(slider_width/(7)))
                    day6=Rectangle(color='white', top=275, width=1, height=50, center_x=day5.center_x+(slider_width/(7)))
                    day7 = Rectangle(color="white", top=275, width=1, height=50, center_x=s1.right)
                    lblM = Label(text="Monday", center_x=(s2.left)+slider_width/(14), top=240)
                    lblT = Label(text="Tuesday", center_x=((lblM.center_x)+slider_width/(7)), top=240)
                    lblW = Label(text="Wednesday", center_x=((lblT.center_x)+slider_width/(7)), top=240)
                    lblTh = Label(text="Thursday", center_x=((lblW.center_x)+slider_width/(7)), top=240)
                    lblF = Label(text="Friday", center_x=((lblTh.center_x)+slider_width/(7)), top=240)
                    lblSa = Label(text="Saturday", center_x=((lblF.center_x)+slider_width/(7)), top=240)
                    lblSu = Label(text="Sunday", center_x=((lblSa.center_x)+slider_width/(7)), top=240)
                    mbs2=MouseButton(widget=s2)
                with UntilDone():
                    Wait(until=mbs2)
                    s2.disabled = True
                    with Parallel():
                        line2=Rectangle(color='red', top=250, width=slider_width, height=1, center_x=s2.center_x)
                        MouseCursor()
                        s3 = Slider(min=0, max=24, value=12, width=slider_width, top=200, padding=0)
                        hour0=Rectangle(color='white', top=175, width=2, height=50, center_x=s3.left)
                        hour1=Rectangle(color='white', top=175, width=2, height=50, center_x=hour0.center_x+(slider_width/(24)))
                        hour2=Rectangle(color='white', top=175, width=2, height=50, center_x=hour1.center_x+(slider_width/(24)))
                        hour3=Rectangle(color='white', top=175, width=2, height=50, center_x=hour2.center_x+(slider_width/(24)))
                        hour4=Rectangle(color='white', top=175, width=2, height=50, center_x=hour3.center_x+(slider_width/(24)))
                        hour5=Rectangle(color='white', top=175, width=2, height=50, center_x=hour4.center_x+(slider_width/(24)))
                        hour6=Rectangle(color='white', top=175, width=2, height=50, center_x=hour5.center_x+(slider_width/(24)))
                        hour7=Rectangle(color='white', top=175, width=2, height=50, center_x=hour6.center_x+(slider_width/(24)))
                        hour8=Rectangle(color='white', top=175, width=2, height=50, center_x=hour7.center_x+(slider_width/(24)))
                        hour9=Rectangle(color='white', top=175, width=2, height=50, center_x=hour8.center_x+(slider_width/(24)))
                        hour10=Rectangle(color='white', top=175, width=2, height=50, center_x=hour9.center_x+(slider_width/(24)))
                        hour11=Rectangle(color='white', top=175, width=2, height=50, center_x=hour10.center_x+(slider_width/(24)))
                        hour12=Rectangle(color='white', top=175, width=2, height=50, center_x=hour11.center_x+(slider_width/(24)))
                        hour13=Rectangle(color='white', top=175, width=2, height=50, center_x=hour12.center_x+(slider_width/(24)))
                        hour14=Rectangle(color='white', top=175, width=2, height=50, center_x=hour13.center_x+(slider_width/(24)))
                        hour15=Rectangle(color='white', top=175, width=2, height=50, center_x=hour14.center_x+(slider_width/(24)))
                        hour16=Rectangle(color='white', top=175, width=2, height=50, center_x=hour15.center_x+(slider_width/(24)))
                        hour17=Rectangle(color='white', top=175, width=2, height=50, center_x=hour16.center_x+(slider_width/(24)))
                        hour18=Rectangle(color='white', top=175, width=2, height=50, center_x=hour17.center_x+(slider_width/(24)))
                        hour19=Rectangle(color='white', top=175, width=2, height=50, center_x=hour18.center_x+(slider_width/(24)))
                        hour20=Rectangle(color='white', top=175, width=2, height=50, center_x=hour19.center_x+(slider_width/(24)))
                        hour21=Rectangle(color='white', top=175, width=2, height=50, center_x=hour20.center_x+(slider_width/(24)))
                        hour22=Rectangle(color='white', top=175, width=2, height=50, center_x=hour21.center_x+(slider_width/(24)))
                        hour23=Rectangle(color='white', top=175, width=2, height=50, center_x=hour22.center_x+(slider_width/(24)))
                        hour24=Rectangle(color='white', top=175, width=2, height=50, center_x=hour23.center_x+(slider_width/(24)))
                        hour25 = Rectangle(color="white", top=375, width=2, height=50, center_x=s1.right)

                        lbl6a = Label(text="6a", center_x=s3.left, top=120)
                        lbl7a = Label(text="7a", center_x=((lbl6a.center_x)+slider_width/(24)), top=120)
                        lbl8a = Label(text="8a", center_x=((lbl7a.center_x)+slider_width/(24)), top=120)
                        lbl9a = Label(text="9a", center_x=((lbl8a.center_x)+slider_width/(24)), top=120)
                        lbl10a = Label(text="10a", center_x=((lbl9a.center_x)+slider_width/(24)), top=120)
                        lbl11a = Label(text="11a", center_x=((lbl10a.center_x)+slider_width/(24)), top=120)
                        lbl12p= Label(text="12p", center_x=((lbl11a.center_x)+slider_width/(24)), top=120)
                        lbl1p = Label(text="1p", center_x=((lbl12p.center_x)+slider_width/(24)), top=120)
                        lbl2p = Label(text="2p", center_x=((lbl1p.center_x)+slider_width/(24)), top=120)
                        lbl3p = Label(text="3p", center_x=((lbl2p.center_x)+slider_width/(24)), top=120)
                        lbl4p = Label(text="4p", center_x=((lbl3p.center_x)+slider_width/(24)), top=120)
                        lbl5p = Label(text="5p", center_x=((lbl4p.center_x)+slider_width/(24)), top=120)
                        lbl6p = Label(text="6p", center_x=((lbl5p.center_x)+slider_width/(24)), top=120)
                        lbl7p= Label(text="7p", center_x=((lbl6p.center_x)+slider_width/(24)), top=120)
                        lbl8p = Label(text="8p", center_x=((lbl7p.center_x)+slider_width/(24)), top=120)
                        lbl9p = Label(text="9p", center_x=((lbl8p.center_x)+slider_width/(24)), top=120)
                        lbl10p = Label(text="10p", center_x=((lbl9p.center_x)+slider_width/(24)), top=120)
                        lbl11p = Label(text="11p", center_x=((lbl10p.center_x)+slider_width/(24)), top=120)
                        lbl12a = Label(text="12p", center_x=((lbl11p.center_x)+slider_width/(24)), top=120)
                        lbl1a = Label(text="1a", center_x=((lbl12a.center_x)+slider_width/(24)), top=120)
                        lbl2a= Label(text="2a", center_x=((lbl1a.center_x)+slider_width/(24)), top=120)
                        lbl3a = Label(text="2a", center_x=((lbl2a.center_x)+slider_width/(24)), top=120)
                        lbl4a = Label(text="4a", center_x=((lbl3a.center_x)+slider_width/(24)), top=120)
                        lbl5a = Label(text="5a", center_x=((lbl4a.center_x)+slider_width/(24)), top=120)
                        lbl6a2= Label(text="6a", center_x=s3.right, top=120)
                        mbs3=MouseButton(widget=s3)
                    with UntilDone():
                        Wait(until=mbs3)
                        s3.disabled = True
                        with Parallel():
                            line3=Rectangle(color='red', top=150, width=slider_width, height=1, center_x=s3.center_x)
                            MouseCursor()
                            s4 = Slider(min=0, max=10, value=5, width=slider_width, top=100, padding=0)
                            #conf0=Rectangle(color='white', top=75, width=2, height=50, center_x=s4.left+100)
                            #conf1=Rectangle(color="white", top=75, width=2, height=50, center_x=s4.right-100)
                            lblvconf = Label(text="<--- Not at all confident", center_x=s4.left+100, top=40)
                            lblnotconf = Label(text="Very confident --->", center_x=s4.right-100, top=40)
                            mbs4=MouseButton(widget=s4)
                        with UntilDone():
                            Wait(until=mbs4)
                            s4.disabled = True
                            Wait(1)


    Log(name="timeline",
                block_num="",
                trial_num=trial.current['trial_num'],
                trial_abs="",
                stim_image=trial.current['stim'],
                value_chosen_1=s1.value,
                value_chosen_2=s2.value,
                value_chosen_3=s3.value,
                value_chosen_4=s4.value,
                stim_appear_time="",
                value_1_time="",
                value_2_time="",
                value_3_time="",
                value_4_time="")


exp.run()
