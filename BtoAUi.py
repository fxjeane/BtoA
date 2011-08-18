import bpy

# Use some of the existing buttons.
from bl_ui import properties_render
properties_render.RENDER_PT_render.COMPAT_ENGINES.add('BtoA')
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add('BtoA')
# properties_render.RENDER_PT_antialiasing.COMPAT_ENGINES.add('POVRAY_RENDER')
properties_render.RENDER_PT_shading.COMPAT_ENGINES.add('BtoA')
properties_render.RENDER_PT_output.COMPAT_ENGINES.add('BtoA')
del properties_render


class RenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (rd.use_game_engine == False) and (rd.engine in cls.COMPAT_ENGINES)

class BtoA_interactive_settings(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Interactive Settings"
    COMPAT_ENGINES = {'BtoA'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        split = layout.split()
        col = split.column()
        col.prop(scene, "BtoA_enable_progressive")
        col.prop(scene,"BtoA_bucket_size")
        col2 = split.column()
        col2.prop(scene,"BtoA_progressive_min")
        col2.label(text="Bucket Scanning")
        col2.prop(scene,"BtoA_bucket_scanning")

class BtoA_render_sample_settings(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Sampler Settings"
    COMPAT_ENGINES = {'BtoA'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        split = layout.split()
        col = split.column()
        col.label(text="Anti-Aliasing")
        split = layout.split()
        col = split.column()
        col.prop(scene, "BtoA_AA_samples")
        col2 = split.column()
        col2.prop(scene,"BtoA_AA_pattern")
        col.prop(scene,"BtoA_AA_seed")
        col2.prop(scene,"BtoA_AA_motionblur_pattern")       
        col.prop(scene,"BtoA_AA_sample_clamp")
        col2.prop(scene,"BtoA_AA_clamp_affect_aovs")       
        col.prop(scene,"BtoA_AA_sampling_dither")
 
        split = layout.split()
        col = split.column()
        col.label(text="GI Samples")
        split = layout.split()
        col = split.column()
        col.prop(scene,"BtoA_GI_diffuse_samples")
        col2 = split.column()
        col2.prop(scene,"BtoA_GI_glossy_samples")

class BtoA_render_raydepth_settings(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Ray Depth"
    COMPAT_ENGINES = {'BtoA'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        split = layout.split()
        col = split.column()
        col.prop(scene, "BtoA_GI_diffuse_depth")
        col.prop(scene,"BtoA_GI_reflection_depth")
        col2 = split.column()
        col2.prop(scene,"BtoA_GI_glossy_depth")
        col2.prop(scene,"BtoA_GI_refraction_depth")


