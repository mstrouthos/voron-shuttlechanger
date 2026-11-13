"""Still images of the v36 model for the README and the assembly guide (vtk, off-screen)."""
import pickle,numpy as np,vtk,trimesh,os
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
import build36 as B
from geo import to_tm
P=B.build(); H=B.hardware(); N={k:to_tm(v) for k,v in {**P,**H}.items()}
old=pickle.load(open("old_parts.pkl","rb"))
for k,(g,v,t,c,m) in old.items(): N.setdefault(k,trimesh.Trimesh(v,t,process=False))
ST='#c4c9cf'
COL=dict(plate='#3f6fb5',slab='#5b8fd6',cplate='#e0a030',cover='#58a36c',arm='#d9622b',tool='#8a6ff0',dock='#3aa6a0',spacer='#7a8794',spacer2='#7a8794',ebb='#1f7a3d',
 g1='#c9a227',g2='#c9a227',dg='#b98b1e',motor='#2b2f35',spring='#7f9bb8',tap='#8d949c',duct='#e0862f',fans='#33373d',tz_sh='#e0862f',tz_fan='#33373d',tz_he='#aab0b7',tz_bl='#d9d9d2',
 dr_sh='#e0862f',dr_fan='#33373d',dr_he='#aab0b7',dr_bl='#d9d9d2',pad='#b3261e',ptfe='#e8e8e2',fil='#e24a8d',inserts='#c8a24a',rail='#b9bec4',mags_h='#8b8f96',mags_t='#8b8f96',dmag='#8b8f96',hooks='#3a3d42',steel='#3a3d42')
HEAD=['plate','slab','cplate','cover','spacer','spacer2','ebb','ebbscrews','g1','dg','brg','motor','axles','pivot','mags_h','gpins','tapscrews','mscrews','cscrews','inserts','adj','spring','tap','duct','fans','dscrew']
ARM=B.ARMG; TOOL=B.TOOLG+['tz_he','tz_bl','tz_sh','tz_fan','fscrew_tz']; DOCK=B.DOCKG
N['rail']=to_tm(__import__('geo').box(-100,100,-54,-34,50,70))
def rgb(h): h=h.lstrip('#'); return [int(h[i:i+2],16)/255 for i in (0,2,4)]
def actor(tm,col,T=None,op=1.0):
    v=np.asarray(tm.vertices,float); f=np.asarray(tm.faces)
    if T is not None: v=(T[:3,:3]@v.T).T+T[:3,3]
    pd=vtk.vtkPolyData(); pts=vtk.vtkPoints(); pts.SetData(numpy_to_vtk(v,deep=True)); pd.SetPoints(pts)
    ca=vtk.vtkCellArray(); ca.SetData(3,numpy_to_vtkIdTypeArray(f.astype(np.int64).ravel(),deep=True)); pd.SetPolys(ca)
    n=vtk.vtkPolyDataNormals(); n.SetInputData(pd); n.SetFeatureAngle(35); n.SplittingOn(); n.ConsistencyOn()
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(n.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m)
    pr=a.GetProperty(); pr.SetColor(*rgb(col)); pr.SetOpacity(op); pr.SetAmbient(0.25); pr.SetDiffuse(0.75); pr.SetSpecular(0.15); pr.SetSpecularPower(20)
    return a
def tr(x=0,y=0,z=0):
    T=np.eye(4); T[:3,3]=[x,y,z]; return T
def rotarm(phi,hx=0,hy=0):
    c,s=np.cos(-phi),np.sin(-phi); R=np.eye(4); R[0,0]=c;R[0,2]=-s;R[2,0]=s;R[2,2]=c      # rotation about Y through the pivot, mirrored sense
    A=tr(-B.PIV[0],0,-B.PIV[1]); Bk=tr(B.PIV[0]+hx,hy,B.PIV[1]); return Bk@R@A
def shot(name,items,pos,tgt,size=(1500,1100),zoom=1.0):
    ren=vtk.vtkRenderer(); ren.SetBackground(1,1,1)
    for k,T,op in items:
        if k in N: ren.AddActor(actor(N[k],COL.get(k,ST),T,op))
    w=vtk.vtkRenderWindow(); w.SetOffScreenRendering(1); w.AddRenderer(ren); w.SetSize(*size); w.SetMultiSamples(8)
    cam=ren.GetActiveCamera(); cam.SetPosition(*pos); cam.SetFocalPoint(*tgt); cam.SetViewUp(0,0,1); cam.SetViewAngle(24); ren.ResetCameraClippingRange(); cam.Zoom(zoom)
    L=vtk.vtkLight(); L.SetLightTypeToCameraLight(); L.SetPosition(-0.6,0.8,1); L.SetIntensity(0.55); ren.AddLight(L)
    w.Render(); f=vtk.vtkWindowToImageFilter(); f.SetInput(w); f.Update(); pw=vtk.vtkPNGWriter(); pw.SetFileName('v36/img/'+name); pw.SetInputConnection(f.GetOutputPort()); pw.Write(); print(name)
os.makedirs('v36/img',exist_ok=True)
def grp(keys,T=None,op=1.0,skip=()): return [(k,T,op) for k in keys if k not in skip]
head=grp(HEAD,skip=('duct','fans','dscrew'))+grp(ARM,rotarm(0))
shot('head_front.png',head+grp(TOOL),(-190,-330,200),(2,5,66),zoom=1.1)
shot('head_right.png',head+grp(TOOL),(260,-250,190),(6,12,66),zoom=1.1)
shot('extruder.png',grp(HEAD,skip=('duct','fans','dscrew','cover','ebb','spacer','spacer2','ebbscrews','tap','cscrews'))+grp(ARM,rotarm(0))+grp(['tool','fil','ptfe','balls']),(-60,-260,150),(0,4,88),zoom=1.25)
shot('tool.png',grp(TOOL),(-150,-170,150),(0,-2,52),zoom=1.0)
S=B.SHIFT
docks=[]
for i in (-1,0,1):
    docks+=grp(DOCK,tr(i*B.PITCH))
    if i!=0: docks+=grp(TOOL,tr(i*B.PITCH+S))
shot('dock.png',docks+[('rail',None,1.0)]+grp(TOOL,tr(S)),(150,210,200),(0,-12,40),zoom=1.15)
shot('toolchange.png',docks+[('rail',None,1.0)]+grp(TOOL,tr(S))+grp(HEAD,tr(S,0),skip=('duct','fans','dscrew'))+grp(ARM,rotarm(B.PHI_MAX,S,0)),(-260,-260,260),(-5,-5,60),zoom=1.1)
# printed parts, as they lie on the bed
import glob
x=0; items=[]
for f in sorted(glob.glob('v36/stl/*.stl')):
    m=trimesh.load(f); k=os.path.basename(f); N[k]=m; col={'01':'plate','02':'slab','03':'cplate','04':'cover','05':'arm','06':'spacer','10':'tool','13':'dock'}[k[:2]]; COL[k]=COL[col]
    w_=m.extents[0]; items.append((k,tr(x+w_/2,0,0),1.0)); x+=w_+12
shot('printed_parts.png',items,(x/2-40,-520,420),(x/2-6,0,10),size=(1800,800),zoom=1.05)
