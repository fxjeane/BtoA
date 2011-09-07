import imp
from arnold import *
from ..GuiUtils import pollLight
from bpy.props import (CollectionProperty,StringProperty, BoolProperty,
                       IntProperty, FloatProperty, FloatVectorProperty,
                       EnumProperty, PointerProperty)
from bl_ui import properties_data_lamp
pm = properties_data_lamp


if "bpy" not in locals():
    import bpy

enumValue = ("POINTLIGHT","Point","")
blenderType = "POINT"

# There must be one class that inherits from bpy.types.PropertyGroup
# Here we place all the parameters for the Material
class BtoAPointLightSettings(bpy.types.PropertyGroup):
    opacity = FloatProperty(name="Opacity",default=1)

className = BtoAPointLightSettings
bpy.utils.register_class(className)

# Define as many GUI pannels as necessary, they must all follow this structure.
# Utility only needs one
class BtoA_pointLight_gui(pm.DataButtonsPanel, bpy.types.Panel):
    bl_label = "Point"
    COMPAT_ENGINES = {'BtoA'}

    @classmethod
    def poll(cls, context):
        # this function from ..Materials handles the polling to display the
        # gui widget
        return False#pollLight(cls,context,enumValue[0],blendLights={"POINT"} )

    def draw(self, context):
        pass
        #mat = pm.active_node_mat(context.material)
        #layout = self.layout
        # Here we see mat.BtoA.utility . The "utility" part is created by the 
        # auto loader and it is derived from the python module name. In this case
        # utility.py
        #layout.prop(mat.BtoA.utility,"colorMode")
        #layout.prop(mat.BtoA.utility,"shadeMode")
        #layout.prop(mat.BtoA.utility,"color")
        #layout.prop(mat.BtoA.utility,"opacity")

