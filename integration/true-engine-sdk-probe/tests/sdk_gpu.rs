mod common;

use common::plate_scene;
use true_engine::{glam::Quat, glam::Vec3, render::Renderer, OrbitCamera};

fn pixels(
    device: &wgpu::Device,
    queue: &wgpu::Queue,
    renderer: &Renderer,
    camera: &OrbitCamera,
    width: u32,
    height: u32,
) -> Vec<u8> {
    let target = device.create_texture(&wgpu::TextureDescriptor {
        label: Some("True Engine SDK acceptance readback target"),
        size: wgpu::Extent3d {
            width,
            height,
            depth_or_array_layers: 1,
        },
        mip_level_count: 1,
        sample_count: 1,
        dimension: wgpu::TextureDimension::D2,
        format: wgpu::TextureFormat::Rgba8Unorm,
        usage: wgpu::TextureUsages::RENDER_ATTACHMENT | wgpu::TextureUsages::COPY_SRC,
        view_formats: &[],
    });
    let row_bytes = (width * 4).div_ceil(wgpu::COPY_BYTES_PER_ROW_ALIGNMENT)
        * wgpu::COPY_BYTES_PER_ROW_ALIGNMENT;
    let readback = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("SDK rendered pixels"),
        size: (row_bytes * height) as u64,
        usage: wgpu::BufferUsages::COPY_DST | wgpu::BufferUsages::MAP_READ,
        mapped_at_creation: false,
    });
    let mut encoder = device.create_command_encoder(&Default::default());
    // All scene drawing, depth handling, materials and camera projection are SDK-owned.
    renderer.draw(
        queue,
        &mut encoder,
        &target.create_view(&Default::default()),
        camera,
        width as f32 / height as f32,
    );
    encoder.copy_texture_to_buffer(
        target.as_image_copy(),
        wgpu::ImageCopyBuffer {
            buffer: &readback,
            layout: wgpu::ImageDataLayout {
                offset: 0,
                bytes_per_row: Some(row_bytes),
                rows_per_image: Some(height),
            },
        },
        target.size(),
    );
    queue.submit(Some(encoder.finish()));
    let (sender, receiver) = std::sync::mpsc::channel();
    readback
        .slice(..)
        .map_async(wgpu::MapMode::Read, move |result| {
            sender.send(result).unwrap();
        });
    device.poll(wgpu::Maintain::Wait);
    receiver.recv().unwrap().unwrap();
    let mapped = readback.slice(..).get_mapped_range();
    let result = mapped
        .chunks_exact(row_bytes as usize)
        .flat_map(|row| row[..(width * 4) as usize].iter().copied())
        .collect();
    drop(mapped);
    readback.unmap();
    result
}

fn center(data: &[u8], width: usize, height: usize) -> &[u8] {
    let offset = ((height / 2) * width + width / 2) * 4;
    &data[offset..offset + 4]
}

#[test]
fn engine_renders_edited_plate_camera_and_resized_target() {
    pollster::block_on(async {
        let instance = wgpu::Instance::default();
        let adapter = instance
            .request_adapter(&wgpu::RequestAdapterOptions::default())
            .await
            .expect("GPU acceptance failed: no compatible adapter; use --test sdk_cpu only for an explicitly CPU-only check");
        eprintln!("True Engine probe adapter: {:?}", adapter.get_info());
        let (device, queue) = adapter
            .request_device(
                &wgpu::DeviceDescriptor {
                    required_limits: wgpu::Limits::downlevel_webgl2_defaults()
                        .using_resolution(adapter.limits()),
                    ..Default::default()
                },
                None,
            )
            .await
            .expect("GPU acceptance requires a usable wgpu device");
        let mut renderer = Renderer::new(&device, wgpu::TextureFormat::Rgba8Unorm, 64, 64);
        let mut camera = OrbitCamera {
            yaw: 0.0,
            pitch: 0.0,
            distance: 60.0,
            ..Default::default()
        };
        let red = plate_scene(
            Vec3::new(30.48, 15.24, 0.15),
            Quat::IDENTITY,
            [0.9, 0.1, 0.1, 1.0],
        );
        renderer.upload(&device, &red, None);
        let first = pixels(&device, &queue, &renderer, &camera, 64, 64);
        let red_center = center(&first, 64, 64);
        assert!(red_center[0] > red_center[2].saturating_add(40));
        assert_ne!(
            red_center,
            &first[..4],
            "plate must differ from clear color"
        );

        let blue = plate_scene(
            Vec3::new(30.48, 15.24, 0.15),
            Quat::IDENTITY,
            [0.1, 0.1, 0.9, 1.0],
        );
        renderer.upload(&device, &blue, None);
        let edited = pixels(&device, &queue, &renderer, &camera, 64, 64);
        let blue_center = center(&edited, 64, 64);
        assert!(blue_center[2] > blue_center[0].saturating_add(40));
        assert_ne!(
            first, edited,
            "engine material edit must change rendered pixels"
        );

        camera.orbit(30.0, -10.0);
        camera.pan(15.0, 4.0);
        let moved = pixels(&device, &queue, &renderer, &camera, 64, 64);
        let changed = moved
            .chunks_exact(4)
            .zip(edited.chunks_exact(4))
            .filter(|(before, after)| before != after)
            .count();
        assert!(
            changed > 12,
            "SDK camera input must change rendered geometry"
        );

        renderer.resize(&device, 96, 48);
        let resized = pixels(&device, &queue, &renderer, &camera, 96, 48);
        assert_eq!(resized.len(), 96 * 48 * 4);
        let background = &resized[..4];
        assert!(resized.chunks_exact(4).any(|pixel| pixel != background));
    });
}
