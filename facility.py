from unit import Unit

class Facility:
    def __init__(self, name, website, address, units):
        self.name = name
        self.website = website
        self.address = address
        self.units = units

    def setName(self, name):
        self.name = name

    def setWebsite(self, web):
        self.website = website

    def setUnits(self, units):
        self.units = units

    def printInfo(self):
        info = self.name + "\n" + self.website + "\n" + self.address + "\n"
        for u in self.units:
            info += u.info()
        info += "END"
        return info
