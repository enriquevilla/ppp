class Memory:
    def __init__(self):
        self.ints = []
        self.floats = []
        self.chars = []

    def insertInt(self, val, vir_address):
        real_address = vir_address % 1000
        if len(self.ints) > real_address:
            self.ints[real_address] = val
        else:
            while len(self.ints) < real_address:
                self.ints.append(0)
            self.ints.append(val)

    def insertFloat(self, val, vir_address):
        real_address = vir_address % 1000
        if len(self.floats) > real_address:
            self.floats[real_address] = val
        else:
            while len(self.floats) < real_address:
                self.floats.append(0.0)
            self.floats.append(val)

    def insertChar(self, val, vir_address):
        real_address = vir_address % 1000
        if len(self.chars) > real_address:
            self.chars[real_address] = val
        else:
            while len(self.chars) < real_address:
                self.chars.append("")
            self.chars.append(val)

    def getInt(self, vir_address):
        real_address = vir_address % 1000
        return self.ints[real_address]

    def getFloat(self, vir_address):
        real_address = vir_address % 1000
        return self.floats[real_address]

    def getChar(self, vir_address):
        real_address = vir_address % 1000
        return self.chars[real_address]

    def printInts(self):
        print(self.ints)

    def printChars(self):
        print(self.chars)

    def adjustIntArrSize(self, supLim):
        realSup = supLim % 1000
        while len(self.ints) < realSup:
            self.ints.append(0)
        if len(self.ints) == 0:
            self.ints.append(0)

    def adjustFloatArrSize(self, supLim):
        realSup = supLim % 1000
        while len(self.floats) < realSup:
            self.floats.append(0.0)
        if len(self.floats) == 0:
            self.floats.append(0)

    def adjustCharArrSize(self, supLim):
        realSup = supLim % 1000
        while len(self.chars) < realSup:
            self.chars.append("")
        if len(self.chars) == 0:
            self.chars.append(0)
