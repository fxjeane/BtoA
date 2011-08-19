import imp
from arnold import *
from bpy.props import CollectionProperty,StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty

if "bpy" in locals():
    pass
else:
    import bpy

########################
#
# custom material properties
#
########################
def rnaPropUpdate(self, context):
    self.update_tag() # this is a func from material, material is the self here if I'm not mistaken

class BtoAStandardMaterialSettings(bpy.types.PropertyGroup):
    specularRoughness = FloatProperty(
                name="Roughness", description="Specular Roughness",
                max = 1, min = 0,default=0.25)

    specularBrdf = EnumProperty(items=(("0","Stretched Phong",""),
                                 ("1","Ward Duer",""),
                                 ("2","Cook Torrance","")),
                                 name="BRDF", description="Specular BRDF", 
                                 default="0")

    specularAnisotropy = FloatProperty(
                name="Anisotropy", description="Specular Anisotropy",
                max = 1, min = 0,default=0.5)

    specularRotation = FloatProperty(
                name="Aniso Rotation", description="Specular Anisotropy Rotation",
                max = 1, min = 0,default=0,update=rnaPropUpdate)

bpy.utils.register_class(BtoAStandardMaterialSettings)

class BtoAMaterialSettings(bpy.types.PropertyGroup):
    name="BtoAMaterialSettings"
    shaderType = EnumProperty(items=(("FLAT","Flat",""),
                             ("AMBIENT_OCCLUSION","Ambient Occlusion",""),
                             ("LAMBERT","Lambert",""),
                             ("STANDARD","Standard",""),
                             ("UTILITY","Utility",""),
                             ("WIREFRAME","Wireframe","")),
                             name="Shader", description="AA pattern", 
                             default="STANDARD")
    
    standard = PointerProperty(type=BtoAStandardMaterialSettings)

bpy.utils.register_class(BtoAMaterialSettings)
bpy.types.Material.BtoA = PointerProperty(type=BtoAMaterialSettings,name='BtoA')

from bl_ui import properties_material
pm = properties_material

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

