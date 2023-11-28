import os
import subprocess
from tqdm import tqdm

import os
import subprocess
from tqdm import tqdm

def encode_to_drc(input_ply_path, output_drc_path, draco_encode_path, compression_level):
    command = [
        'powershell',
        '-Command',
        f'& "{draco_encode_path}" -point_cloud -i "{input_ply_path}" -o "{output_drc_path}" -cl {compression_level}'
    ]
    subprocess.run(command, check=True)

def decode_to_ply(input_drc_path, output_ply_path, draco_decode_path):
    command = [
        'powershell',
        '-Command',
        f'& "{draco_decode_path}" -i "{input_drc_path}" -o "{output_ply_path}"'
    ]
    subprocess.run(command, check=True)

def process_files(input_directory, output_directory, draco_encode_path, draco_decode_path, compression_level):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    ply_files = [f for f in os.listdir(input_directory) if f.endswith('.ply')]

    for ply_file in tqdm(ply_files, desc="Processing files", unit="file"):
        ply_file_path = os.path.join(input_directory, ply_file)
        drc_file_path = os.path.join(output_directory, os.path.splitext(ply_file)[0] + '.drc')

        # Encode to Draco format
        encode_to_drc(ply_file_path, drc_file_path, draco_encode_path, compression_level)

        # Decode back to PLY format
        decoded_ply_path = os.path.join(output_directory, os.path.splitext(ply_file)[0] + '_decoded.ply')
        decode_to_ply(drc_file_path, decoded_ply_path, draco_decode_path)

if __name__ == "__main__":
    input_directory = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\ply_velodyne"
    output_directory = "D:\\Admin\\KITTI\\KITTI_pcd_completion\\dracoed_ply_velodyne"
    draco_encode_path = "D:\\Admin\\KITTI\\draco\\draco-master\\build\\Debug\\draco_encoder.exe"
    draco_decode_path = "D:\\Admin\\KITTI\\draco\\draco-master\\build\\Debug\\draco_decoder.exe"
    compression_level = 14  # Adjust the quantization value as needed

    process_files(input_directory, output_directory, draco_encode_path, draco_decode_path, compression_level)
