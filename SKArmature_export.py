## SKArmature_export.py
#  This is a script to apply armature modifier and export frames.
#  Path syntax is hardcoded so that it will work on Windows only.

bl_info = {
    "name": "SKArmature export",
    "blender": (4, 0, 0),
    "category": "Import-Export"
}

import bpy
from os import mkdir
from os.path import exists

def apply_export_frames():
    folder_name = bpy.data.filepath.split('\\')[-1].split('.')[0]
    folder_name += "_frames"
    if not exists(folder_name):
        mkdir(folder_name)
    
    bpy.ops.screen.frame_jump(end=True)
    last_frame_number = bpy.data.scenes[0].frame_current
    
    if len(bpy.context.selected_objects) != 1:
        print("SKArmature ERROR: Please select only 1 object! Objects selected:", bpy.context.selected_objects)
        return
    
    # Going through all frames
    for i in range(last_frame_number):
        bpy.ops.ed.undo_push()
        bpy.data.scenes['Scene'].frame_set(i + 1)
        modified_object = bpy.context.selected_objects[0]

        print("SKArmature DEBUG: Processing frame no.", bpy.data.scenes[0].frame_current)

        modifier_found = False
        for modifier in modified_object.modifiers:
            if modifier.type == 'ARMATURE':
                bpy.ops.object.modifier_apply(modifier=modifier.name)
                modifier_found = True
                break

        if not modifier_found:
            print("SKArmature ERROR: ARMATURE modifier not found! Object modifiers:", modified_object.modifiers)
            return

        bpy.ops.export_scene.fbx(filepath=folder_name + '\\frame_' + str(i + 1) + '.fbx')
        bpy.ops.ed.undo()


### Menu entry

class ApplyExportOperator(bpy.types.Operator):
    bl_idname = "ska.apply_export"
    bl_label = "SKArmature export"
    
    def execute(self, context):
        apply_export_frames()
        return {'FINISHED'}

def aemenu_draw(self, context):
    self.layout.operator(ApplyExportOperator.bl_idname)

def register():
    bpy.utils.register_class(ApplyExportOperator)
    bpy.types.TOPBAR_MT_file.append(aemenu_draw)

def unregister():
    bpy.utils.unregister_class(ApplyExportOperator)