from tkinter import *
import os
import tkinter.ttk as ttk
from tkinter import scrolledtext
import sqlite3
from location import Location
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from PIL import ImageTk,Image
import time

import datetime

class GUI():
    def __init__(self, office):
        self.office = office
        if(self.office == "Ukiah"):
            self.conn = sqlite3.connect("sites.db")
        elif(self.office == "Eureka"):
            self.conn = sqlite3.connect("sitesEureka.db")
        elif (self.office == "Santa Rosa"):
            self.conn = sqlite3.connect("sitesSantaRosa.db")
        self.cur = self.conn.cursor()

        # Creating the window
        self.window = Tk() #window object
        self.window.title("LACO FORECAST DATA APPLICATION 2018")

        self.window.geometry('700x900')
        chromedriverpath = "/Users/phuctruong/Documents/Python\ files/LACO\ Forecast\ Data/chromedriver"
        #print("DEBUG!!!: driver exist:" , os.path.exist(chromedriverpath))
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        #mainFrame = Frame(window, width = 1000, height = 800, bg="powder blue", relief = FLAT)
        #mainFrame.pack(side = RIGHT)
        #mainFrame.pack_propagate(False) #making the frame not shrink to fit
        #menuFrame = Frame(window, width = 400, height = 800, bg = "powder blue")
        #menuFrame.pack(side = LEFT)


        self.menuTabs = ttk.Notebook(self.window)

##########################################GET DATA TAB SECTION #######################################################
        self.getDataTab = Frame(self.menuTabs, bg="powder blue", relief = SUNKEN)
        self.answerBox = scrolledtext.ScrolledText(self.getDataTab, width = 40, height = 30)
        self.answerBox.place(relx = 1, rely = 0.5, anchor = E)

        #locations = {"6843.29 Westport Sink": 0, "7414.02 SPRQ": 0, "7425.00 Soils Plus": 0, "7655.03 Rhys Vineyards": 0, "7760.06 Ford Road":0, "8229.00 Pt. Arena":0, "8545.11 Black Mountain": 0, "8592.01 Big Daddy": 0, "8761.00 Frey Winery":0, "9192.01 Payne":0 }
        self.locations = {}
        self.locationsDel = {}

        self.cur.execute("SELECT projectNumber, site FROM SiteURL ORDER BY projectNumber")
        sitesFetch = self.cur.fetchall() #sitesFetch is an array
        index = 0
        while(index < len(sitesFetch)):
            self.locations[sitesFetch[index]] = 0 #add to the location dictionary and set checks to 0
            index = index + 1
        self.locationsDel = dict(self.locations)

    

        Label(self.getDataTab, text = "LACO STORM WATER APPLICATION 2019", font = ("Helvetica", 24), bg = "DarkOliveGreen2").pack(pady = (40,5))
        Label(self.getDataTab, text = "For " + self.office, font = ("Helvetica", 20), bg = "DarkOliveGreen2" ).pack(pady = 5)
        self.checkBoxMainFrame = Frame(self.getDataTab, width = 1000, height = 500)
        self.checkBoxMainFrame.place(x = 40, y = 170)

        self.checkBoxCanvas= Canvas(self.checkBoxMainFrame, width = 250, height = 500)
        self.checkBoxCanvas.pack(side = "left")
        self.checkBoxFrame = Frame(self.checkBoxCanvas)
        #checkBoxFrame.pack_propagate(False) #making the frame not shrink to fit
        #checkBoxFrame.place(x = 0, rely = 0.2)
        self.checkBoxScrollBar = Scrollbar(self.checkBoxMainFrame, orient = "vertical")
        self.checkBoxScrollBar.configure(command = self.checkBoxCanvas.yview)
        self.checkBoxCanvas.configure(yscrollcommand=self.checkBoxScrollBar.set)

        self.checkBoxScrollBar.pack(side = "right", fill = "y")
        self.checkBoxCanvas.create_window((0,0), window = self.checkBoxFrame, anchor = "nw")
        self.checkBoxFrame.bind("<Configure>", self.configureFunction)


        self.data(self.checkBoxFrame, self.locations)
        self.allOffButton = Button(self.getDataTab, text = "All Off", bg = "green", command = self.allOff )
        self.allOffButton.place(x = 49, y = 140)
        self.allOnButton = Button(self.getDataTab, text = "All On", bg = "green", command = self.allOn )
        self.allOnButton.place(x = 100, y = 140)

        self.extraFrame = Frame(self.getDataTab, relief = RIDGE)
        self.extraFrame.place(x = 40, y =400)

        self.currentTime = None
        Label(self.extraFrame, text = "Hour offset:   ", pady = 5, bg = "powder blue", padx = 5, relief = "ridge").grid(column = 1, row = 1, pady = 5, padx = 5)
        Label(self.extraFrame, text = "Time last used:", pady = 5, bg = "powder blue", padx = 5, relief = "ridge").grid(column = 1, row = 2, pady = 5, padx = 5)
        self.timeLabel = Label(self.extraFrame, text = "empty", pady = 5, padx = 5, relief = "ridge", bg = "yellow")
        self.timeLabel.grid(column = 2, row = 2, pady = 5, padx = 5)
        self.updateTimeLabel()
        self.updateTimeBtn = Button(self.extraFrame, text = "Update Time", command = self.updateTime, bg = "yellow")
        self.updateTimeBtn.grid(column = 2, row = 3, pady = 5, padx = 5)

        self.spinBox = Spinbox(self.extraFrame, from_= 1, to= 48, width = 5)
        self.spinBox.grid(column = 2, row = 1, sticky = "w", pady = 5, padx = 5)
        self.spinBox.delete(0, "end")
        self.spinBox.insert(0, 24)

        #self.dogCanvas = Canvas(self.extraFrame)
        #img = PhotoImage(file="wait.gif")
        #img = ImageTk.PhotoImage(Image.open("please_wait.jpg"))
        #self.dogCanvas.create_image(30, 30, anchor=NW, image=img)
        #self.dogCanvas.grid(column = 1, columnspan = 2, row = 4)
        #self.dogCanvas.grid_remove()


        self.precipString = ""
        self.getFCDataBtn = Button(self.getDataTab, text = "Get Data Now!!!", bg = "green", padx = 5, pady = 5, command = self.clicked)
        self.getFCDataBtn.place(relx = 0.75, rely = 0.2, x = -40, y = -20)
        #getFCDataBtn.pack()
