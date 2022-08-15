import bpy

class COMMON_PT_myPanel(bpy.types.Panel):
    bl_label = "Common"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CDBA"

    def draw(self,ctx):
        col =self.layout.column()

        row = col.row(align = True)
        row.prop(ctx.scene, 'character_name', text='Character')

        row = col.row(align = True)
        row.prop(ctx.scene, 'armature_name', text='Armature')

        row = col.row(align = True)
        row.prop(ctx.scene, 'ip', text='IP')

        row = col.row(align = True)
        row.prop(ctx.scene, 'port', text='Port')

        row = col.row(align = True)
        row.prop(ctx.scene, 'gpu', text='Use GPU')

        row = col.row(align = True)
        row.prop(ctx.scene, 'translation', text='Use Translation')

        row = col.row(align = True)
        row.prop(ctx.scene, 'insert_keyframe', text='Insert Keyframe')

        row = col.row(align = True)
        row.prop(ctx.scene, 'insert_interval', text='Insert Interval')

        row = col.row(align = True)
        row.prop(ctx.scene, 'quality', text='Compression(0~100)')

        row = col.row(align = True)
        row.operator("ops.fix_bones", text = "Fix Bones")
        

class OFFLINE_PT_myPanel(bpy.types.Panel):
    bl_label = "Image or Video"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CDBA"

    def draw(self,ctx):
        col =self.layout.column()

        row = col.row(align = True)
        row.operator("ops.offline_animation", text = "Offline Animation")

class WEBCAM_PT_myPanel(bpy.types.Panel):
    bl_label = "Webcam"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CDBA"

    def draw(self,ctx):
        col =self.layout.column()

        row = col.row(align = True)
        row.prop(ctx.scene, 'fps', text='FPS')

        row = col.row(align = True)
        row.prop(ctx.scene, 'width', text='Width')        
        
        row = col.row(align = True)
        row.prop(ctx.scene, 'height', text='Height')

        row = col.row(align = True)
        row.operator("ops.webcam_animation", text = "Webcam Animation")