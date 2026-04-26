# -*- coding: utf-8 -*-

"""
Shared utilities for mise tasks.
"""

import re
import sys
import subprocess
from pathlib import Path
from functools import cached_property

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        print("Error: tomli not installed. Run: uv sync --extra mise")
        sys.exit(1)


class ProjectConfig:
    @cached_property
    def project_root(self) -> Path:
        return Path(__file__).parent.parent.parent

    @cached_property
    def pyproject_data(self) -> dict:
        pyproject_path = self.project_root / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            return tomllib.load(f)

    @cached_property
    def project_name(self) -> str:
        return self.pyproject_data["project"]["name"]

    @cached_property
    def project_description(self) -> str:
        return self.pyproject_data["project"]["description"]

    @cached_property
    def git_remote_url(self) -> str:
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("Error: Failed to get git remote URL")
            sys.exit(1)

    @cached_property
    def github_owner(self) -> str:
        match = re.match(
            r"(?:https://github\.com/|git@github\.com:)([^/]+)/(.+?)(?:\.git)?$",
            self.git_remote_url,
        )
        if not match:
            print(f"Error: Could not parse GitHub URL: {self.git_remote_url}")
            sys.exit(1)
        return match.group(1)

    @cached_property
    def github_repo_name(self) -> str:
        match = re.match(
            r"(?:https://github\.com/|git@github\.com:)([^/]+)/(.+?)(?:\.git)?$",
            self.git_remote_url,
        )
        if not match:
            print(f"Error: Could not parse GitHub URL: {self.git_remote_url}")
            sys.exit(1)
        return match.group(2)

    @cached_property
    def github_repo_url(self) -> str:
        url = self.git_remote_url
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
        if url.endswith(".git"):
            url = url[:-4]
        return url

    @cached_property
    def readthedocs_slug(self) -> str:
        return self.project_name.replace("_", "-")

    @cached_property
    def readthedocs_url(self) -> str:
        return f"https://{self.readthedocs_slug}.readthedocs.io/"


config = ProjectConfig()
