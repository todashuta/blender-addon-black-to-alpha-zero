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


bl_info = {
    "name": "Black to Alpha Zero",
    "author": "todashuta",
    "version": (1, 0, 0),
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
        if hasattr(context.space_data, "image"):
            if context.space_data.image is not None:
                return True
        return False

    def execute(self, context):
        image = context.space_data.image
        width, height = image.size
        pxs = list(image.pixels[:])

        for i in range(0, width*height*4, 4):
            r, g, b = pxs[i], pxs[i+1], pxs[i+2]
            if r == 0 and g == 0 and b == 0:
                pxs[i+3] = 0  # Alpha

        image.pixels = pxs

        return {"FINISHED"}


class BLACK_TO_ALPHA_ZERO_PT_panel(bpy.types.Panel):
    bl_label = "Black to Alpha Zero"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.operator(BLACK_TO_ALPHA_ZERO_OT_main.bl_idname)


classes = [
    BLACK_TO_ALPHA_ZERO_OT_main,
    BLACK_TO_ALPHA_ZERO_PT_panel,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
