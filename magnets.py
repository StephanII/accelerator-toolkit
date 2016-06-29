from base import Device
import math as math


# -----------------------------------------------------------------------------------------
# M_Dipol
# 

class SectorBendingMagnet(Device):
    def __init__(self, nomenclature, width, height, length, angle):

        Device.__init__(self, nomenclature, width, height, length)
        self.angle = angle

    def __repr__(self):

        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "angle=" + str(self.angle) + "rad)"
        return r

    def transport(self, ion):

        if self.angle == 0:
            ion.x += self.length * ion.dx
            ion.y += self.length * ion.dy
        else:
            radius = self.length / self.angle
            cos_angle = math.cos(self.angle)
            sin_angle = math.sin(self.angle)

            x = cos_angle * ion.x
            x += radius * sin_angle * ion.dx
            x += radius * (1. - cos_angle) * ion.dp

            dx = -(1. / radius) * sin_angle * ion.x
            dx += cos_angle * ion.dx + sin_angle * ion.dp

            y = ion.y + self.length * ion.dy

            dl = -sin_angle * ion.x
            dl -= radius * (1. - cos_angle) * ion.dx
            dl -= radius * (self.length - radius * sin_angle) * ion.dp

            ion.x = x
            ion.dx = dx
            ion.y = y
            ion.dl = dl
        self.forward_if_not_lost(ion)


# -----------------------------------------------------------------------------------------
# 
# M_kante*M_Dipole*M_Kante

class RectangleBendingMagnet(Device):
    pass


# -----------------------------------------------------------------------------------------
# 
# 

class HorizontalKickerMagnet(Device):
    def __init__(self, nomenclature, width, height, angle=0.):

        Device.__init__(self, nomenclature, width, height)
        self.angle = angle

    def __repr__(self):

        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "angle=" + str(self.angle) + "rad)"
        return r

    def transport(self, ion):

        ion.dx += self.angle
        self.forward_if_not_lost(ion)


# -----------------------------------------------------------------------------------------
# 
# 

class QuadrupoleMagnet(Device):
    def __init__(self, nomenclature, width, height, length, strength=0.):

        Device.__init__(self, nomenclature, width, height, length)
        self.strength = strength

    def __repr__(self):

        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "strength=" + str(self.strength) + "rad)"
        return r

    def transport(self, ion):
        sqrts = math.sqrt(abs(self.strength))
        omega = self.length * sqrts

        cosomega = math.cos(omega)
        coshomega = math.cosh(omega)
        sinomega = math.sin(omega)
        sinhomega = math.sinh(omega)

        if self.strength < 0:
            x = cosomega * ion.x + (sinomega / sqrts) * ion.dx
            dx = -sinomega * sqrts * ion.x + cosomega * ion.dx
            y = coshomega * ion.y + (sinhomega / sqrts) * ion.dy
            dy = sinhomega * sqrts * ion.y + coshomega * ion.dy
            ion.x = x
            ion.dx = dx
            ion.y = y
            ion.dy = dy
        elif self.strength > 0:
            x = coshomega * ion.x + (sinhomega / sqrts) * ion.dx
            dx = sinhomega * sqrts * ion.x + coshomega * ion.dx
            y = cosomega * ion.y + (sinomega / sqrts) * ion.dy
            dy = -sinomega * sqrts * ion.y + cosomega * ion.dy
            ion.x = x
            ion.dx = dx
            ion.y = y
            ion.dy = dy
        else:
            ion.x += self.length * ion.dx
            ion.y += self.length * ion.dy

        self.forward_if_not_lost(ion)

# -----------------------------------------------------------------------------------------
# 


class SixtupoleMagnet(Device):
    pass
