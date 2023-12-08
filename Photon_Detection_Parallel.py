import numpy as np
from artiq.experiment import *
class Photon_Detection_Parallel(EnvExperiment):
    """Photon_Detection_Parallel"""
    
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl20")	
        self.setattr_device("ttl0")

    
    @kernel
    def run(self):
        self.core.reset()
        self.ttl0.input()
        delay(100*ms)
        try:
            while True:
                self.set_dataset("Time", np.full(100, np.nan), broadcast=True)
                self.set_dataset("Photon_Counts", np.full(100, np.nan), broadcast=True)
                delay(100*ms)
                Num_get_risings_arr = 0
                for i in range(100):
                    with parallel:
                        delay(500*ms)
                        self.ttl20.pulse(10*ms)
                        gate_end_mu = self.ttl0.gate_rising(10 * ms)
                        Num_get_risings = self.ttl0.count(gate_end_mu)
                        
                    delay(500*ms)   
                    Num_get_risings_arr += Num_get_risings
                    print("Gate", Num_get_risings)
                    #print(Num_get_risings)
                    delay(100*ms)
                    self.set_dataset("gate_risings",Num_get_risings_arr, broadcast=True)
                    self.mutate_dataset("Photon_Counts", i, Num_get_risings_arr)
                    self.mutate_dataset("Time", i, i)
                    #self.analyse(i, Num_get_risings)
            
        except RTIOUnderflow:
            print("Error for time")
            
    
    # def analyse(self, time, count):

    #     self.array1.append(time)
    #     self.array2.append(count)
    #     self.set_dataset("gate_risings",count,broadcast=True)
    #     self.set_dataset("Photon_Counts",self.array2,broadcast=True)
    #     self.set_dataset("Time",self.array1,broadcast=True)




































    # @kernel
    # def run(self):
    #     self.core.reset()
    #     self.ttl0.input()
    #     delay(10*ms)
    #     try:
    #         while True:
                
                
    #             for i in range(100):
    #                 gate_end_mu = self.ttl0.gate_rising(100 * ms)
    #                 Num_get_risings = self.ttl0.count(gate_end_mu)
    #                 self.set_dataset("Time", np.full(100, np.nan), broadcast=True)
    #                 self.set_dataset("Photon_Counts", np.full(100, np.nan), broadcast=True)
                
    #                 delay(100*ms)
                
    #                 for i in range(100):
    #                     self.set_dataset("gate_risings", Num_get_risings, broadcast=True)
    #                     self.mutate_dataset("Photon_Counts", i, i)
    #                     self.mutate_dataset("Time", i, i)
    #                     # self.analyze(i, Num_get_risings)
                    
            
            
    #     except RTIOUnderflow:
    #         print("Error for time")
            
    
                # self.set_dataset("Time", np.full(100, np.nan), broadcast=True, archive=False)
                # self.set_dataset("Photon_Counts", np.full(100, np.nan), broadcast=True, archive=False)
