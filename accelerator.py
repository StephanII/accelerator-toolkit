from sources import *
from diagnostic import *
from magnets import *
from pipes import *
import xml.etree.ElementTree as ET


class Accelerator:
    def __init__(self, source=IonSource(), xml_root=None):

        if xml_root:
            self.devices = []
            for child in xml_root.iter():
                if child.tag != 'accelerator':
                    instance = eval(child.tag)()
                    instance.from_xml(child)
                    self.append_device(instance)
        else:
            self.devices = [source]

    def __repr__(self):

        r = "Accelerator {\n"
        for device in self.devices:
            r += str("\t") + repr(device) + str("\n")
        r += "}"
        return r

    def append_device(self, device):

        if device in self.devices:
            raise Exception("error, device " + str(device) + " is already part of this accelerator")
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

    def get_devices_by_class_name(self, class_name):
        pass

    def reset(self):

        if len(self.devices) > 1:
            self.devices[1].reset()

    def start_simulation(self, number_of_ions):

        self.devices[0].run(number_of_ions)

    def to_xml(self):

        xml_root = ET.Element('accelerator')
        for device in self.devices:
            device.to_xml(xml_root)
        xml_byte_string = ET.tostring(element=xml_root, method="xml", short_empty_elements=True, encoding='utf-8')
        return xml_byte_string.decode('UTF-8').replace(">", ">\n")

    def to_file(self, filename):

        f = open(filename, 'w')
        f.write(self.to_xml())
        f.close()

