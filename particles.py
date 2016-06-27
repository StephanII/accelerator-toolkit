import numpy as np


# -----------------------------------------------------------------------------------------
# 
# 

class Ion:
    def __init__(self, protons, neutrons, electrons, energy, x=0., dx=0., y=0., dy=0., dl=0., dp=0.):
        self.protons = protons
        self.neutrons = neutrons
        self.electrons = electrons
        self.energy = energy
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.dl = dl
        self.dp = dp

    def __repr__(self):
        r = "Ion(mass=" + str(self.mass) + "u, "
        r += "chargeState=" + str(self.charge) + "e, "
        r += "energy=" + str(self.energy) + "eV, "
        r += "x=" + str(self.x) + "m, "
        r += "dx=" + str(self.dx) + "rad, "
        r += "y=" + str(self.y) + "m, "
        r += "dy=" + str(self.dy) + "rad, "
        r += "dl=" + str(self.dl) + "m, "
        r += "dp=" + str(self.dp) + ")"
        return r

    def __str__(self):
        if self.charge>0:
            return str(self.mass_number) + self.nomenclature + "+" + str(self.charge)
        else:
            return str(self.mass_number) + self.nomenclature + str(self.charge)

    @property
    def charge(self):
        return self.protons-self.electrons

    @property
    def mass_number(self):
        return self.protons+self.neutrons

    @property
    def nomenclature(self):
        symbols = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na",
         "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti",
         "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
         "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru",
         "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs",
         "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
         "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir",
         "Pt", "Au", "Hg", "TI", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra",
         "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es",
         "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
         "Rg", "Cn", "Uut", "Fl", "Uup", "Lv"]
        if self.protons > 117:
            return "??"
        elif self.protons < 1:
            raise Exception("Number of protons < 1")
        else:
            return symbols[self.protons-1]

