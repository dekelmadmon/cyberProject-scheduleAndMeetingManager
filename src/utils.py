import webbrowser

'''print("how many hours would you like to sleep?")
        sleeptime= input()
        self.sleeptime= sleeptime
        print("how many hours would you like to sleep?")
        sleeptime = input()
        self.workoutTime= workoutTime
        self.workTime= workTime
        self.restTime=restTime'''
Time = 24*60
class activity:
    def __init__(self, nameOfActivity, durationOfActivity, startingPointOfActivity):
        self.name = nameOfActivity
        self.duration = durationOfActivity
        self.startingPoint = startingPointOfActivity

    def displayActivity(self):
        return(self.startingPoint, " - ", (self.startingPoint + self.duration), "   ", self.name)
    def getStartingPoint(self):
        return self.startingPoint
    def getDuration(self):
        return self.duration
    def getName(self):
        return self.name
    def setStartingPoint(self, newStartingPoint):
        self.startingPoint = newStartingPoint
    def setStartingPoint(self, newDuration):
        self.duration = newDuration
    def setName(self, newName):
        self.name = newName
class scheduleForADay:
    def __init__(self):
        activityList= []

        self.activityList = activityList

        print ("when do you wake up?")
        wakingTime = float(input())
        self.wakingTime = float(wakingTime)
    def userAssistant(self):
        print("would you like to add an Item or a Task to your schedule?")
        add = input()
        if (add=="yes" or add == "true"):
            print("what would it be?")
            nameOfActivity = input()
            print("what the duration of Item in hours?")
            durationOfActivity = int(input())
            while (durationOfActivity<=0):
                print("what the duration of Item in hours?")
                durationOfActivity = input()
            print("from what hour?")
            startingPointOfActivity = input()
            newActivity = activity
            newActivity.__innit__(newActivity, nameOfActivity, durationOfActivity, startingPointOfActivity)
            self.activityList.append(newActivity)
            self.userAssistant()
    def outputSchedule(self):
        arrHours = [self.wakingTime]
        h = float(self.wakingTime+0.5)

        while(h<24.0):
            arrHours.append(h)
            h = h + 0.5
        for i in range(len(arrHours)):
            print (arrHours[i],)
        webbrowser.open_new_tab('schedule.html')


    def addItem(self, nameOfTask):
        self.ItemsList.append(nameOfTask)
    def addItemsDurationInHours(self, duration):
        self.ItemsDurationInHours.append(duration)
    def addItemsStartTime(self, StartingHour):
        self.ItemsDurationInHours.append(StartingHour)
def main():
    sundaySchedule=scheduleForADay()
    sundaySchedule.__innit__()
    sundaySchedule.userAssistant()
    sundaySchedule.outputSchedule()
if __name__ == '__main__':
    main()



