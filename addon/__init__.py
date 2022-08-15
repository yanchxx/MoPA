import bpy
from . import ops
from .panels import *

bl_info = {
    "name" : "CDBA",
    "author" : "Chuanhang Yan",
    "description" : "CharacterDriven-BlenderAddon",
    "blender" : (2, 93, 0),
    "version" : (1, 0, 0),
}

CLASSES = [
    CommonPanel,
    OfflinePanel,
    WebcamPanel,
    ops.FixBones,
    ops.OfflineAnimation,
    ops.WebcamAnimation,
]

PROPS = [
    ('character_name',bpy.props.StringProperty(name='armature_name', default='Armature')),
    ('armature_name',bpy.props.StringProperty(name='character_name', default='Armature')),
    ('ip',bpy.props.StringProperty(name='ip', default='127.0.0.1')),
    ('port',bpy.props.StringProperty(name='port', default='10005')),
    ('fps',bpy.props.IntProperty(name='fps', default=24)),
    ('insert_keyframe',bpy.props.BoolProperty(name='insert_keyframe', default=True)),
    ('gpu',bpy.props.BoolProperty(name='gpu', default=True)),
    ('translation',bpy.props.BoolProperty(name='translation', default=True)),
    ('quality',bpy.props.IntProperty(name='quality', default=60)),
    ('width',bpy.props.IntProperty(name='width', default=512)),
    ('height',bpy.props.IntProperty(name='height', default=512)),
]

def register():
    # register bpy.context variable
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for cls in CLASSES:
        bpy.utils.register_class(cls)

def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)