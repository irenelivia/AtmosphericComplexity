import numpy as np

class DiscPicker:
    def __init__(self, max_radius, centredOn=(0,0)):
        C = np.array(centredOn)
        pxls = []
        rad2L = []
        for i in range(-int(max_radius), int(max_radius)+1):
            for j in range(-int(max_radius), int(max_radius)+1):
                rad2 = (i-C[0])**2 + (j-C[1])**2
                if rad2 < max_radius*max_radius:
                    pxls += [[i,j]]
                    rad2L += [rad2]
        order = np.argsort(rad2L)

        self.rad = np.copy(np.sqrt(rad2L)[order])
        self.pxls = np.copy(np.array(pxls)[order])
        DiscPicker.__C = C
#         DiscPicker.C = C
    
    def get_centredOn(self):
        return DiscPicker.__C
        
    def centredDisc(self, radius):
        idxMax = np.where(self.rad <= radius)[0][-1]
        return self.pxls[:idxMax+1]
    
    def discSum(self, center, radius, im):
        idxMax = np.where(self.rad <= radius)[0][-1]
        pxls = (self.pxls[:idxMax] + np.array(center, dtype=int)) % np.array(im.shape, dtype=int)
        return im[tuple(pxls.T)].sum()
    
    def discCOM_rel(self, center, radius, im, offset=0.):
#         idxMax = np.where(self.rad <= radius)[0][-1]
        idxMax = np.searchsorted(self.rad, radius, side='right')
        pxlsLocal = self.pxls[:idxMax]
        pxlsGlobal = (self.pxls[:idxMax] + np.array(center, dtype=int)) % np.array(im.shape, dtype=int)
        weights = im[tuple(pxlsGlobal.T)] + offset
        return np.average(pxlsLocal, axis=0, weights=weights)
