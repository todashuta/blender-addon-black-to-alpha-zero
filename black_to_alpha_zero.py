# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import numpy as np


bl_info = {
    "name": "Black to Alpha Zero",
    "author": "todashuta",
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "location": "Image Editor > Sidebar > Tool > Black to Alpha Zero",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Image"
}


class BLACK_TO_ALPHA_ZERO_OT_main(bpy.types.Operator):
    bl_idname = "image.black_to_alpha_zero"
    bl_label = "Black to Alpha 0"
    bl_description = "Black to Alpha Zero"

    @classmethod
    def poll(cls, context):
        #for area in context.screen.areas:
        #    if area.type == "IMAGE_EDITOR":
        #        if area.spaces.active.image is not None:
        #            print("active", area.spaces.active.image)
        #            print("ctx", context.space_data.image)
        #            return True
        scene = context.scene
        use_another_image = scene.black_to_alpha_zero_use_another_image
        mask_source_imagename = scene.black_to_alpha_zero_mask_source_imagename
        if not hasattr(context.space_data, "image"):
            return False
        if context.space_data.image is None:
            return False
        if use_another_image:
            if mask_source_imagename not in bpy.data.images:
                return False
            target_image = context.space_data.image
            mask_source_image = bpy.data.images[mask_source_imagename]
            if target_image.size[:] != mask_source_image.size[:]:
                return False
        return True

    def execute(self, context):
        scene = context.scene
        target_image = context.space_data.image

        if scene.black_to_alpha_zero_use_another_image:
            mask_source_image = bpy.data.images[scene.black_to_alpha_zero_mask_source_imagename]
        else:
            mask_source_image = target_image

        width, height = target_image.size
        target_image_pixel_data = np.zeros((width, height, 4), "f")
        mask_source_pixel_data = np.zeros((width, height, 4), "f")

        target_image.pixels.foreach_get(target_image_pixel_data.ravel())
        mask_source_image.pixels.foreach_get(mask_source_pixel_data.ravel())

        R = mask_source_pixel_data[:,:,0]
        G = mask_source_pixel_data[:,:,1]
        B = mask_source_pixel_data[:,:,2]
        A = mask_source_pixel_data[:,:,3]

        A[np.where((R == 0) & (G == 0) & (B == 0))] = 0

        target_image_pixel_data[:,:,3] = A

        target_image.pixels.foreach_set(target_image_pixel_data.ravel())
        target_image.update()

        return {"FINISHED"}


class BLACK_TO_ALPHA_ZERO_PT_panel(bpy.types.Panel):
    bl_label = "Black to Alpha Zero"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene, "black_to_alpha_zero_use_another_image")
        row = layout.row()
        row.enabled = scene.black_to_alpha_zero_use_another_image
        row.prop_search(scene, "black_to_alpha_zero_mask_source_imagename", bpy.data, "images", text="")
        layout.operator(BLACK_TO_ALPHA_ZERO_OT_main.bl_idname)


classes = (
        BLACK_TO_ALPHA_ZERO_OT_main,
        BLACK_TO_ALPHA_ZERO_PT_panel,
)

scene_props = {
        "black_to_alpha_zero_mask_source_imagename": bpy.props.StringProperty(name="Mask Source Image", default="", description=""),
        "black_to_alpha_zero_use_another_image": bpy.props.BoolProperty(name="Use Another Image as a Mask", default=False, description=""),
}


def register():
    for c in classes:
        bpy.utils.register_class(c)

    for name, prop in scene_props.items():
        setattr(bpy.types.Scene, name, prop)


def unregister():
    for name in scene_props.keys():
        if hasattr(bpy.types.Scene, name):
            delattr(bpy.types.Scene, name)

    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
