import re
class Unit:
    def setName(self, name):
        self.name = name

    def setPrice(self, price):
        self.price = (''.join(ele for ele in price if ele.isdigit() or ele == '.'))
        if "." not in self.price:
            self.price += ".00"


    def setDimensions(self, s):
        dims = re.split("x", s, flags=re.IGNORECASE)
        # print(dims)
        if (len(dims) < 1):
            self.width = ""
            self.depth = ""
        else:
            self.width = (''.join(ele for ele in dims[0] if ele.isdigit() or ele == '.'))
            self.depth = (''.join(ele for ele in dims[1] if ele.isdigit() or ele == '.'))
        self.name = self.width + "' x " + self.depth + "'"


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

    def __eq__(self, other):
        return self.name==other.name and self.floor == other.floor and self.type == other.type
    def __hash__(self):
        return hash(('name', self.name,
                     'type', self.type, 'floor', self.floor))

    def info(self):
        info = ".\n"
        info += self.name + "\n"
        if self.type == "":
            self.type = "Non-Climate"
        info += self.type + "\n"
        info += self.width + "\n"
        info += self.depth + "\n"
        info += "\n"
        if self.floor == "":
            self.floor = "1"
        info += self.floor + "\n"
        info += "\n"
        info += "\n"
        if self.price == "":
            self.price = "0.00"
        info += self.price + "\n"
        info += "\n"
        return info

    def __str__(self):
        return "name=" + self.name + "\nprice=" + self.price + "\ntype=" + self.type + "\nfloor=" + self.floor + "\nwidth=" + self.width + " \ndepth=" + self.depth + "\n\n"
    def __repr__(self):
        return "name=" + self.name + "\nprice=" + self.price + "\ntype=" + self.type + "\nfloor=" + self.floor + "\nwidth=" + self.width + " \ndepth=" + self.depth + "\n\n"
#TODO: name, type, width, depth, floor
