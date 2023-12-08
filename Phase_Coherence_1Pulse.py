# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 15:58:31 2023

@author: LAB_QOL1
"""

from artiq.experiment import *

class Phase_Coherence_1Pulse(EnvExperiment):
    '''Phase_Coherence_1Pulse'''
    def build(self):                                            # set up devices
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul1_ch1")
        self.setattr_device("urukul1_cpld")

    @kernel
    def run(self):                                              # initialize devices
        self.core.reset()
        self.urukul1_cpld.init()
        delay(10 * ms)
        self.urukul1_ch0.init()
        delay(10 * ms)
        self.urukul1_ch1.init()
        delay(10 * ms)
        self.urukul1_ch0.sw.on()                                # switch on dds0 
        delay(10 * ms)
        self.urukul1_ch0.set(frequency=15 * MHz, phase=0.0)     # start constant laser pulse on dds0
        for i in range(100):                                    # start loop 
            with sequential:
                self.urukul1_ch1.sw.on()                                     # turn on dds1
                self.urukul1_ch0.set(frequency=15 * MHz, phase=0.0)          # turn on dds1 and set the required parameters, changing phase by 1.0 changes by 2π 
                delay(1000 * ms)                                             # lenght of the laser pulse
                self.urukul1_ch1.sw.off()                                    # turn off dds1
                delay(500 * ms)                                              # delay between laser pulses
        


