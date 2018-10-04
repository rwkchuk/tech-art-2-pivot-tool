''' Made By Robert Kowalchuk '''
import maya.cmds as cmds
from maya import mel
from maya import OpenMayaUI as omui
import string

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import os.path
import pymel.core as pm

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)

class PivotTool_MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        #set up
        super(PivotTool_MainWindow, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setObjectName('PivotTool_MainWindow_uniqueId')
        self.setWindowTitle('Pivot Tool')
        #window position and size
        self.setGeometry(150, 50, 400, 200)#x,y pos then wdith, height
        self.Layout_Main = QVBoxLayout(self)
        self.Pivot = PivotTool()
        self.initUI()
        self.show()

    def initUI(self):

        #labels for tool info
        self.Label_Info = QLabel('<font size="4">This tool will export the selected mesh for UE4 as if the mesh was at the world origin in respect to the pivot point </font><font size="3"><ul><li><b>Select</b> all the meshes you want to export</li><li>Click the <b>Remember Selection button</b></li><li>Click the <b>Export Selection button</b></li><li>Each mesh will have a fbx file named the same as the outliner name in this projects folder</li></ul></font> ', self)
        self.Layout_Main.addWidget(self.Label_Info)

        #button to select waht to export
        self.Button_SelectExport = QPushButton('Remember Selection for Export', self)
        self.Layout_Main.addWidget(self.Button_SelectExport)

        #button for exporting to fbx
        self.Button_ExportFBX = QPushButton('Export Selection to FBX', self)
        self.Layout_Main.addWidget(self.Button_ExportFBX)

        #label for where the object is located and named
        self.Label_Result = QLabel('The export location is {}'.format(self.Pivot.FilePath))
        self.Layout_Main.addWidget(self.Label_Result)
        self.Label_Result.setVisible(False)

        #bindings
        self.Button_SelectExport.clicked.connect(self.ClickedSelected)
        self.Button_ExportFBX.clicked.connect(self.ClickedExport)

    def ClickedSelected(self):
        self.Label_Result.setVisible(False)
        self.Pivot.selectExport()

    def ClickedExport(self):
        self.Pivot.export()
        self.Label_Result.setText('<b>The export location is {}</b>'.format(self.Pivot.FilePath))
        self.Label_Result.setVisible(True)


class PivotTool():
    def __init__(self):
        self.ExportList = [None]
        self.FilePath = cmds.workspace(q=True, rd=True)

    def selectExport(self):
        self.ExportList = cmds.ls(sn=True, sl=True)
        print cmds.workspace(q=True, dir=True)

    def export(self):
        for selected in self.ExportList:
            cmds.select(clear = True)
            cmds.select(selected)
            self.setExportOrigin(selected)
            self.exportFBX(selected)
            self.resetExport(selected)

    def exportFBX(self, selected = None):
        """ exports the selected to an fbx located in the project folder """
        # TODO include logic for skeleton export
        pm.mel.FBXExport(f= self.FilePath + '\{}'.format(selected), s=True)
        print '{} has been exported'.format(selected)

    def setExportOrigin(self, selected = None):
        ''' moves the selected object to the origin of the scene '''
        #get the current pivot position and store it
        self.RotatePivotTransform = cmds.xform(selected, q=True, ws=True, rp=True)
        print self.RotatePivotTransform
        #Change the relative positon as invers of pivto
        self.InverseRotatePivotTransform = (self.RotatePivotTransform[0] * -1, self.RotatePivotTransform[1] * -1, self.RotatePivotTransform[2] * -1)
        # take the original for the final transform
        cmds.xform(selected, r=True, t=self.InverseRotatePivotTransform)
        print cmds.xform(selected, q=True, ws=True, rp=True)


    def resetExport(self, selected = None):
        ''' resets modified values of the selected object '''
        cmds.xform(selected, r=True, t=self.RotatePivotTransform)
        print cmds.xform(selected, q=True, ws=True, rp=True)

def main():
    ui = PivotTool_MainWindow()


if __name__ == '__main__':
    main()