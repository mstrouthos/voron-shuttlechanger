import numpy as np, trimesh, manifold3d as mf
def to_mf(t):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices,np.float32),tri_verts=np.asarray(t.faces,np.uint32)))
def to_tm(m):
    g=m.to_mesh(); return trimesh.Trimesh(np.asarray(g.vert_properties)[:,:3],np.asarray(g.tri_verts),process=False)
def box(x0,x1,y0,y1,z0,z1):
    return mf.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cyl(axis,c,r,a0,a1,n=64):
    # axis 'x','y','z'; c = 2 coords of the centre in the other two axes (in order x,y,z skipping axis); a0..a1 along axis
    m=mf.Manifold.cylinder(a1-a0,r,r,n)  # along z from 0
    if axis=='z': return m.translate([c[0],c[1],a0])
    if axis=='y':  # rotate z->y : rotate -90 about x maps z to y
        m=m.rotate([-90,0,0]); return m.translate([c[0],a0,c[1]])
    if axis=='x':
        m=m.rotate([0,90,0]); return m.translate([a0,c[0],c[1]])
def prism_xz(pts,y0,y1):
    # polygon in XZ plane (x,z) extruded along +Y from y0 to y1
    P=np.asarray(pts,float)
    a=0.5*np.sum(P[:,0]*np.roll(P[:,1],-1)-np.roll(P[:,0],-1)*P[:,1])
    if a<0: P=P[::-1]
    cs=mf.CrossSection([P])
    m=mf.Manifold.extrude(cs,y1-y0)   # along z, polygon in xy -> (x, y=z_asm)
    m=m.rotate([90,0,0])   # (x,y,z)->(x,-z,y): poly y becomes z, extrude z becomes -y
    return m.translate([0,y1,0])
def union(*ms):
    out=ms[0]
    for m in ms[1:]: out=out+m
    return out
def project_y(m,y0,y1):
    """XZ silhouette of m extruded from y0 to y1"""
    cs=m.rotate([90,0,0]).project()          # (x,y,z)->(x,-z,y); project onto XY = (x,-z)
    e=mf.Manifold.extrude(cs,y1-y0)          # (x,-z_asm) in xy, extrude along z
    return e.rotate([-90,0,0]).translate([0,y0,0])   # (x,y,z)->(x,z,-y): y'=extrude, z'=z_asm
