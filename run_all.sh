#!/bin/bash
# Sequential driver: one clip at a time, raw data deleted after each; stops if free disk < 8 GB.
cd "$(dirname "$0")"
for l in $(cat clip_list.txt); do
  free=$(df --output=avail -BG / | tail -1 | tr -dc 0-9)
  if [ "$free" -lt 8 ]; then echo "LOW DISK ${free}G, stopping"; exit 1; fi
  for try in 1 2; do python3 process_clip.py "$l" && break; echo "RETRY $l"; done
done
echo ALLDONE
