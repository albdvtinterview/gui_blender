import bpy
import sys
import json
import os


def import_fbx(fbx_path):
    try:
        if not os.path.exists(fbx_path):
            return {
                "success": False,
                "desc": f"Fbx file not found with import file path!",
                "imported_file": f"{fbx_path}"
            }
        else:
            bpy.ops.import_scene.fbx(
                filepath=fbx_path,
                axis_forward='-Y',
                axis_up='Z'
            )
            bpy.ops.wm.save_mainfile()

        return {
            "success": True,
            "desc": "Fbx successfully imported to blender!",
            "imported_file": f"{fbx_path}"
        }
    except Exception as e:
        return {
            "success": False,
            "desc": str(e),
            "imported_file": f"{fbx_path}"
        }


# Получаем путь FBX из аргументов
in_fbx_path = sys.argv[-1]

result = import_fbx(in_fbx_path)

# Выводим JSON с метками
print("===BEGIN_JSON===")
print(json.dumps(result))
print("===END_JSON===")
