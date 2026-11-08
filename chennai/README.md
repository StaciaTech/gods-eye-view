# Chennai City Twin pack for God's Eye View

A Director scene with six camera shots over Adyar zone (Greater Chennai Corporation, Zone XIII), backed by six GeoJSON data packs. It uses the app's documented data-pack format. No core code is changed.

## What's inside

| Pack | Features | Status | Source |
|---|---|---|---|
| `adyar-wards` | 13 ward boundaries | Real | DataMeet Municipal Spatial Data, CC BY-SA 2.5 IN |
| `transit-stops` | 318 bus and metro stops | Real | Chennai unified GTFS v0.2.0 (Ithu Ungal Soththu) |
| `bus-network` | 727 stop-to-stop links | Real (derived) | Same GTFS feed |
| `places-real` | 5 bridges, 10 organisations, 3 news locations | Real, positions approximate | Wikipedia, DT Next, Deccan Chronicle, The News Minute |
| `utilities` | Water, sewerage, drains, groundwater, power, telecom (486) | **Synthetic placeholders** | Chennai City Twin generator |
| `street-assets` | Streetlights, dustbins, toilets, shops, rooftop solar (1,640) | **Synthetic placeholders** | Chennai City Twin generator |

The last shot turns on the app's own Radio layer, which lists Chennai stations through Radio Browser.

Files:
- `chennai/chennai-adyar-twin.scene.json` is the scene to import.
- `public/scene-assets/chennai/*.geojson` holds the data packs, served by the app at `/scene-assets/chennai/`.
- `chennai/twin/chennai-city-twin.html` is the Chennai City Twin itself, a standalone 2D twin of Adyar zone that opens in any browser with no install. It has Map, Wireframe and Split views; the real MTC and CMRL timetable with stop departures and moving vehicles; 21 infrastructure layers with toggles, legend, source tags and info cards; consent, sentiment and decision-maker panels; sun position; and the Chennai radio station list.
- `chennai/chennai-city-twin-bundle.zip` bundles all of the above in one download.

## Open the 2D twin

Download `chennai/twin/chennai-city-twin.html` and open it in a browser. It runs fully offline, except the sun-position panel, which loads the SunCalc library from jsDelivr. The "Data & methods" button lists every layer as real, approximate, modelled or synthetic.

## Run it

1. Install Node 24 (24.14 or later) or use Docker, as in the main README.
2. From the repo root, run `npm ci` and then `npm run dev`.
3. Open the app, go to Director, choose **IMPORT**, and pick `chennai/chennai-adyar-twin.scene.json`.
4. Review the import, apply it, and play the scene. Each shot loads only its own packs.

## Notes

- **Heights:** GeoJSON heights are WGS84 ellipsoid metres. In Chennai, ground level sits about 88 m below the ellipsoid, so features are placed at −88 m plus a small offset. If they float or sink on the 3D tiles, change `GROUND` in `tools/chennai/build_pack.py` and rebuild.
- **Styling:** the data-pack format ignores feature properties for styling, so every feature draws in the default pack style. Names and layer types are kept in `properties` for later use.
- **Timetables:** the GTFS feed is a static timetable. The app's Transit layer expects GTFS-Realtime, which Chennai doesn't publish, so stops and links appear as geometry rather than moving vehicles.
- **Cameras:** there is no Chennai traffic camera feed. Neither the Greater Chennai Police nor the Corporation publishes one, so the CCTV layer stays empty here.
- **Integrity:** each pack's `byteLength` and `sha256` are recorded in the scene. If you rebuild a pack, rebuild the scene too, so both scripts need to run.

## Rebuild

From `tools/chennai/`, after exporting `twin-export.json` from the City Twin page:

```
python3 build_pack.py
python3 build_scene.py
```
