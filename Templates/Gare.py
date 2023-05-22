from Templates.Aviao import Aviao

class Gare:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.type = tipo
        self.aviao = None
        
    def park_aviao(self, aviao):
        self.aviao = aviao

    def is_available(self):
        return self.aviao is None
        
    def dist(self, obj):
        return abs(self.x - obj.x) + abs(self.y - obj.y)
    
    def free_gare(self):
        self.aviao = None

    def get_tipo(self):
        return self.type

    def get_aviao(self):
        return self.aviao