import subprocess
import time
import statistics
import os
import uuid
import sys

PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

LOCAL_PACKAGE_PATH = "sdk/evaluation/azure-ai-evaluation"

EXTRAS = ["pyrit", None]

NUM_RUNS_PER_SCENARIO = 3


def create_conda_env(python_version, env_name):
    cmd = [
        "conda", "create", "-y",
        "-n", env_name,
        f"python={python_version}"
    ]

    
    subprocess.run(cmd, check=True)

def remove_conda_env(env_name):
    cmd = ["conda", "remove", "-y", "--all", "-n", env_name]
    print("Removing conda environment:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def time_pip_install_in_conda_env(env_name, install_target):
    start = time.perf_counter()
    cmd = ["conda", "run", "-n", env_name, "pip", "install", install_target, "--no-cache-dir"]
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
                    print(f"\n=== Creating conda env for Python {py_ver} (extras={extras}) run {run_idx+1} ===")
                    create_conda_env(py_ver, env_name)

                    target = make_install_target(LOCAL_PACKAGE_PATH, extras)
                    elapsed = time_pip_install_in_conda_env(env_name, target)

                    print(f"    => Installation took {elapsed:.2f} seconds.")
                    install_times.append(elapsed)

                finally:
                    print(f"Removing conda env {env_name}...")
                    remove_conda_env(env_name)

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
