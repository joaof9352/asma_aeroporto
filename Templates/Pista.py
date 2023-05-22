
class Pista:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.assigned_plane = None

    def assign_plane(self, aviao):
        self.assigned_plane = aviao

    def dist(self, obj):
        return abs(self.x - obj.x) + abs(self.y - obj.y)
    
    def is_available(self):
        return self.assigned_plane is None

    def free_pista(self):
        self.assigned_plane = None