#----------------------------------------------------END OF SECTION-----------------------------------------------------------





#########3################################             MODIFY TAB SECTION        ###############################################
        self.modifyTab = Frame(self.menuTabs, bg = "powder blue", relief = SUNKEN)
        ######ADD NEW FRAME
        self.addNewFrame = Frame(self.modifyTab, bg = "DarkOliveGreen1", relief = GROOVE, width = 300, height = 175)
        self.addNewFrame.pack()#grid(column = 1, row = 1)



        Label(self.addNewFrame, text = "ADD NEW SITE", font = ("Helvetica", 15)).grid(column = 1, columnspan = 2, row = 1, pady = 10, padx = 10)
        Label(self.addNewFrame, text = "Enter New Site's Project Number (ex: 1000.00): ").grid(column = 1, row = 3)
        Label(self.addNewFrame, text = "Enter New Site's Name: ").grid(column = 1, row = 4)
        Label(self.addNewFrame, text = "Enter New Site's Forecast URL Address: ").grid(column = 1, row = 5)
        Label(self.addNewFrame, text = "Enter New Site's Recorded Precip URL: ").grid(column = 1, row = 6)
        Label(self.addNewFrame, text = "Enter Node number, leave empty if not needed: ").grid(column = 1, row = 7)
        
        self.newName = Entry(self.addNewFrame)
        self.newFCURL = Entry(self.addNewFrame)
        self.newRPURL = Entry(self.addNewFrame)
        self.newNode = Entry(self.addNewFrame)
        self.newProjectNumber = Entry(self.addNewFrame)

        self.newName.grid(column = 2, row = 4)
        self.newFCURL.grid(column = 2, row = 5)
        self.newRPURL.grid(column = 2, row = 6)
        self.newNode.grid(column = 2, row = 7)
        self.newProjectNumber.grid(column = 2, row = 3)

        self.DeleteSiteFrame = Frame(self.modifyTab,  bg = "DarkOliveGreen1", relief = GROOVE, width = 300, height = 175)
        self.DeleteSiteFrame.pack(pady = 20)
        Label(self.DeleteSiteFrame, text = "DELETE UNWANTED SITES HERE", font = ("Helvetica", 15)).pack(padx = 10, pady = 10)

        self.checkBoxMainFrameDel = Frame(self.DeleteSiteFrame, width = 1000, height = 500)
        self.checkBoxMainFrameDel.pack()

        self.checkBoxCanvasDel= Canvas(self.checkBoxMainFrameDel, width = 250, height = 500)
        self.checkBoxCanvasDel.pack(side = "left")
        self.checkBoxFrameDel = Frame(self.checkBoxCanvasDel)
        #checkBoxFrame.pack_propagate(False) #making the frame not shrink to fit
        #checkBoxFrame.place(x = 0, rely = 0.2)
        self.checkBoxScrollBarDel = Scrollbar(self.checkBoxMainFrameDel, orient = "vertical")
        self.checkBoxScrollBarDel.configure(command = self.checkBoxCanvasDel.yview)
        self.checkBoxCanvasDel.configure(yscrollcommand=self.checkBoxScrollBarDel.set)

        self.checkBoxScrollBarDel.pack(side = "right", fill = "y")
        self.checkBoxCanvasDel.create_window((0,0), window = self.checkBoxFrameDel, anchor = "nw")
        self.checkBoxFrameDel.bind("<Configure>", self.configureFunctionDel)

        self.data(self.checkBoxFrameDel, self.locationsDel)

        self.getFCDataBtn = Button(self.DeleteSiteFrame, text = "Delete Chosen Sites!!!", bg = "green", padx = 5, pady = 5, command = self.clickedDel)
        self.getFCDataBtn.pack(pady = 10, padx = 10)

        self.addSiteBtn = Button(self.addNewFrame, text = "ADD NOW", bg = "green", command = self.AddNewSite )
        self.addSiteBtn.grid(column = 1, columnspan = 2 ,  row = 8, pady = 10)


