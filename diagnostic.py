from base import Device
import matplotlib.pyplot as plt
from multiprocessing import Lock, Value, Array
import multiprocessing


# -----------------------------------------------------------------------------------------
# 
# 

class Transformator(Device):
    def __init__(self, nomenclature, width, height):

        Device.__init__(self, nomenclature, width, height)
        self.count = Value('i', 0)

    def __repr__(self):

        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "count=" + str(self.count.value) + ")"

    def transport(self, ion):
        if not self.is_particle_lost(ion):
            with self.count.get_lock():
                self.count.value += 1
            if self.next:
                return self.next.transport(ion)

    def reset(self):

        self.count.value = 0
        if self.next:
            self.next.reset()


# -----------------------------------------------------------------------------------------
# 
# 

class Screen(Device):
    def __init__(self, nomenclature, width, height, screenWidth, screenHeight):

        Device.__init__(self, nomenclature, width, height)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.count = Array('i', 10000)

    def __repr__(self):

        r = "Screen " + self.nomenclature + " (width=" + str(self.width) + "m, height=" + str(
            self.height) + "m, screenWidth=" + str(self.screenWidth) + "m, screenHeight=" + str(
            self.screenHeight) + "m)"
        return r

    def transport(self, ion):

        if not self.is_particle_lost(ion):

            self.collect(ion)
            if self.next:
                return self.next.transport(ion)
            else:
                return ion
        else:
            return None

    def collect(self, ion):

        half_screen_width = 0.5 * self.screenWidth
        half_screen_height = 0.5 * self.screenHeight
        cell_width = 0.01 * self.screenWidth
        cell_height = 0.01 * self.screenHeight

        if half_screen_width > ion.x > -half_screen_width and half_screen_height > ion.y > -half_screen_height:
            x = int((ion.x + half_screen_width) / cell_width)
            y = int((ion.y + half_screen_height) / cell_height)
            with self.count.get_lock():
                self.count[100*x+y] += 1

    def reset(self):

        self.count = Array('i', 10000)
        if self.next:
            self.next.reset()

    def show(self):

        x = []
        y = []
        z = []

        for i in range(100):
            for j in range(100):
                x.append(float(i))
                y.append(float(j))
                z.append(float(self.count[100*i+j]))

        plt.hist2d(x, y, bins=100, weights=z)
        plt.colorbar()
        plt.show()


# -----------------------------------------------------------------------------------------
# 
# 

class Slit(Device):
    def __init__(self, nomenclature, width, height):

        Device.__init__(self, nomenclature, width, height)
        self.xpos_left = -0.5 * width
        self.xpos_right = 0.5 * width
        self.ypos_bottom = -0.5 * height
        self.ypos_top = 0.5 * height
        self.count_left = Value('i', 0)
        self.count_right = Value('i', 0)
        self.count_bottom = Value('i', 0)
        self.count_top = Value('i', 0)

    def __repr__(self):

        r = "Slit " + self.nomenclature + " ("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "xpos_left=" + str(self.xpos_left) + "m, "
        r += "xpos_right=" + str(self.xpos_right) + "m, "
        r += "ypos_bottom=" + str(self.ypos_bottom) + "m, "
        r += "ypos_top=" + str(self.ypos_top) + "m"
        r += "count_left=" + str(self.count_left.value) + " particles"
        r += "count_right=" + str(self.count_right.value) + " particles"
        r += "count_bottom=" + str(self.count_bottom.value) + " particles"
        r += "count_top=" + str(self.count_top.value) + " particles"
        r += ")"
        return r

    def transport(self, ion):

        if not self.is_particle_lost(ion) and not self.collect(ion):

            if self.next:
                return self.next.transport(ion)
            else:
                return ion
        else:
            return None

    def collect(self, ion):

        if ion.x < self.xpos_left:
            with self.count_left.get_lock():
                self.count_left.value += 1
            return True
        elif ion.x > self.xpos_right:
            with self.count_right.get_lock():
                self.count_right.value += 1
            return True
        elif ion.y < self.ypos_bottom:
            with self.count_bottom.get_lock():
                self.count_bottom.value += 1
            return True
        elif ion.y > self.ypos_top:
            with self.count_top.get_lock():
                self.count_top.value += 1
            return True
        else:
            return False

    def reset(self):

        self.count_left.value = 0
        self.count_right.value = 0
        self.count_bottom.value = 0
        self.count_top.value = 0

        if self.next:
            self.next.reset()

    def set_positions(self, xpos_left, xpos_right, ypos_bottom, ypos_top):

        self.xpos_left = xpos_left
        self.xpos_right = xpos_right
        self.ypos_bottom = ypos_bottom
        self.ypos_top = ypos_top
