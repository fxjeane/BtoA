import bpy
from mathutils import Matrix
from arnold import *

class BaseLight():
    def __init__(self, light):
        self.lightdata = light 
        self.light = bpy.context.scene.objects[light.name]
        self.alight = None

    def write(self):
        # intensity and color
        AiNodeSetStr(self.alight,b"name",self.lightdata.name.encode('utf-8'))
        AiNodeSetFlt(self.alight,b"intensity",self.lightdata.energy)
        AiNodeSetFlt(self.alight,b"exposure",self.lightdata.BtoA_exposure)
        lcol = self.lightdata.color
        AiNodeSetRGB(self.alight,b"color",lcol.r,lcol.g,lcol.b)
        
        
        # shadows
        if not self.lightdata.BtoA_shadow_enable:
            AiNodeSetBool(self.alight,b"cast_shadows",0)
        else:
            scol = self.lightdata.shadow_color
            AiNodeSetRGB(self.alight,b"shadow_color",scol.r,scol.g,scol.b)
            AiNodeSetFlt(self.alight,b"shadow_density",self.lightdata.BtoA_shadow_density)
            AiNodeSetFlt(self.alight,b"radius",self.lightdata.shadow_soft_size)
            AiNodeSetInt(self.alight,b"samples",self.lightdata.shadow_ray_samples)
            
            AiNodeSetBool(self.alight,b"affect_diffuse",self.lightdata.use_diffuse)
            AiNodeSetBool(self.alight,b"affect_specular",self.lightdata.use_specular)
