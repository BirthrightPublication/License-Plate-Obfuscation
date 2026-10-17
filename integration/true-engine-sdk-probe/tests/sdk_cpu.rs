mod common;

use common::plate_scene;
use true_engine::{glam::Quat, glam::Vec3, OrbitCamera, Primitive, Project};

#[test]
fn application_edits_use_validated_engine_nodes() {
    let initial = plate_scene(
        Vec3::new(30.48, 15.24, 0.15),
        Quat::IDENTITY,
        [0.9, 0.9, 0.9, 1.0],
    );
    let rotation = Quat::from_rotation_y(0.35);
    let dimensions = Vec3::new(28.0, 14.0, 0.2);
    let color = [0.15, 0.3, 0.7, 1.0];
    // Scene nodes are read-only. Rebuild from application parameters through add.
    let edited = plate_scene(dimensions, rotation, color);
    let node = &edited.nodes()[0];
    assert_eq!(node.primitive, Some(Primitive::Cube));
    assert_eq!(node.transform.scale, dimensions);
    assert_eq!(node.transform.rotation, rotation);
    assert_eq!(node.material.color, color);
    assert_ne!(edited, initial);
    let world = edited.world_matrix(node.id).unwrap();
    assert!((world.transform_vector3(Vec3::X).length() - 28.0).abs() < 0.0001);
    assert!((world.transform_vector3(Vec3::Y).length() - 14.0).abs() < 0.0001);
    assert!((world.transform_vector3(Vec3::Z).length() - 0.2).abs() < 0.0001);
}

#[test]
fn project_reopens_plate_dimensions_rotation_and_material() {
    let project = Project::new(plate_scene(
        Vec3::new(30.48, 15.24, 0.15),
        Quat::from_rotation_z(0.25),
        [0.8, 0.7, 0.15, 1.0],
    ));
    let saved = project.to_json().unwrap();
    let reopened = Project::from_json(&saved).unwrap();
    assert_eq!(reopened, project);
    assert_eq!(reopened.scene.nodes()[0].name, "SDK acceptance plate body");
    let future_schema = saved.replace("\"schema_version\": 1", "\"schema_version\": 999");
    assert!(Project::from_json(&future_schema).is_err());
    assert_eq!(Project::from_json(&saved).unwrap(), project);
}

#[test]
fn camera_ray_selects_the_plate_and_misses_empty_space() {
    let scene = plate_scene(
        Vec3::new(30.48, 15.24, 0.15),
        Quat::from_rotation_z(0.2),
        [0.9, 0.9, 0.9, 1.0],
    );
    let camera = OrbitCamera {
        yaw: 0.0,
        pitch: 0.0,
        distance: 60.0,
        ..Default::default()
    };
    let (origin, direction) = camera.ray(400.0, 300.0, 800.0, 600.0);
    assert_eq!(scene.pick(origin, direction), Some(42));
    let (origin, direction) = camera.ray(1.0, 1.0, 800.0, 600.0);
    assert_eq!(scene.pick(origin, direction), None);
}

#[test]
fn sdk_input_and_resized_aspect_change_camera_outputs() {
    let mut camera = OrbitCamera::default();
    let initial_eye = camera.eye();
    camera.orbit(35.0, -12.0);
    assert_ne!(camera.eye(), initial_eye);
    let target = camera.target;
    camera.pan(14.0, 8.0);
    assert_ne!(camera.target, target);
    let distance = camera.distance;
    camera.zoom(2.0);
    assert!(camera.distance < distance);
    assert_ne!(
        camera.view_projection(4.0 / 3.0),
        camera.view_projection(2.0)
    );
    let (_, narrow_ray) = camera.ray(600.0, 300.0, 800.0, 600.0);
    let (_, wide_ray) = camera.ray(900.0, 300.0, 1200.0, 600.0);
    assert!((narrow_ray - wide_ray).length() > 0.01);
    assert!(wide_ray.is_finite());
}