###########################################################END OF MODIFY SECTION#######################################

        self.menuTabs.add(self.getDataTab, text = "Get Data")
        self.menuTabs.add(self.modifyTab, text = "Modify Data")
        self.menuTabs.pack(expand = 1, fill = 'both')
        self.window.mainloop()

    def updateTimeLabel(self):
        self.cur.execute('SELECT lastTime from currentTime')
        self.currentTime = self.cur.fetchone()
        self.timeLabel.config(text = self.currentTime[0])

    def updateTime(self):
        currentTime = datetime.datetime.now().strftime("%a, %b %d, %Y %H:%M")
        self.cur.execute('DELETE FROM currentTime')
        self.conn.commit()
        q = 'INSERT INTO currentTime (lastTime) VALUES ("' + str(currentTime) + '")'
        self.cur.execute(q)
        self.conn.commit()
        self.updateTimeLabel()

    def clickedDel(self): #When the delete Button is pressed
        i = 0
        siteKeys = list(self.locationsDel.keys())
        for item in self.locationsDel:
            if(self.locationsDel[item].get() == 1):
                t1 = (siteKeys[i][0])
                t = (t1,)
                self.cur.execute("DELETE FROM SiteURL WHERE projectNumber = ?", t)
                self.conn.commit()


            i = i + 1

        self.updateCheckBoxes()

    def AddNewSite(self):
        if(self.newName.get() != "" and self.newFCURL.get() != "" and self.newRPURL.get() != "" and self.newProjectNumber.get() != ""):
            #print(self.newName.get())
            query = 'INSERT INTO SiteURL (site, fcurl, rpurl, node, projectNumber) VALUES ("' + self.newName.get() + '", "' + self.newFCURL.get() + '","' + self.newRPURL.get() + '","' + self.newNode.get()+ '",' + self.newProjectNumber.get() + ')'
            self.cur.execute(query)
            self.conn.commit()
        
            self.updateCheckBoxes()
        else: print("Please Enter Values")


    

    
	######DELETE SITE FRAME

    def getFCData(self, fcurl, rpurl, node, site):
        print(str(site) + ":" + "\n" + "--FORECAST URL: " + str(fcurl) + "\n" + "--RECORDED RAINFALL URL: " + str(rpurl))
        newLocation = Location(fcurl, rpurl, node, self.browser, self.spinBox.get())
        data = newLocation.getAnswer()
        self.answerBox.insert(INSERT, data + '\n')
        self.precipString = self.precipString + str(newLocation.recordedRain) + '\n'


    def clicked(self): #When the getData Button is pressed

        self.precipString = ""
        self.answerBox.delete(1.0,END)
        print("DETAIL REPORT FOR EACH SITES: ")
        self.answerBox.insert(INSERT, "Forecast Data" + '\n')
        i = 0
        siteKeys = list(self.locations.keys())
        for item in self.locations:
            if(self.locations[item].get() == 1):
                pt = siteKeys[i][0]
                t = (pt,) #Creating a tuple so query can work, have to add "," at the end to make it work
                self.cur.execute("SELECT fcurl FROM SiteURL WHERE projectNumber = ?", t)
                fcfetch = self.cur.fetchone()
                self.cur.execute("SELECT rpurl FROM SiteURL WHERE projectNumber = ?", t)
                rpfetch = self.cur.fetchone()
                self.cur.execute("SELECT node FROM SiteURL WHERE projectNumber = ?", t)
                nodefetch = self.cur.fetchone()
                
                self.getFCData(fcfetch[0], rpfetch[0], nodefetch[0], siteKeys[i])
            i = i + 1
        self.answerBox.insert(INSERT, "Precip Accumulative Data" + '\n')
        self.answerBox.insert(INSERT, self.precipString)
        #self.dogCanvas.grid_remove()

    def updateCheckBoxes(self): #Called to update the check boxes everytime the database changes
        #update the dictionaries
        self.locations.clear()
        #locationsDel.clear()
        self.cur.execute("SELECT projectNumber, site FROM SiteURL ORDER BY projectNumber")
        sitesFetch = self.cur.fetchall() #sitesFetch is an array
        index = 0
        while(index < len(sitesFetch)):
            self.locations[sitesFetch[index]] = 0 #add to the location dictionary and set checks to 0
            index = index + 1
        self.locationsDel = dict(self.locations)

        #Destroy the frames to rebuild them
        for child in self.checkBoxFrame.winfo_children():
            child.destroy()
        for child in self.checkBoxFrameDel.winfo_children():
            child.destroy()
        self.data(self.checkBoxFrame, self.locations)
        self.data(self.checkBoxFrameDel, self.locationsDel)

    def data(self, frame, diction): #Creates all check box in check box frame
        for i in diction:
            diction[i] = IntVar()
            l = Checkbutton(frame, text = i, variable = diction[i])
            l.pack(side = TOP, anchor = W)

    def allOff(self):
        for i in self.locations:
            self.locations[i].set(0)
    def allOn(self):
        for i in self.locations:
            self.locations[i].set(1)

    def configureFunctionDel(self, event): 
        self.checkBoxCanvasDel.configure(scrollregion=self.checkBoxCanvasDel.bbox("all"),width=200,height=200)
  
    def configureFunction(self, event): 
        self.checkBoxCanvas.configure(scrollregion=self.checkBoxCanvas.bbox("all"),width=200,height=200)


