
import numpy as np

from artiq.experiment import *

class All_changer_without_phase(EnvExperiment):
    """All_changer_without_phase"""
    def build(self):
        # sets core device drivers as attributes
        self.setattr_device("core")
        self.pmt = self.get_device("ttl0")

        # global attenuation
        self.setattr_argument("attenuation",
                            NumberValue(0*dB, unit='dB', scale=dB, min=0*dB, max=31*dB),
                            )
        # global stop 
        self.setattr_argument(f"STOP", BooleanValue(False))
        
        for ch in range(4):
            # sets urukul0, channel 0-3 device drivers as attributes
            self.setattr_device(f"urukul1_ch{ch}")

            ### This two attributes will be shown in the GUI grouped by channel
            # use/don't use each channel
            self.setattr_argument(f"state_ch{ch}", BooleanValue(ch==0), f"canal_{ch}")
            # each channel's frequency
            self.setattr_argument(f"freq_ch{ch}",
                                NumberValue(200.0*MHz, unit='MHz', scale=MHz, min=1*MHz, max=400*MHz),
                                f"canal_{ch}")
            # phase
            self.setattr_argument(f"phase_ch{ch}", NumberValue(1.0), f"canal_{ch}")
            # each channel's amplitude
            self.setattr_argument(f"amp_ch{ch}",
                                NumberValue(0.5, min=0., max=1.),
                                f"canal_{ch}")

        self.all_amps = [self.amp_ch0, self.amp_ch1, self.amp_ch2, self.amp_ch3]
        self.all_freqs = [self.freq_ch0, self.freq_ch1, self.freq_ch2, self.freq_ch3]
        self.all_phase = [self.phase_ch0, self.phase_ch1, self.phase_ch2, self.phase_ch3]
        self.states = [self.state_ch0, self.state_ch1, self.state_ch2, self.state_ch3]
        self.all_channels = [self.urukul1_ch0, self.urukul1_ch1, self.urukul1_ch2, self.urukul1_ch3]

        self.use_amps = []
        self.use_freqs = []
        self.use_phase = []
        self.use_channels = []

        for state, ch_n, freq_n, amp_n, phase_n in zip(self.states, self.all_channels,
                                              self.all_freqs, self.all_amps, self.all_phase):
            if state:
                self.use_channels.append(ch_n)
                self.use_freqs.append(freq_n)
                self.use_amps.append(amp_n)
                self.use_phase.append(phase_n)
           
        print (self.use_channels)


    @kernel
    def run(self):
        if not self.STOP:
            
          #  print (self.STOP)
            self.core.reset()

    
           
    
            for channel in self.use_channels:
                channel.cpld.init()
                channel.init()
                
    
    
    
            delay(10 * ms)
            
            for i in range(len(self.use_channels)):
                # writes global attenuation and specific
                # frequency and amplitude variables to each
                # urukul channel outputting function
                self.use_channels[i].set_att(self.attenuation)
                #self.use_channels[i].set_amplitude(self.use_amps[i])
               # self.use_channels[i].set_phase(self.use_phase[i])
                #self.use_channels[i].set_amplitude(self.use_amps[i])
                print(self.use_phase[i])
                self.use_channels[i].set(self.use_freqs[i], phase = self.use_phase[i], amplitude=self.use_amps[i])
                self.use_channels[i]
            # turn on every selected channel
            for i in range(4):
                print (self.states[i])
                if self.states[i] == True:
                    #print (self.states[i])
                    self.all_channels[i].sw.on()
                    
                else:
                    self.all_channels[i].sw.off()
                
                delay(10*ms)
            self.core.break_realtime()
  
        else:
            for channel in self.all_channels:
                self.core.reset()
                channel.cpld.init()
                channel.init()
            for i in range(4):
                self.all_channels[i].sw.off()
            




        
            

            
            
            
