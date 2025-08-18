import bpy
import sys
import json
import os

# Получаем путь FBX из аргументов
fbx_path = sys.argv[-1]

result = {}
try:
    if not os.path.exists(fbx_path):
        result = {
            "success": False,
            "desc": f"Fbx file not found with import file path!",
            "imported_file": f"{fbx_path}"
        }
    else:
        bpy.ops.import_scene.fbx(filepath=fbx_path)

    imported_objects = [obj.name for obj in bpy.context.selected_objects]

    result = {
        "success": True,
        "desc": "Fbx successfully imported to blender!",
        "imported_file": f"{fbx_path}"
    }
except Exception as e:
    result = {
        "success": False,
        "desc": str(e),
        "imported_file": f"{fbx_path}"
    }

# Выводим JSON с метками
print("===BEGIN_JSON===")
print(json.dumps(result))
print("===END_JSON===")
