// The Poster for a Place That Isn't There
// Entry for the make.fun bounty
// "the-poster-for-a-place-that-i-2-20261121-0539".
//
// The poster is designed in this repository (see compose.py).
// This program emits the finished poster as a single PNG image
// at /output/entry.png — no network, no clock, no randomness —
// so two runs are byte-identical.

import {
  copyFileSync,
  mkdirSync,
  readFileSync,
  statSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const MAX_BYTES = 1_048_576; // the bounty's 1 MiB cap
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const bytes = statSync(target).size;
if (bytes > MAX_BYTES) {
  throw new Error(`image is ${bytes} bytes, over the 1 MiB cap`);
}

const data = readFileSync(target);
const head = data.subarray(0, PNG_MAGIC.length);
for (let i = 0; i < PNG_MAGIC.length; i++) {
  if (head[i] !== PNG_MAGIC[i]) {
    throw new Error("output is not a PNG file");
  }
}

// The first chunk of a PNG is always IHDR: 4 bytes of length,
// the type "IHDR", then width and height as big-endian uint32.
// The bounty fixes the poster at 1024x1024, so verify the real
// dimensions instead of trusting the file name.
const ihdrType = data.subarray(12, 16).toString("ascii");
if (ihdrType !== "IHDR") {
  throw new Error("first PNG chunk is not IHDR");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`image is ${width}x${height}, not the required 1024x1024`);
}

console.log(`Wrote ${target} (${bytes} bytes)`);
