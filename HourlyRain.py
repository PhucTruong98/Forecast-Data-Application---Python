class HourlyRain():
  def __init__(self, dateString, onePrip):
    self.string = dateString
    stringArray = dateString.split()
    timeArray = stringArray[2].split(":")
    self.date = int(stringArray[0])
    self.month = self.turnToMonth(stringArray[1])
    self.hour = int(timeArray[0])
    self.minute = int(timeArray[1])
    self.amOrpm = stringArray[3]
    if(onePrip == "T" or onePrip == ""): self.amount = 0.00
    else: self.amount = round(float(onePrip),2)
    
  def turnToMonth(self, monthString):
    if(monthString == "Jan"): return 1
    elif(monthString == "Feb"): return 2
    elif(monthString == "Mar"): return 3
    elif(monthString == "Apr"): return 4
    elif(monthString == "May"): return 5
    elif(monthString == "Jun"): return 6
    elif(monthString == "Jul"): return 7
    elif(monthString == "Aug"): return 8
    elif(monthString == "Sep"): return 9
    elif(monthString == "Oct"): return 10
    elif(monthString == "Nov"): return 11
    elif(monthString == "Dec"): return 12

  def isANode(self, nodeNumber):
          if(self.minute == int(nodeNumber)): return True
          else: return False

  def returnResult(self):
    if(self.amount == ""):
      result = self.string +  " 0.00"
    else:
      result = self.string + " " + str(self.amount)
    return result


                        

    


#testOb = HourlyRain("04 Apr 7:56 am", "1.3")
#print(testOb.date, testOb.month, testOb.hour, testOb.minute, testOb.amOrpm, testOb.isANode())

    


