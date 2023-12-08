import numpy as np
from artiq.experiment import *
class Photon_Detection_probability(EnvExperiment):
    """Photon_Detection_probability"""
    def build(self):                                                                # setup devices
        self.setattr_device("core")
        self.setattr_device("ttl0")
         
    @kernel
    def run(self):                                                                  
        self.core.reset()
        self.ttl0.input()                                                           # initialize measuring ttl
        delay(10*ms)
        try:
            measurements = 10                                                      # here enter number of desired measurements
            meas = measurements
            self.set_dataset("Time", np.full(meas, np.nan), broadcast=True)          # create dataset for time
            self.set_dataset("Photon_Counts", np.full(meas, np.nan), broadcast=True) # create dataset for number of incoming photons
            self.set_dataset("Probability", np.full(meas, np.nan), broadcast=True)   # create dataset for probability of photons in each time stamp
            delay(100*ms)
            p = [0] * meas                                                            # creates probability list                                                          
            for i in range(meas):
                gate_end_mu = self.ttl0.gate_rising(200 * ms)                         # measurement
                delay(100*ms)
                Num_get_risings = self.ttl0.count(gate_end_mu)                        # writes number of measurements for each time stamp 
                p[i] = Num_get_risings                                                # writes measurement in the probability list
                self.set_dataset("gate_risings",Num_get_risings,broadcast=True)       # number of photons coming to ttl
                self.mutate_dataset("Photon_Counts", i, Num_get_risings)              # add number of photons for each time stamp to the dataset
                self.mutate_dataset("Time", i, i)                                     # writes time for each time stamp
            p_sum = 0                                                                 # creates sum number
            for i in p:                                                               # sums up all of the number of incoming photons
                p_sum += i
                
            if p_sum == 0: 
                print("--------------------------------------")                       # checks if there were some photons coming to the detector
                print("|!!  zero photons to the detector  !!|")
                print("--------------------------------------")
                
            else:
                p_sum_list = [p_sum] * meas                                               # distrubets the sum in the in the list to do element wise divison
                p_final = [0.0] * meas                                                    # creates empty probability distribution list
                
                for i in range(len(p)):                                                   # loop for element wise division
                    i1 = p[i]
                    i2 = p_sum_list[i]
                    dv = i1 / i2                                                          # makes element wise division
                    p_final[i] = dv                                                       # adds division to the list
                    self.mutate_dataset("Probability", i, dv)                             # adds probality to the dataset
                
                # p_final_sum = 0.0    
                # for k in p_final:
                #     p_final_sum += k
                
                # print(p_final_sum)                                                      # check if probability sum equals to 1
                
            
        except RTIOUnderflow:
            print("Error for time")
            
    
   
        