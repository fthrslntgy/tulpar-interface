import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Model(QVTKRenderWindowInteractor):

    def __init__(self, parent=None):

        filename = "model.obj"
        self.reader = vtk.vtkOBJReader()
        self.reader.SetFileName(filename)
