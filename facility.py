from unit import Unit

class Facility:
    def __init__(self,company, companywebsite, name, website, address, units):
        self.company = company
        self.companywebsite = companywebsite
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
        info = "-\n" + self.company + "\n"
        info += self.companywebsite + "\n~\n"
        info += self.name + "\n"
        info += self.website + "\n" # website
        # members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        # print(members)
        info += self.address + "\n" # street address 1
        info += "\n"                # street address 2
        info += "\n"                # city
        info += "\n"                # state
        info += "\n"                # zip
        info += "\n"                # country
        info += self.website + "\n" # website
        info += "\n"                # setUpFee
        info += "\n"                # percent full
        info += "\n"                # hasRetailStore
        info += "\n"                # hasInsurance
        info += "\n"                # hasOnlineBillPay
        info += "\n"                # hasWineStorage
        info += "\n"                # hasKiosk
        info += "\n"                # hasOSM
        info += "\n"                # hasCameras
        info += "\n"                # hasVP
        info += "\n"                # hasCL
        info += "\n"                # hasOSS
        info += "\n"                # hasAutopay
        info += "\n"                # hasOC
        info += "\n"                # hasPM
        info += "\n"                # hasML
        info += "\n"                # hasEL
        info += "\n"                # hasPLB
        info += "\n"                # MO
        info += "\n"                # MC
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"
        info += "\n"                # SO
        info += "\n"                # SC
        info += "\n"                # rating
        info += "\n"                # promos
        self.units = set(self.units)
        for u in self.units:
            info += u.info()
        return info
