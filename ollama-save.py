#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModelName:
    host: str = "registry.ollama.ai"
    namespace: str = "library"
    model: str = ""
    tag: str = "latest"


def parse_model_name(name: str) -> ModelName:
    # Define regex patterns for different scenarios
    patterns = [
        r"^(?P<namespace>[^/]+)/(?P<model>[^:]+):(?P<tag>.+)$",  # { namespace } "/" { model } ":" { tag }
        r"^(?P<namespace>[^/]+)/(?P<model>[^:]+)$",  # { namespace } "/" { model }
        r"^(?P<model>[^:]+):(?P<tag>.+)$",  # { model } ":" { tag }
        r"^(?P<model>[^:]+)$",  # { model }
    ]

    for pattern in patterns:
        match = re.match(pattern, name)
        if match:
            groups = match.groupdict()
            return ModelName(
                namespace=groups.get("namespace", "library"),
                model=groups["model"],
                tag=groups.get("tag", "latest"),
            )

    raise ValueError(f"Invalid name format: {name}")


def parse_manifest(path: Path) -> list[str]:
    """Returns a list of blob SHAs."""
    data = json.loads(path.read_text())
    shas = []
    shas.append(data["config"]["digest"])
    for layer in data["layers"]:
        shas.append(layer["digest"])
    return ["sha256-" + s[7:] for s in shas]


def get_file_paths(model_name: ModelName, model_path: Path) -> list[Path]:
    """Returns a list of "relative" paths."""
    manifest_abs_path = (
        model_path
        / "manifests"
        / model_name.host
        / model_name.namespace
        / model_name.model
        / model_name.tag
    )
    blob_shas = parse_manifest(manifest_abs_path)
    # Generate relative paths
    blob_paths = []
    blob_paths.append(
        Path("manifests")
        / model_name.host
        / model_name.namespace
        / model_name.model
        / model_name.tag
    )
    for sha in blob_shas:
        blob_paths.append(Path("blobs") / sha)
    return blob_paths


def create_tarball(model_path: Path, blob_paths: list[Path]):
    """Creates a tarball from the given paths and outputs it to stdout."""
    tar_command = ["tar", "-cf", "-", "-C", str(model_path)]
    tar_command.extend([str(path) for path in blob_paths])
    subprocess.run(tar_command, stdout=sys.stdout)


def main():
    model_name = parse_model_name(sys.argv[1])
    # print(model_name, file=sys.stderr)
    model_path = Path(os.getenv("OLLAMA_MODELS", "~/.ollama/models")).expanduser()
    blob_paths = get_file_paths(model_name, model_path)
    # print(blob_paths, file=sys.stderr)
    create_tarball(model_path, blob_paths)


if __name__ == "__main__":
    main()
