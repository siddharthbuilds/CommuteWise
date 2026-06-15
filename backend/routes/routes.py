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

    def get_rating(self,max_values):
        self.rating=0
        current_values=[self.distance,self.duration,self.expenditure,self.timedelay,self.carbonrate]
        rating_weights=[0.20,0.35,0.25,0.05,0.15]
        i=0
        while(i<5):
            normalised_value=((1-(current_values[i]/max_values[i]))*100)
            self.rating+=normalised_value*rating_weights[i]
            i+=1

    def add_badge(self,str):
        self.badges.append(str)
    
    def __init__(self,mode):
        self.mode=mode
        self.badges=[]
        self.get_distance()
        self.get_duration()
        self.get_expenditure()
        self.get_timedelay()
        self.get_carbonrate()