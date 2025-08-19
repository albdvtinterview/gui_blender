import bpy
import sys
import json
import os


def get_all_objects_in_collection(in_collection):
    objs = list(in_collection.objects)
    for child in in_collection.children:
        objs.extend(get_all_objects_in_collection(child))
    return objs


def export_collection_to_fbx(in_collection_name, in_output_fbx_path):
    blender_file_name = os.path.basename(bpy.data.filepath)

    if in_collection_name == "Scene Collection":
        collection = bpy.context.scene.collection
    else:
        collection = bpy.data.collections.get(in_collection_name)

    if collection is None:
        return {
            "success": False,
            "desc": f"Collection name not found in {blender_file_name}!",
            "collection": in_collection_name,
            "export_path": in_output_fbx_path
        }

    # Снимаем выделение если оно есть на обьектах
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

    # Получаем все объекты из коллекции и подколлекций
    objects_to_export = get_all_objects_in_collection(collection)

    # Выделяем объекты нужной нам коллекции
    for obj in objects_to_export:
        obj.select_set(True)

    # Делаем активным первый объект
    if objects_to_export:
        bpy.context.view_layer.objects.active = objects_to_export[0]

    # Экспорт FBX
    bpy.ops.export_scene.fbx(
        filepath=in_output_fbx_path,
        use_selection=True,
        apply_unit_scale=True,
        bake_space_transform=True,
        object_types={'MESH'}
    )

    return {
        "success": True,
        "desc": "FBX successfully exported from Blender!",
        "collection": in_collection_name,
        "export_path": in_output_fbx_path
    }


# Получаем аргументы после "--"
collection_name = sys.argv[-2]
output_fbx_path = sys.argv[-1]

result = export_collection_to_fbx(collection_name, output_fbx_path)

# Выводим JSON
print("===BEGIN_JSON===")
print(json.dumps(result))
print("===END_JSON===")
