#!/usr/bin/env python3
import argparse
import subprocess


def gpu_ok(gpu_usage, mem_usage, max_gpu_usage, max_mem_usage):
    return gpu_usage <= max_gpu_usage and mem_usage < max_mem_usage


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="Command to execute", type=str)
    parser.add_argument("--gpu_usage", default=5, help="Maximum GPU usage on available GPU, default 5%", type=int)
    parser.add_argument("--mem_usage", default=10, help="Maximum GPU memory usage on available GPU, default 10%", type=int)

    args = parser.parse_args()

    smi_command = ['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory', '--format=csv,noheader']
    with subprocess.Popen(smi_command, stdout=subprocess.PIPE) as proc:
        gpu_info = [[int(y.replace('%', '')) for y in x.decode().strip().split(',')] for x in proc.stdout.readlines()]

        selected_gpu_id = -1
        for gpu_id in range(len(gpu_info)):
            if gpu_ok(gpu_info[gpu_id][0], gpu_info[gpu_id][1], args.gpu_usage, args.mem_usage):
                selected_gpu_id = gpu_id
                break

        if selected_gpu_id == -1:
            exit(selected_gpu_id)

        print("selected GPU %d" % selected_gpu_id)
        cmd = 'export CUDA_VISIBLE_DEVICES=%d; %s' % (selected_gpu_id, args.cmd)
        subprocess.call(cmd, shell=True)
