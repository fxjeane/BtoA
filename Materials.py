import imp, os
from arnold import *
from bpy.props import (CollectionProperty,StringProperty, BoolProperty,
IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bl_ui import properties_material
pm = properties_material

if "bpy" in locals():
    pass
else:
    import bpy

for member in dir(properties_material):
    subclass = getattr(properties_material, member)
    try:
        if subclass.bl_label in ["Preview"]:
            subclass.COMPAT_ENGINES.add('BtoA')
            pass
    except:
        pass
########################
#
# custom material properties
#
########################
def rnaPropUpdate(self, context):
    self.update_tag()

def pollMaterial(cls,context,shaderType,matTypes={'SURFACE','WIRE'}):
    mat = context.material
    activeMat = pm.active_node_mat(mat)
    engine = context.scene.render.engine
    btoaSpec = activeMat.BtoA.shaderType == shaderType
    return pm.check_material(mat) and btoaSpec and (mat.type in matTypes) and (engine in cls.COMPAT_ENGINES)

class BtoAMaterialSettings(bpy.types.PropertyGroup):
    name="BtoAMaterialSettings"
    defaultMatDir = os.path.join(os.path.dirname(__file__),"materials")
    defaultMats = os.listdir(defaultMatDir)
    # if the dir is not a "module", lets turn it into one
    if not os.path.exists(os.path.join(defaultMatDir,"__init__py")):
        fin = open(os.path.join(defaultMatDir,"__init__.py"),'w')
        fin.close()

    # load all materials from the materials folder
    materials = []
    loadedMaterials = {}
    for module in defaultMats:
        moduleName = module[:-3]
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        
        foo = __import__("BtoA.materials."+moduleName, locals(), globals())
        module = eval("foo.materials."+moduleName)
        materials.append(module.enumValue)
        vars()[moduleName] = PointerProperty(type=module.className)
        loadedMaterials[module.enumValue[0]] = module
    del module

    shaderType = EnumProperty(items=materials,
                             name="Shader", description="Surface Shader", 
                             default="STANDARD")

bpy.utils.register_class(BtoAMaterialSettings)
bpy.types.Material.BtoA = PointerProperty(type=BtoAMaterialSettings,name='BtoA')


class BtoA_material_shader_gui(pm.MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Arnold Shader"
    COMPAT_ENGINES = {'BtoA'}

    @classmethod
    def poll(cls, context):
        mat = context.material
        engine = context.scene.render.engine
        return pm.check_material(mat) and (mat.type in {'SURFACE', 'WIRE'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        mat = pm.active_node_mat(context.material)
        split = layout.split()
        split.prop(mat.BtoA,"shaderType")


del properties_material

class Materials:
    def __init__(self, scene,textures=None):
        self.scene = scene
        self.textures = None
        if textures:
            self.textures = textures.texturesDict
        self.materialDict = {}

    def writeMaterials(self):
        for mat in bpy.data.materials:
            outmat = None
            currentMaterial = mat.BtoA.loadedMaterials[mat.BtoA.shaderType]
            outmat = currentMaterial.writeMaterial(mat,self.textures)

            AiNodeSetStr(outmat,b"name",mat.name.encode('utf-8'))
            self.materialDict[mat.as_pointer()] = outmat

    def writeMaterial(self,mat):
        outmat = None
        currentMaterial = mat.BtoA.loadedMaterials[mat.BtoA.shaderType]
        outmat = currentMaterial.writeMaterial(mat,self.textures)

        AiNodeSetStr(outmat,b"name",mat.name.encode('utf-8'))
        self.materialDict[mat.as_pointer()] = outmat
        return outmat
