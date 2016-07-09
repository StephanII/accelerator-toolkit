from base import Device
from particles import Ion
from random import gauss


class IonSource(Device):
    def __init__(self, protons=92, neutrons=146, electrons=19, extraction_energy=5000.):

        Device.__init__(self, "Penning Ion Source", 0, 0)
        self.protons = protons
        self.neutrons = neutrons
        self.electrons = electrons
        self.extraction_energy = extraction_energy

    def __repr__(self):

        r = str(self) + "("
        r += "protons=" + str(self.protons) + ", "
        r += "neutrons=" + str(self.neutrons) + ", "
        r += "electrons=" + str(self.electrons) + ", "
        r += "extraction_energy=" + str(self.extraction_energy) + "eV)"
        return r

    def append_device(self, device):

        self.next = device

    def run(self, number_of_ions):

        for i in range(0, number_of_ions):
            x = gauss(mu=0, sigma=0.01)
            dx = gauss(mu=0, sigma=0.005)
            y = gauss(mu=0, sigma=0.01)
            dy = gauss(mu=0, sigma=0.001)
            dl = gauss(mu=0, sigma=0.001)
            dp = gauss(mu=0, sigma=0.01)

            ion = Ion(self.protons, self.neutrons, self.electrons, self.extraction_energy, x, dx, y, dy, dl, dp)

            if self.next:
                self.next.transport(ion)

    def xml_add_properties(self, element):
        element.set("protons", str(self.protons))
