#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 22:46:16 2019

@author: wangchong
exit"""

import math
import numpy as np
from matplotlib import pyplot as plt
from model.ET_filtered import RNN
from util.draw import draw_fig

class PatternGen:
    def __init__(self, nsecs):
        dt = 0.1;
        simtime = np.arange(0, nsecs, dt);
        simtime2 = np.arange(1*nsecs, 1.25*nsecs, dt);
        
        amp = 1;
        freq = 1.0/60;
        ft = (amp/1.0)*np.sin(1.0*math.pi*freq*simtime) + \
             (amp/2.0)*np.sin(2.0*math.pi*freq*simtime) + \
             (amp/6.0)*np.sin(3.0*math.pi*freq*simtime) + \
             (amp/3.0)*np.sin(4.0*math.pi*freq*simtime);
#        ft = (amp/1.0)*np.sin(1.0*math.pi*freq*simtime) + \
#             (amp/2.0)*np.sin(2.0*math.pi*freq*simtime);
        self.ft = ft/1.5;
        
        self.clock = np.sin(1.0*math.pi*freq*simtime);
        
        ft2 = (amp/1.0)*np.sin(1.0*math.pi*freq*simtime2) + \
              (amp/2.0)*np.sin(2.0*math.pi*freq*simtime2) + \
              (amp/6.0)*np.sin(3.0*math.pi*freq*simtime2) + \
              (amp/3.0)*np.sin(4.0*math.pi*freq*simtime2);
#        ft2 = (amp/1.0)*np.sin(1.0*math.pi*freq*simtime2) + \
#             (amp/2.0)*np.sin(2.0*math.pi*freq*simtime2);
        self.ft2 = ft2/1.5;
        
        self.net = RNN(1, 128, 1);
        
        # prob to sample from ground truth input
        self.epsilon = 0.999;
        
        # number of steps to condition the RNN during test
        self.condition = 120;
        
        self.n_plot = 24000;
        
    def run(self):
        
        global trainOut, trainRecording, testOut, testRecording, dw
        
        trainOut = np.zeros(self.ft.shape);
        trainRecording = np.zeros((self.net.recDim, self.ft.shape[0]));
        
        dw = np.zeros(self.ft.shape)
        
        
        for i in range(0, list(self.ft.shape)[0]-1):
#            useInput = np.random.binomial(1, self.epsilon);
#            if useInput:
#                trainOut[i], trainRecording[:, i], dW = self.net.trainStep(np.array([[self.ft[i]]]), self.ft[i+1]);
#            else:
#                trainOut[i], trainRecording[:, i], dW = self.net.trainStep(np.array([[trainOut[i-1]]]), self.ft[i+1]);
                
            trainOut[i], trainRecording[:, i], dw[i] = self.net.trainStep(np.array([[self.clock[i]]]), self.ft[i]);
            if i%7200==0 and i!=0:
                print(i);
                self.net.rHH *= 0.999;
                self.net.rIH *= 0.999;
                self.net.rHO *= 0.999;
                
#                if self.net.beta<20:
#                    self.net.beta *= 1.005;
                
            
#            if i%self.n_plot==0 and i!=0:
#                global ax1, ax2, ax3;
#                draw_fig(ax1, ax2, ax3, i-self.n_plot, i, self.ft, trainOut, trainRecording, dw);
        
        testOut = np.zeros(self.ft2.shape);
        testRecording = np.zeros((self.net.recDim, self.ft2.shape[0]));
        
# =============================================================================
#         for i in range(self.condition):    
#             testOut[i], testRecording[:, i] = self.net.testStep(np.array([[self.ft2[i]]]));
#             
#         for i in range(self.condition, list(self.ft2.shape)[0]):
#             testOut[i], testRecording[:, i] = self.net.testStep(np.array([[testOut[i-1]]]));
#             if i%500==0:
#                 print(i, testOut[i]-self.ft2[i]);
# =============================================================================
            
        # reset output unit to get rid of existing activities
#        self.net.o = 0;
        for i in range(0, list(self.ft2.shape)[0]):
             testOut[i], testRecording[:, i] = self.net.testStep(np.array([[self.clock[i]]]));
             if i%500==0:
                 print(i, testOut[i]-self.ft2[i]);
        
#        plt.plot(trainOut);
#        plt.plot(self.ft)
#        plt.imshow(self.net.HH);
        
        fig, (ax1, ax2) = plt.subplots(2);
        ax1.plot(testOut);
        ax1.plot(self.ft2);
#        ax1.imshow(trainRecording);
        ax1.set_aspect("auto");
        ax2.imshow(testRecording);
        ax2.set_aspect("auto");
        

if __name__=="__main__":
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1);
    test = PatternGen(24000);
    test.run();