from isa.inst import *
import tensorflow as tf 
import numpy as np

class Meconv_mm(Inst):
    name = 'meconv.mm'  

    def golden(self):
        if np.isinf( self['vs1'] ).any():
            vd = tf.nn.conv2d(self['vs1'], self['vs2'], [1, 1, 1, 1], 'VALID', data_format='NHWC')       
        else:
            tf_pad = [[0, 0], [self['padding'][0], self['padding'][1]], [self['padding'][2], self['padding'][3]], [0, 0]]
            vd = tf.nn.conv2d(self['vs1'], self['vs2'], [1, self['sk'], self['sk'], 1], tf_pad, data_format='NHWC', dilations=[1, self['dl'], self['dl'], 1])
        
        vd = vd.numpy()
        return vd