#testGui = GUI()

def ukiahClicked():
    window.destroy()
    gui = GUI("Ukiah")
def eurekaClicked():
    window.destroy()
    gui = GUI("Eureka")
def santaRosaClicked():
    window.destroy()
    gui = GUI("Santa Rosa")


window = Tk() #window object
window.title("LACO FORECAST DATA APPLICATION 2018")
window.geometry('700x200')


Label(window, text="Welcome To LACO Forecast Program, Please Pick Your Office Location", font=("Helvetica", 15)).grid(column=1, columnspan = 3, row=1, pady=10,
                                                                          padx=10)
Button(window, text = "Ukiah", font = ("Comic Sans MS", 14), bg = "DeepSkyBlue2", command = ukiahClicked).grid(column = 1, row = 3, pady = 10, padx = 10)
Button(window, text = "Eureka", font = ("Comic Sans MS", 14), bg = "pale green", command = eurekaClicked).grid(column = 2, row = 3, pady = 10, padx = 10)
Button(window, text = "Santa Rosa", font = ("Comic Sans MS", 14), bg = "orange", command = santaRosaClicked).grid(column = 3, row = 3, pady = 10, padx = 10)

window.mainloop()


"""
# Creating a drop down box
        combo = ttk.Combobox(window)
        combo['values'] = (1,2,3,4,5,6, "text")
        combo.current(1)

# Creating Label and Button
lbl = Label(window, text="test label") #label is a text label

txt = Entry(window,width=10) #text input box 

def clicked():
    response = txt.get()
 
    lbl.configure(text= response)
btn = Button(window, text="Click Me", command=clicked) 

# Creating check button
check_value = BooleanVar()
check_value.set(True)
chkButton = Checkbutton(window, text = "choose", var = check_value)
"""











