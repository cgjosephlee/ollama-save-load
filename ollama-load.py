#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


def extract_tarball(model_path: Path, file_name: str):
    if file_name.endswith(".tar"):
        tar_option = "-xf"
    elif file_name.endswith(".tar.gz"):
        tar_option = "-zxf"
    elif file_name.endswith(".tar.bz"):
        tar_option = "-jxf"
    elif file_name.endswith(".tar.xz"):
        tar_option = "-Jxf"
    else:
        raise ValueError(f"Unsupported file extension for {file_name}")

    tar_command = ["tar", tar_option, file_name, "-C", str(model_path)]
    subprocess.run(tar_command, stdout=sys.stdout)


def main():
    file_name = sys.argv[1]
    model_path = Path(os.getenv("OLLAMA_MODELS", "~/.ollama/models")).expanduser()
    extract_tarball(model_path, file_name)


if __name__ == "__main__":
    main()
