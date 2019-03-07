class Ward_Data:
    def __init__(self, id, lat, lng, electorate, area, unionist, nationalist):
        self.id = id
        self.lng = lng
        self.lat = lat
        self.electorate = electorate
        self.area = area
        self.unionist = unionist
        self.nationalist = nationalist

    def get_id(self):
        return self.id

    def get_lng(self):
        return self.lng

    def get_lat(self):
        return self.lat
    
    def get_electorate(self):
        return self.electorate

    def get_area(self):
        return self.area

    def get_unionist(self):
        return self.unionist

    def get_nationalist(self):
        return self.nationalist
