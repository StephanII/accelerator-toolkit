from multiprocessing import Queue

from base import Device
import sources
import multiprocessing
from multiprocessing import Process

# -----------------------------------------------------------------------------------------
# 
# 

class Accelerator:
    def __init__(self, source=sources.IonSource()):

        self.source = source
        self.devices = [source]

    def __repr__(self):

        r = "Accelerator {\n"
        for device in self.devices:
            r += "\t" + repr(device) + "\n"
        r += "}";
        return r

    def append_device(self, device):

        self.devices[-1].append_device(device)
        self.devices.append(device)

    def append_devices(self, devices):

        for device in devices:
            self.append_device(device)

    def get_device_by_nomenclature(self, nomenclature):
        for device in self.devices:
            if device.nomenclature == nomenclature:
                return device

    def reset(self):
        if len(self.devices) > 1:
            self.devices[1].reset()

    def start_simulation(self, numberOfIons):



        #print("starting simulation with ", numberOfIons, " ions")
        self.source.run(numberOfIons)
        #print("simulation finished")
