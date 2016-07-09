from base import Device
import matplotlib.pyplot as plt
from multiprocessing import Value, Array


class Transformator(Device):
    def __init__(self, nomenclature="", width=0, height=0):

        Device.__init__(self, nomenclature, width, height)
        self.count = Value('i', 0)

    def __repr__(self):

        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "count=" + str(self.count.value) + ")"
        return r

    def transport(self, particle):
        if not self.is_particle_lost(particle):
            with self.count.get_lock():
                self.count.value += 1
            if self.next:
                return self.next.transport(particle)

    def reset(self):

        self.count.value = 0
        if self.next:
            self.next.reset()


class ProfileGrid(Device):
    def __init__(self, nomenclature="", width=0, height=0, number_of_wires_h=100, number_of_wires_v=100):
        Device.__init__(self, nomenclature, width, height)
        self.number_of_wires_horizontal = number_of_wires_h
        self.number_of_wires_vertical = number_of_wires_v
        self.count_h = Array('i', 100)
        self.count_v = Array('i', 100)

    def __repr__(self):
        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "number_of_wires_h=" + str(self.number_of_wires_h) + "m, "
        r += "number_of_wires_v=" + str(self.number_of_wires_v) + "m )"
        return r

    def transport(self, particle):
        pass

    def reset(self):
        self.count_h = Array('i', 10000)
        self.count_v = Array('i', 10000)
        if self.next:
            self.next.reset()


class Screen(Device):
    def __init__(self, nomenclature="", width=0, height=0, screen_width=0, screen_height=0):

        Device.__init__(self, nomenclature, width, height)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.count = Array('i', 10000)

    def __repr__(self):

        r = str(self) + "("
        r += "width=" + str(self.width) + "m, "
        r += "height=" + str(self.height) + "m, "
        r += "length=" + str(self.length) + "m, "
        r += "screen_width=" + str(self.screen_width) + "m, "
        r += "screen_height=" + str(self.screen_height) + "m )"
        return r

    def transport(self, particle):

        if not self.is_particle_lost(particle):

            self.collect(particle)
            if self.next:
                return self.next.transport(particle)
            else:
                return particle
        else:
            return None

    def collect(self, particle):

        half_screen_width = 0.5 * self.screenWidth
        half_screen_height = 0.5 * self.screenHeight
        cell_width = 0.01 * self.screenWidth
        cell_height = 0.01 * self.screenHeight

        if half_screen_width > particle.x > -half_screen_width and half_screen_height > particle.y > -half_screen_height:
            x = int((particle.x + half_screen_width) / cell_width)
            y = int((particle.y + half_screen_height) / cell_height)
            with self.count.get_lock():
                self.count[100 * x + y] += 1

    def num_of_particles(self):
        c = 0
        for i in self.count:
            c += i
        return c

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
                z.append(float(self.count[100 * i + j]))

        plt.hist2d(x, y, bins=100, weights=z)
        plt.colorbar()
        plt.show()


# -----------------------------------------------------------------------------------------
# 
# 

class Slit(Device):
    def __init__(self, nomenclature="", width=0, height=0):

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

    def transport(self, particle):

        if not self.is_particle_lost(particle) and not self.collect(particle):

            if self.next:
                return self.next.transport(particle)
            else:
                return particle
        else:
            return None

    def collect(self, particle):

        if particle.x < self.xpos_left:
            with self.count_left.get_lock():
                self.count_left.value += 1
            return True
        elif particle.x > self.xpos_right:
            with self.count_right.get_lock():
                self.count_right.value += 1
            return True
        elif particle.y < self.ypos_bottom:
            with self.count_bottom.get_lock():
                self.count_bottom.value += 1
            return True
        elif particle.y > self.ypos_top:
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
