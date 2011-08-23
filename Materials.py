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
                max = 1, min = 0,default=0)
bpy.utils.register_class(BtoAStandardMaterialSettings)

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

bpy.utils.register_class(BtoAUtilityMaterialSettings)

class BtoAMaterialSettings(bpy.types.PropertyGroup):
    name="BtoAMaterialSettings"
    shaderType = EnumProperty(items=(("FLAT","Flat",""),
                             ("AMBIENT_OCCLUSION","Ambient Occlusion",""),
                             ("LAMBERT","Lambert",""),
                             ("STANDARD","Standard",""),
                             ("UTILITY","Utility",""),
                             ("WIREFRAME","Wireframe","")),
                             name="Shader", description="Surface Shader", 
                             default="STANDARD")
    standard = PointerProperty(type=BtoAStandardMaterialSettings)
    utility  = PointerProperty(type=BtoAUtilityMaterialSettings)

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
        activeMat = pm.active_node_mat(mat)
        engine = context.scene.render.engine
        BtoADif = activeMat.BtoA.shaderType == "STANDARD" or activeMat.BtoA.shaderType == "LAMBERT"
        return pm.check_material(mat) and BtoADif  and (mat.type in {'SURFACE', 'WIRE'}) and (engine in cls.COMPAT_ENGINES)

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
        activeMat = pm.active_node_mat(mat)
        engine = context.scene.render.engine
        btoaSpec = activeMat.BtoA.shaderType == "STANDARD"
        return pm.check_material(mat) and btoaSpec and (mat.type in {'SURFACE', 'WIRE'}) and (engine in cls.COMPAT_ENGINES)

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

for member in dir(properties_material):
    subclass = getattr(properties_material, member)
    try:
        print (subclass.bl_label)
        if subclass.bl_label not in ["xxxreview"]:
            subclass.COMPAT_ENGINES.add('BtoA')
            pass
    except:
        pass
for member in dir(properties_material):
    subclass = getattr(properties_material, member)
    try:
        print (subclass.bl_label)
        if subclass.bl_label not in ["xxxreview"]:
            subclass.COMPAT_ENGINES.add('BtoA')
            pass
    except:
        pass


del properties_material

def writeStandardMaterial(mat,textures):
    tslots = {}
    tslots['kd_color'] = None

    if textures:
        for i in textures:
            tname = textures[i]['name']
            if tname in mat.texture_slots:
                map = mat.texture_slots[tname]
            #use_map_alpha
            #use_map_ambient
                if map.use_map_color_diffuse:
                    tslots['kd_color'] =textures[i]['pointer']
            #use_map_color_emission
            #use_map_color_reflection
            #use_map_color_spec
            #use_map_color_transmission
            #use_map_density
            #use_map_diffuse
            #use_map_displacement
            #use_map_emission
            #use_map_emit
            #use_map_hardness
            #use_map_mirror
            #use_map_normal
            #use_map_raymir
            #use_map_reflect
            #use_map_scatter
            #use_map_specular
            #use_map_translucency
            #print tname 

    standard = AiNode(b"standard")
    if tslots['kd_color']:
        AiNodeLink(tslots['kd_color'],b"Kd_color",standard)
    else:
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

def writeAmbientOcclusion(mat,textures):
    ao = AiNode(b"ambien_occlusion")
    return ao

def writeUtility(mat,textures):
    util = mat.BtoA.utility
    node = AiNode(b"utility")
    AiNodeSetInt(node,b"color_mode",int(util.colorMode))
    AiNodeSetInt(node,b"shade_mode",int(util.shadeMode))
    AiNodeSetRGB(node,b"color",util.color.r,
                              util.color.g,
                              util.color.b)
    AiNodeSetFlt(node,b"opacity",util.opacity)
    return node

def writeWireframe(mat,textures):
    ao = AiNode(b"wireframe")
    AiNodeSetFlt(ao,b"line_width",2)
    AiNodeSetInt(ao,b"edge_type",1)
    return ao

class Materials:
    def __init__(self, scene,textures=None):
        self.scene = scene
        self.textures = None
        if textures:
            self.textures = textures.texturesDict
        self.materialDict = {}

    def writeMaterials(self):
        for mat in bpy.data.materials:
            self.writeMaterial(mat)

    def writeMaterial(self,mat):
        outmat = None
        if mat.BtoA.shaderType == 'STANDARD':
            outmat =writeStandardMaterial(mat,self.textures)
        elif mat.BtoA.shaderType =='AMBIENT_OCCLUSION':
            outmat = writeAmbientOcclusion(mat,self.textures)
        elif mat.BtoA.shaderType =='WIREFRAME':
            outmat = writeWireframe(mat,self.textures)
        elif mat.BtoA.shaderType =='UTILITY':
            outmat = writeUtility(mat,self.textures)

        AiNodeSetStr(outmat,b"name",mat.name.encode('utf-8'))
        self.materialDict[mat.as_pointer()] = outmat
        return outmat

 
