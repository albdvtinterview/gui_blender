import bpy
import sys
import json
import os


# Получаем аргументы после "--"
collection_name = sys.argv[-2]
output_fbx_path = sys.argv[-1]

collection = bpy.data.collections.get(collection_name)
blender_file_name = os.path.basename(bpy.data.filepath)

if collection is None:
    result = {
        "success": False,
        "desc": f"Collection name not found in {blender_file_name}!",
        "collection": collection_name,
        "export_path": output_fbx_path
    }
else:
    # Снимаем выделение со всех объектов
    bpy.ops.object.select_all(action='DESELECT')

    # Выбираем объекты коллекции
    for obj in collection.objects:
        obj.select_set(True)

    bpy.ops.export_scene.fbx(filepath=output_fbx_path, use_selection=True, path_mode='COPY')

    result = {
        "success": True,
        "desc": "Fbx successfully exported from blender!",
        "collection": collection_name,
        "export_path": output_fbx_path
    }

# Выводим JSON с метками
print("===BEGIN_JSON===")
print(json.dumps(result))
print("===END_JSON===")
