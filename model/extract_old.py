"""Pull the v32 meshes (Tap, hotends, shrouds, duct, fans) out of the v32.4 viewer page into old_parts.pkl.
Run from this folder: python extract_old.py   (reads `git show redesign-v31:docs/index.html`)"""
import re,json,base64,pickle,subprocess,numpy as np
s=subprocess.check_output(['git','show','redesign-v31:docs/index.html']).decode()
D=json.loads(re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>',s,re.S).group(1)); out={}
for p in D['parts']:
    v=np.frombuffer(base64.b64decode(p['v']),dtype=np.float32).reshape(-1,3).astype(float)
    t=np.frombuffer(base64.b64decode(p['i']),dtype=np.uint32).reshape(-1,3).astype(int) if 'i' in p else np.arange(len(v)).reshape(-1,3)
    out[p['id']]=(p.get('grp'),v,t,p.get('col'),p.get('metal'))
pickle.dump(out,open('old_parts.pkl','wb')); print(len(out),'parts')
