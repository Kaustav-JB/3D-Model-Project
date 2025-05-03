import torch
import numpy as np
import open3d as o3d
from pathlib import Path

from point_e.diffusion.configs import DIFFUSION_CONFIGS, diffusion_from_config
from point_e.diffusion.sampler import PointCloudSampler
from point_e.models.download import load_checkpoint
from point_e.models.configs import MODEL_CONFIGS, model_from_config

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

prompt = input("Enter a prompt for the 3D object: ")
if not prompt:
    prompt = "A red cube"

output_dir = Path("Outputs")
output_dir.mkdir(exist_ok=True)

print('Loading base model...')
base_name = 'base40M-textvec'
base_model = model_from_config(MODEL_CONFIGS[base_name], device)
base_model.load_state_dict(load_checkpoint(base_name, device))
base_model.eval()
base_diffusion = diffusion_from_config(DIFFUSION_CONFIGS[base_name])

print('Loading upsampler model...')
upsampler_model = model_from_config(MODEL_CONFIGS['upsample'], device)
upsampler_model.load_state_dict(load_checkpoint('upsample', device))
upsampler_model.eval()
upsampler_diffusion = diffusion_from_config(DIFFUSION_CONFIGS['upsample'])

sampler = PointCloudSampler(
    device=device,
    models=[base_model, upsampler_model],
    diffusions=[base_diffusion, upsampler_diffusion],
    num_points=[1024, 3072],
    aux_channels=['R', 'G', 'B'],
    guidance_scale=[3.0, 0.0],
    model_kwargs_key_filter=('texts', '')  # Only the base model uses the prompt
)

print(f"Generating point cloud for : '{prompt}'")
samples = None
for x in sampler.sample_batch_progressive(batch_size=1, model_kwargs=dict(texts=[prompt])):
    samples = x

pc = sampler.output_to_point_clouds(samples)[0]

points = np.array(pc.coords)
colors = np.random.rand(points.shape[0], 3)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

ply_path = output_dir / f"{prompt}.ply"
o3d.io.write_point_cloud(f"{ply_path}", pcd)
print(f"Saved: {prompt}.ply")

print("Converting point cloud to mesh...")
pcd.estimate_normals()

dists = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(dists)
radius = 3 * avg_dist

mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector([radius, radius * 2])
)
obj_path = output_dir / f"{prompt}_obj.obj"
stl_path = output_dir / f"{prompt}_stl.stl"

o3d.io.write_triangle_mesh(f"{obj_path}", mesh)
o3d.io.write_triangle_mesh(f"{stl_path}", mesh)
print(f"Saved: {prompt}.obj, {prompt}.stl")