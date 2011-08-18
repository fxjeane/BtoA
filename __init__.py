
bl_info = {
    "name": "BtoA - Blender to Arnold",
    "author": "Rudy Cortes - fxjeane@gmail.com",
    "version": (0, 0, 1),
    "blender": (2, 5, 8),
    "api": 35622,
    "location": "Render > Engine > Arnold",
    "description": "Basic Arnold integration for blender",
    "warning": "Still early alpha",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"\
        "Scripts/Render/PovRay",
    "tracker_url": "https://projects.blender.org/tracker/index.php?"\
        "func=detail&aid=23145",
    "category": "Render"}


import imp
if "bpy" in locals():
    imp.reload(utils)
    imp.reload(BtoAUi)
    imp.reload(Renderer)
    imp.reload(Options)
    imp.reload(Camera)
    imp.reload(Lights)
    imp.reload(Materials)
    imp.reload(Meshes)
else:
    import bpy
    from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty
    from . import utils
    from . import BtoAUi
    from . import Renderer
    from . import Options
    from . import Camera
    from . import Lights
    from . import Materials
    from . import Meshes


def register():
    bpy.utils.register_module(__name__)
    print("BtoA Registered")
    
    #############################
    # Scene data
    ############################# 
    Scene = bpy.types.Scene
    # Sampling
    Scene.BtoA_AA_samples = IntProperty(
            name="Global Samples", description="Number of samples per pixel",
            min=-10, max=32, default=2)
    
    Scene.BtoA_AA_pattern = EnumProperty(items=(("0","regular",""),
                             ("1","random",""),
                             ("2","jittered",""),
                             ("3","multi_jittered",""),
                             ("4","poisson_bc",""),
                             ("5","dithered",""),
                             ("6","nrooks",""),
                             ("7","schlick","")), 
                             name="Pattern", description="AA pattern", default="3")

    Scene.BtoA_AA_seed = IntProperty(
            name="Seed", description="Seed for samples",
            min=-1000, max=1000, default=1)

    Scene.BtoA_AA_motionblur_pattern = EnumProperty(items=(("0","regular",""),
                             ("1","random",""),
                             ("2","jittered",""),
                             ("3","multi_jittered",""),
                             ("4","poisson_bc",""),
                             ("5","dithered",""),
                             ("6","nrooks",""),
                             ("7","schlick","")), 
                             name="MBlur Pattern", description="Motionblur pattern",
                             default="2")

    Scene.BtoA_AA_sample_clamp = FloatProperty(
            name="Sample Clamp", description="Clamp distance",default=1e+30)

    Scene.BtoA_AA_clamp_affect_aovs = BoolProperty(name="Clamp AOVs", 
                                            description="Clamp affects AOVs")
    Scene.BtoA_AA_sampling_dither = IntProperty(
            name="Dither", description="Dither for samples",
            min=0, max=100, default=4)

    # GI Settings
    Scene.BtoA_GI_diffuse_samples = IntProperty(
            name="GI Diffuse", description="Number of samples for GI diffuse",
            min=0, max=32, default=2)
    Scene.BtoA_GI_glossy_samples = IntProperty(
            name="GI Glossy", description="Number of samples for GI glossy",
            min=0, max=32, default=2)


    Scene.BtoA_GI_diffuse_depth = IntProperty(
            name="Diffuse Depth", description="Number of bounces for GI diffuse",
            min=0, max=32, default=2)
    Scene.BtoA_GI_glossy_depth = IntProperty(
            name="Glossy Depth", description="Number of bounces for glossy",
            min=0, max=32, default=2)
    Scene.BtoA_GI_reflection_depth = IntProperty(
            name="Reflection", description="Number of bounces for reflection",
            min=0, max=32, default=2)
    Scene.BtoA_GI_refraction_depth = IntProperty(
            name="Refraction", description="Number of bounces for refraction",
            min=0, max=32, default=2)

    # interactive settings
    
    Scene.BtoA_progressive_min = IntProperty(
            name="Progressive Min", description="lowest sample for progressive",
            min=-20, max=0, default=-3)
    Scene.BtoA_enable_progressive = BoolProperty(name="Progressive", 
                                            description="Enable Progressive Rendering",
                                            default=True)
    Scene.BtoA_bucket_size = IntProperty(
            name="Bucket Size", description="Size of buckets",
            min=8, max=1024, default=64)
    Scene.BtoA_bucket_scanning = EnumProperty(items=(("-1","Bucket Scan",""),
                             ("0","top",""),
                             ("1","bottom",""),
                             ("2","letf",""),
                             ("3","right",""),
                             ("4","random",""),
                             ("5","woven",""),
                             ("6","spiral",""),
                             ("7","hilbert","")), 
                             name="", description="bucket scanning", default="0")


def unregister():
    import bpy
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

