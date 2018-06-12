class Unit:
    def __init__(self, price, name, size):
        self.name = name
        self.price = price
        self.size = size

    def __str__(self):
        return "Name: " + self.name + "\nPrice: " + self.price + "\nSize: " + self.size + "\n\n"

    def setName(self, name):
        self.name = name

    def setPrice(self, price):
        self.price = price

    def setSize(self, size):
        self.size = size
