# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:40:53 2022

@author: abdul
"""
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class Parent:
      
    def __init__(self):              
        
        from  tkinter import ttk
        import sqlite3
        
        window=Tk()
        
        
        # def show_in_table(name):
        #     #database 
        #     dbname='labeled.db'
        #     conn =  sqlite3.connect(dbname)
        #     c = conn.cursor()
        #     cmnd1 = "select * from "
        #     cmnd2 = "Allah"
        #     cmnd = cmnd1+cmnd2
        #     c.execute(cmnd)
        #     rows = c.fetchall()
        #     total= c.rowcount
        
        def scrape_comments():
            try:
                url = txtfld_url.get()
                url_i = url.split('?v=')
                url_id = url_i[1].split('&list=')
            except:
                messagebox.showinfo("showinfo", "Error")
                
            print()
        
            # api_key = txtfld_api.get()  # Replace this dummy api key with your own.
            api_key = ''
            from apiclient.discovery import build
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            import pandas as pd
            
            ID = url_id[0] # Replace this YouTube video ID with your own.
            
            box = [['Name', 'Comment', 'Reply Count']]
            
            
            
            def enter_in_database(title):
                #database
                t= title
                dbname='lb.db'
                conn =  sqlite3.connect(dbname)
                c = conn.cursor()
                c.execute('DROP TABLE IF EXISTS Comments')
                for rec in tab.get_children():
                 tab.delete(rec)
                sql = """
                
                CREATE TABLE Comments (Name TEXT, Comment TEXT)
                
                """
                
                c.execute(sql)
                #print('database has been created')
                
                with open(t, 'r' , encoding = 'utf8' ) as file:
                    records = 0
                    for row in file:
                        try:
                            row2 = row.split(',')
                            row3 = row2[0]
                            row4 = row2[1]
                            c.execute("INSERT INTO Comments VALUES(?,?)",[((row3)),((row4))])
                            conn.commit()
                            row2 = 0
                            records += 1
                        except:
                            print(" ")
                    
                
                cmnd = "select * from Comments"
                c.execute(cmnd)
                rows = c.fetchall()
                total= c.rowcount
                
                
                #inserting data in the table
                for t in rows:
                    tab.insert('', 'end', values=t)
                
                tab.pack()
            
            def get_video_details(youtube, **kwargs):
                return youtube.videos().list(
                    part="snippet",
                    **kwargs
                ).execute()
        
            def print_video_infos(video_response):
                items = video_response.get("items")[0]
                snippet = items["snippet"]
                title = snippet["title"]
                t2 = title.split(' ')
                        
                #t2 = title.replace(' ', '_')
                t3 = '.csv'
                title_final = t2[0]+t3
                return title_final
           
            def scrape_comments_with_replies():
                try:
                    # api call
                    data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='100', textFormat="plainText").execute()
                    
                    #get comments
                    for i in data["items"]:
                
                        name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                        
                        
                        box.append([name, comment])
                        
                       
                    while ("nextPageToken" in data):
                
                        data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"], maxResults='100', textFormat="plainText").execute()
                        
                        for i in data["items"]:
                            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                            
                           
                            box.append([name, comment])
                            
                    df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box]})
                    response = get_video_details(youtube, id=ID)
                    title = print_video_infos(response)
                    
                    df.to_csv(title , index=False, header=False)
                    messagebox.showinfo("showinfo", "Comments Scrapped Successfully! Will be uploaded in table soon.")
                    return title
                except:
                    messagebox.showinfo("showinfo", "Invalid URl")
            
            
            title = scrape_comments_with_replies()
            enter_in_database(title)
                
            
            
        
        
        
        lbll=Text(window, fg='black',  font=("Calibiri", 8), height=5, width =50)
        lbll.place(x=230, y=600, anchor='s') 
        
        
        def select_la(e):
            lbll.delete(1.0,END)

            selected = tab.focus()
            print(selected)
            v = tab.item(selected, 'values')
            print(v)
            lbll.insert(1.0, v[1])
        
        
        
        
        
        
        window.title('Information')
        window.geometry("1250x670")
        window.configure(bg='#455D6F')
        
        #window.attributes('-alpha', 0.96)
        
        
        can3 = Canvas(window, width=1500, height = 33, bg='#D8E4ED')
        can3.place(x=0,y=105)
        
        
        lbl=Label(window, text="Sentiment", fg='#D1F0BD', bg='#455D6F', font=("Calibiri", 32))
        lbl.place(x=550, y=78, anchor='s')
        lbl=Label(window, text="Analyzer", fg='White', bg='#455D6F', font=("Calibiri", 32))
        lbl.place(x=750, y=78, anchor='s')
        
        #table frame
        
        ta = Frame(window)
        ta.place(x=450,y=250)
        
        
        #adding scroolbar
        # scrool = Scrollbar(ta,orient='horizontal')
        # scrool.pack(side=BOTTOM, fill=X)
        
        # scrool = Scrollbar(ta,orient='vertical')
        # scrool.pack(side= LEFT,fill=Y)
        
        #adding colomn
        
        
        #tab = ttk.Treeview(ta,yscrollcommand=scrool.set, xscrollcommand =scrool.set)
        tab = ttk.Treeview(ta)
        tab.place(x=400,y=200)
        tab['columns'] = ('Name', 'Comment')
        
        tab.column("#0", width=0,  stretch=NO)
        tab.column("Name", width=100)
        tab.column("Comment",width=300)
        
        
        tab.heading("#0",text="",anchor=CENTER)
        tab.heading("Name",text="Name",anchor=CENTER)
        tab.heading("Comment",text="Comment",anchor=CENTER)
        tab.bind("<Double-1>", select_la)

        tab.pack()
        def dashboard():
            window.withdraw()
            dashboard_class()        
        
        btn_a=Button(window, text="Information", fg='#D1F0BD',bg='#455D6F' ,bd=2, width=15,relief="solid")
        btn_a.place(x=70, y=110)
        
        btn_c=Button(window, text="Classifier", fg='#D1F0BD',bg='#455D6F' ,bd=2, width=15,relief="solid", command = dashboard)
        btn_c.place(x=220, y=110)

        

        
        
        lbl=Label(window, text="Please Enter the URL of the video you want to classify", fg='black',  font=("Calibiri", 8))
        lbl.place(x=155, y=300, anchor='s')
        
        
        lbl_url=Label(window, text="video url", fg='black',bg='white', width=10)
        lbl_url.place(x=20, y=330)
        
        txtfld_url=Entry(window, text="URL", bd=5, width=30)
        txtfld_url.place(x=120, y=330)
        
        btn_dwn=Button(window, text="Start", fg='#D1F0BD',bg='#455D6F' , bd=2, width=15, command = scrape_comments)
        btn_dwn.place(x=200, y=400)
        lbl=Label(window, text="Above Comments will be Classified", fg='black',  font=("Calibiri", 8))
        lbl.place(x=600, y=555, anchor='s')
        

        btn_cls=Button(window, text="Classify", fg='#D1F0BD',bg='#455D6F' , bd=2, width=15, command = dashboard)
        btn_cls.place(x=730, y=530)
        
        
        
        
        
        window.mainloop()








class dashboard_class(Parent):
  
    # create a parent class method
    def __init__(self):
                # -*- coding: utf-8 -*-
            """
            Created on Wed Mar 16 05:23:52 2022
            
            @author: abdul
            """
            
            
            from  tkinter import ttk
            import sqlite3
            import joblib
            window=Tk()
            
            
            window.title('Classifier')
            window.geometry("1250x670")
            window.configure(bg='#455D6F')
            
            can = Canvas(window, width=1500, height = 135, bg='#455D6F')
            can.place(x=0,y=0)
            #window.attributes('-alpha', 0.85)
            
            can2 = Canvas(window, width=560, height = 160, bg='#D8E4ED')
            can2.place(x=630,y=500)
            
            can3 = Canvas(window, width=1500, height = 33, bg='#D8E4ED')
            can3.place(x=0,y=105)
            
            can4 = Canvas(window, width=435, height = 260, bg='#D8E4ED',relief="solid",bd=2)
            can4.place(x=640,y=190)
            
            can5 = Canvas(window, width=435, height = 260, bg='#D8E4ED',relief="solid",bd=2)
            can5.place(x=90,y=190)
            
            Output = Text(window, height = 1,width = 6,bg='#D1F0BD')
            Output.place(x=1135, y = 200)
            lbl=Label(window, text="Percent", fg='#D1F0BD', bg = '#455D6F' , font=("Calibiri", 8))
            lbl.place(x=1220, y=220, anchor='s')

            
            
            def Appreciation():
                o()
            
                dbname='classified.db'
                conn =  sqlite3.connect(dbname)
                c = conn.cursor()
                
                cmnd = "select * from classified Where Sentiment = 'Appreciation'"
                c.execute(cmnd)
                rows = c.fetchall()
                total= c.rowcount
                for t in rows:
                    tab.insert('', 'end', values=t)
                    
                    tab.pack()
                print(len(rows))
                Output.delete("1.0","end")
                l = len(rows)
                percentage = ((l/ttt)*100)
                percentage = str(round(percentage, 2))
                print(percentage)
                print(ttt)
                Output.insert(1.0, percentage)
                   
            def Greeting():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Greeting'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                   
                except:
                    messagebox.showinfo("showinfo", "No Greeting Comment")
            def Sad():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Sad'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                              
                except:
                    messagebox.showinfo("showinfo", "No Sad Comment")
            
            def Question():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Question'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Question Comment")
            def Sarcasm():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Sarcasm'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Sarcasm Comment")
            
            def Attention_Seeker():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Attention Seeker'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Attention Seeker Comment")
            
            def Recommend():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Recommendation'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Recommendation Comment")
            
            
            def Wish():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Wish'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Wish Comment")
            
            
            def Love():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Love Giver'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Love Giver Comment")
            
            
            def Excitement():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Excitement'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Excitement Comment")
            
            def Blessing():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Blessing'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Blessing Comment")
            
            def Link():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Link'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Information Comment")
            
            
            def Request():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Request'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Request Comment")
            
            
            
            def Quotation():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Quotation'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Quotation Comment")
            
            
            def Other():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Other'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Other Comment")
            
            
            def Positive():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Positive'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Positive Comment")
            
            
            
            
            def Negative():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from classified where Sentiment = 'Negative'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Negative Comment")
            
            
            def Hate():
                o()
                try:
                    dbname='classified.db'
                    conn =  sqlite3.connect(dbname)
                    c = conn.cursor()
                    cmnd = "select * from Classified where Sentiment = 'Hate'"
                    c.execute(cmnd)
                    rows = c.fetchall()
                    total= c.rowcount
                    for t in rows:
                        tab.insert('', 'end', values=t)
            
                        tab.pack()
                    Output.delete("1.0","end")
                    l = len(rows)
                    percentage = ((l/ttt)*100)
                    percentage = str(round(percentage, 2))
                    print(percentage)
                    print(ttt)
                    Output.insert(1.0, percentage)
                                 
                except:
                    messagebox.showinfo("showinfo", "No Hate Comment")
            def o():
                
                 dbname='classified.db'
                 conn =  sqlite3.connect(dbname)
                 c = conn.cursor()
                 for rec in tab.get_children():
                     tab.delete(rec)
                    
            
            def classify():
                dbname='lb.db'
                conn =  sqlite3.connect(dbname)
                c = conn.cursor()
                cmnd = "select Comment from Comments"
                c.execute(cmnd)
                rows = c.fetchall()
                
                total= c.rowcount
                global ttt
                ttt = len(rows)
                filename = 'log_reg_saved_model.joblib'
                loaded_model = joblib.load(filename)
                    
                    #tab.insert('', 'end', values=t)
                conn.close()    
                
                
                
                dbname='classified.db'
                conn =  sqlite3.connect(dbname)
                c = conn.cursor()
                c.execute('DROP TABLE IF EXISTS Classified')
                for rec in tab.get_children():
                    tab.delete(rec)
                sql = """
                        
                CREATE TABLE classified (Comment TEXT, Sentiment TEXT)
                        
                """
                        
                c.execute(sql)
                        #print('database has been created')
                import functools
                import operator           
                
                records = 0
                for row in rows:
                
                    result = loaded_model.predict(row)  
                    result = functools.reduce(operator.add, (result))
                    row = functools.reduce(operator.add, (row))
                    c.execute("INSERT INTO Classified VALUES(?,?)",[(str(row)),(str(result))])
                    conn.commit()
                    #tab.insert('', 'end', values=row)
                
                
            def show_in_table():
                dbname='classified.db'
                conn =  sqlite3.connect(dbname)
                c = conn.cursor()
                cmnd = "select * from Classified"
                c.execute(cmnd)
                rows = c.fetchall()
                total= c.rowcount
                return rows
            
            
            
            lbll=Text(window, fg='black',  font=("Calibiri", 8), height=5, width =50)
            lbll.place(x=230, y=600, anchor='s') 
        
        
            def select_la(e):
                lbll.delete(1.0,END)

                selected = tab.focus()
                print(selected)
                v = tab.item(selected, 'values')
                print(v)
                lbll.insert(1.0, v[0])
            
            
            
            
            
            
            
            
            
            
            
            
            lbl=Label(window, text="Sentiment", fg='#D1F0BD', bg='#455D6F', font=("Calibiri", 32))
            lbl.place(x=550, y=78, anchor='s')
            lbl=Label(window, text="Analyzer", fg='White', bg='#455D6F', font=("Calibiri", 32))
            lbl.place(x=750, y=78, anchor='s')
            ta = Frame(window)
            ta.place(x=100,y=200)
            
            #database 
            
            
            #adding scroolbar
            # scrool = Scrollbar(ta,orient='horizontal')
            # scrool.pack(side=BOTTOM, fill=X)
            
            # scrool = Scrollbar(ta,orient='vertical')
            # scrool.pack(side= LEFT,fill=Y)
            
            #adding colomn
            
            
            # tab = ttk.Treeview(ta,yscrollcommand=scrool.set, xscrollcommand =scrool.set)
            tab = ttk.Treeview(ta)
            tab.place(x=400,y=200)
            tab['columns'] = ('comment', 'sentiment')
            
            tab.column("#0", width=0,  stretch=NO)
            tab.column("comment", width=320, stretch=YES)
            tab.column("sentiment",anchor=CENTER,width=100)
            
            
            tab.heading("#0",text="",anchor=CENTER)
            tab.heading("comment",text="Comment",anchor=CENTER)
            tab.heading("sentiment",text="Sentiment",anchor=CENTER)
            
            
            
            classify()
            rows = show_in_table()
            
            # rows, row2 =zip(*rows)
            # print(rows)
            import string
            
            #inserting data in the table
            for t in rows:
                
                tab.insert('', 'end', values=t)
            
            tab.pack()
            
            
            def parent():
                window.withdraw()
                Parent()     
            
            
            btn_a=Button(window, text="Information", fg='#D1F0BD',bg='#455D6F' ,bd=2, width=15,relief="solid", command = parent)
            btn_a.place(x=70, y=110)
            
            btn_c=Button(window, text="Classifier", fg='#D1F0BD',bg='#455D6F' ,bd=2, width=15,relief="solid")
            btn_c.place(x=220, y=110)

            

            
            
            lbl=Label(window, text="Classified Comments ", fg='#D1F0BD', bg = '#455D6F' , font=("Calibiri", 16))
            lbl.place(x=200, y=488, anchor='s')
            
            lbl=Label(window, text="Specific Comments ", fg='#D1F0BD',bg = '#455D6F',  font=("Calibiri", 16))
            lbl.place(x=740, y=488, anchor='s')
            
            lbl=Label(window, text="Please select the category you want to see the comments for ", fg='#455D6F', bg = '#D8E4ED' , font=("Calibiri", 12))
            lbl.place(x=860, y=525, anchor='s')
            
            #Second table
            
            
            
            ta2 = Frame(window)
            ta2.place(x=650,y=200)
            #adding scroolbar
            # scrool = Scrollbar(ta2,orient='horizontal')
            # scrool.pack(side=BOTTOM, fill=X)
            
            # scrool = Scrollbar(ta2,orient='vertical')
            # scrool.pack(side= LEFT,fill=Y)
            
            #adding colomn
            
            
            # tab = ttk.Treeview(ta2,yscrollcommand=scrool.set, xscrollcommand =scrool.set)
            tab = ttk.Treeview(ta2)
            tab.place(x=400,y=200)
            tab['columns'] = ('comment', 'sentiment')
            
            tab.column("#0", width=0,  stretch=NO)
            tab.column("comment", width=320)
            tab.column("sentiment",anchor=CENTER,width=100)
            
            
            tab.heading("#0",text="",anchor=CENTER)
            tab.heading("comment",text="Comment",anchor=CENTER)
            tab.heading("sentiment",text="Sentiment",anchor=CENTER)
            
            # dbname=' classified.db'
            # conn =  sqlite3.connect(dbname)
            # c = conn.cursor()
            # cmnd = "select * from classified where Sentiment = 'Appreciation'"
            # c.execute(cmnd)
            # rows = c.fetchall()
            # total= c.rowcount
            # for t in rows:
            #     tab.insert('', 'end', values=t)
            tab.bind("<Double-1>", select_la)

            tab.pack()
            
            
            btn_appriciation=Button(window, text="Appreciation", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Appreciation)
            btn_appriciation.place(x=650, y=530)
            
            btn_greeting=Button(window, text="Greeting", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Greeting)
            btn_greeting.place(x=740, y=530)
            
            btn_hate=Button(window, text="Hate", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Hate)
            btn_hate.place(x=830, y=530)
            
            btn_sad=Button(window, text="Sad", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Sad)
            btn_sad.place(x=920, y=530)
            
            btn_question=Button(window, text="Question", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Question)
            btn_question.place(x=1010, y=530)
            
            # btn_sarcasm=Button(window, text="Sarcasm", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Sarcasm)
            # btn_sarcasm.place(x=1100, y=530)
            
            # btn_attention=Button(window, text="Attention", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Attention_Seeker)
            # btn_attention.place(x=650, y=580)
            
            btn_recommend=Button(window, text="Recommend", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Recommend)
            btn_recommend.place(x=740, y=580)
            
            btn_wish=Button(window, text="Wish", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Wish)
            btn_wish.place(x=830, y=580)
            
            btn_love=Button(window, text="Love", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Love)
            btn_love.place(x=920, y=580)
            
            btn_excitement=Button(window, text="Excitement", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Excitement)
            btn_excitement.place(x=1010, y=580)
            
            btn_blessing=Button(window, text="Blessing", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Blessing)
            btn_blessing.place(x=1100, y=580)
            
            btn_info=Button(window, text="Link", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Link)
            btn_info.place(x=650, y=630)
            
            btn_request=Button(window, text="Request", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Request)
            btn_request.place(x=740, y=630)
            
            btn_quote=Button(window, text="Quotation", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Quotation)
            btn_quote.place(x=830, y=630)
            
            btn_positive=Button(window, text="Positive", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Positive)
            btn_positive.place(x=920, y=630)
            
            btn_negative=Button(window, text="Negative", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Negative)
            btn_negative.place(x=1100, y=530)
            
            btn_other=Button(window, text="Other", fg='#D1F0BD',bg='#455D6F' , bd=2, width=10, command = Other)
            btn_other.place(x=650, y=580)
            
            
            
            window.mainloop()




        
        
        





Parent()