class BtoA_material_diffuse_gui(pm.MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Diffuse"
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
        col = split.column()
        col.prop(mat, "diffuse_color", text="")
        sub = col.column()
        sub.active = (not mat.use_shadeless)
        sub.prop(mat, "diffuse_intensity", text="Intensity")

        col = split.column()
        col.active = (not mat.use_shadeless)
        #col.prop(mat, "diffuse_shader", text="")
        #col.prop(mat, "use_diffuse_ramp", text="Ramp")

        #col = layout.column()
        #col.active = (not mat.use_shadeless)
        
        if mat.BtoA.shaderType == 'STANDARD':
            col.prop(mat, "roughness")

        #elif mat.diffuse_shader == 'MINNAERT':
        #    col.prop(mat, "darkness")
        #elif mat.diffuse_shader == 'TOON':
        #    row = col.row()
        #    row.prop(mat, "diffuse_toon_size", text="Size")
        #    row.prop(mat, "diffuse_toon_smooth", text="Smooth")
        #elif mat.diffuse_shader == 'FRESNEL':
        #    row = col.row()
        #    row.prop(mat, "diffuse_fresnel", text="Fresnel")
        #    row.prop(mat, "diffuse_fresnel_factor", text="Factor")

        #if mat.use_diffuse_ramp:
        #    layout.separator()
        #    layout.template_color_ramp(mat, "diffuse_ramp", expand=True)
        #    layout.separator()

        #    row = layout.row()
        #    row.prop(mat, "diffuse_ramp_input", text="Input")
        #    row.prop(mat, "diffuse_ramp_blend", text="Blend")

        #    layout.prop(mat, "diffuse_ramp_factor", text="Factor")


class MATERIAL_PT_specular(pm.MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Specular"
    COMPAT_ENGINES = {'BtoA'}

    @classmethod
    def poll(cls, context):
        mat = context.material
        engine = context.scene.render.engine
        return pm.check_material(mat) and (mat.type in {'SURFACE', 'WIRE'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        mat = pm.active_node_mat(context.material)
        layout.active = (not mat.use_shadeless)
        split = layout.split()
        col = split.column()
        col.prop(mat, "specular_color", text="")
        col.prop(mat, "specular_intensity", text="Intensity")
        col = split.column()
        col.prop(mat.BtoA.standard, "specularBrdf", text="")
        #col.prop(mat, "use_specular_ramp", text="Ramp")

        col = layout.column()
        col.prop(mat.BtoA.standard, "specularRoughness", text="Roughness")
        if mat.BtoA.standard.specularBrdf == "1":
        #if mat.BtoAStandardSpecBrdf == "1":
            col.prop(mat.BtoA.standard, "specularAnisotropy", text="Anisotropy")
            #col.prop(mat.BtoAStandard, "specularAnisotropy", text="Anisotropy")
            col.prop(mat.BtoA.standard, "specularRotation", text="Rotation")
            #col.prop(mat.BtoAStandard, "specularRotation", text="Rotation")
        
        #if mat.specular_shader in {'COOKTORR', 'PHONG'}:
        #    col.prop(mat, "BtoA_standard_spec_roughness", text="Roughness")
        #elif mat.specular_shader == 'BLINN':
        #    row = col.row()
        #    row.prop(mat, "specular_hardness", text="Hardness")
        #    row.prop(mat, "specular_ior", text="IOR")
        #elif mat.specular_shader == 'WARDISO':
        #    col.prop(mat, "specular_slope", text="Slope")
        #elif mat.specular_shader == 'TOON':
        #    row = col.row()
        #    row.prop(mat, "specular_toon_size", text="Size")
        #    row.prop(mat, "specular_toon_smooth", text="Smooth")

        #if mat.use_specular_ramp:
        #    layout.separator()
        #    layout.template_color_ramp(mat, "specular_ramp", expand=True)
        #    layout.separator()

        #    row = layout.row()
        #    row.prop(mat, "specular_ramp_input", text="Input")
        #    row.prop(mat, "specular_ramp_blend", text="Blend")

        #    layout.prop(mat, "specular_ramp_factor", text="Factor")

for member in dir(properties_material):
    subclass = getattr(properties_material, member)
    try:
        if subclass.bl_label not in ["Diffuse","Specular"]:
            subclass.COMPAT_ENGINES.add('BtoA')
    except:
        pass


del properties_material

def writeStandardMaterial(mat):
    standard = AiNode(b"standard")
    AiNodeSetRGB(standard,b"Kd_color",mat.diffuse_color.r,
                                      mat.diffuse_color.g,
                                      mat.diffuse_color.b)
    AiNodeSetFlt(standard,b"Kd",mat.diffuse_intensity)
    AiNodeSetRGB(standard,b"Ks_color",mat.specular_color.r,
                                      mat.specular_color.g,
                                      mat.specular_color.b)
    AiNodeSetFlt(standard,b"Ks",mat.specular_intensity)
    AiNodeSetFlt(standard,b"specular_roughness",mat.BtoA.standard.specularRoughness)
    AiNodeSetInt(standard,b"specular_brdf",int(mat.BtoA.standard.specularBrdf))
    AiNodeSetFlt(standard,b"specular_anisotropy",mat.BtoA.standard.specularAnisotropy)
    AiNodeSetFlt(standard,b"specular_rotation",mat.BtoA.standard.specularRotation)

    return standard

def writeAmbientOcclusion(mat):
    ao = AiNode(b"ambien_occlusion")
    return ao

def writeWireframe(mat):
    ao = AiNode(b"wireframe")
    AiNodeSetFlt(ao,b"line_width",2)
    AiNodeSetInt(ao,b"edge_type",1)
    return ao

class Materials:
    def __init__(self, scene):
        self.scene = scene
        self.materialDict = {}

    def writeMaterials(self):
        for mat in bpy.data.materials:
            self.writeMaterial(mat)

    def writeMaterial(self,mat):
        outmat = None
        if mat.BtoA.shaderType == 'STANDARD':
            outmat =writeStandardMaterial(mat)
        elif mat.BtoA.shaderType =='AMBIENT_OCCLUSION':
            outmat = writeAmbientOcclusion(mat)
        elif mat.BtoA.shaderType =='WIREFRAME':
            outmat = writeWireframe(mat)

        AiNodeSetStr(outmat,b"name",mat.name.encode('utf-8'))
        self.materialDict[mat.as_pointer()] = outmat
        return outmat

 
