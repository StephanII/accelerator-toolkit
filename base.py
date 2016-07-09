import xml.etree.ElementTree as ET


class Device(object):
    def __init__(self, nomenclature, width, height, length=0., aperture_type=1):

        self.nomenclature = nomenclature
        self.width = width
        self.height = height
        self.length = length
        self.aperture_type = aperture_type
        self.previous = None
        self.next = None

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
        if self.aperture_type == 1:
            # ellipse
            return (4 * (ion.x ** 2) / (self.width ** 2) + 4 * (ion.y ** 2) / (self.height ** 2)) > 1
        elif self.aperture_type == 2:
            # rectangle
            return ion.x < -0.5 * self.width or \
                ion.x > 0.5 * self.width or \
                ion.y < -0.5 * self.height or \
                ion.y > 0.5 * self.height
        else:
            print(self)
            print(self.aperture_type, 1, 2)
            raise Exception("Aperture type = " + self.aperture_type + " unknown")

    def to_xml(self, xml_root):

        a = ET.SubElement(xml_root, self.__class__.__name__)
        for key in self.__dict__.keys():
            if type(self.__dict__.get(key)).__name__ in ['float', 'int', 'str']:
                a.set(key, str(self.__dict__.get(key)))

    def from_xml(self, xml):

        for att in xml.attrib:
            self.__dict__.__setitem__(att, self.change_type(xml.get(att)))

    def change_type(self, str):
        try:
            return int(str)
        except ValueError:
            try:
                return float(str)
            except ValueError:
                return str
