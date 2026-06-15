class Routes:
    def get_distance(self):
        self.distance=0

    def get_duration(self):
        self.duration=0

    def get_expenditure(self):
        self.expenditure=0

    def get_timedelay(self):
        self.timedelay=0

    def get_carbonrate(self):
        self.carbonrate=0

    def get_rating(self):
        self.marks=0

    def add_badge(self,str):
        self.badge.append(str)
    
    def __init__(self,mode):
        self.mode=mode
        self.badges=[]
        self.get_distance()
        self.get_duration()
        self.get_expenditure()
        self.get_timedelay()
        self.get_carbonrate()
        self.get_rating()