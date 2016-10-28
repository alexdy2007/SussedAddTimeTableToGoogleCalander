from getClasses import getClasses
from addToCalender import addTocalendar

def run():
    print("Starting")
    getNumberOfWeekInAdvance = 2
    try:
        timeTableClasses = getClasses(getNumberOfWeekInAdvance)
    except Exception as e:
        print(format("A error has occured in retriving classes : {}", str(e)))
    try:
        addTocalendar(timeTableClasses)
    except Exception as e:
        print(format("A error has occured in adding to calendar: {}", str(e)))
    print("Finished")

if __name__ == "__main__":
    run()



