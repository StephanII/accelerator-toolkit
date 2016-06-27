#!/usr/bin/env python
"""
application

2016 Stephan Reimann
"""

import sys

import multiprocessing
# from PyQt5.QtWidgets import QApplication
# from mainwindow import mainWindow
from multiprocessing import Process

from accelerator import Accelerator
from pipes import Pipe
from magnets import QuadrupoleMagnet
from magnets import SectorBendingMagnet
from magnets import HorizontalKickerMagnet
from diagnostic import Transformator
from diagnostic import Screen
from diagnostic import Slit
from simulator import Simulator
import time


def simulate(accelerator, num_of_particles, threaded=True, measure_time=True):
    if measure_time:
        start = time.time()
    if threaded:
        processes = []
        num_of_cpus = max(multiprocessing.cpu_count(), 1)
        for i in range(0, num_of_cpus):
            process = Process(target=accelerator.start_simulation, args=(int(num_of_particles / num_of_cpus),))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
    else:
        accelerator.start_simulation(numberOfIons=num_of_particles)

    if measure_time:
        print("duration ", (time.time() - start), " s")


def main():
    print("Test")
    acc = Accelerator()

    width = 0.4
    height = 0.2

    t0 = Transformator("T0", width, height)
    p1 = Pipe(width, height, 1.0)
    s0 = Screen("Screen", width, height, 0.2, 0.2)
    t1 = Transformator("T1", width, height)
    q1 = QuadrupoleMagnet("UN4QD11", width, height, 1.0, 0.8)
    q2 = QuadrupoleMagnet("UN4QD12", width, height, 1.0, -0.8)
    sl1 = Slit("Slit1", width, height)
    p2 = Pipe(width, height, 3.0)
    sl2 = Slit("Slit2", width, height)
    k1 = HorizontalKickerMagnet("kicker", width, height, 0.02)
    p3 = Pipe(width, height, 3.0)
    t2 = Transformator("T2", width, height)
    m1 = SectorBendingMagnet("UN4MU1", width, height, length=1.0, angle=0.5)
    t3 = Transformator("T3", width, height)
    s1 = Screen("Screen", width, height, 0.2, 0.2)

    # acc.append_devices([t0])
    acc.append_devices([t0, s0, p1, t1, q1, sl1, q2, sl1, p2, sl2, k1, p3, t2, m1, t3])
    n = 8000

    acc.reset()

    simulate(accelerator=acc, num_of_particles=n, threaded=False, measure_time=True)
    print(t0.count.value, " particles in T0\n")

    acc.reset()

    simulate(accelerator=acc, num_of_particles=n, threaded=True, measure_time=True)
    print(t0.count.value, " particles in T0\n")

    s0.show()

    # print(t1.particleCount, " particles in T1")
    # print(t2.particleCount, " particles in T2")
    # print(t3.particleCount, " particles in T3")
    # print repr(sl1)
    # print repr(sl2)

    # s0.show()
    # s1.show()


#    app = QApplication(sys.argv)
#    form = mainWindow()
#    form.show()
#    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
