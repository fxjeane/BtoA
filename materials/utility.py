import imp
from arnold import *
from bpy.props import (CollectionProperty,StringProperty, BoolProperty,
IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bl_ui import properties_material
pm = properties_material

if "bpy" in locals():
    pass
else:
    import bpy
class BtoAUtilityMaterialSettings(bpy.types.PropertyGroup):
    colorMode = EnumProperty(items=(("0","color",""),("1","ng",""),("2","n",""),
                                    ("3","bary",""),("4","uv",""),("5","u",""),
                                    ("6","v",""),("7","dpdu",""),("8","dpdv",""),
                                    ("9","p",""),("10","prims",""),("11","wire",""),
                                    ("12","polywire",""),("13","obj",""),("14","edgelength",""),
                                    ("15","floatgrid",""),("16","reflectline",""),("17","bad_uvs","")),
                                    name="Color Mode", description="", 
                                    default="0")
    shadeMode = EnumProperty(items=(("0","ndoteye",""),("1","lambert",""),("2","flat",""),
                                    ("3","ambocc","")),
                                    name="Color Mode", description="", 
                                    default="0")
    color = FloatVectorProperty(name="Color",default=(1,1,1),subtype="COLOR")
    opacity = FloatProperty(name="Opacity",default=1)


class BtoA_material_utility_gui(pm.MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Utility"
    COMPAT_ENGINES = {'BtoA'}

    @classmethod
    def poll(cls, context):
        mat = context.material
        activeMat = pm.active_node_mat(mat)
        engine = context.scene.render.engine
        BtoAUtil = activeMat.BtoA.shaderType == "UTILITY"
        return pm.check_material(mat) and BtoAUtil  and (mat.type in {'SURFACE', 'WIRE'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        mat = pm.active_node_mat(context.material)
        layout = self.layout
        layout.prop(mat.BtoA.utility,"colorMode")
        layout.prop(mat.BtoA.utility,"shadeMode")
        layout.prop(mat.BtoA.utility,"color")
        layout.prop(mat.BtoA.utility,"opacity")

def writeMaterial(mat,textures):
    util = mat.BtoA.utility
    node = AiNode(b"utility")
    AiNodeSetInt(node,b"color_mode",int(util.colorMode))
    AiNodeSetInt(node,b"shade_mode",int(util.shadeMode))
    AiNodeSetRGB(node,b"color",util.color.r,
                              util.color.g,
                              util.color.b)
    AiNodeSetFlt(node,b"opacity",util.opacity)
    return node

className = BtoAUtilityMaterialSettings
bpy.utils.register_class(className)
enumValue = ("UTILITY","Utility","")
del properties_material
