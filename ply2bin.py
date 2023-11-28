import os
import struct
import numpy as np
from tqdm import tqdm

def ply_to_bin_kitti(ply_file_path, bin_file_path):
    with open(ply_file_path, 'rb') as ply_file:
        # Skip header lines in PLY file
        while True:
            line = ply_file.readline().strip().decode('utf-8', errors='ignore')
            if line.startswith("end_header"):
                break

        # Read the rest of the data as binary
        data = ply_file.read()

    # Determine the number of points and adjust the size if needed
    num_points = len(data) // struct.calcsize("ffff")
    data_size = num_points * struct.calcsize("ffff")
    remainder = len(data) % struct.calcsize("ffff")

    if remainder != 0:
        data = data[:data_size]  # Discard the remaining bytes if not an exact multiple

    # Reshape binary data into a NumPy array (assuming x, y, z, intensity format)
    points = np.frombuffer(data, dtype=np.float32).reshape((-1, 4))

    # Convert to KITTI binary format (x, y, z, intensity)
    binary_data = bytearray()
    for point in points:
        binary_data += struct.pack('ffff', point[0], point[1], point[2], point[3])

    # Write to binary file with the desired name format
    with open(bin_file_path, 'wb') as bin_file:
        bin_file.write(binary_data)

def convert_ply_files_to_kitti_bin(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    ply_files = [f for f in os.listdir(input_directory) if f.endswith('_decoded.ply')]

    for ply_file in tqdm(ply_files, desc="Converting to KITTI bin", unit="file"):
        ply_file_path = os.path.join(input_directory, ply_file)
        
        # Extract the base name without extension (e.g., "000000")
        base_name = os.path.splitext(ply_file)[0].split('_')[0]
        
        bin_file_path = os.path.join(output_directory, base_name + '.bin')

        # Convert PLY to KITTI binary format
        ply_to_bin_kitti(ply_file_path, bin_file_path)

        
if __name__ == "__main__":
    input_directory = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\dracoed_ply_velodyne"
    output_directory = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\dracoed_bin"

    convert_ply_files_to_kitti_bin(input_directory, output_directory)
