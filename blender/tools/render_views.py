"""Rebuild B1 and render the named cameras into blender/renders/.

Run from the repository root (Windows and Linux alike):
    blender -b blender/buildings/b1/B1.blend -P blender/tools/render_views.py -- Cam_Ref Cam_Lobby Cam_Porch Cam_Aerial
An .osm path may come first after "--" if you do not want the default blender/data/map.osm.
This script does not save the .blend.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER_DIR = os.path.dirname(HERE)
SRC = os.path.join(BLENDER_DIR, 'buildings', 'b1', 'build_b1.py')
exec(compile(open(SRC, encoding='utf-8').read(), SRC, 'exec'), {'__file__': SRC, '__name__': '__main__'})

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
cams = [a for a in args if not a.endswith('.osm')] or ['Cam_Ref']
scene = bpy.context.scene
out_dir = os.path.join(BLENDER_DIR, 'renders')
os.makedirs(out_dir, exist_ok=True)
for name in cams:
    inside = name.startswith('Cam_Aud')   # interior shots: hide the exterior shell (the hall sits inside it)
    for cname in ('B1_Building', 'B1_Context'):
        bpy.data.collections[cname].hide_render = inside
    bpy.data.objects['B1_AudCeiling'].hide_render = name == 'Cam_AudPlan'
    scene.camera = bpy.data.objects[name]
    scene.render.filepath = os.path.join(out_dir, name + '.png')
    bpy.ops.render.render(write_still=True)
scene.camera = bpy.data.objects['Cam_Ref']
