# True Engine SDK assessment — integration restart

The owner explicitly restarted Plate Studio integration and selected the published
True Engine v0.1.2 SDK. This supersedes the previous blanket development hold for
this iteration. It does not make the rejected CSS interface approved or turn the
existing executable into an engine application.

## Exact dependency

- Repository: https://github.com/BirthrightPublication/True-Engine
- Stable engine tag: `v0.1.2`
- Immutable source: `8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0`
- Rust package: `true-engine`, version `0.1.2`
- Public SDK contract: `0.1`; scene schema: `1`
- Declared toolchain: Rust `1.85.1`; renderer dependency: wgpu `0.19`
- Inspected main: `0de66e1baafa533391c72c342ac003aa70de74d4`; its SDK,
  renderer, scene, camera and example source match the stable tag.

The supported integration is a Rust consumer of the public crate. The Windows
viewport EXE is a sample application, not an embeddable SDK DLL. The Rust/WASM
example is also a host example, not a JavaScript scene-control API. A native Rust
host can own a window/device/surface and call the engine renderer directly; lack
of a Python binding alone is not a renderer limitation.

## Capability assessment

| Requested capability | Public SDK 0.1 support |
| --- | --- |
| Actual GPU rendering | `render::Renderer::{new,upload,draw,resize}` |
| Rectangular plate dimensions | A nonuniformly scaled `Primitive::Cube` |
| Plate orientation | Public `Transform` rotation/translation/scale |
| Material editing | Opaque linear RGBA color only |
| Orbit, pan, zoom | `OrbitCamera::{orbit,pan,zoom}` |
| Perspective and selection | Camera perspective/ray plus `Scene::pick` |
| Viewport resizing | Engine depth resize plus host surface/target resize |
| Save/reopen scene | Schema-1 `Project::{to_json,from_json}` |
| Property changes | Rebuild a small validated `Scene`, then upload; no mutable node API |
| Editable plate text | No supported font, text, texture or custom-mesh submission path |
| Orthographic view | No supported orthographic projection usable by `Renderer::draw` |
| Roughness/metallic/textured material | No corresponding material/shader API |

Sources at the immutable dependency:

- [SDK contract](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/docs/SDK-0.1.md)
- [Scene/geometry/material types](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/crates/true-engine/src/scene.rs)
- [Camera](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/crates/true-engine/src/camera.rs)
- [Renderer](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/crates/true-engine/src/render.rs)
- [Native/WASM integration example](https://github.com/BirthrightPublication/True-Engine/blob/8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0/examples/viewport/src/lib.rs)

`OrbitCamera::view_projection` always creates a perspective matrix.
`Renderer::draw` takes that concrete camera and writes its matrix internally;
its uniform/pipeline are private. Plate Studio cannot add a correct orthographic
view through this contract. `geometry::Mesh` exists, but no `Node` or renderer
submission path accepts it: upload and picking consume only the three primitive
variants. A public struct alone does not constitute a usable custom-mesh API.

Normal editable plate lettering therefore needs an engine-supported geometry or
text/texture path. Composing crude letters from cubes would sidestep the intended
capability rather than establish a suitable plate-text integration. Color-only
materials are usable today; additional material properties require actual engine
support rather than inspector controls with no rendering effect.

## Work and release boundary

`integration/true-engine-sdk-probe` is a separate compatibility-test consumer.
It references the exact Git commit and exercises real engine rendering without
copying engine source, adding a renderer, modifying shaders, or replacing the
application. Its results establish only the tested subset, not application
integration, interactive performance, Windows 11 GPU qualification or an approved
editor. Full CPU/GPU results are recorded in TEST_REPORT.md and docs/true-engine-sdk-test-results.txt; absent adapters fail the GPU
test rather than being reported as a pass.

The production interface stays unchanged while the hard gaps are outstanding.
The professional editor architecture remains the target, with a compact toolbar,
collapsible left object/style panel, central engine viewport, right inspector and
bottom status/legal area. No new CSS viewport or fake engine bridge is added.

See [the issue-ready engine feature request](TRUE-ENGINE-FEATURE-REQUEST.md).
No engine source change is authorized here. Once a compatible engine release is
available, pin its exact commit, rerun compatibility tests, implement the native
editor through the documented APIs and validate mouse input, resizing, editing,
save/reopen and recovery on Windows before publishing an integrated release.
The current app remains v0.1.2; no version or tag implies missing work is complete.
