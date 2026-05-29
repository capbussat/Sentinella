#!/usr/bin/env python3
"""
Simple multithreaded SSH executor using Fabric.
Sembla que podria funcionar, almenys no dona errors.

Requirements:
    pip install fabric

SSH authentication:
    Configure SSH keys previously:
        ssh-copy-id user@host

Execution:
    python ssh_fabric_threads.py
"""

from fabric import Connection
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import time

# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------

SSH_USER = "admin"

HOSTS = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    "192.168.1.13",
    "192.168.1.14",
    "192.168.1.15",
    "192.168.1.16",
    "192.168.1.17",
    "192.168.1.18",
    "192.168.1.19",
    "192.168.1.20",
    "192.168.1.21",
    "192.168.1.22",
    "192.168.1.23",
    "192.168.1.24",
    "192.168.1.25",
    "192.168.1.26",
    "192.168.1.27",
    "192.168.1.28",
    "192.168.1.29",
    "192.168.1.30",
    "192.168.1.31",
    "192.168.1.32",
    "192.168.1.33",
    "192.168.1.34",
    "192.168.1.35",
    "192.168.1.36",
    "192.168.1.37",
    "192.168.1.38",
    "192.168.1.39",
]

COMMAND = "hostname && uptime"

MAX_THREADS = 10
CONNECT_TIMEOUT = 5

# -------------------------------------------------------------------
# SSH EXECUTION FUNCTION
# -------------------------------------------------------------------


def execute_ssh_command(host: str) -> dict:
    """
    Execute a remote bash command using Fabric.
    """

    result_data = {
        "host": host,
        "success": False,
        "output": "",
        "error": "",
    }

    try:
        connection = Connection(
            host=host,
            user=SSH_USER,
            connect_timeout=CONNECT_TIMEOUT,
        )

        result = connection.run(
            COMMAND,
            hide=True,
            warn=True,
        )

        result_data["success"] = result.ok
        result_data["output"] = result.stdout.strip()

        if result.stderr:
            result_data["error"] = result.stderr.strip()

        connection.close()

    except socket.timeout:
        result_data["error"] = "Connection timeout"

    except Exception as e:
        result_data["error"] = str(e)

    return result_data


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------


def main():

    start_time = time.time()

    print(f"\nExecuting on {len(HOSTS)} hosts...\n")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

        futures = {
            executor.submit(execute_ssh_command, host): host
            for host in HOSTS
        }

        for future in as_completed(futures):

            data = future.result()

            print("=" * 60)
            print(f"HOST: {data['host']}")
            print(f"SUCCESS: {data['success']}")

            if data["output"]:
                print("\nOUTPUT:")
                print(data["output"])

            if data["error"]:
                print("\nERROR:")
                print(data["error"])

    elapsed = time.time() - start_time

    print("\nFinished")
    print(f"Elapsed time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()