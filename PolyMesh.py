import bpy
import math
import imp
from arnold import *
import ctypes
from mathutils import Matrix
from . import utils

class PolyMesh():

    
    def __init__(self,mesh,materials):
        self.mesh = mesh
        self.meshdata = mesh.data
        self.materials = materials

    def write(self):
        # create the node
        self.amesh = AiNode(b"polymesh")
        AiNodeSetStr(self.amesh,b"name",self.mesh.name.encode('utf-8')) 
        # create shorthand variables
        faces = self.meshdata.faces
        vertices = self.meshdata.vertices
        numFaces = len(faces)
        numVerts = len(vertices)

        # Number of sides per polygon
        nsides = AiArrayAllocate(numFaces, 1, AI_TYPE_UINT)
        for i in range(numFaces):
            face = faces[i]
            AiArraySetUInt(nsides, i, len(face.vertices))
        AiNodeSetArray(self.amesh,b"nsides",nsides)
       
        # IDs of each vertex
        numindex = 0
        for i in faces:
            numindex += len(i.vertices)

        vidxs = AiArrayAllocate(numindex, 1, AI_TYPE_UINT)
        count = 0
        for i in range(numFaces):
            face = faces[i]
            for j in face.vertices:
                AiArraySetUInt(vidxs, count, j.numerator)
                count +=1
        AiNodeSetArray(self.amesh,b"vidxs",vidxs)

        vlist = AiArrayAllocate(numVerts,1,AI_TYPE_POINT)
        for i in range(numVerts):
            vertex = vertices[i].co
            AiArraySetPnt(vlist,i,AtPoint(vertex.x,vertex.y,vertex.z))
        AiNodeSetArray(self.amesh,b"vlist",vlist)
        
        # write the matrix
        mmatrix = Matrix.Rotation(math.radians(-90),4,'X') * self.mesh.matrix_world
        matrix = utils.MakeAtMatrix(mmatrix)
        positions = AiArrayAllocate(1,1,AI_TYPE_MATRIX)
        AiArraySetMtx(positions,0,matrix)
        AiNodeSetArray(self.amesh,b'matrix',positions)

        # Material
        for mat in self.meshdata.materials:
            matid = mat.as_pointer()
            if matid in self.materials.materialDict.keys():
                AiNodeSetPtr(self.amesh,b"shader",self.materials.materialDict[matid])
                
