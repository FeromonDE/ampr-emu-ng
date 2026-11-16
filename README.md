# ampr-emu-ng

A hard fork of [drakmor/ampr_emu](https://github.com/drakmor/ampr_emu), built to run PKG, zstd, LZ4 and plain games quickly and reliably.

## How to

### Use

Copy `libSceAmpr.sprx` into the game's `fakelib/`, mount the game with
ShadowMountPlus and turn off fakelib updates in its settings. At launch the
console shows `ampr-emu-ng: vx.x.x (zstd) running`, where the mode is `zstd`,
`pkg`, `lz4`, or `plain` for a game with only loose files.

A PKG game runs through [kraken-mount](https://github.com/quer3q/kraken-mount),
the PKG launcher, which copies `libSceAmpr.sprx` into the game's `fakelib/`
itself.

### Make packs

[ps5-dump-forge](https://github.com/quer3q/ps5-dump-forge) builds PKGs, zstd
packs and LZ4 packs. Other tools that write the same formats should work too,
but are untested.

### Build

The build needs Docker. The first run builds the toolchain image
`ampr-emu-ng-ps5:latest` from `ps5/Dockerfile` (Rust 1.99.0, LLVM 19,
ps5-payload-sdk v0.43); `AMPR_PS5_IMAGE` picks another image.

```sh
./ps5/build-docker.sh            # make dist
```

`dist` builds the PRX, checks it with `tools/verify_payload_prx.py` and
copies two files to the project root:

- `libSceAmpr.sprx`, the release build;
- `libSceAmpr-debug.sprx`, the same runtime plus metrics, tuning and
  failure logs, for testing ([docs/debug-build.md](docs/debug-build.md)).

This fork publishes verified builds with diagnostic traces in
`/download/ampr_emu_trace.txt`. The `libSceAmpr-debug.sprx` asset is the
diagnostic build; install it as `libSceAmpr.sprx` in the game's `fakelib/`.

## Thanks

- [drakmor/ampr_emu](https://github.com/drakmor/ampr_emu), the C++ AMPR
  emulator this project ports.
- [ps5-payload-sdk](https://github.com/ps5-payload-dev/sdk), the PS5
  toolchain and libraries.
- [AnyPS5](https://github.com/boykopovar/AnyPS5), for its libSceAmpr
  implementation and notes on the libc exports of retail libSceAmpr.

## License

GPL-3.0-or-later, the same as upstream (`LICENSE`).

## Fork diagnostic builds

This fork keeps diagnostic logs in `/download`, outside mounted game images. Source changes on `main` build and verify the modules and publish the results in this fork's Releases.

The upstream release workflow checks the latest stable release of `quer3q/ampr-emu-ng` every six hours. New source is merged into this fork, its own CI is preserved, the log patch is reapplied and checked, and a reusable workflow builds and publishes the result. A source conflict or an unexpected logging implementation stops the update for review. Unchanged releases are not rebuilt, and failed builds are retried. Both workflows support manual runs.
