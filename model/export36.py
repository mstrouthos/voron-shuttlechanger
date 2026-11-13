"""Export the v35 printed parts in print orientation and run the repo's layer audit on each."""
import sys,json,numpy as np,trimesh
sys.path.insert(0,'/Users/michalis/Development/voron-shuttlechanger/audit/tools')
from layer_audit import layer_audit
import build36 as B
from geo import to_tm
P=B.build()
R={'back':[[1,0,0],[0,0,1],[0,-1,0]],'right':[[0,0,1],[0,1,0],[-1,0,0]],'left':[[0,0,-1],[0,1,0],[1,0,0]],'up':[[1,0,0],[0,1,0],[0,0,1]],'yaxis':[[1,0,0],[0,0,-1],[0,1,0]],'front':[[1,0,0],[0,0,-1],[0,1,0]],'xaxis':[[0,0,-1],[0,1,0],[1,0,0]]}
ORI=dict(plate='back',slab='back',cplate='back',cover='front',arm='left',tool='up',dock='front',spacer='xaxis')
NAME=dict(plate='01_back_plate_body',slab='02_back_plate_front_slab',cplate='03_coupling_plate',cover='04_gear_housing',arm='05_swing_arm',spacer='06_SB2209_spacer_x2',tool='10_tool_body_x_each_tool',dock='13_dock_with_wiper_x_each_tool')
import os; os.makedirs('v36/stl',exist_ok=True); rep={}
for k,m in P.items():
    t=to_tm(m); t.apply_transform(np.vstack([np.c_[np.array(R[ORI[k]],float),[0,0,0]],[0,0,0,1]])); t.apply_translation([-t.bounds[:,0].mean(),-t.bounds[:,1].mean(),-t.bounds[0,2]])
    t=trimesh.Trimesh(t.vertices,t.faces,process=True); t.export('v36/stl/%s.stl'%NAME[k])
    r=trimesh.load('v36/stl/%s.stl'%NAME[k]); ev=layer_audit(r)
    bed=r.section(plane_origin=[0,0,0.1],plane_normal=[0,0,1]); bed_a=sum(p.area for p in bed.to_2D()[0].polygons_full) if bed is not None else 0
    bad=[e for e in ev if e['kind']=='island' or (e['kind']=='bridge' and e.get('span',0)>10) or (e['kind']=='lip' and e.get('depth',0)>3)]
    chk=[e for e in ev if e['kind']=='lip' and 1.5<e.get('depth',0)<=3]
    rep[NAME[k]]=dict(size=[round(float(x),1) for x in r.extents],watertight=bool(r.is_watertight),bodies=len(r.split(only_watertight=False)),bed_mm2=round(float(bed_a)),fails=bad,check=chk,
        max_bridge=max([e.get('span',0) for e in ev if e['kind']=='bridge'],default=0),max_lip=max([e.get('depth',0) for e in ev if e['kind']=='lip'],default=0))
    print(NAME[k],rep[NAME[k]]['size'],'wt',r.is_watertight,'bodies',rep[NAME[k]]['bodies'],'bed',round(bed_a),'fails',len(bad),'check',len(chk),'maxbridge',rep[NAME[k]]['max_bridge'],'maxlip',rep[NAME[k]]['max_lip'])
    for e in bad[:8]: print('    FAIL',e)
json.dump(rep,open('v36/layer_audit.json','w'),indent=1)
