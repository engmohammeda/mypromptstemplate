# Icon export pipeline — reference

Never hand-resize. Generate everything from one vector source, in a script committed to the repo.

## 1. Source layout
```
design/icons/
├── launcher/
│   ├── foreground.svg      # 108×108 viewBox, art inside the central 66
│   ├── background.svg      # 108×108, fully filled
│   └── monochrome.svg      # 108×108, single-color silhouette
├── ui/                     # 24×24 viewBox each
│   ├── ic_action_save.svg
│   └── ...
└── export.sh
```

## 2. Dependencies
```bash
# Vector → raster and cleanup
sudo apt-get install -y librsvg2-bin imagemagick optipng
npm i -g svgo
```

## 3. Export script

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC="design/icons/launcher"
RES="app/src/main/res"
OUT="build/icons"
mkdir -p "$OUT"

# --- Play Store icon: 512×512, flattened onto white (NO alpha) ---
rsvg-convert -w 512 -h 512 "$SRC/background.svg" -o "$OUT/bg512.png"
rsvg-convert -w 512 -h 512 "$SRC/foreground.svg" -o "$OUT/fg512.png"
magick "$OUT/bg512.png" "$OUT/fg512.png" -composite \
       -background white -alpha remove -alpha off \
       "$OUT/play-icon-512.png"
optipng -quiet -o5 "$OUT/play-icon-512.png"

# --- Legacy mipmaps for API < 26 ---
declare -A DPI=( [mdpi]=48 [hdpi]=72 [xhdpi]=96 [xxhdpi]=144 [xxxhdpi]=192 )
for d in "${!DPI[@]}"; do
  px=${DPI[$d]}
  mkdir -p "$RES/mipmap-$d"
  magick "$OUT/bg512.png" "$OUT/fg512.png" -composite \
         -resize "${px}x${px}" "$RES/mipmap-$d/ic_launcher.png"
  magick "$RES/mipmap-$d/ic_launcher.png" \
         \( +clone -alpha extract -draw "fill black polygon 0,0 0,$px $px,0 fill white circle $((px/2)),$((px/2)) $((px/2)),0" \) \
         -alpha off -compose CopyOpacity -composite "$RES/mipmap-$d/ic_launcher_round.png"
  optipng -quiet -o5 "$RES/mipmap-$d/"*.png
done

# --- iOS ---
rsvg-convert -w 1024 -h 1024 "$SRC/foreground.svg" -o "$OUT/ios-1024.png"
magick "$OUT/ios-1024.png" -background white -alpha remove -alpha off "$OUT/ios-1024.png"

# --- Web ---
svgo -i "$SRC/foreground.svg" -o "$OUT/favicon.svg"
for s in 16 32 48 180 192 512; do
  rsvg-convert -w $s -h $s "$SRC/foreground.svg" -o "$OUT/icon-$s.png"
done
magick "$OUT/icon-16.png" "$OUT/icon-32.png" "$OUT/icon-48.png" "$OUT/favicon.ico"
mv "$OUT/icon-180.png" "$OUT/apple-touch-icon.png"

echo "✅ Icons exported to $OUT and $RES"
```

## 4. UI icon set → VectorDrawables

```bash
#!/usr/bin/env bash
set -euo pipefail
# Optimize SVGs then convert with Android Studio's vd-tool (ships with the SDK)
for f in design/icons/ui/*.svg; do
  svgo -i "$f" -o "build/ui-opt/$(basename "$f")"
done
vd-tool -c -in build/ui-opt -out app/src/main/res/drawable
```
Post-process each generated XML:
- Replace hardcoded `android:fillColor="#000000"` with `?attr/colorControlNormal` or `@android:color/white` + `android:tint`.
- Add `android:autoMirrored="true"` to directional icons.
- Remove `android:width/height` overrides that differ from 24dp.

## 5. Validation script (run in CI)

```bash
#!/usr/bin/env bash
set -euo pipefail
fail=0

# Play icon must have no alpha
if magick identify -format '%A' build/icons/play-icon-512.png | grep -qi 'true\|blend'; then
  echo "❌ Play icon has an alpha channel"; fail=1
fi

# Play icon must be exactly 512×512
dim=$(magick identify -format '%wx%h' build/icons/play-icon-512.png)
[ "$dim" = "512x512" ] || { echo "❌ Play icon is $dim, expected 512x512"; fail=1; }

# Adaptive icon XML must declare a monochrome layer
grep -q '<monochrome' app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml \
  || { echo "❌ Missing <monochrome> layer"; fail=1; }

# UI icons must be 24dp and themed
for f in app/src/main/res/drawable/ic_*.xml; do
  grep -q 'android:width="24dp"' "$f" || { echo "⚠️  $f is not 24dp"; }
  grep -q '#FF000000\|#000000' "$f" && { echo "❌ $f has a hardcoded black fill"; fail=1; }
done

exit $fail
```

## 6. Safe-zone visual check
Render the foreground with a 66dp guide overlay and eyeball it:
```bash
rsvg-convert -w 432 -h 432 design/icons/launcher/foreground.svg -o /tmp/fg.png
magick /tmp/fg.png -fill none -stroke red -strokewidth 3 \
  -draw "circle 216,216 216,72" -draw "rectangle 84,84 348,348" /tmp/fg-guides.png
```
Anything crossing the red circle will be clipped on circular-mask launchers.

## 7. Device verification matrix
| Check | How |
|---|---|
| Circle / squircle / rounded-square masks | Pixel launcher developer options, or Android Studio's Image Asset preview |
| Themed (monochrome) icons | Pixel: Wallpaper & style → Themed icons |
| Notification icon | Trigger a notification; it must be a clean white silhouette |
| Small size legibility | View the app list, then the search results, then the recents switcher |
| Against real neighbours | Install next to WhatsApp, Gmail, Chrome — does it hold its own? |
| Light & dark wallpapers | Switch wallpapers and re-check contrast |

## 8. Commit policy
- Commit the **source SVGs** and the **generated Android resources** (they are build inputs).
- Do not commit intermediate PNGs in `build/`.
- Regenerate in CI and fail if the committed resources differ from the freshly generated ones.
