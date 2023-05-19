
class Pista:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.landing_plane = None

    def land_plane(self, aviao):
        self.landing_plane = aviao

    def dist(self, obj):
        return abs(self.x - obj.x) + abs(self.y - obj.y)
    
    def is_available(self):
        return self.landing_plane is None