import json
meta=json.load(open('pack-meta.json'))
A={'adyar-wards':("Ward boundaries: DataMeet Municipal Spatial Data (Greater Chennai Corporation wards)","CC BY-SA 2.5 IN","https://github.com/datameet/Municipal_Spatial_Data"),
   'transit-stops':("Bus and metro stops: Chennai unified GTFS v0.2.0 (Ithu Ungal Soththu)","IIIT-Delhi open data terms","https://github.com/ungalsoththu/ChennaiGTFS"),
   'bus-network':("Stop-to-stop links derived from Chennai unified GTFS v0.2.0","IIIT-Delhi open data terms","https://github.com/ungalsoththu/ChennaiGTFS"),
   'places-real':("Bridges, organisations and news locations: public reference (Wikipedia, DT Next, Deccan Chronicle, The News Minute); positions approximate","CC BY-SA (Wikipedia facts); news linked, not reproduced",None),
   'utilities':("SYNTHETIC placeholders from the Chennai City Twin (water, sewerage, drains, groundwater, power, telecom). Not real assets.","Synthetic, no third-party content",None),
   'street-assets':("SYNTHETIC placeholders from the Chennai City Twin (streetlights, dustbins, toilets, shops, rooftop solar). Not real assets.","Synthetic, no third-party content",None)}
packs=[]
for pid,(t,lic,url) in A.items():
    att={"text":t,"license":lic}
    if url: att["url"]=url
    packs.append({"id":pid,"version":1,"format":"geojson","source":{"adapter":"assets","path":f"chennai/{pid}.geojson"},"attribution":att,"placement":{"altitudeReference":"ellipsoid"},"byteLength":meta[pid]["byteLength"],"sha256":meta[pid]["sha256"]})
def shot(i,t,lat,lon,alt,pitch,ids,heading=0,layers=None):
    s={"id":i,"title":t,"durationSec":4,"holdSec":3,"camera":{"lat":lat,"lon":lon,"alt":alt,"heading":heading,"pitch":pitch,"roll":0},"dataPackIds":ids}
    if layers: s["layers"]=layers
    return s
doc={"version":5,"scenes":[{"id":"chennai-adyar-twin","title":"Chennai City Twin: Adyar zone","dataPacks":packs,"shots":[
  shot("overview","Adyar zone, 13 wards",13.000,80.245,14000,-70,["adyar-wards"]),
  shot("transit","Real bus and metro network",13.005,80.240,7000,-55,["adyar-wards","transit-stops","bus-network"]),
  shot("places","Bridges, institutions and news",13.010,80.250,4500,-45,["adyar-wards","places-real"],heading=20),
  shot("utilities","Utilities (synthetic placeholders)",13.000,80.245,6000,-60,["adyar-wards","utilities"]),
  shot("street","Street assets (synthetic placeholders)",13.000,80.257,2200,-45,["adyar-wards","street-assets"],heading=330),
  shot("radio","Chennai radio stations",13.050,80.250,30000,-80,[],layers={"radio":{"enabled":True}})]}]}
open('../../chennai/chennai-adyar-twin.scene.json','w').write(json.dumps(doc,indent=1))
print('ok')
