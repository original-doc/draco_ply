import numpy as np
import struct
import open3d
import matplotlib.pyplot as plt

def read_bin_velodyne(path):
    '''read bin file and transfer to array data'''
    pc_list = []
    with open(path, 'rb') as f:
        content = f.read()
        pc_iter = struct.iter_unpack('ffff', content)
        for idx, point in enumerate(pc_iter):
            pc_list.append([point[0], point[1], point[2], point[3]])
    return np.asarray(pc_list, dtype=np.float32)

def main():
    # pc_path = 'D:\\Admin\\KITTI\\KITTI_pcd_completion\\training\\velodyne\\000001.bin'
    # pc_path = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\dracoed_bin\\000001.bin"
    pc_path = "D:\\Admin\\KITTI\\000000_decoded.bin"
    example = read_bin_velodyne(pc_path)
    example_xyz = example[:, :3]
    example_xyz = example_xyz[example_xyz[:, 2] > -3]

    # Extract intensity values (assuming they are in the fourth column)
    intensity = example[:, 3]

    # Normalize intensity values to [0, 1]
    normalized_intensity = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

    # Map normalized intensity values to a colormap (using matplotlib colormap 'viridis' as an example)
    colormap = plt.get_cmap('viridis')
    colors = colormap(normalized_intensity)[:, :3]

    # From numpy to Open3D
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(example_xyz)
    pcd.colors = open3d.utility.Vector3dVector(colors)

    vis = open3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    render_options = vis.get_render_option()
    render_options.point_size = 1
    render_options.background_color = np.array([0, 0, 0])
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    main()
