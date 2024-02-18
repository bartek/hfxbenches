# Benches of Halifax

Work in progress rendering at [justbartek.ca/hfxbenches](https://justbartek.ca/hfxbenches)

_A nice place to sit welcomes you to your city._

This project contains open-format data, a rendered map, and a variety of helper
scripts which supported the cataloging of all public benches within the Halifax
peninsula (and surrounding)

## Categorization

* Types
    * Park (Benches located in playgrounds, recreational areas)
    * School (Benches located on school grounds)
    * Public (Benches in public spaces)

## Cataloging

I run around with my phone and capture benches!

As I wish to capture photos of every bench, and Apple makes it simple to interact with their photo data pragmatically, I use a combination of open source tooling and simple Python to obtain geo data for each bench I capture. This makes it fairly simple to automate plotting the benches onto a map.

```
brew install dogsheep-photos
dogsheep-photos apple-photos photos.db
```

This gets us an sqlite database containing metadata for all photos within Apple Photos. Prior to exporting, I will place the most recent capture of benches into an album (which is used later), and I use the `Information` tab to set the bench type through keywords (eg `type:public` keyword)

With the sqlite database processed, obtaining the GeoJSON data is simply running `scripts/fetch.py`. Ensure any new albums are in the top level variable (within the script):

```
python3 scripts/fetch.py > data.geojson
```

The resulting FeatureCollection then represents all points of interest collected thus far.

## Rendered Map

A work in progress map containing the rendered data is available.

```
brew install http-server
http-server --cors=localhost
```

Visit http://localhost:8081/static/index.html

Prettier map soon!

## TODO:

* Artifacts:
    -> Coverage map so I can see where I need to run
    -> Map of rendered benches
* Utility to export Strava runs, pick the "bench catalog" ones, and import into sqlite database as part of coverage map

## Resources

* [Secrets of good benches and seating in public space](https://issuu.com/stipoteam/docs/benches)
