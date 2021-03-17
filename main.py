#!/usr/bin/env python
from tkinter import *
from tkinter import ttk     #styles
from tkinter import messagebox
import webbrowser
import sys
import os
import MySQLdb

      
connection = MySQLdb.connect(user='freedbtech_dscproject', password='dscdevice',host='freedb.tech',port=3306,database='freedbtech_Associatesdata')

#import Temperature_Sensor


average_temp=0
def restart_program():   #After Exit button
        python = sys.executable
        os.execl(python, python, * sys.argv)

def callback(url):       #open url fucntion
        webbrowser.open_new(url)
#Window 1
def main():
    connection.commit()
    Selected_Ans1=0
    Selected_Ans2=0
    Selected_Ans3=0
    win=Tk()
    s=ttk.Style()
    win.attributes('-fullscreen', True)


    background_win1 = Canvas(win, bg="blue", height=250, width=300)
    filename = PhotoImage(file ="/home/pi/Desktop/DSC Project/bg.png")
    background_label = Label(win, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_win1.pack()

    win.title("Contacltless Self Scanning Device")
    #Question 1
    Q1=Label(win,text="Have you had any Covid-19 related symptoms\n :(dry cough, fever, tirdness)?",bg="white",font=("Arial",25))
    Q1.place(x=130,y=50)
    Ans1=IntVar()
    Ans1.set(0)
    Q1_Op1=Radiobutton(win,text="Yes", variable=Ans1,value=1,font=("Arial",25),fg="grey",bg="white")
    Q1_Op1.place(x=100,y=150)
    Q1_Op2=Radiobutton(win,text="No",variable=Ans1,value=2,font=("Arial",25),fg="grey",bg="white")
    Q1_Op2.place(x=250,y=150)

    #Question 2
    Q2=Label(win,text="Have you been outside of Canada in\n the past 14 days?",bg="white",font=("Arial",25))
    Q2.place(x=100,y=220)
    Ans2=IntVar()
    Ans2.set(0)
    Q2_Op1=Radiobutton(win,text="Yes",variable=Ans2,value=1,font=("Arial",25),fg="grey",bg="white")
    Q2_Op1.place(x=100,y=325)
    Q2_Op2=Radiobutton(win,text="No", variable=Ans2,value=2,font=("Arial",25),fg="grey",bg="white")
    Q2_Op2.place(x=250,y=325)

    #Question 3
    Q3=Label(win,text="Have you had any contact with a confirmed Covid-19 case,\n or caring for someone diagnosed with Covid-19?",bg="white",font=("Arial",25))
    Q3.place(x=100,y=400)
    Ans3=IntVar()
    Ans3.set(0)
    Q3_Op1=Radiobutton(win,text="Yes", variable=Ans3,value=1,font=("Arial",25),fg="grey",bg="white")
    Q3_Op1.place(x=100,y=500)
    Q3_Op2=Radiobutton(win,text="No", variable=Ans3,value=2,font=("Arial",25),fg="grey",bg="white")
    Q3_Op2.place(x=250,y=500)


    def evaluate():
        global Selected_Ans1,Selected_Ans2,Selected_Ans3
        Selected_Ans1=int(Ans1.get())
        Selected_Ans2=int(Ans2.get())
        Selected_Ans3=int(Ans3.get())
        if Selected_Ans1!=0 and Selected_Ans2!=0 and Selected_Ans3!=0: 
                win.destroy()
        else:
            messagebox.showerror( "Warning", "You have not answered all the questions yet!")    

    button1=Button(win,text="Next", command=evaluate,font=("Raleway",40), bg="#D8D8D8", fg="#800000").place(x=850,y=500)

    
    win.mainloop()



start=Tk()
start.attributes('-fullscreen', True)

background_win1 = Canvas(start, bg="blue", height=250, width=300)
filename = PhotoImage(file ="/home/pi/Desktop/DSC Project/bg.png")
background_label = Label(start, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_win1.pack()



sql_select_Query1 = "select * from info"
cursor = connection.cursor()
cursor.execute(sql_select_Query1)
records = cursor.fetchall()
check_in_list=[]
for row in records:
        check_in=row[8].strip('}')
        check_in_list.append(check_in)
if "Warning" in check_in_list:
        Label(start,text="Someone is suspected to have Covid-19,\n Please call a manager !",fg="red" ,bg="white",font=("Arial",35)).place(x=140,y=10)
        messagebox.showwarning("Danger","Someone in the store is in danger and could be a risk for others, please call a manager!")




start.title("Contacltless Self Scanning Device")
Label(start,text="Hello !",bg="white",font=("Arial",50)).place(x=430,y=150)
Label(start,text="Please scan the barcode on your badge to start screening",font=("Arial",25),bg="white").place(x=120,y=270)
s= Entry(start,width=20,font=("Arial",25),show='*')
s.place(x=330,y=350)
s.focus_set()
range1=0
range2=4
def see_data():
        
        #show who did and did not do their temp checks
        scanner=s.get()
        
        admin_barcode=['002252082391']
        
            
        if scanner in admin_barcode:

            connection.commit()
            sql_select_Query1 = "select * from info"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query1)
            records = cursor.fetchall()
            check_done=[]
            check_not_done=[]
            temp_list=[]
            for row in records:
                id_num=row[0]
                Firstname=row[1].strip('}')
                Lastname=row[2].strip('}')
                position=row[3].strip('}')
                barcode=row[4].strip('}')
                start_time=row[5].strip('}')
                end_time=row[6].strip('}')
                temp=(row[7],"C")
                check_in=row[8].strip('}')

                if check_in=="Done" or check_in=="Warning":
                    temp_list.append(Firstname)
                    temp_list.append(Lastname)
                    temp_list.append(temp)
                    temp_list.append(start_time)
                    temp_list.append(end_time)
                    temp_list.append(check_in)
                    check_done.append(temp_list)
                else:
                    temp_list.append(Firstname)
                    temp_list.append(Lastname)
                    temp_list.append("0 C")
                    temp_list.append(start_time)
                    temp_list.append(end_time)
                    temp_list.append("Not Done")
                    check_not_done.append(temp_list)

                temp_list=[]

            #Display data Window
                
            admin_window=Toplevel(start)
            admin_window.attributes('-fullscreen', True)
            admin_window.configure(background='white')
            def scroll(check_done,check_not_done,up_down):
                    #Display the check_done list
                    def list1(range1,range2,check_done):
                            y_val=78
                            for i in range(range1,range2):
                                    x_val=0
                                    for j in range(0,3):
                                          e = Entry(admin_window, bg="white",font=("Arial",20),bd=2)
                                          e.grid(row=i,column=j)
                                          e.insert(END,check_done[i][j])
                                          e.place(x=x_val,y=y_val)
                                          x_val+=120
                                    x_val=0
                                    y_val+=40
                                    for k in range(3,6):
                                          e = Entry(admin_window, bg="white",font=("Arial",20),bd=2)
                                          e.grid(row=i,column=k)
                                          e.insert(END,check_done[i][k])
                                          e.place(x=x_val,y=y_val)
                                          x_val+=120
                                    y_val+=40
                    def list2(range1,range2,check_not_done):
                    #Display the check_not_done list
                            y_val=78
                            for i in range(range1,range2):
                                    x_val=550
                                    for j in range(0,3):
                                          e = Entry(admin_window, bg="white",font=("Arial",20),bd=2)
                                          e.grid(row=i,column=j)
                                          e.insert(END,check_not_done[i][j])
                                          e.place(x=x_val,y=y_val)
                                          
                                          x_val+=120
                                    x_val=550
                                    y_val+=40
                                    for k in range(3,6):
                                          e = Entry(admin_window, bg="white",font=("Arial",20),bd=2)
                                          e.grid(row=i,column=k)
                                          e.insert(END,check_not_done[i][k])
                                          e.place(x=x_val,y=y_val)
                                          x_val+=120
                                    y_val+=40
                                    
                    global range1,range2
                    if up_down=="up":
                            
                            range1=0
                            range2=4
                    if up_down==True: 
                            if range2<=len(check_done):
                                    if (range2+1)>len(check_done):
                                            x=(range2 +1)-len(check_done)
                                            for i in range(x):
                                                    new_row=["  ", "  ","  ","  ","  ","  "]
                                                    check_done.append(new_row)
                                            
                                    range1+=1
                                    range2+=1
                                    
                                    list1(range1,range2,check_done)
                                    
                            if range2<=len(check_not_done):
                                    if (range2+1)>len(check_not_done):
                                            x=(range2 +1)-len(check_not_done)
                                            for i in range(x):
                                                    new_row=["  ", "  ","  ","  ","  ","  "]
                                                    check_not_done.append(new_row)
                                            
                                    range1+=1
                                    range2+=1
                                    list2(range1,range2,check_not_done)
                            
                                            
                    else:
                                  
                          try:               
                                  list1(0,4,check_done)
                                  
                          except IndexError:
                                  pass
                          try:
                                  list2(0,4,check_not_done)
                          except IndexError:
                                  pass
                          Button(admin_window,text="Go Back", command=restart_program,font=("Raleway",30),width=11,height=1, bg="#D8D8D8", fg="#800000").place(x=0,y=0)

            scroll(check_done,check_not_done," ")            
            def clear_warnings():
                    connection.commit()
                    update="UPDATE info SET check_in='Done' WHERE check_in='Warning'"
                    cursor = connection.cursor()
                    cursor.execute(update)
                    connection.commit()
                    
            Button(admin_window,text="Go Up", command=lambda: scroll(check_done,check_not_done,"up"),font=("Raleway",30), bg="#D8D8D8", fg="#800000").place(x=475,y=0)
            Button(admin_window,text="Down", command=lambda: scroll(check_done,check_not_done,True),font=("Raleway",30), bg="#D8D8D8", fg="#800000").place(x=325,y=0)
            Button(admin_window,text="Clear Warnings", command=clear_warnings,font=("Raleway",30), bg="#D8D8D8", fg="#800000").place(x=650,y=0)
            Button(admin_window,text="Go Back", command=restart_program,font=("Raleway",30),width=11,height=1, bg="#D8D8D8", fg="#800000").place(x=0,y=0)
        else:
            messagebox.showerror( "Warning", "You are not an athorized personnel")
             
        
Button(start,text="Manager login",font=("Raleway",30), bg="#D8D8D8", fg="#800000", command=see_data).place(x=100,y=510)

def start_():
        global scanner
        scanner=s.get()

        s.delete(0, END)
        
        sql_select_Query2 = "select * from Associates"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query2)
        records = cursor.fetchall()
        barcodes=[]
        for row in records:
                barcode=row[4]
                barcodes.append(barcode)
        if scanner in barcodes:
                    
                start.destroy()
                main()
        else:
                messagebox.showerror( "Warning", "please scan a valid badge")
                    
