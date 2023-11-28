import os
import struct
import numpy as np
from plyfile import PlyData, PlyElement
from tqdm import tqdm

def convert_kitti_bin_to_ply(bin_file_path, ply_file_path):
    # Read KITTI binary file
    with open(bin_file_path, 'rb') as bin_file:
        data = bin_file.read()

    # Parse binary data
    num_points = len(data) // struct.calcsize("ffff")  # assuming x, y, z, intensity

    # Check if the data size is consistent with the expected size
    if len(data) % struct.calcsize("ffff") != 0:
        raise ValueError("Invalid binary file format. Check the structure of the data.")

    # Unpack binary data
    points = struct.unpack("{}".format("ffff" * num_points), data)

    # Reshape data
    points = np.array(points).reshape((-1, 4))

    # Create PlyData object
    vertex = np.array([(point[0], point[1], point[2], int(point[3])) for point in points],
                      dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('intensity', 'u1')])

    ply_data = PlyData([PlyElement.describe(vertex, 'vertex')])

    # Save as PLY file
    ply_data.write(ply_file_path)

def convert_all_kitti_bin_files(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all .bin files in the input directory
    bin_files = [f for f in os.listdir(input_directory) if f.endswith('.bin')]

    for bin_file in tqdm(bin_files, desc="Converting files", unit="file"):
        # Construct input and output file paths
        bin_file_path = os.path.join(input_directory, bin_file)
        ply_file_path = os.path.join(output_directory, os.path.splitext(bin_file)[0] + '.ply')

        # Convert KITTI binary file to PLY format
        convert_kitti_bin_to_ply(bin_file_path, ply_file_path)

if __name__ == "__main__":
    input_directory = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\training\\velodyne"
    output_directory = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\ply_velodyne"

    convert_all_kitti_bin_files(input_directory, output_directory)
