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


class Activity:
    def __init__(self, name_of_activity, duration_of_activity, starting_point_of_activity):
        self.name = name_of_activity
        self.duration = duration_of_activity
        self.startingPoint = starting_point_of_activity

    def display_activity(self):
        return self.startingPoint, " - ", (self.startingPoint + self.duration), "   ", self.name

    def get_starting_point(self):
        return self.startingPoint

    def get_duration(self):
        return self.duration

    def get_name(self):
        return self.name

    def set_starting_point(self, new_starting_point):
        self.startingPoint = new_starting_point

    def set_duration(self, new_duration):
        self.duration = new_duration

    def set_name(self, new_name):
        self.name = new_name


class ScheduleForADay:
    def __init__(self):
        activity_list = []

        self.activityList = activity_list

        print("when do you wake up?")
        waking_time = float(input())
        self.wakingTime = float(waking_time)

    def user_assistant(self):
        print("would you like to add an Item or a Task to your schedule?")
        add = input()
        if add == "yes" or add == "true":
            print("what would it be?")
            name_of_activity = input()
            print("what the duration of Item in hours?")
            duration_of_activity = int(input())
            while duration_of_activity <= 0:
                print("what the duration of Item in hours?")
                duration_of_activity = input()
            print("from what hour?")
            starting_point_of_activity = input()
            new_activity = Activity(name_of_activity, duration_of_activity, starting_point_of_activity)
            self.activityList.append(new_activity)
            self.user_assistant()

    def output_schedule(self):
        arr_hours = [self.wakingTime]
        h = float(self.wakingTime+0.5)

        while h < 24.0:
            arr_hours.append(h)
            h = h + 0.5
        for i in range(len(arr_hours)):
            print(arr_hours[i],)
        webbrowser.open_new_tab('schedule.html')

    def add_item(self, name_of_task):
        self.items_list.append(name_of_task)

    def add_items_duration_in_hours(self, duration):
        self.items_duration_in_hours.append(duration)

    def add_items_start_time(self, starting_hour):
        self.items_duration_in_hours.append(starting_hour)


def main():
    sunday_schedule = ScheduleForADay()
    sunday_schedule.__init__()
    sunday_schedule.user_assistant()
    sunday_schedule.output_schedule()


if __name__ == '__main__':
    main()
