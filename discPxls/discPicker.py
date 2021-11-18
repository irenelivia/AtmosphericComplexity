import numpy as np

class DiscPicker:
    def __init__(self, max_radius, dxdy=(1,1), x0y0=(0,0)):
        dx, dy = dxdy
        x0, y0 = x0y0
        pxls = []
        rad2L = []

        ilim = np.sort( np.array((int(np.floor((-max_radius-x0)/dx)), int(np.ceil((max_radius-x0)/dx))), dtype=int) )
        jlim = np.sort( np.array((int(np.floor((-max_radius-y0)/dy)), int(np.ceil((max_radius-y0)/dy))), dtype=int) )
        for i in range( ilim[0], ilim[1]+1):
            for j in range( jlim[0], jlim[1]+1):
                rad2 = (i*dx+x0)**2 + (j*dy+y0)**2
                if rad2 < max_radius*max_radius:
                    pxls += [[i,j]]
                    rad2L += [rad2]
        order = np.argsort(rad2L)
        self.rad = np.copy(np.sqrt(rad2L)[order])
        self.pxls = np.copy(np.array(pxls)[order])
        self.dxdy = np.array(dxdy)
        DiscPicker.__x0y0 = np.array(x0y0)
        
    def centredDiscPxlArr(self, radius):
        idxMax = np.searchsorted(self.rad, radius, side='right')
        return self.pxls[:idxMax+1]
    
    def discPxlArr(self, center, radius, image):
        cdpa = self.centredDiscPxlArr(radius)
        return (cdpa+np.array(center/self.dxdy,dtype=int)) % np.array(image.shape, dtype=int)
    
    def discPxls(self, center, radius, image):
        dpa = self.discPxlArr(center, radius, image)
        return tuple(dpa.T)
    
    def discSum(self, center, radius, image):
        pxls = self.discPxls(center, radius, image)
        return image[pxls].sum()
    
    def discMean(self, center, radius, image):
        pxls = self.discPxls(center, radius, image)
        return image[pxls].mean()
    
    def discCOM_rel(self, center, radius, image, offset=0.):
#         idxMax = np.where(self.rad <= radius)[0][-1]
        idxMax = np.searchsorted(self.rad, radius, side='right')
        pxlsLocal = self.pxls[:idxMax]
        pxlsGlobal = (self.pxls[:idxMax] + np.array(center, dtype=int)) % np.array(image.shape, dtype=int)
        weights = im[tuple(pxlsGlobal.T)] + offset
        return np.average(pxlsLocal, axis=0, weights=weights)

    def get_x0y0(self):
        return DiscPicker.__x0y0