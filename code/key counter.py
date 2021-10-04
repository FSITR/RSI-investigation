import keyboard as kb
from time import sleep
import datetime
import pandas as pd
import os

#Command line interaction and parameter setting
###############################################################################
hours=float(input('Enter the recording time frame, in hours:\n'))
recording_time_frame=60*60*hours#conversion to seconds
recording_split=3#seconds

start=datetime.datetime.now()
end=start+datetime.timedelta(seconds=recording_time_frame)

print('\nRecording frequency:\t',str(recording_split),'seconds')
print('Start time:\t\t',str(start.time())[:5])
print('End time:\t\t',str(end.time())[:5],'\n')
print('***key counting in progress***\n')

#define function for counting the number of recorded keys
###############################################################################
def count_kb_objects_by_keyword(recorded,keyword,delim):
    keys=[]
    recorded_list=list(map(str,recorded))#convert list of keyboard objects to strings
    for i in range(len(recorded_list)):
        keyword_found = recorded_list[i].find(keyword)#find keyword, will return index if true, -1 if false
        letter_index = recorded_list[i].find(delim)+1#find index of delimitter then +1 to find letter index
        recorded_list[0].find(' ')
        if keyword_found > 0:#if keyword was found then add to list
            letter = recorded_list[i][letter_index:recorded_list[i].find(' ')]
            keys.append(letter)
    return(len(keys))

#Key recording
###############################################################################
ALL_key_stroke_rates=[]
runs=int(recording_time_frame/recording_split)
for i in range(runs):
    key_stroke_rate=[]#per unit time defined

    #Record key strokes in given timeframe
    kb.start_recording()
    sleep(recording_split)
    recorded = kb.stop_recording()

    #Get hour and minute
    t = str(datetime.datetime.now().time())[:5]
    d = str(datetime.datetime.now().date())

    #store date, time and key stroke rate
    key_stroke_rate=[d,t,count_kb_objects_by_keyword(recorded,'down','(')]
    ALL_key_stroke_rates.append(key_stroke_rate)

#Data conversion, storage and graphing
###############################################################################

#convert data to Pandas dataframe
df=pd.DataFrame.from_records(ALL_key_stroke_rates,columns=['date','time','frequency'])
total_keys_pressed=df['frequency'].sum()
print(str(total_keys_pressed),"keys pressed in",str(recording_time_frame),"seconds")

#save dataframe as .csv
##filepath=r'C:\Users\Jbuck.ad\Documents\WIP\python\RSI'
##files=os.listdir(filepath)
##files_dates=[]
##for i in files:
##	files_dates.append(i[:files[0].find('_')])
##file_count=str(1+files_dates.count(d))
##filename=d+'_keystrokes_'+file_count+'.csv'
##path=os.path.join(filepath,filename)
##df.to_csv(path)

filepath=r'C:\Users\Jbuck.ad\Documents\WIP\python\RSI'
files=os.listdir(filepath)
file_dates = [i.split('_')[0] for i in files if '.csv' in i]
file_count= str(1+file_dates.count(d))
filename=d+'_keystrokes_'+file_count+'.csv'
path=os.path.join(filepath,filename)
df.to_csv(path)

#option to show graph after counting has finished
show_graph=input("show graph? (y/n)\n")
if show_graph == 'y':
    for i in range(1):
            import matplotlib.pyplot as plt
            cumsum=df['frequency'].cumsum()
            cumsum_upper=df['frequency'].clip(upper=20).cumsum()
            cumsum.plot()
            cumsum_upper.plot()
            plt.show()


#plot
#measure in CPM, characters per minute
#count spaces for approximate word count
#count backspaces
