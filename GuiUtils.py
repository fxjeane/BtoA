from bl_ui import properties_material
pm = properties_material

def pollMaterial(cls,context,shaderType,matTypes={'SURFACE','WIRE'}):
    mat = context.material
    activeMat = pm.active_node_mat(mat)
    engine = context.scene.render.engine
    btoaSpec = activeMat.BtoA.shaderType == shaderType
    return pm.check_material(mat) and btoaSpec and (mat.type in matTypes) and (engine in cls.COMPAT_ENGINES)

def pollLight(cls,context,lightType,blendLights={'POINT'}):
    lmp = context.lamp
    matchLight = lmp.BtoA.lightType == lightType
    matchEngine = context.scene.render.engine in cls.COMPAT_ENGINES
    matchBlendLight = lmp.type in blendLights
    return matchBlendLight and matchEngine and matchLight
