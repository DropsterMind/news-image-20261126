// news-image-20261126 v1: copies the drawn entry image to the output directory.
// Node 22, standard library only, no network. The image itself is drawn by draw.py;
// this program only validates it (PNG signature, 1024x1024, at most 1 MiB) and
// copies it to MAKEFUN_OUTPUT_DIR (or /output), then re-reads both files and
// byte-compares them so a truncated copy can never pass silently.
//
// The image is resolved relative to THIS FILE (import.meta.url), not to the
// process working directory: the grader runs `node /bot/main.ts` from a
// different directory, so a bare relative path ("entry.png") is not found there
// and the run exits 1. Resolving against import.meta.url works from any
// working directory.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const SRC = new URL("./entry.png", import.meta.url);
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const DST = join(OUT_DIR, "entry.png");

const buf = readFileSync(SRC);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(PNG_SIG)) throw new Error("entry.png is not a PNG");
if (buf.length > 1048576) throw new Error(`entry.png is ${buf.length} bytes, over 1 MiB`);
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(DST, buf);
const back = readFileSync(DST);
if (!back.equals(buf)) throw new Error("output copy differs from entry.png");
console.log(`wrote ${DST} (${buf.length} bytes, 1024x1024, byte-identical)`);