Button(start,text="Next",font=("Raleway",40), bg="#D8D8D8", fg="#800000",command=start_).place(x=850,y=500)


start.mainloop()

        
def warning(average_temp):           #warning window
    connection.commit()
    
    Label(win2,text="Return Home Immedietly !\n\n It is not safe for you to work,\n it is important that you self isolate\n and seek testing.\n\n Please review the Covid-19\n guidlines on Ontario.ca",bg="white",font=("Arial",30)).place(x=250,y=100)
    
    def scan_update():

            global scanner
                    
            connection.commit()
            update="UPDATE info SET temp=%(average_temp)s, check_in='Warning' WHERE barcode_num=%(scanner)s"
            cursor = connection.cursor()
            cursor.execute(update,{ 'average_temp': average_temp, 'scanner': scanner })
            connection.commit()
            restart_program()
            
    
            
    button2=Button(win2,text="Exit", font=("Raleway",40), bg="#D8D8D8", fg="#800000",command=lambda:[scan_update()]).place(x=850,y=500)


#Window 2
win2=Tk()
win2.attributes('-fullscreen', True)
win2.title("Contacltless Self Scanning Device")

background_win1 = Canvas(win2, bg="blue", height=250, width=300)
filename = PhotoImage(file = "/home/pi/Desktop/DSC Project/bg.png")
background_label = Label(win2, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_win1.pack()

if Selected_Ans1==2 and Selected_Ans2==2 and Selected_Ans3==2: 
    label=Label(win2,text="Please be within 10cm range\n away from the sensor",font=("Arial",30),bg="white")
    label.place(x=250,y=270)
    def next():
        win2.destroy()

    #average=Temperature_Sensor.run_sensor()

    average_temp=36  #test

    if average_temp>=36 and average_temp<38:
        button3=Button(win2,text="Next", command=next,font=("Raleway",40), bg="#D8D8D8", fg="#800000").place(x=850,y=500)
        #we could update the temps in thr database later
        pass_=True
    else:
        label.destroy()
        messagebox.showinfo( "Warning", "Your temperature is too high, Please go home and let a manager be aware of this !")
        warning(average_temp)

elif Selected_Ans1!=0 and Selected_Ans2!=0 and Selected_Ans3!=0:
    messagebox.showinfo( "Warning", "You are not allowed to start you shift, Please contact your manager !")
    warning(average_temp)

win2.mainloop()


#Window 3 based on %pass_ 
if pass_==True:
    win3=Tk()
    win3.attributes('-fullscreen', True)
    win3.title("Contacltless Self Scanning Device")
    background_win1 = Canvas(win3, bg="blue", height=250, width=300)
    filename = PhotoImage(file = "/home/pi/Desktop/DSC Project/bg.png")
    background_label = Label(win3, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_win1.pack()

    global scanner


    try:
        connection.commit()
        #Getting values from table of the day 
        sql_select_Query = "select * from info where barcode_num=%(scanner)s"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,{ 'scanner': scanner })
        records = cursor.fetchall()
        for row in records:
            id_num=row[0]
            Firstname=row[1].strip('}')
            Lastname=row[2].strip('}')
            position=row[3].strip('}')
            barcode=row[4].strip('}')
            start_time=row[5].strip('}')
            end_time=row[6].strip('}')

        def update_data():      #update the temp and check_in into table
            update="UPDATE info SET temp=%(average_temp)s, check_in='Done' WHERE barcode_num=%(scanner)s"
            cursor = connection.cursor()
            cursor.execute(update,{ 'average_temp': average_temp, 'scanner': scanner })
            connection.commit()
            restart_program()

        lbl2=Label(win3,text="Please click on your shift to confirm !",font=("Arial",30),bg="white")
        lbl2.place(x=180,y=200)
        Label(win3,text=(Firstname + ' '+ Lastname+ '\n'+ position),font=("Raleway",25), bg="white", fg="#800000").place(x=500,y=330, anchor="center")
        but=('Shift: '+ start_time+ ' To '+ end_time)
        button4=Button(win3,text=(but), command=update_data,font=("Raleway",25), bg="#D8D8D8", fg="#800000").place(x=285,y=480)

    except NameError:
        Label(win3,text="Nothing matches the barcode scanned,\n no shift for you today",font=("Arial",30),bg="white").place(x=180,y=270)
        lbl2.destroy()
        Button(win3,text="Exit", command=restart_program,font=("Raleway",40), bg="#D8D8D8", fg="#800000").place(x=850,y=500)
    
    win3.mainloop()



connection.close()
