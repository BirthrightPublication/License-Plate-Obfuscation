use true_engine::{glam::Quat, glam::Vec3, Material, Node, Primitive, Scene, Transform};

/// Application-owned plate parameters, expressed with supported SDK primitives.
/// Units are centimetres for this probe; the SDK itself has no fixed unit.
pub fn plate_scene(dimensions: Vec3, rotation: Quat, color: [f32; 4]) -> Scene {
    let mut scene = Scene::default();
    scene
        .add(Node {
            id: 42,
            parent: None,
            name: "SDK acceptance plate body".into(),
            transform: Transform {
                translation: Vec3::ZERO,
                rotation,
                scale: dimensions,
            },
            primitive: Some(Primitive::Cube),
            material: Material { color },
        })
        .expect("documented plate-body parameters must be a valid SDK scene");
    scene
}
