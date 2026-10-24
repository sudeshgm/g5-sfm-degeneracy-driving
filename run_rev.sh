#!/bin/bash
# Second worker: clip list in reverse; skips clips done or in progress (tmp dir exists). Same disk guard.
cd "$(dirname "$0")"
for l in $(tac clip_list.txt); do
  id=${l#*/}
  [ -e results/clips/$id.json ] && continue
  [ -d /workspace/g5/tmp/$id ] && { echo MEET; exit 0; }
  free=$(df --output=avail -BG / | tail -1 | tr -dc 0-9)
  [ "$free" -lt 8 ] && { echo LOWDISK; exit 1; }
  python3 process_clip.py "$l" || echo "FAIL $l"
done
echo REVDONE
