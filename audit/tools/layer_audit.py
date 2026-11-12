"""Layer-by-layer printability check (like a slicer's support detection).
For each 0.2 mm layer: region with nothing under it (beyond a 45 deg step) is classified as
 island   - starts in mid-air (no contact with the layer below)        -> always a failure
 bridge   - anchored on two opposite sides; report the span            -> ok to 10 mm
 lip      - anchored on one side only (cantilever); report the depth   -> ok to ~1.5 mm, check to 3, fail beyond
"""
import numpy as np, trimesh, shapely
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
from shapely.ops import unary_union, polylabel
LH=0.2; ALLOW=0.25
def geoms(g):
    if g.is_empty: return []
    if g.geom_type=='Polygon': return [g]
    return [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
def slices(m):
    z0,z1=m.bounds[:,2]; hs=np.arange(LH/2,z1-z0,LH)
    secs=m.section_multiplane([0,0,z0],[0,0,1],hs)
    out=[]
    for s in secs:
        if s is None: out.append(Polygon()); continue
        out.append(unary_union([p.buffer(0) for p in s.polygons_full]))
    return hs,out
def layer_audit(m):
    hs,L=slices(m); ev=[]
    for i in range(1,len(L)):
        cur,prev=L[i],L[i-1]
        if cur.is_empty: continue
        sup=prev.buffer(ALLOW,join_style=2) if not prev.is_empty else Polygon()
        uns=cur.difference(sup)
        anchor=cur.intersection(sup)
        for c in geoms(uns):
            if c.area<0.08: continue
            host=[g for g in geoms(cur) if g.intersects(c)]
            touching=any(g.intersects(prev) for g in host) if not prev.is_empty else False
            cen=polylabel(c,0.05) if c.area>0.2 else c.representative_point(); r=c.exterior.distance(cen)
            if not touching:
                ev.append(dict(kind='island',z=float(hs[i]),area=round(c.area,2),size=round(2*r,2),at=[round(cen.x,1),round(cen.y,1)])); continue
            if 2*r<0.45: continue      # sub-line-width sliver
            # depth = farthest point of the patch from anything supported
            pts=[Point(p) for p in np.array(c.exterior.coords)[::max(1,len(c.exterior.coords)//60)]]+[cen]
            D=max(p.distance(anchor) for p in pts)
            far=max(pts,key=lambda p:p.distance(anchor))
            # bridge test: supported material on both sides of the farthest point, along the shortest crossing
            best=None
            for a in np.radians(np.arange(0,180,10)):
                u=np.array([np.cos(a),np.sin(a)]); span=[]
                for sgn in (1,-1):
                    ray=LineString([(far.x,far.y),(far.x+sgn*u[0]*30,far.y+sgn*u[1]*30)])
                    hit=ray.intersection(anchor)
                    span.append(None if hit.is_empty else hit.distance(far))
                if None not in span:
                    # the crossing must stay inside the layer (not jump a gap)
                    seg=LineString([(far.x+u[0]*span[0],far.y+u[1]*span[0]),(far.x-u[0]*span[1],far.y-u[1]*span[1])])
                    if seg.difference(cur.buffer(0.05)).length<0.1:
                        s=span[0]+span[1]; best=s if best is None else min(best,s)
            if best is not None and best<2.2*D+0.5:
                ev.append(dict(kind='bridge',z=float(hs[i]),span=round(best,2),area=round(c.area,2),at=[round(far.x,1),round(far.y,1)]))
            else:
                ev.append(dict(kind='lip',z=float(hs[i]),depth=round(D,2),area=round(c.area,2),at=[round(far.x,1),round(far.y,1)]))
    return ev
def summarize(ev):
    isl=[e for e in ev if e['kind']=='island']; br=[e for e in ev if e['kind']=='bridge']; lip=[e for e in ev if e['kind']=='lip']
    s=dict(islands=len(isl),island_max_area=max([e['area'] for e in isl],default=0),
           bridge_max=max([e['span'] for e in br],default=0),lip_max=max([e['depth'] for e in lip],default=0),
           lips_over_1p5=len([e for e in lip if e['depth']>1.5]),lip_area_over_1p5=round(sum(e['area'] for e in lip if e['depth']>1.5),1))
    s['verdict']='FAIL' if (max([e['area'] for e in isl if e['size']>=0.45 or e['area']>2],default=0)>0.5 or s['lip_max']>3.0 or s['bridge_max']>10) else ('CHECK' if (s['islands'] or s['lip_max']>1.5) else 'OK')
    return s
if __name__=='__main__':
    import sys,glob,os,json
    R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','stl',''); out={}
    for f in sorted(glob.glob(R+'*.stl')):
        m=trimesh.load(f); m.merge_vertices(); ev=layer_audit(m); s=summarize(ev); out[os.path.basename(f)]=dict(summary=s,events=ev)
        print(os.path.basename(f)[:30].ljust(30),s,flush=True)
    json.dump(out,open('layers.json','w'))
