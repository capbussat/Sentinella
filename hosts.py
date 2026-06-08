#!/usr/bin/env python3

from pathlib import Path


def load_hosts_from_file(filename="hosts") -> list[str]:

    file_path = Path(filename)

    if not file_path.exists():
        print(f"[ERROR] File not found: {filename}")
        raise FileNotFoundError(f"Hosts file not found: {file_path}")
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

        # garanteix unicitat
        hosts = list(dict.fromkeys(hosts))   

    return hosts


print ("Host loaded")
