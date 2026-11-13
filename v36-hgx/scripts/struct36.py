"""Thin-wall check: rays cast inward from surface samples; report clusters thinner than 1.2 mm."""
import numpy as np,trimesh,json,glob,os
rep={}
for f in sorted(glob.glob('v36/stl/*.stl')):
    m=trimesh.load(f); n=os.path.basename(f)[:-4]
    pts,fi=trimesh.sample.sample_surface(m,12000,seed=1); nr=m.face_normals[fi]
    o=pts-nr*0.02; loc,ri,ti=m.ray.intersects_location(o,-nr,multiple_hits=False)
    d=np.full(len(pts),np.inf); cos=np.abs((m.face_normals[ti]*nr[ri]).sum(1)); dist=np.linalg.norm(loc-o[ri],axis=1)+0.02
    ok=cos>0.5; d[ri[ok]]=dist[ok]
    thin=d<1.2; P=pts[thin]; D=d[thin]; cl=[]
    if len(P):
        left=np.ones(len(P),bool)
        while left.any():
            i=np.where(left)[0][0]; grp=np.zeros(len(P),bool); grp[i]=True; fr=[i]
            while fr:
                j=fr.pop(); nb=left&~grp&(np.linalg.norm(P-P[j],axis=1)<2.0); grp|=nb; fr+=list(np.where(nb)[0])
            left&=~grp
            if grp.sum()>=4: cl.append(dict(n=int(grp.sum()),area=round(float(grp.sum()/12000*m.area),1),min=round(float(D[grp].min()),2),med=round(float(np.median(D[grp])),2),lo=np.round(P[grp].min(0),1).tolist(),hi=np.round(P[grp].max(0),1).tolist()))
    cl.sort(key=lambda c:-c['area']); rep[n]=cl
    print(n,'thin clusters',len(cl))
    for c in cl[:9]: print('   ',c)
json.dump(rep,open('v36/struct_audit.json','w'),indent=1)
