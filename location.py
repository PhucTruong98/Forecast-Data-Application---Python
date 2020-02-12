import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from HourlyRain import HourlyRain

class Location():
  def __init__ (self, fcUrl, tpUrl, node, browser, hourOffset):
    self.fcUrl = fcUrl
    self.tpUrl = tpUrl
    
    self.chanceOfRain = ""

    self.pageFC = None
    self.treeFC = None


    self.chanceOfRainArray = None
    self.chanceOfRainArray2 = []
    self.amountOfRainArray = None
    self.amountOfRainArray2 = []

    self.rain24h = 0.00
    self.rain48h = 0.00
    self.rain72h = 0.00
    self.rain96h = 0.00
    self.FCStorm = 0.00
    self.qualify = "No"
    self.qualified = "No"
    self.totalRained = 0.00
    self.linkDict = {}
    self.pripList = []
######

    self.hasPrecipAcc = False
    self.has1HourPrecip = False
    self.has24HourPrecip = False
    self.node = node
    self.hourOffset = hourOffset
    self.browser = None
    self.pripColumnIndex = 0
    self.browser = browser
    self.browser.get(self.tpUrl)
    self.cleanRainList = []
    self.recordedRain = 0.00

    

    self.finalResult = ""

  def DONTSTOPMENOW(self):
    self.getChanceOfRain()
    self.getAmountOfRain()
    self.checkPripAvailability()
    self.fillUpCleanRainList()
    self.getRecordedRain()
    #self.getAnswer()

  
  def preProcess(self):
    
    self.pageFC = requests.get(self.fcUrl)
    self.treeFC = html.fromstring(self.pageFC.content)
    self.chanceOfRainArray = self.treeFC.xpath('//*[@id="mainTable"]/tr[10]/td[@class="tdbody"]/text()')
    self.amountOfRainArray = self.treeFC.xpath('//*[@id="mainTable"]/tr[12]/td[@class="tdbody"]/text()')

  def getChanceOfRain(self):
    self.preProcess()
    if(self.chanceOfRainArray[0] == "--"):
      self.chanceOfRainArray[0] = "0%"
    i = 0  
    while(i < 8):
      newStr = self.chanceOfRainArray[i].replace("%", "")
      self.chanceOfRainArray2.append(int(newStr))
      i = i + 1
    lowChance = 110
    highChance = 0
    for x in self.chanceOfRainArray2:
      if(lowChance >= x):
        lowChance = x
      if(highChance <= x):
        highChance = x
    self.chanceOfRain += str(lowChance) + '-' + str(highChance)
    

  def getAmountOfRain(self):
    if(self.amountOfRainArray[0] == u"\xa0"):
      self.amountOfRainArray[0] = '0.00"'
    for x in self.amountOfRainArray:
      newStr = x.replace('"', "" )
      self.amountOfRainArray2.append(float(newStr))
    
    #Populate the rest of the table
    size = len(self.amountOfRainArray2)
    if(size < 18):
      while(size <= 18):
        self.amountOfRainArray2.append(0.00)
        size += 1
    #print(self.amountOfRainArray2)
    self.rain24h = self.amountOfRainArray2[0] + self.amountOfRainArray2[1] + self.amountOfRainArray2[2] + self.amountOfRainArray2[3]

    self.rain48h = self.amountOfRainArray2[4] + self.amountOfRainArray2[5] + self.amountOfRainArray2[6] + self.amountOfRainArray2[7] + self.rain24h

    self.rain72h = self.amountOfRainArray2[8] + self.amountOfRainArray2[9] + self.amountOfRainArray2[10] + self.amountOfRainArray2[11] + self.rain48h

    self.rain96h = self.amountOfRainArray2[12] + self.amountOfRainArray2[13] + self.amountOfRainArray2[14] + self.amountOfRainArray2[15] + self.rain72h

    self.FCStorm = self.rain96h

    self.rain24h = round(self.rain24h, 2)
    self.rain48h = round(self.rain48h, 2)
    self.rain72h = round(self.rain72h, 2)
    self.rain96h = round(self.rain96h, 2)
    self.FCStorm = round(self.FCStorm, 2)




    #print(self.rain24h, self.rain48h, self.rain72h, self.rain96h)

    if(self.FCStorm >= 0.5):
      self.qualify = "Yes"
    else:
      self.qualify = "No"

  def checkPripAvailability(self): #check if the website has precip accumulation or hourly precip
    topRow = self.browser.find_elements_by_xpath('//*[@id="timeseries"]/table/tbody/tr[1]/th')
    i = 0
    while(i <= len(topRow)):
        try: 
            rowString = topRow[i].find_element_by_xpath(".//div").text
            rowString = rowString.replace("\n", "")

            if(rowString == "PrecipAccumulated(inches)"):
                print("--This site has Precip Accumulative")
                self.hasPrecipAcc = True
                self.pripColumnIndex = i + 1
                break
            if(rowString == "1 HourPrecip(inches)"):
                print("--This site has 1 hour Precip ")

                self.has1HourPrecip = True
                self.pripColumnIndex = i + 1
                break

            if(rowString == "24 HourPrecip(inches)"):
              print("--This site has 24 Hour Precip ")
              self.has24HourPrecip = True
              self.pripColumnIndex = i + 1
              break
            i = i + 1
        except:
            i = i + 1



  def fillUpCleanRainList(self):
    i = 0
    rainTable = self.browser.find_elements_by_xpath('//*[@id="timeseries"]/table/tbody/tr')
    if(self.hasPrecipAcc):
      currentRain = rainTable[1].find_element_by_xpath('.//td[' + str(self.pripColumnIndex) + ']').text
      pastHourRain = rainTable[int(self.hourOffset)].find_element_by_xpath('.//td[' + str(self.pripColumnIndex) + ']').text
      #if(currentRain == ""): currentRain = "0.00"
      #if(past24HourRain == ""): past24HourRain = "0.00"
      totalRain = float(currentRain) - float(pastHourRain)
      self.cleanRainList.append(round(totalRain, 2))
      print("--Calculated Rain Using Most Recent Precip Accumulation Subtracted By The One ", self.hourOffset, " Hours Before That: " + currentRain + " - " + pastHourRain + "\n")
    
    elif(self.has1HourPrecip):
      i = 1
      if(self.node == "None"): self.node = "00"
      while(i <= len(rainTable) - 1):
        precip = rainTable[i].find_element_by_xpath('.//td['+ str(self.pripColumnIndex) + ']').text
        dateString = rainTable[i].find_element_by_xpath('.//td[1]').text
        precipObj = HourlyRain(dateString, precip)
        if(precipObj.isANode(self.node)): self.cleanRainList.append(precipObj)
        i = i + 1

      print("--Calculated Rain Using The Sum Of Hourly Rain Records As Follow With Node: " + str(self.node))
      for item in self.cleanRainList:
        item.returnResult()

    elif(self.has24HourPrecip):
      if(self.hourOffset == "24"):
        currentRain = rainTable[1].find_element_by_xpath('.//td[' + str(self.pripColumnIndex) + ']').text
        self.cleanRainList.append(round(float(currentRain),2))
        print("--Calculated Rain Using The Most Recent 24 Hour Precipitation: " + str(currentRain))
      else:
        self.cleanRainList.append("#.##")
        print("--Unable to calculate rain since this site only has 24 Hours Precipitation and hour offset is in effect")


  def getRecordedRain(self):
    if(self.hasPrecipAcc or self.has24HourPrecip):
      self.recordedRain = self.cleanRainList[0]
    elif(self.has1HourPrecip):
      i = 0
      while(i < int(self.hourOffset)):
        print(self.cleanRainList[i].returnResult())
        self.recordedRain = self.recordedRain + self.cleanRainList[i].amount
        i = i + 1




    
  def getAnswer(self):
    #print("FORECAST DATA FOR ",self.locationName,'\n')
    #print("Chance Of Rain: ", self.chanceOfRain)
    #print("Forecasted Rain in 24 Hours: ", self.rain24h)
    #print("Forecasted Rain in 48 Hours: ", self.rain48h)
    #print("Forecasted Rain in 72 Hours: ", self.rain72h)
    #print("Forecasted Rain in 96 Hours: ", self.rain96h)
    #print("Forecasted Total Rain : ", self.FCStorm)
    #print("Accumulated Rain Fall : ", self.totalRained)
    #print("Qualifying event?: ", self.qualify)
    #print("\n","FINAL DATA TO BE EXPORTED FOR: ", self.locationName)
    #self.getAmountOfRain()
    self.DONTSTOPMENOW()
    self.finalResult += self.chanceOfRain + ' ' + str(self.rain24h) + ' ' + str(self.rain48h) + ' '+ str(self.rain72h) + ' '+ str(self.rain96h) #+ ' ' + str(self.recordedRain) 
    return self.finalResult

  
      
"""

browser = webdriver.Chrome()
testLocation1 = Location("https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.150167999999994&lon=-123.207777", "https://www.wrh.noaa.gov/mesowest/timeseries.php?sid=F2270&table=1&banner=off", "None", browser) #24 Hour
testLocation1.DONTSTOPMENOW()
print(testLocation1.cleanRainList, testLocation1.finalResult)

testLocation2 = Location("https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.150167999999994&lon=-123.207777", "https://www.wrh.noaa.gov/mesowest/getobext.php?wfo=eka&sid=KUKI&num=168&raw=0&dbn=m", "56", browser) #1 hour
testLocation2.DONTSTOPMENOW()
print(testLocation2.cleanRainList, testLocation2.finalResult)


testLocation3 = Location("https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.150167999999994&lon=-123.207777", "https://www.wrh.noaa.gov/mesowest/timeseries.php?sid=LAYC1&table=1&banner=off", "None", browser) #precip acc
testLocation3.DONTSTOPMENOW()
print(testLocation3.cleanRainList, testLocation3.finalResult)



"""


