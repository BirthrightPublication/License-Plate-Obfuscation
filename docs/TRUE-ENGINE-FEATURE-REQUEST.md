# Feature request: supported plate text and orthographic projection

**Target:** BirthrightPublication/True-Engine

**Consumer:** License Plate Obfuscation Studio

**Baseline:** engine v0.1.2, SDK 0.1, schema 1, exact source
`8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0`.

This is an issue-ready request, not a claim that a GitHub issue was created or an
engine change was implemented. No minimum future SDK version is invented.

## Required: engine-owned orthographic projection

Current evidence: `camera.rs::OrbitCamera::view_projection` unconditionally calls
`Mat4::perspective_rh`. `render.rs::Renderer::draw` requires `&OrbitCamera` and
writes its view-projection to a private uniform. Consumers cannot provide an
orthographic camera through the supported SDK.

Request a documented projection selection/camera interface supported by the
renderer and ray generation. Preserve perspective behavior and existing callers.
The engine should define orthographic extent, aspect/resize handling, clipping,
zoom, units and consistent ray/picking semantics. The consumer must not need to
fork renderer/camera internals or simulate orthographic with a distant camera.

Acceptance:

- Render the same scene in perspective and orthographic modes using public APIs.
- Equal-size objects at different depths have equal projected size in orthographic
  mode; they differ appropriately in perspective mode.
- Orbit, pan, zoom, pixel-based picking and resize remain consistent in both modes.
- Tests cover finite/invalid inputs and non-square targets on native Windows.

## Required: validated custom geometry or supported plate-text geometry

Current evidence: `scene.rs::Primitive` has only Cube, Plane and Sphere;
`Node::primitive` accepts only those variants. `render.rs::Renderer::upload` and
`Scene::pick` regenerate those primitive meshes. The public `geometry::Mesh`
cannot be submitted as a renderable/pickable node.

Prefer an application-agnostic validated custom-mesh path, used by renderer and
picking, so consumer-owned glyph tessellation can use the engine renderer.
An engine-owned text/glyph geometry capability is also acceptable if it meets
editable lettering requirements. Document index/vertex validation, normals,
ownership, updates, resource lifecycle and persistence/versioning. Keep plate,
jurisdiction and legal rules in Plate Studio.

Acceptance:

- A separate Git-pinned consumer submits a plate and visible lettering geometry
  through public SDK APIs without custom rendering pipelines or private fields.
- Editing text updates geometry and reuses/releases resources correctly.
- Picking and save/reopen have documented, tested behavior for that geometry.
- Malformed indices, nonfinite vertices and invalid resource references fail
  clearly without losing the previous valid scene.
- Native Windows GPU pixel tests and an external host example verify the path.

## Material scope: clarify and extend only when supported

`Material` currently contains only opaque color. That is sufficient for initial
color editing, but not roughness, metallic, textures or reflectivity. Document
supported initial material properties; additional inspector controls must await
real SDK material/shader support and corresponding render tests.

## Useful follow-up, not a hard blocker

A validated node update/replace/remove interface would avoid rebuilding a small
scene for every property edit. Current scene rebuilding is valid for the initial
plate and must not be misreported as a total inability to edit dimensions or
rotation. Performance claims require measurements rather than assumptions.

## Delivery

Publish a tested, versioned SDK with an immutable source commit, public contract,
external native host example, compatibility/migration notes and Windows evidence.
Plate Studio will update its dependency only after those checks pass. It will not
edit or duplicate the True Engine repository to implement these capabilities.
