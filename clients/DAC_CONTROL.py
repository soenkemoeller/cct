import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from numpy import *
import labrad
from qtui.QDACControl import QDACControl
from qtui.QCustomLevelSpin import QCustomLevelSpin

UpdateTime = 100 # ms

class DAC_CONTROL(QDACControl):

    def __init__(self, parent=None):
        #self.cxn = cxn
        #self.dacserver = cxn.cctdac

        QDACControl.__init__(self, parent)

        self.Nelectrodes = 18

        ''' 
        Build Dictionary of controls
        '''
        self.controls = {}
        self.controls['Ex'] = QCustomLevelSpin('Ex', (-2.,2.))
        self.controls['Ey'] = QCustomLevelSpin('Ey', (-2.,2.))
        self.controls['Ez'] = QCustomLevelSpin('Ez', (-2.,2.))
        self.controls['U1'] = QCustomLevelSpin('U1', (-20.,20.))
        self.controls['U2'] = QCustomLevelSpin('U2', (0.,20.))
        self.controls['U3'] = QCustomLevelSpin('U3', (-10.,10.))
        self.controls['U4'] = QCustomLevelSpin('U4', (-10.,10.))
        self.controls['U5'] = QCustomLevelSpin('U5', (-10.,10.))

        self.getMultipoleVectors() # read from a text file (at the moment -- find a more elegant way to do this)
        
        self.ex_l.addWidget(self.controls['Ex'])
        self.ey_l.addWidget(self.controls['Ey'])
        self.ez_l.addWidget(self.controls['Ez'])
        self.u1_l.addWidget(self.controls['U1'])
        self.u2_l.addWidget(self.controls['U2'])
        self.u3_l.addWidget(self.controls['U3'])
        self.u4_l.addWidget(self.controls['U4'])
        self.u5_l.addWidget(self.controls['U5'])

        self.labels = [self.el1, self.el2, self.el3, self.el4, self.el5,
                             self.el6, self.el7, self.el8, self.el9, self.el10,
                             self.el11, self.el12, self.el13, self.el14, self.el15,
                             self.el16, self.el17, self.el18]

        self.inputUpdated = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        for k in self.controls.keys():
            self.controls[k].onNewValues.connect(self.inputHasUpdated)

    def inputHasUpdated(self):
        self.inputUpdated = True

    def sendToServer(self):
        # Send the new values to the server
        if self.inputUpdated:
            realVolts = self.convertMultis(self.multipoleVectors)
            for (label, v, n) in zip(self.labels, realVolts, range(1,19)):
                label.setText("El. " + str(n) + ": " + str(v))
            print realVolts
            print "Updated!"
            self.inputUpdated = False
    def getMultipoleVectors(self):
        '''
        Read in the multipole vector matrix
        '''

        data = genfromtxt("Cfile_pos_5E6_8elecs.txt")
        self.multipoleVectors = {}
        self.multipoleVectors['Ex'] = data[:,0]
        self.multipoleVectors['Ey'] = data[:,1]
        self.multipoleVectors['Ez'] = data[:,2]
        self.multipoleVectors['U1'] = data[:,3]
        self.multipoleVectors['U2'] = data[:,4]
        self.multipoleVectors['U3'] = data[:,5]
        self.multipoleVectors['U4'] = data[:,6]
        self.multipoleVectors['U5'] = data[:,7]
        

    def convertMultis(self, multipoleVectors): # Convert multipole values -> direct dc potentials

        '''
        multipoles should have the form [ Ex, Ey, Ez, U1, U2, U3, U4, U5 ]
        '''
        
        realVolts = zeros(self.Nelectrodes)
        for k in self.controls.keys():
            realVolts += self.controls[k].spinLevel.value() * multipoleVectors[k]
        return realVolts
'''
    def sendRealVoltages(self, realVolts): # Send a list of voltages to the DAC

        self.dacserver.set_analog_voltages( realVolts )
'''
    
if __name__=='__main__':
	#cxn = labrad.connect()
	#server = cxn.dc_box
	app = QtGui.QApplication(sys.argv)
	icon = DAC_CONTROL()
	icon.show()
	app.exec_()
