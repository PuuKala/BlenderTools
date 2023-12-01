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
    
    saved_properties = None
    saved_modifier = None
    
    if len(bpy.context.selected_objects) != 1:
        print("SKArmature ERROR: Please select only 1 object! Objects selected:", bpy.context.selected_objects)
        return
    
    # Going through all frames
    for i in range(last_frame_number):
        bpy.ops.ed.undo_push()
        bpy.data.scenes['Scene'].frame_set(i + 1)
        modified_object = bpy.context.selected_objects[0]
        print("SKArmature DEBUG: Processing frame no.", bpy.data.scenes[0].frame_current)
        for modifier in modified_object.modifiers:
            if modifier.type == 'ARMATURE':
                print("SKArmature DEBUG: Modifier found frame no.", bpy.data.scenes[0].frame_current)
                #bpy.ops.ed.undo_push()
                bpy.ops.object.modifier_apply(modifier=modifier.name)
                print("SKArmature DEBUG: Modifier applied frame no.", bpy.data.scenes[0].frame_current)
                break
        """
        for obj in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            #modifier_found = False
            if saved_properties:
                new_modifier = obj.modifiers.new('Armature', 'ARMATURE')
                for property in saved_properties:
                    setattr(new_modifier, saved_
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE':
                    saved_modifier = modifier
                    #modifier_found = True
                    #bpy.ops.object.modifier_set_active(modifier=modifier.name)
                    saved_property_names = [property.identifier for property in modifier.bl_rna.properties
                                        if not property.is_readonly]
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
                    break
        """
            
            #if not modifier_found:
            #    print("SKArmature ERROR: No ARMATURE modifier found in", obj.name)
            #    return
        
        print("SKArmature DEBUG: Exporting frame no.", bpy.data.scenes[0].frame_current)
        bpy.ops.export_scene.fbx(filepath=folder_name + '\\frame_' + str(i + 1) + '.fbx')
        print("SKArmature DEBUG: Undoing frame no.", bpy.data.scenes[0].frame_current)
        bpy.ops.ed.undo()
        print("Jumping to frame", bpy.data.scenes['Scene'].frame_current, "+", i, "+", 1)


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
    #aemenu = next(iter([i for i in bpy.types.TOPBAR_MT_file._dyn_ui_initialize() if i.__name__ == aemenu_draw.__name__]), None)
    #if not aemenu:
    bpy.utils.register_class(ApplyExportOperator)
    bpy.types.TOPBAR_MT_file.append(aemenu_draw)

def unregister():
    bpy.utils.unregister_class(ApplyExportOperator)