import subprocess
import time
import statistics
import os
import uuid
import sys
import shutil

PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

LOCAL_PACKAGE_PATH = "sdk/evaluation/azure-ai-evaluation"

EXTRAS = ["pyrit", None]

NUM_RUNS_PER_SCENARIO = 3


def create_uv_venv(python_version, env_name):
    cmd = [
        "uv", "venv", 
        "-n", "-p", python_version, env_name,
    ]

    subprocess.run(cmd, check=True)

def remove_venv(env_name):
    # cmd = ["Remove-Item", env_name, "-Recurse", "-Force"]
    print("Removing uv venv:", " ".join(env_name))
    # subprocess.run(cmd, check=True)
    shutil.rmtree(env_name)

def time_pip_install_in_uv_venv(install_target):
    start = time.perf_counter()
    cmd = ["uv", "pip", "install", install_target, "-n"]
    print("Running install:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    end = time.perf_counter()
    return end - start

def make_install_target(local_pkg_path, extras):
    if extras is None:
        return local_pkg_path
    else:
        return f"{local_pkg_path}[{extras}]"

if __name__ == "__main__":
    results = []

    for py_ver in PYTHON_VERSIONS:
        for extras in EXTRAS:
            install_times = []

            for run_idx in range(NUM_RUNS_PER_SCENARIO):
                env_name = f"temp_env_py{py_ver.replace('.', '')}_{extras}_{uuid.uuid4().hex[:8]}"

                try:
                    print(f"\n=== Creating uv venv for Python {py_ver} (extras={extras}) run {run_idx+1} ===")
                    create_uv_venv(py_ver, env_name)
                    os.environ["VIRTUAL_ENV"]=env_name

                    target = make_install_target(LOCAL_PACKAGE_PATH, extras)
                    elapsed = time_pip_install_in_uv_venv(target)

                    print(f"    => Installation took {elapsed:.2f} seconds.")
                    install_times.append(elapsed)

                finally:
                    print(f"Removing uv venv {env_name}...")
                    remove_venv(env_name)

            avg_time = statistics.mean(install_times)
            std_dev = statistics.pstdev(install_times) if len(install_times) > 1 else 0.0

            results.append({
                "python_version": py_ver,
                "extras": extras,
                "times": install_times,
                "avg": avg_time,
                "std_dev": std_dev
            })

    print("\n=== Final Benchmark Results ===")
    for r in results:
        print(
            f"Python {r['python_version']} with extras={r['extras']}:\n"
            f"  Individual times: {r['times']}\n"
            f"  Avg time: {r['avg']:.2f} s\n"
            f"  Std dev: {r['std_dev']:.2f} s\n"
        )
