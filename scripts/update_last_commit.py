# This module is part of a cronjob, running daily to have the latest commit and project status.

import yaml
import requests
import os
from datetime import datetime


def get_repo_info(repo_url, headers={}):
    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"token {os.getenv('GITHUB_TOKEN')}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        return {
            "status": "Archived" if repo_data.get("archived", False) else "Active",
            "last_commit": repo_data.get("pushed_at", "unknown").split("T")[0],
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {repo_url}: {e}")
        return None


def update_extensions(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    xblocks = data.get("xblocks", [])

    for xblock in xblocks:
        repo_url = xblock.get("url")
        if not repo_url:
            print(f"Skipping xblock {xblock['name']}: No repository URL")
            continue

        repo_info = get_repo_info(repo_url)
        if not repo_info:
            print(f"Skipping xblock {xblock['name']}: No last commit found")
            continue

        xblock["status"] = repo_info["status"]
        xblock["last_commit"] = repo_info["last_commit"]
        print(f"Repo info updated for {xblock['name']}")

    xblocks.sort(key=lambda x: x["name"].lower())

    updated_content = ["xblocks:\n"]
    previous_initial = ""

    for xblock in xblocks:
        initial = xblock["name"][0].upper()
        if initial != previous_initial:
            updated_content.append(f"  # {initial}")
            previous_initial = initial

        description = xblock.get("description", "").strip()
        description_lines = description.split("\n")
        if len(description_lines) > 1:
            multiline_description = "|\n      " + "\n      ".join(description_lines)
        else:
            multiline_description = description

        updated_content.append(f"  - name: {xblock['name']}")
        updated_content.append(f"    description: {multiline_description}")
        for key, value in xblock.items():
            if key not in ["name", "description"]:
                updated_content.append(f"    {key}: {value}")

        updated_content.append("")  # Ensure a newline after each xblock

    with open(file_path, "w") as file:
        file.write("\n".join(updated_content))


if __name__ == "__main__":
    file_path = "extensions.yml"
    update_extensions(file_path)
