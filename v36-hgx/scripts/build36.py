"""v36 draft: build35 mirrored left-right, so the swing arm is on the left (as the idler arm on a CW2) and the
EBB SB2209 USB stands on the right side in its stock orientation. Everything except the Tap holes is a plain mirror."""
import numpy as np, manifold3d as mf
import build35 as B0
from geo import *
from build35 import cy,cx_,cz,ok,tear,above
B0.TAP_TOP=[(-15.05,62.4),(15.7,62.4)]; B0.TAP_LOW=[(-17.45,11.9),(17.9,11.9)]   # pre-mirrored: the Tap's holes are not symmetric
MIR=lambda m: m.mirror([1,0,0])
PIV=np.array([-B0.PIV[0],B0.PIV[1]]); SCR=(-B0.SCR[0],B0.SCR[1]); XPIN=-B0.XPIN; ZPIN=B0.ZPIN; G2=(-B0.G2[0],B0.G2[1])
SHIFT=-B0.SHIFT; DODGE=B0.DODGE; SAFE=B0.SAFE; PITCH=B0.PITCH; PHI_MAX=B0.PHI_MAX; LS,LP,LG=B0.LS,B0.LP,B0.LG
XE=-B0.XLT                                           # right edge of the head where the board mounts
EB_HOLE=B0.EB_HOLE
# board (BigTreeTech CAD): 39.5 (bx) x 66.5 (by); holes at (bx,by) = (24.79,15.18) and (12.01,27.2). Stock CW2 orientation: Y = y0 + by, Z = z0 - bx.
EB_Y0=EB_HOLE[0][0]-15.18; EB_Z1=EB_HOLE[0][1]+24.79; EB_X=XE+6.7     # board front edge (y), top edge (z), PCB face towards the head (x)
def rotY(m,c,ang): return B0.rotY(m,c,-ang)          # the mirrored arm opens the other way
def build():
    P={k:MIR(v) for k,v in B0.build().items()}
    P['tool']=B0.build()['tool'] if False else P['tool']        # the tool is symmetric
    return P
def hardware():
    H={k:MIR(v) for k,v in B0.hardware().items()}
    H['ebb']=box(EB_X,EB_X+1.6,EB_Y0,EB_Y0+66.5,EB_Z1-39.5,EB_Z1)
    env=box(EB_X+1.6,EB_X+8.1,EB_Y0+0.5,EB_Y0+66.0,EB_Z1-39.0,EB_Z1-0.5)+box(EB_X-6.35,EB_X,EB_Y0+0.5,EB_Y0+66.0,EB_Z1-39.0,EB_Z1-0.5)
    for y,z in EB_HOLE: env-=cx_(y,z,3.7,EB_X-7,EB_X+9)
    H['ebbenv']=env
    sc=None
    for y,z in EB_HOLE:
        q=cx_(y,z,1.5,EB_X-10.4,EB_X+1.6)+cx_(y,z,2.75,EB_X+1.6,EB_X+4.6); sc=q if sc is None else sc+q
    H['ebbscrews']=sc
    H['spacer2']=cx_(EB_HOLE[1][0],EB_HOLE[1][1],3.2,XE+0.05,XE+6.65)-cx_(EB_HOLE[1][0],EB_HOLE[1][1],1.7,XE-1,XE+8)
    for k,v in H.items(): ok(v,k)
    return H
ARMG=B0.ARMG; TOOLG=B0.TOOLG; DOCKG=B0.DOCKG
if __name__=='__main__':
    P=build(); H=hardware()
    for k,v in P.items(): print(k,'bodies',len(v.decompose()),'bbox',np.round(v.bounding_box(),1).tolist())
    print('board: y %.1f..%.1f  z %.1f..%.1f  x %.1f..%.1f (with connectors)'%(EB_Y0,EB_Y0+66.5,EB_Z1-39.5,EB_Z1,EB_X-6.35,EB_X+8.1))
