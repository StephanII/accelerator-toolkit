from base import Device


class Pipe(Device):
    def __init__(self, width=0, height=0, length=0):
        Device.__init__(self, "", width, height, length)

    def __repr__(self):
        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m)"
        return r

    def transport(self, ion):

        ion.x += self.length * ion.dx
        ion.y += self.length * ion.dy
        self.forward_if_not_lost(ion)
