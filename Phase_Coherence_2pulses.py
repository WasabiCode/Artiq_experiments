# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:10:27 2023

@author: LAB_QOL1
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:10:27 2023

@author: LAB_QOL1
"""


from artiq.experiment import *
from artiq.coredevice import ad9910                                     # import Urukul board modes


class Phase_Coherence_2pulses(EnvExperiment):
    '''Phase_Coherence_2pulses'''
    def build(self):                                                    # set up devices
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul1_ch1")
        self.setattr_device("urukul1_cpld")
        
        
    @kernel
    def run(self):                                                      # initialize devices
        self.core.reset()
        self.urukul1_cpld.init()
        delay(10 * ms)
        self.urukul1_ch0.init()
        delay(15 * ms)
        self.urukul1_ch1.init()
        delay(10 * ms)
        self.urukul1_ch0.sw.on()                                        # switch on dds0 
        delay(500 * ms)
        self.urukul1_ch0.set(frequency=2 * MHz, phase=0.0)              # start constant laser pulse on dds0, changing phase by 1.0 changes by 2π 
        for i in range(50):                                             # start your loop 
            with sequential:
                delay(35*us)                                                                                    # delay between sections of two laser pulses
                self.urukul1_ch1.sw.on()                                                                        # turn on your dds1
                self.urukul1_ch1.set(frequency=2 * MHz, phase=0.0, phase_mode=ad9910.PHASE_MODE_CONTINUOUS)     # turn on dds1 and set the required parameters 
                delay(3 * us)                                                                                   # set duration of the laser                                  
                self.urukul1_ch1.sw.off()                                                                       # turn off your laser pulse
                
                delay(15 * us)                                                                                  # delay between two laser pulses
                
                self.urukul1_ch1.sw.on()
                self.urukul1_ch1.set(frequency=2 * MHz, phase=0.0, phase_mode=ad9910.PHASE_MODE_TRACKING)       
                delay(3 * us)
                self.urukul1_ch1.sw.off()
                delay(35 * us)                                                                                  # delay between sections of two laser pulses
                
             






