import imp
from arnold import *
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty
from bl_ui.properties_data_lamp import DataButtonsPanel

if "bpy" in locals():
    imp.reload(PointLight)
    imp.reload(SpotLight)
else:
    import bpy
    from . import PointLight
    from . import SpotLight

#################
# Lamp
################
Lamp = bpy.types.Lamp
Lamp.BtoA_exposure = FloatProperty(name="Exposure",description="Light Exposure",
                    min=0,max=100,default=0)
Lamp.BtoA_shadow_enable = BoolProperty(name="Enable Shadows",description="",default=True)

Lamp.BtoA_shadow_density = FloatProperty(name="Density",description="Shadow Density",
                                        min = 0,max=1000,default=1)

Spot = bpy.types.SpotLamp
Spot.BtoA_penumbra_angle = FloatProperty(name="Penumbra Angle",description="Penumbra Angle",
        min = 0,max=180,default=1,subtype="ANGLE")
Spot.BtoA_aspect_ratio = FloatProperty(name="Aspect Ratio",description="Aspect",
        min = 0,max=10,default=1)



class BtoA_lamp_ui(DataButtonsPanel, bpy.types.Panel):
    bl_label = "Lamp"
    COMPAT_ENGINES = {'BtoA'}

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp

        layout.prop(lamp, "type", expand=True)

        split = layout.split()

        col = split.column()
        sub = col.column()
        sub.prop(lamp, "color", text="")
        sub.prop(lamp, "energy")
        sub.prop(lamp,"BtoA_exposure")

        #if lamp.type in {'POINT', 'SPOT'}:
            #sub.label(text="Falloff:")
            #sub.prop(lamp, "falloff_type", text="")
            #sub.prop(lamp, "distance")

            #if lamp.falloff_type == 'LINEAR_QUADRATIC_WEIGHTED':
            #    col.label(text="Attenuation Factors:")
            #    sub = col.column(align=True)
            #    sub.prop(lamp, "linear_attenuation", slider=True, text="Linear")
            #    sub.prop(lamp, "quadratic_attenuation", slider=True, text="Quadratic")

            #col.prop(lamp, "use_sphere")

        if lamp.type == 'AREA':
            col.prop(lamp, "distance")
            col.prop(lamp, "gamma")

        col = split.column()
        #col.prop(lamp, "use_negative")
        col.prop(lamp, "use_own_layer", text="This Layer Only")
        col.prop(lamp, "use_specular")
        col.prop(lamp, "use_diffuse")

class BtoA_shadow_ui(DataButtonsPanel, bpy.types.Panel):
    bl_label = "Shadow"
    COMPAT_ENGINES = {'BtoA'}

    @classmethod
    def poll(cls, context):
        lamp = context.lamp
        engine = context.scene.render.engine
        return (lamp and lamp.type in {'POINT', 'SUN', 'SPOT', 'AREA'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp

        #layout.prop(lamp, "shadow_method", expand=True)
        layout.prop(lamp,"BtoA_shadow_enable")

        #if lamp.shadow_method == 'NOSHADOW' and lamp.type == 'AREA':
        #    split = layout.split()

         #   col = split.column()
         #   col.label(text="Form factor sampling:")

          #  sub = col.row(align=True)

           # if lamp.shape == 'SQUARE':
           #     sub.prop(lamp, "shadow_ray_samples_x", text="Samples")
           # elif lamp.shape == 'RECTANGLE':
           #     sub.prop(lamp, "shadow_ray_samples_x", text="Samples X")
           #     sub.prop(lamp, "shadow_ray_samples_y", text="Samples Y")

        if (lamp.BtoA_shadow_enable):
            split = layout.split()
            col = split.column()
            col.prop(lamp, "shadow_color")
            col.prop(lamp, "BtoA_shadow_density", text="Density")

            col = split.column()
            col.prop(lamp, "use_shadow_layer", text="This Layer Only")
            #col.prop(lamp, "use_only_shadow")

            split = layout.split()
        
            col = split.column()
            col.label(text="Sampling:")

            if lamp.type in {'POINT', 'SUN', 'SPOT'}:
                sub = col.row()
                sub.prop(lamp, "shadow_ray_samples", text="Samples")
                sub.prop(lamp, "shadow_soft_size", text="Soft Size")

            elif lamp.type == 'AREA':
                sub = col.row(align=True)

                if lamp.shape == 'SQUARE':
                    sub.prop(lamp, "shadow_ray_samples_x", text="Samples")
                elif lamp.shape == 'RECTANGLE':
                    sub.prop(lamp, "shadow_ray_samples_x", text="Samples X")
                    sub.prop(lamp, "shadow_ray_samples_y", text="Samples Y")

                #col.row().prop(lamp, "shadow_ray_sample_method", expand=True)

                #if lamp.shadow_ray_sample_method == 'ADAPTIVE_QMC':
                #    layout.prop(lamp, "shadow_adaptive_threshold", text="Threshold")

            if lamp.type == 'AREA' and lamp.shadow_ray_sample_method == 'CONSTANT_JITTERED':
                row = layout.row()
                row.prop(lamp, "use_umbra")
                row.prop(lamp, "use_dither")
                row.prop(lamp, "use_jitter")

class BtoA_spotlamp_ui(DataButtonsPanel, bpy.types.Panel):
    bl_label = "Spot Shape"
    COMPAT_ENGINES = {'BtoA'}

    @classmethod
    def poll(cls, context):
        lamp = context.lamp
        engine = context.scene.render.engine
        return (lamp and lamp.type == 'SPOT') and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp
        split = layout.split()

        col = split.column()
        sub = col.column()
        sub.prop(lamp, "spot_size", text="Cone Angle")
        sub.prop(lamp, "BtoA_penumbra_angle", text="Penumbra")
        sub.prop(lamp, "BtoA_aspect_ratio", text="Aspect Ratio")
        #col.prop(lamp, "use_square")
        col.prop(lamp, "show_cone")

        col = split.column()

        #col.prop(lamp, "use_halo")
        #sub = col.column(align=True)
        #sub.active = lamp.use_halo
        #sub.prop(lamp, "halo_intensity", text="Intensity")
        #if lamp.shadow_method == 'BUFFER_SHADOW':
            #sub.prop(lamp, "halo_step", text="Step")

del DataButtonsPanel



class Lights:
    '''This class handles the export of all lights'''
    def __init__(self):
        pass
        
    def writeLights(self):
        for i in bpy.data.lamps:
            if i.type == 'POINT':
               light = PointLight.PointLight(i)
               light.write()
            elif i.type == 'SPOT':
               light = SpotLight.SpotLight(i)
               light.write()


