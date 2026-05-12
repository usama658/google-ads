"""
Google Tag Manager API client.
Lists tags, triggers, and variables for the configured container.

Usage:
    python gtm_client.py            # list tags
    python gtm_client.py --triggers
    python gtm_client.py --variables
"""
import argparse
import sys

import requests
import yaml

CONFIG_FILE = "gtm-config.yaml"


def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: '{path}' not found.")
        sys.exit(1)


def get_access_token(config: dict) -> str:
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "refresh_token": config["refresh_token"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "grant_type": "refresh_token",
    })
    r.raise_for_status()
    return r.json()["access_token"]


def gtm_get(url: str, headers: dict) -> dict:
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def list_tags(config: dict, headers: dict) -> None:
    base = f"https://www.googleapis.com/tagmanager/v2/accounts/{config['account_id']}/containers/{config['container_id']}"
    workspaces = gtm_get(f"{base}/workspaces", headers)["workspace"]
    ws_id = workspaces[0]["workspaceId"]
    tags = gtm_get(f"{base}/workspaces/{ws_id}/tags", headers).get("tag", [])
    print(f"\nTags in {config['public_id']} ({len(tags)} total):")
    print(f"  {'Name':<40} {'Type':<30} {'Status'}")
    print("  " + "-" * 75)
    for t in sorted(tags, key=lambda x: x["name"]):
        status = "paused" if t.get("paused") else "active"
        print(f"  {t['name']:<40} {t['type']:<30} {status}")


def list_triggers(config: dict, headers: dict) -> None:
    base = f"https://www.googleapis.com/tagmanager/v2/accounts/{config['account_id']}/containers/{config['container_id']}"
    workspaces = gtm_get(f"{base}/workspaces", headers)["workspace"]
    ws_id = workspaces[0]["workspaceId"]
    triggers = gtm_get(f"{base}/workspaces/{ws_id}/triggers", headers).get("trigger", [])
    print(f"\nTriggers in {config['public_id']} ({len(triggers)} total):")
    print(f"  {'Name':<40} {'Type'}")
    print("  " + "-" * 60)
    for t in sorted(triggers, key=lambda x: x["name"]):
        print(f"  {t['name']:<40} {t['type']}")


def list_variables(config: dict, headers: dict) -> None:
    base = f"https://www.googleapis.com/tagmanager/v2/accounts/{config['account_id']}/containers/{config['container_id']}"
    workspaces = gtm_get(f"{base}/workspaces", headers)["workspace"]
    ws_id = workspaces[0]["workspaceId"]
    variables = gtm_get(f"{base}/workspaces/{ws_id}/variables", headers).get("variable", [])
    print(f"\nVariables in {config['public_id']} ({len(variables)} total):")
    print(f"  {'Name':<40} {'Type'}")
    print("  " + "-" * 60)
    for v in sorted(variables, key=lambda x: x["name"]):
        print(f"  {v['name']:<40} {v['type']}")


def main():
    parser = argparse.ArgumentParser(description="Inspect GTM container")
    parser.add_argument("--triggers", action="store_true")
    parser.add_argument("--variables", action="store_true")
    parser.add_argument("--config", default=CONFIG_FILE)
    args = parser.parse_args()

    config = load_config(args.config)
    token = get_access_token(config)
    headers = {"Authorization": f"Bearer {token}"}

    if args.triggers:
        list_triggers(config, headers)
    elif args.variables:
        list_variables(config, headers)
    else:
        list_tags(config, headers)


if __name__ == "__main__":
    main()
