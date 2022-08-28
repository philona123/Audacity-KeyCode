import bpy
import os


height = 0.902
width = 0.916

bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
bpy.ops.object.delete(use_global=False)
fp = '/Users/user/Desktop/audacity/bp/plan.svg'
bpy.ops.import_curve.svg(filepath = fp)
bpy.ops.object.select_all(action='DESELECT') 
bpy.ops.object.select_by_type(type='CURVE')
bpy.context.view_layer.objects.active=bpy.data.objects["Curve"]
bpy.ops.object.join() 
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='CURVE')
bpy.ops.object.modifier_add(type='SOLIDIFY')


#import plane
fp = '/Users/user/Desktop/audacity/bp/plane.svg'
plane = bpy.ops.import_curve.svg(filepath = fp)
bpy.context.object.modifiers['Solidify'].offset = 1
bpy.context.object.active_material.diffuse_color = (1, 1, 1, 1)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.convert(target='MESH')
bpy.ops.object.select_all(action='SELECT')

bpy.context.view_layer.objects.active=bpy.data.objects["Curve"]
bpy.context.view_layer.objects.active=bpy.data.objects["Curve.001"]
bpy.ops.object.parent_set(type='OBJECT')

#bpy.ops.object.join()
bpy.context.object.dimensions = [width,-1 * height,0.300]
bpy.context.object.location[1] = -1 * height

bpy.ops.object.select_all(action='SELECT')
bpy.context.object.scale[2] =  18


objects = [
{'imageSize': (902, 916), 'item': 'window', 'length': 104, 'width': 19, 'origin': (879, 136), 'orientation': 'vertical', 'coordinates': [869, 84, 888, 188]},
{'imageSize': (902, 916), 'item': 'window', 'length': 104, 'width': 20, 'origin': (583, 860), 'orientation': 'horizontal', 'coordinates': [531, 850, 635, 870]},
{'imageSize': (902, 916), 'item': 'window', 'length': 107, 'width': 19, 'origin': (141, 860), 'orientation': 'horizontal', 'coordinates': [87, 850, 194, 869]},
{'imageSize': (902, 916), 'item': 'door', 'length': 102, 'width': 102, 'origin': (528, 204), 'orientation': 'left', 'coordinates': [477, 153, 579, 255]},
{'imageSize': (902, 916), 'item': 'door', 'length': 106, 'width': 105, 'origin': (418, 385), 'orientation': 'left', 'coordinates': [365, 332, 471, 437]},
{'imageSize': (902, 916), 'item': 'window', 'length': 104, 'width': 20, 'origin': (50, 136), 'orientation': 'vertical', 'coordinates': [40, 84, 60, 188]},
{'imageSize': (902, 916), 'item': 'window', 'length': 102, 'width': 19, 'origin': (200, 36), 'orientation': 'horizontal', 'coordinates': [149, 26, 251, 45]},
{'imageSize': (902, 916), 'item': 'door', 'length': 106, 'width': 103, 'origin': (639, 388), 'orientation': 'left', 'coordinates': [587, 335, 690, 441]},
{'imageSize': (902, 916), 'item': 'basin', 'length': 165, 'width': 60, 'origin': (836, 608), 'orientation': 'right', 'coordinates': [806, 525, 866, 690]},
{'imageSize': (902, 916), 'item': 'basin', 'length': 120, 'width': 62, 'origin': (599, 76), 'orientation': 'top', 'coordinates': [539, 45, 659, 107]},
{'imageSize': (902, 916), 'item': 'window', 'length': 105, 'width': 21, 'origin': (879, 381), 'orientation': 'vertical', 'coordinates': [868, 328, 889, 433]},
{'imageSize': (902, 916), 'item': 'window', 'length': 99, 'width': 21, 'origin': (879, 627), 'orientation': 'vertical', 'coordinates': [868, 577, 889, 676]},
{'imageSize': (902, 916), 'item': 'bed', 'length': 138, 'width': 94, 'origin': (224, 370), 'orientation': 'top', 'coordinates': [177, 301, 271, 439]},
{'imageSize': (902, 916), 'item': 'window', 'length': 108, 'width': 25, 'origin': (52, 616), 'orientation': 'vertical', 'coordinates': [39, 562, 64, 670]},
{'imageSize': (902, 916), 'item': 'window', 'length': 109, 'width': 25, 'origin': (52, 330), 'orientation': 'vertical', 'coordinates': [39, 275, 64, 384]},
{'imageSize': (902, 916), 'item': 'roundTable', 'length': 125, 'width': 93, 'origin': (644, 395), 'orientation': 'none', 'coordinates': [597, 332, 690, 457]},
{'imageSize': (902, 916), 'item': 'bed', 'length': 110, 'width': 105, 'origin': (805, 391), 'orientation': 'top', 'coordinates': [752, 336, 857, 446]},
{'imageSize': (902, 916), 'item': 'roundTable', 'length': 153, 'width': 106, 'origin': (228, 375), 'orientation': 'none', 'coordinates': [175, 298, 281, 451]},
{'imageSize': (902, 916), 'item': 'bed', 'length': 117, 'width': 107, 'origin': (545, 198), 'orientation': 'left', 'coordinates': [486, 144, 603, 251]}
]

def do_boolean():
    return

def get_shape(origin,length,width,orient):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(origin[0]/1000, (origin[1]/1000)*-1, 0.1), scale=(length/1000,(width*2.5)/1000,0.075))
    if orient == 'vertical':
     bpy.context.object.rotation_euler[2] = 1.5708
    bpy.ops.object.select_all(action='DESELECT')
    scene.objects["Curve"].select_set(True)
    bpy.context.view_layer.objects.active = scene.objects["Curve"]
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cube"]
    bpy.ops.object.modifier_apply(modifier="Boolean")
    # Select the object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()
    bpy.ops.object.select_all(action='DESELECT')
    file_loc = '/Users/user/Desktop/audacity/bp/repo/window.obj'
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
    



context = bpy.context
scene = context.scene
for i in objects:
    if i['item']=="window":
        get_shape(i['origin'],i['length'],i['width'],i['orientation'])


# WINDOW
foo_objs = [obj for obj in bpy.data.objects if obj.name.startswith("window")]
for index, obj in enumerate(foo_objs, start=0): 
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    info = [x for x in objects if x['item']=='window'][index]
    bpy.context.object.dimensions = [info['length']/1000,0.075, (info['width']*1.5)/1000 ]
    if info['orientation'] == 'vertical':
     bpy.context.object.rotation_euler[2] = 1.5708
    bpy.context.object.location = (info['origin'][0]/1000, (info['origin'][1]/1000)*-1  ,0.1)

## BED

##blend_file_path = bpy.data.filepath
##directory = os.path.dirname(blend_file_path)
##target_file = os.path.join(directory, 'myfile.obj')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.obj(filepath='/Users/user/Desktop/audacity/bp/out/scene.obj')