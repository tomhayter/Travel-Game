import random
import time

class DateTime:
    def __init__(self, day=1, hour=0, minute=0):
        self.day = day
        self.hour = hour
        self.minute = minute

    def get_total_minutes(self):
        return (self.hour * 60) + self.minute

    def add_time(self, hour, minute):
        self.minute += minute
        if self.minute >= 60:
            self.minute - 60
            self.hour += 1
        self.hour += hour
        if self.hour >= 24:
            self.hour - 24
            self.day += 1
    
    def __str__(self):
        h_string = f"{self.hour}"
        m_string = f"{self.minute}"
        if self.hour < 10:
            h_string = f"0{self.hour}"
        if self.minute < 10:
            m_string = f"0{self.minute}"
        return f"Day  {self.day}\n{h_string}:{m_string}"
    
    def get_time_string(self):
        h_string = f"{self.hour}"
        if self.hour < 10:
            h_string = f"0{self.hour}"
        if self.minute < 10:
            return f"{h_string}:0{self.minute}"
        return f"{h_string}:{self.minute}"

    def before(self, other_time):
        if self.day != -1 and other_time.day != -1:
            if self.day < other_time.day:
                return True
            if self.day > other_time.day:
                return False
        if self.hour < other_time.hour:
            return True
        if self.hour > other_time.hour:
            return False
        if self.minute < other_time.minute:
            return True
        return False

def generate_random_time():
    random.seed(time.time() * 1000)
    day = -1
    hour = random.randint(6, 22)
    minute = random.randint(0, 59)
    return DateTime(day, hour, minute)

def minutes_to_time_string(mins):
    if mins < 60:
        return f"{mins}m"
    else:
        hours = mins // 60
        new_mins = mins % 60
        return f"{hours}h {new_mins}m"


class Clock:
    def __init__(self):
        self.datetime = DateTime(1, 7)

    def tick(self):
        self.datetime.minute += 1
        if self.datetime.minute >= 60:
            self.datetime.minute = 0
            self.datetime.hour += 1
        if self.datetime.hour >= 24:
            self.datetime.hour = 0
            self.datetime.day += 1

    def pass_time(self, hour, minute):
        self.datetime.add_time(hour, minute)

    def set_time(self, time, tomorrow):
        if tomorrow:
            self.datetime.day +=1
        self.datetime.hour = time.hour
        self.datetime.minute = time.minute

    def __str__(self):
        return f"{self.datetime}"
