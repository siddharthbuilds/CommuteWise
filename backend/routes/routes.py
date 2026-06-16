class Routes:

    @classmethod
    def from_dict(cls, route_dict):
        return cls(
            mode=route_dict["mode"],
            stops=route_dict["stops"],
            segments=route_dict["segments"],
            duration=route_dict["duration"],
            distance=route_dict["distance"]
        )


    def get_expenditure(self):
        self.expenditure=5

    def get_timedelay(self):
        self.timedelay=0

    def get_carbonrate(self):
        self.carbonrate=5

    def get_rating(self,max_values):
        self.rating=0
        current_values=[self.distance,self.duration,self.expenditure,self.timedelay,self.carbonrate]
        rating_weights=[0.20,0.35,0.25,0.10,0.10]
        i=0
        while(i<5):
            normalised_value=((1-(current_values[i]/max_values[i]))*100)
            self.rating+=normalised_value*rating_weights[i]
            i+=1
        self.rating = round(self.rating / 10, 2)

    def add_badge(self,str):
        self.badges.append(str)
    
    def __init__(self,mode,stops,segments,duration,distance):
        self.mode=mode
        self.stops=stops
        self.segments=segments
        self.duration=duration
        self.distance=distance
        self.badges=[]
        self.get_expenditure()
        self.get_timedelay()
        self.get_carbonrate()