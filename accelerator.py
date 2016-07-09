from sources import IonSource
from diagnostic import *
from magnets import *
from pipes import *
import xml.etree.ElementTree as ET


class Accelerator:
    def __init__(self, source=IonSource(), xml_root=None):

        if xml_root:
            self.devices = []
            for child in xml_root.iter():
                print(child.tag)
                if child.tag != 'accelerator':
                    instance = eval(child.tag)()
                    instance.from_xml(child)
                    #instance = eval(child.tag)(child.get('nomenclature'))
                    self.append_device(instance)
        else:
            self.source = source
            self.devices = [source]

    def __repr__(self):

        r = "Accelerator {\n"
        for device in self.devices:
            r += str("\t") + repr(device) + str("\n")
        r += "}"
        return r

    def append_device(self, device):

        if len(self.devices) > 0:
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

    def start_simulation(self, number_of_ions):

        self.source.run(number_of_ions)

    def to_xml(self):

        x = ET.Element('accelerator')
        for device in self.devices:
            device.to_xml(x)
        xml_byte_string = ET.tostring(element=x, method="xml", short_empty_elements=False, encoding='utf-8')
        return xml_byte_string.decode('UTF-8')

    def to_file(self, filename):

        f = open(filename, 'w')
        f.write(self.to_xml())
        f.close()

