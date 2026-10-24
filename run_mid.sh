#!/bin/bash
# Third worker: from clip 101 forward; skips done/in-progress clips; same disk guard.
cd "$(dirname "$0")"
for l in $(tail -n +101 clip_list.txt); do
  id=${l#*/}; [ -e results/clips/$id.json ] && continue
  free=$(df --output=avail -BG / | tail -1 | tr -dc 0-9); [ "$free" -lt 8 ] && { echo LOWDISK; exit 1; }
  python3 process_clip.py "$l" || echo "FAIL $l"
done; echo MIDDONE
