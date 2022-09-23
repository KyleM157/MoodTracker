# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:05:50 2020

@author: KLM
"""

#Startup Code Begin
import PySimpleGUI as sg
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import itertools
import collections
import numpy as np
#Startup Code End

#Set up the GUI Format
#Menu
def create_window():
    '''
    Events and Values
        3 Possible Events
            1.Submit data to be written to file
            2.Cancel -> exits the program
            3.Plot -> Plots previous data
            4.Print Report -> Prints values in interpreter (eventually export report)
            
        Values:
            Key Value Pairs
                0:Mood Score
                1:Hours of Sleep
                2:Exercise
                3:House Cleanliness
                4:Alcohol Use
                5:SI
                :Journal Entry
            
            
    '''
    sg.theme('SandyBeach')
    
    msymptoms = [
        [sg.Text("Manic Symptoms:")],
        [sg.Checkbox("Incresed Energy",default=False)],
        [sg.Checkbox("Euphoria",default=False)],
        [sg.Checkbox("Decresed Need for Sleep",default=False)],
        [sg.Checkbox("Racing Thoughts/Distractibility",default=False)],
        [sg.Checkbox("Overly Talkative",default=False)],
        [sg.Checkbox("Risky Decisions",default=False)]
        ]
    
    dsymptoms = [
        [sg.Text("Depression Symptoms")],
        [sg.Checkbox("Loss on Interes/Pleasure",default=False)],
        [sg.Checkbox("Fatigue",default=False)],
        [sg.Checkbox("Insomnia or Hypersomnia",default=False)],
        [sg.Checkbox("Cognitive Difficulty",default=False)],
        [sg.Checkbox("Suicidal Ideation",default=False)],
        [sg.Checkbox("Agitation or Leaden Feeling",default=False)]
        ]
        
    layout = [
        [sg.Text("Mood Tracker v1.0",size=(30,1),justification='center',font=('Arial',20))],
        [sg.Text("Survey:")],
        [sg.Text("1.What is the mood today?"), sg.Slider(range=(0,100),orientation='h',default_value=50,size=(34,20))],
        [sg.Text("2.How many hours of sleep did you get last night?"),  sg.Spin(values=np.linspace(0,24,49),initial_value=8.0,size=(5,1))],
        [sg.Text("3.Did you exercise today?"),  sg.Radio('Yes','Radio2'),  sg.Radio('No','Radio2')],
        [sg.Text("4.Is the house clean?"),  sg.Slider(range=(0,100),orientation='h',default_value=50,size=(34,20))],
        [sg.Text("5.Did you drink alcohol today?"),  sg.Radio('Yes','Radio4'), sg.Radio('No','Radio4')],
        [sg.Text("6.Did you have Suicidal Ideation Today"), sg.Slider(range=(0,100),orientation='h',default_value=50,size=(34,20))],
        [sg.Text('_'*80)],
        [sg.Frame(title="Symptom Checklist",layout=[[
            sg.Column(msymptoms), sg.Column(dsymptoms)]])],
        [sg.Text('_'*80)],
        [sg.Text("Energy Level"),  sg.Slider(range=(0,100),orientation='h',size=(34,20),default_value=50)],
        [sg.Text('_'*80)],
        [sg.Text("General Comments"), sg.Multiline(default_text='',size=(50,3))],
        [sg.Submit(button_text='Submit'), sg.Button("Plot"), sg.Button("Print Report"), sg.Cancel()],
    ]
    
    window = sg.Window("mqq4",layout,default_element_size=(40,1),grab_anywhere=False)
    return(window)
    

def write_results(data):
    '''
    :type filename: str
    :param filename: path to data file
    :type data: dict
    :param data: dictionary of values obtained from survey
    
    keys:
        MS = Mood Score
        S = Hours of Sleep
        E = Exercise
        C = Home Cleanliness
        A = Alcohol Use
        SI = Suicidal ideation
        GC = General Comments
    '''
        
    dd = {}
    
    dd['MS'] = data[0]
    
    dd['S'] = data[1]
    
    if data[2] == True:
        dd['E'] = 'Y'
    else:
        dd['E'] = 'N'
    
    dd['C']=data[4] 
        
    
    if data[5] == True:
        dd['A'] = 'Y'
    else:
        dd['A'] = 'N'
    
    dd['SI'] = data[7]
        
    dd['EL'] = float(data[20])
    
    dd['GC'] = data[21].strip()
    

    #Write survey results to survey data file
    fname = r'E:/Project_Code/cdata_20200309.csv'
    current_date = datetime.today().strftime('%Y-%m-%d')
    mdata = [current_date]
    key_list = ['MS','S','E','C','A','SI','EL','GC']
    for i in range(len(key_list)):
        mdata.append(dd[key_list[i]])
    
    
    with open(fname,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(mdata)
        
    #Write symptoms results to symptom file
        
    '''
    Currently keys 11-22
    Manic symptoms: 11-16 8-13
    Depressive symptoms: 17-22 14-19
    
    Keys:
        M1 = Increased Energy
        M2 = Euphoria
        M3 = Decreased Need for Sleep
        M4 = Racing Thoughts/Distractibility
        M5 = Overly Talkative
        M6 = Risky Decisions
        
        D1 = Loss of Intrest/Pleasure
        D2 = Fatigue
        D3 = Insomnia/Hypersomnia
        D4 = Cognitive Difficulty
        D5 = Suicidal Ideation
        D6 = Agitation/Leaden Feeling
    '''    

    sfname = r'E:/Project_Code/sdata_20200303.csv'
    sdata = [current_date]
    sdict = {'11':'Increased Energy','12':'Euphoria','13':'Decreased Need for Sleep',
             '14':'Racing Thoughts/Distractibility','15':'Overly Talkative','16':'Risky Decisions',
             '17':'Loss of Interest/Pleasure','18':'Fatigue','19':'Insomnia/Hypersomnia','20':'Cognitive Difficulty',
             '21':'Suicidal Ideation','22':'Agitation/Leaden Feeling'}
    
    for i in range(8,20):
        if data[i]==True:
            sdata.append(sdict[str(i)])
        else:
            pass
        
    with open(sfname,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(sdata)
            
def get_scores(data):
    '''
    :type data: nested list
    :param data: data from file
    form: [date,score,sleep,exercise,cleanliness,alcohol,si,journal]
    '''
    #Change the depressed scores first (I prefer doing two passes of the data for the time being)
    for i in range(len(data)):
        x = data[i]
        score = int(x[1])
        if x[6]=='Y':
            score-=1
        else:
            pass
        data[i][1] = score
        
        
    #For hypo get all of the sleep values in a string
    temp=[]
    for x in data:
        score,sleep = int(x[1]),float(x[2])
        if score==1 and sleep<6:
            x[2] = 1
        else:
            x[2]=0
        temp.append(x)
        
    #Creates a list of data where possible hypo sleep is a 1 and other values are set to 0
    s_list = [int(x[2]) for x in temp]
    s_string = ''.join(str(x) for x in s_list)
    
    #Seperate the values using a split command
    #Possible hypo =1 else =0 -> split on 0
    ph = s_string.split('0')
    indexes = [x for x in range(len(ph)) if ph[x]!='']
    
    #Now check length of each index. If length is 4 or above get all of the indexes
    i_list = []
    for i in indexes:
        if len(ph[i])>=4:
            total=len(ph[i])
            i_list.extend([x for x in range(i,(i+total))])
        else:
            pass
            
    #Modify scores at given index
    for i in i_list:
        data[i][1] = int(data[i][1])+1  #Generalized if I ever choose to go above that score
        
    return(data)



def scatter_plot(x,y,title):
    
    plt.scatter(x,y,c='b')
    plt.plot(x,y,c='k')
    #fmt = mdates.AutoDateFormatter('%Y-%m')
    plt.title(title)
    plt.grid(True)
    plt.xlabel('Days')
    plt.ylabel('Mood Score')
    #plt.gca().xaxis.set_major_formatter(fmt)
    #plt.gcf().xaxis.auto_fmt_xdate()
    plt.yticks([-1,0,1,2],['SD','D','E','H'])
    plt.show()
            
def plot_bp(data):
    '''
    The plotting portion for MAOI management.
    Blood pressure readings take the form of systolic/diastolic (120/80)
    
    ***Keys Must Be As Follows***
    sitting
    standing1
    standing2
    
    ***Values Must be in the Form (Systolic,Diastolic)***
    
    :type data: dict -> {sitting:[(systolic,diastolic)],standing1:[()],standing2:[()]}
    '''
    #Seperate the data based on sitting and standing
    sitting_data = data['sitting']
    standing1_data = data['standing1']
    standing2_data = data['standing2']
    
    sitting_s = [x[0] for x in sitting_data]
    sitting_d = [x[1] for x in sitting_data]
    
    standing1_s = [x[0] for x in standing1_data]
    standing1_d = [x[1] for x in standing1_data]
    
    standing2_s = [x[0] for x in standing2_data]
    standing2_d = [x[1] for x in standing2_data]
    
    
    total = len(sitting_s)  #Total number of days
    xlabels = [str(x) for x in range(total)]
    
    x = np.arange(0,(total*2),step=2)   #set x axis loctions for bars
    w=0.4   #Bar width
    
    #Graph stuff
    fig,ax = plt.subplots()
    r_sitting_s = ax.bar(x,sitting_s,width=w,align='edge',color='c')
    r_sitting_d = ax.bar(x,sitting_d,width=w,align='edge',color='r')
    
    r_standing1_s = ax.bar(x+.5,standing1_s,width=w,align='edge',color='g')
    r_standing1_d = ax.bar(x+.5,standing1_d,width=w,align='edge',color='r')
    
    r_standing2_s = ax.bar(x+1,standing2_s,width=w,align='edge',color='y')
    r_standing2_d = ax.bar(x+1,standing2_d,width=w,align='edge',color='r')
    
    ax.set_ylabel("mmHg")
    ax.set_xlabel("Days")
    ax.set_title("Blood Pressure Chart")
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    ax.set_ylim(0,200,20)
    ax.set_yticks([x for x in range(0,220,20)])
    
    ax.legend((r_sitting_s[0],r_standing1_s[0],r_standing2_s[0]),
              ("Sitting","1st Standing","2nd Standing"),loc='upper right')

    rects = [r_sitting_s,r_sitting_d,r_standing1_s,r_standing1_d,r_standing2_s,r_standing2_d]
   
    for rect in rects:
        for r in rect:
            h = r.get_height()
            ax.annotate('{}'.format(h),xy=(r.get_x()+r.get_width()/2,h),
                        xytext=(0,3),textcoords='offset points',ha='center',va='bottom')
    
    plt.show()
    


def main():
    
    while True:
        #Load data
        fname = r'E:/Project_Code/cdata_20200303'
        with open(fname,'r') as f:
            reader = csv.reader(f)
            d = []
            for row in reader:
                d.append(row)
                
        #Create GUI
        window = create_window()
        event,values=window.read()
        
        if event in [None,'Cancel']:
            break
            
        elif event=='Submit':
            if datetime.today().strftime('%Y-%m-%d') == d[-1][0]:
                sg.popup("You already submitted data for the day!")
                window.close()
                
            else:
                
                write_results(values)
               
    
                # sg.popup('Title',
                #           'The results of the window.',
                #           'The button clicked was "{}"'.format(event),
                #           'The values are',values)
                
                window.close()
                
                
        elif event=='Plot':
            window.close()
            
                    
            scores=[int(x[1]) for x in get_scores(d)]
            
            #Create new window to get data range form user
            
            
            sg.theme('SandyBeach')
            layout = [
                [sg.Text("Please Choose an Option Below")],
                [sg.Checkbox("All Data",key='AD')],
                [sg.Checkbox("Past Year",key='PY')],
                [sg.Checkbox("Past Tertile",key='PT')],
                [sg.Button("Plot"), sg.Cancel()]
                ]
               
                
            
            pwindow = sg.Window(title="Plot Function",layout=layout,grab_anywhere=False)
            e2,v2 = pwindow.read()
            
            if e2 in [None,'Cancel']:
                pwindow.close()
            else:
                if v2['AD'] == True:
                    y=scores
                    x=[x for x in range(len(y))]
                    t1,t2 = d[0][0],d[-1][0]
                    scatter_plot(x,y,"All Data ({}:{})".format(t1,t2))
    
                elif v2['PY'] == True:
                    try:
                        y = scores[-365:]
                        x = [x for x in range(len(y))]
                        t1,t2 = d[-365][0],d[-1][0]
                        scatter_plot(x,y,"Pasy Year ({}:{})".format(t1,t2))
                    except IndexError:
                        print("Not Enough Data Yet, Plotting All Data")
                        y=scores
                        x=[x for x in range(len(y))]
                        t1,t2 = d[0][0],d[-1][0]
                        scatter_plot(x,y,"All Data ({}:{})".format(t1,t2))
    
                elif v2['PT'] == True:
                    try:
                        y=scores[-120:]
                        x=[x for x in range(len(y))]
                        t1,t2 = d[-120][0],d[-1][0]
                        scatter_plot(x,y,"Past Tertile ({}:{})".format(t1,t2))
                    except IndexError:
                           print("Not Enough Data Yet, Plotting All Data")
                           y=scores
                           x=[x for x in range(len(y))]
                           t1,t2 = d[0][0],d[-1][0]
                           scatter_plot(x,y,"All Data ({}:{}".format(t1,t2))
                else:
                    print("Something went wrong")
                
                pwindow.close()
            
                
        elif event == 'Print Report':
            
            #Create Window to get Time Range
            window.close()
            
            rlayout = [
                [sg.Text(text='Number of Months'), sg.Spin(values=[x for x in range(7)],initial_value=1)],
                [sg.Submit(), sg.Cancel()]
                ]
            
            report_window = sg.Window("Time Range",layout=rlayout)
            r_event,r_value=report_window.read()
            
            if r_event in [None,'Cancel']:
                pass
            else:
                tr = int(r_value[0])    #range of time given by user
            
            report_window.close()


            scores = [int(x[1]) for x in get_scores(d)]
            h = len([x for x in scores if x>1])
            e = len([x for x  in scores if x==1])
            d = len([x for x in scores if x<1])
            total = len(scores)
            
            #Get global percentages
            hp,ep,dp = (h/total)*100.,(e/total)*100.,(d/total)*100.
            
            #Get past months scores
            #Going to assume month = 30 days
            nd = 30*tr
            mh = len([x for x in scores[-nd:] if x>1])
            me = len([x for x  in scores[-nd:] if x==1])
            md = len([x for x in scores[-nd:] if x<1])
            total = nd
            
            mhp,mep,mdp = (mh/total)*100.,(me/total)*100.,(md/total)*100.
            
            print("Mood Report")
            print("\nGlobal Percentages\n")
            print("Time spent hypo: {}".format(hp))
            print("Time spent euthymic: {}".format(ep))
            print("Time spent depressed: {}".format(dp))
            print("\n\nLast Month\n")
            print("Time spent hypo: {}".format(mhp))
            print("Time spent euthymic: {}".format(mep))
            print("Time spent depressed: {}".format(mdp))
            
            #Load symptom list
            #Format is date then symptoms in a csv file
            s_fname = r'E:/Project_Code/sdata_20200303.csv'
            with open(s_fname,'r') as f:
                reader=csv.reader(f)
                sdata=[]
                for row in reader:
                    sdata.append(row)
                    
            #Get All Symptoms
            if len(sdata)<tr:
                slist = list(itertools.chain.from_iterable([x[1:] for x in sdata]))
                scounter = collections.Counter(slist)
                mc = scounter.most_common()
                if tr==1:
                    print("Most Common Symptoms Over the Past Month")
                else:
                    print("Most Common Symptoms Over the Past {} Months\n".format(tr))
                    
                for x in mc:
                    print("{}: {}".format(x[0],x[1]))
                    
            else:
                print("Not Enough Data")
                
        else:
            sg.popup("Something went very wrong")

    window.close()
    
    
    
if __name__=='__main__':
    main()
