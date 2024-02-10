#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <partial_geojson>" >&2
  exit 1
fi

# Take partial and merge it with existing data.geojson, creating a merged.geojson
# Once validated, can move into data.geojson
cp data.geojson data.geojson.back
jq -s '{type: "FeatureCollection", features: (.[0].features + .[1].features)}' data.geojson.back $1 > data.geojson
rm data.geojson.back
