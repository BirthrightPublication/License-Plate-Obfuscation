# True Engine SDK acceptance probe

This is a separate consumer compatibility test, **not Plate Studio integration,
an editor, a Windows application package, or a replacement renderer**. It does
not change the existing prototype or projects. Engine source is fetched by Cargo
as a dependency; it is neither copied here nor modified.

The dependency is `true-engine` **0.1.2**, SDK **0.1**, schema **1**, pinned to the
immutable v0.1.2 source commit
`8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0`. Use Rust **1.85.1**, a native linker
and the platform's graphics drivers. Windows builds require the MSVC C++ build
tools and Windows SDK. Cargo requires network access on first dependency fetch.

From this directory:

```text
cargo +1.85.1 test --locked --test sdk_cpu
cargo +1.85.1 test --locked --test sdk_gpu -- --nocapture
cargo +1.85.1 test --locked
```

On Linux the offscreen test can use Mesa software rendering without a desktop:

```sh
EGL_PLATFORM=surfaceless cargo +1.85.1 test --locked --test sdk_gpu -- --nocapture
```

The default test command includes the GPU check. Missing adapters/devices are
failures, never automatic skips. `--test sdk_cpu` is an explicitly limited CPU
check and must not be reported as GPU/rendering acceptance. Adapter information
is printed by the GPU test; software rendering does not qualify hardware or
Windows driver behavior. This test creates an offscreen target, not a real window
or native mouse events. Its camera calls and resize are programmatic.

The CPU tests validate a scaled/rotated SDK cube representing a rectangular plate
body, an application-owned parameter edit rebuilt through `Scene::add`, material
color, schema-1 project serialization/reopen, actual engine ray picking, orbit,
pan, zoom and changed aspect/ray output. The GPU test calls the engine's public
`Renderer::new`, `upload`, `draw` and `resize`; it reads back real rendered pixels,
requires a visible plate, verifies an actual material-color change, checks camera
input changes the image, and renders a different target size. No independent
pipeline, shader, projection matrix, or mesh implementation is included.

## Capabilities still missing for the requested editor

- **Orthographic rendering:** `OrbitCamera::view_projection` is hardcoded to
  perspective; `Renderer::draw` accepts only that concrete camera. No documented
  projection selector or supplied-matrix route exists. Screen rays use the same
  perspective projection. Plate Studio cannot implement an honest orthographic
  view through this SDK without an engine API extension.
- **Plate text:** nodes accept only Cube/Plane/Sphere primitives, and renderer
  upload only processes those primitives. The public `geometry::Mesh` type has
  no scene/renderer submission API. No text, glyph, texture, or font interface is
  provided. A plate body is not a complete text-editable plate.
- **Material scope:** `Material` exposes opaque RGBA color only. Roughness,
  metallic properties, textures and transparency have no supported API.
- **Editing scope:** scene nodes are read-only; reconstructing a small scene from
  app parameters works. Incremental validated update/remove would improve editor
  performance but is not needed for this small compatibility check.

Source contract and integration example:

- [SDK contract at the pinned commit](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/docs/SDK-0.1.md)
- [Native/browser integration example](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/examples/viewport/src/lib.rs)
- [Concrete renderer camera and upload APIs](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/crates/true-engine/src/render.rs)
- [Perspective-only camera](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/crates/true-engine/src/camera.rs)

Actual execution results belong in the repository's test report. Merely adding
these tests is not evidence that they passed or that Plate Studio is integrated.

## Executed consumer checks

The initial Linux cloud run with Rust 1.85.1 passed all **4 CPU tests and 1
offscreen-rendering test**, with no failures or ignored tests. The renderer used
Mesa **llvmpipe (LLVM 19.1.7, 256 bits)**, a software adapter through the GL backend.
`cargo fmt --all -- --check` also passed. This confirms this pinned consumer's
tested SDK subset; it does not establish application integration, real window
input, interactive Windows graphics, or the missing orthographic/text APIs.

The cloud used writable local `XDG_RUNTIME_DIR` and `MESA_SHADER_CACHE_DIR` values
and `EGL_PLATFORM=surfaceless`. Command output was captured under ignored
`Build/true-engine-sdk-{lock,cpu,gpu,all}.txt`; the repository's test report records
the durable result. Dependency versions are preserved in this probe's
`Cargo.lock`; use `--locked` when reproducing the checks.
