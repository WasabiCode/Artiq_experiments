from artiq.experiment import *

class Phase_Shift(EnvExperiment):
    '''Phase_Shift'''
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul1_cpld")

    @kernel
    def run(self):
        self.core.reset()
        self.urukul1_cpld.init()
        delay(10 * ms)
        self.urukul01_ch0.init()
        delay(10 * ms)
        self.urukul1_ch0.sw.on()
        delay(10 * ms)
        self.urukul1_ch0.set(frequency=1 * MHz, phase=1) # changing phase by 1.0 changes by 2π 
