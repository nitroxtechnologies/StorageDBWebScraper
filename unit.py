import re
class Unit:
    def setName(self, name):
        self.name = name

    def setPrice(self, price):
        self.price = (''.join(ele for ele in price if ele.isdigit() or ele == '.'))


    def setDimensions(self, s):
        dims = re.split("x", s, flags=re.IGNORECASE)
        # print(dims)
        if (len(dims) < 1):
            self.width = ""
            self.depth = ""
        else:
            self.width = (''.join(ele for ele in dims[0] if ele.isdigit() or ele == '.'))
            self.depth = (''.join(ele for ele in dims[1] if ele.isdigit() or ele == '.'))


    def setType(self, s):
        self.type = s

    def setFloor(self, f):
        self.floor = f

    def __init__(self, name, price, type, floor):
        self.name = name
        self.price = price
        self.type = type
        self.floor = floor
        self.setDimensions(name)

    def info(self):
        return self.name + "," + self.price + "," + self.type + "," + self.floor + "," + self.width + "," + self.depth + "\n"

    def __str__(self):
        return "name=" + self.name + "\nprice=" + self.price + "\ntype=" + self.type + "\nfloor=" + self.floor + "\nwidth=" + self.width + " \ndepth=" + self.depth + "\n\n"
    def __repr__(self):
        return "name=" + self.name + "\nprice=" + self.price + "\ntype=" + self.type + "\nfloor=" + self.floor + "\nwidth=" + self.width + " \ndepth=" + self.depth + "\n\n"
#TODO: name, type, width, depth, floor
