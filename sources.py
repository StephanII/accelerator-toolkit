from particles import Ion
from random import gauss


class IonSource:
    def __init__(self, protons=92, neutrons=146, electrons=19, extraction_energy=5000.):

        self.nomenclature = "Penning Ion Source"
        self.protons = protons
        self.neutrons = neutrons
        self.electrons = electrons
        self.extraction_energy = extraction_energy
        self.firstDevice = None

    def __repr__(self):

        r = "IonSource (mass=" + str(self.mass) + "u, chargeState=" + str(
            self.chargeState) + "e, extractionEnergy=" + str(self.extraction_energy) + "eV)"
        return r

    def append_device(self, device):

        self.firstDevice = device

    def run(self, number_of_ions):

        for i in range(0, number_of_ions):
            x = gauss(mu=0, sigma=0.01)
            dx = gauss(mu=0, sigma=0.005)
            y = gauss(mu=0, sigma=0.01)
            dy = gauss(mu=0, sigma=0.001)
            dl = gauss(mu=0, sigma=0.001)
            dp = gauss(mu=0, sigma=0.01)

            ion = Ion(self.protons, self.neutrons, self.electrons, self.extraction_energy, x, dx, y, dy, dl, dp)

            if self.firstDevice:
                self.firstDevice.transport(ion)

