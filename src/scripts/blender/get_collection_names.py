import bpy
import json

names = [c.name for c in bpy.data.collections]
names.insert(0, "All")

print("===BEGIN_JSON===")
print(json.dumps(names, indent=4))
print("===END_JSON===")
