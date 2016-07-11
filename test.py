from particles import Ion

from accelerator import Accelerator
from pipes import Pipe
from magnets import QuadrupoleMagnet
from magnets import SectorBendingMagnet
from magnets import HorizontalKickerMagnet
from diagnostic import Transformator
from diagnostic import Screen
from diagnostic import Slit
import xml.etree.ElementTree as ET

ion = Ion(92, 146, 19, 1000)

print(ion)

ion = Ion(protons=6, neutrons=8, electrons=4, energy=1000)

print(ion)

acc = Accelerator()

width = 0.4
height = 0.2

t0 = Transformator("T0", width, height)
p1 = Pipe(width, height, 1.0)
s0 = Screen("Screen", width, height, 0.2, 0.2)
t1 = Transformator("T1", width, height)
q1 = QuadrupoleMagnet("UN4QD11", width, height, 1.0, 0.8)
q2 = QuadrupoleMagnet("UN4QD12", width, height, 1.0, -0.5)
sl1 = Slit("Slit1", width, height)
p2 = Pipe(width, height, 3.0)
sl2 = Slit("Slit2", width, height)
k1 = HorizontalKickerMagnet("kicker", width, height, 0.02)
p3 = Pipe(width, height, 3.0)
t2 = Transformator("T2", width, height)
m1 = SectorBendingMagnet("UN4MU1", width, height, length=1.0, angle=0.5)
t3 = Transformator("T3", width, height)
s1 = Screen("Screen1", width, height, 0.2, 0.2)
s2 = Screen("Screen2", width, height, 0.2, 0.2)

#acc.append_devices([t0])
#print(repr(acc))
sl1.set_positions(xpos_left=-0.01, xpos_right=0.01, ypos_bottom=-0.01, ypos_top=0.01)
acc.append_devices([t0, p1, sl1, s0, t1, q2, p2, sl2, s1, k1, p3, t2, m1, t3, s2])

#print(acc.to_xml())
acc.to_file('acc.xml')

xml_root = ET.parse('acc.xml').getroot()
acc2 = Accelerator(xml_root=xml_root)
print(acc)
print(acc2)


acc.start_simulation(100000)
acc.get_device_by_nomenclature("Screen1").show()
print("T0:", acc.get_device_by_nomenclature("T0").count.value)
print("T1:", acc.get_device_by_nomenclature("T1").count.value)

#acc2.start_simulation(10000)
#acc2.get_device_by_nomenclature("Screen2").show()
#print("T1:", acc.get_device_by_nomenclature("T1").count.value)