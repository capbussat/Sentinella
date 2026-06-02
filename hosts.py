#!/usr/bin/env python3

from pathlib import Path


def load_hosts_from_file(filename="hosts") -> list[str]:

    file_path = Path(filename)

    if not file_path.exists():
        print(f"[ERROR] File not found: {filename}")
        return []

    hosts = []

    with open(file_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments
            if line.startswith("#"):
                continue

            hosts.append(line)

    return hosts
