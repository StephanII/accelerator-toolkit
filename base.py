import numpy as np


class Device(object):
    def __init__(self, nomenclature, width, height, length=0.):

        self.nomenclature = nomenclature
        self.width = width
        self.height = height
        self.length = length
        self.previous = None
        self.next = None
        self.transportMatrix = None

    def __str__(self):

        if self.nomenclature != "":
            return self.nomenclature
        else:
            return self.__class__.__name__

    def append_device(self, device):

        self.next = device
        device.previous = self

    def forward_if_not_lost(self, ion):

        if not self.is_particle_lost(ion):
            if self.next:
                self.next.transport(ion)

    def reset(self):

        if self.next:
            self.next.reset()

    def is_particle_lost(self, ion):

        return (4 * (ion.x ** 2) / (self.width ** 2) + 4 * (ion.y ** 2) / (self.height ** 2)) > 1
