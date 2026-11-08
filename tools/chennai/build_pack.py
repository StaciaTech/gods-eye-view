import json, math, os, hashlib
GEV='../..'; OUT=f'{GEV}/public/scene-assets/chennai'; os.makedirs(OUT, exist_ok=True)
COS=math.cos(math.radians(13.03))
GROUND=-88.0   # approx. ellipsoid height of ground in Chennai (geoid sits ~88 m below the ellipsoid). Adjust if features float or sink.
H=lambda up: round(GROUND+up,1)
def unproj(x,y): return [round(80+x/COS/1e5,6), round(12-y/1e5,6)]
d=json.load(open('twin-export.json'))
def pt(fid,lonlat,up,props): return {"type":"Feature","id":fid,"properties":props,"geometry":{"type":"Point","coordinates":[lonlat[0],lonlat[1],H(up)]}}
def ln(fid,a,b,up,props): return {"type":"Feature","id":fid,"properties":props,"geometry":{"type":"LineString","coordinates":[[a[0],a[1],H(up)],[b[0],b[1],H(up)]]}}
def write(name, feats):
    fc={"type":"FeatureCollection","features":feats}
    b=json.dumps(fc,separators=(',',':')).encode()
    open(f'{OUT}/{name}.geojson','wb').write(b)
    npos=sum(1 if f['geometry']['type']=='Point' else (len(f['geometry']['coordinates']) if f['geometry']['type']=='LineString' else sum(len(r) for r in f['geometry']['coordinates'])) for f in feats)
    assert len(feats)<=2000 and npos<=50000 and len(b)<=8*1024*1024, (name,len(feats),npos)
    print(f'{name}: {len(feats)} features, {npos} positions, {len(b)//1024} KB')
    return {"byteLength":len(b),"sha256":hashlib.sha256(b).hexdigest()}
meta={}
# 1 wards
w=json.load(open('wards_s.json')); feats=[]
for f in w['features']:
    p=f['properties']
    if p['Zone_No']!='XIII': continue
    g=f['geometry']; polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
    for k,poly in enumerate(polys):
        rings=[[[round(c[0],6),round(c[1],6),H(5)] for c in r] for r in poly]
        feats.append({"type":"Feature","id":f"ward-{p['Ward_No']}-{k}","properties":{"ward":p['Ward_No'],"zone":"XIII Adyar"},"geometry":{"type":"Polygon","coordinates":rings}})
meta['adyar-wards']=write('adyar-wards',feats)
# 2 stops
meta['transit-stops']=write('transit-stops',[pt(f"stop-{i}",unproj(s['x'],s['y']),15,{"name":s['n'],"operator":s['ag'],"ward":s['w']}) for i,s in enumerate(d['ts'])])
# 3 network
meta['bus-network']=write('bus-network',[ln(f"edge-{i}",unproj(d['ts'][e[0]]['x'],d['ts'][e[0]]['y']),unproj(d['ts'][e[1]]['x'],d['ts'][e[1]]['y']),10,{"mode":"metro" if e[2] else "bus"}) for i,e in enumerate(d['te'])])
L={x['id']:x for x in d['inf']}
def pts(ids,up):
    out=[]
    for i in ids:
        for f in L[i]['f']: out.append(pt(f"{i}-{f['id']}",unproj(f['x'],f['y']),up,{"name":f['n'],"layer":L[i]['n'],"source":L[i]['src']}))
    return out
def lines(ids,up):
    out=[]
    for i in ids:
        for k,l in enumerate(L[i]['lines']): out.append(ln(f"{i}-{k}",unproj(*l[0]),unproj(*l[1]),up,{"layer":L[i]['n'],"source":"syn"}))
    return out
meta['places-real']=write('places-real',pts(['bridge','org','news'],40))
meta['utilities']=write('utilities',pts(['wstn','spump','mh','gw','sub','xf','tower','bb','exch'],20)+lines(['wmain','sewer','drain','feeder'],8))
meta['street-assets']=write('street-assets',pts(['light','bin','toilet','shop','solar'],12))
json.dump(meta,open('pack-meta.json','w'))
