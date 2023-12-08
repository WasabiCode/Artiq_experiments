import numpy as np
from artiq.experiment import *
class Photon_Detction_itself(EnvExperiment):
    """Photon_Detction_itself"""
    
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl20")	
        self.setattr_device("ttl1")

    
    @kernel
    def run(self):
        self.core.reset()
        self.ttl1.input()
        delay(100*ms)
        try:
            while True:
                self.set_dataset("Time", np.full(1000, np.nan), broadcast=True)
                self.set_dataset("Photon_Counts", np.full(1000, np.nan), broadcast=True)
                delay(100*ms)
                Num_get_risings_arr = 0
                for i in range(100):
                    with parallel:
                        #delay(500*ms)
                        self.ttl20.pulse(100*ms)
                        self.ttl20.pulse(100*ms)
                        #print(i)
                        #delay(1000*ms)
                        gate_end_mu = self.ttl1.gate_rising(200 * ms)
                        #print(gate_end_mu)
                        
                        delay(100*ms)
                        Num_get_risings = self.ttl1.count(gate_end_mu)
                        
                        
                    Num_get_risings_arr += Num_get_risings
                    print("Gate",Num_get_risings_arr)
                    #print(Num_get_risings)
                    delay(100*ms)
                    self.set_dataset("gate_risings",Num_get_risings_arr, broadcast=True)
                    self.mutate_dataset("Photon_Counts", i, Num_get_risings_arr)
                    self.mutate_dataset("Time", i, i)
                    
            
        except RTIOUnderflow:
            print("Error for time")
            
