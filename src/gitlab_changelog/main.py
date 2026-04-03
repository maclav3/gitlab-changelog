#!/usr/bin/env python3
"""
Generate a changelog of commits between an environment's current deployment and a git reference.
Usage:
    python changelog.py <environment_name> [-from <ref>]
    python changelog.py --list
"""

import argparse
import sys
import os
from . import gitlab_client
from . import formatter
from . import __version__ as pkg_version

PROJECT_ID = os.getenv("PROJECT_ID")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")


def run():
    main()


def main():
    parser = argparse.ArgumentParser(
        description="Generate a changelog of commits between an environment's current deployment and a git reference."
    )
    parser.add_argument(
        "env", nargs="?", help="Environment name (required unless --list is used)"
    )
    parser.add_argument(
        "-from",
        dest="from_ref",
        help="Git reference to compare against (defaults to project's default branch, e.g., main or master)",
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available environments"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {pkg_version}"
    )

    args = parser.parse_args()

    if not GITLAB_TOKEN or not PROJECT_ID:
        print("Error: Set GITLAB_TOKEN and PROJECT_ID environment variables")
        sys.exit(1)

    try:
        if args.list:
            envs = gitlab_client.get_environments(PROJECT_ID)
            formatter.list_environments(envs)
            return

        if not args.env:
            parser.error("the following arguments are required: env (or use --list)")

        env_name = args.env
        to_ref = args.from_ref

        if not to_ref:
            print("🔍 Fetching default branch...")
            to_ref = gitlab_client.get_default_branch(PROJECT_ID)

        print(f"🔍 Fetching current deployment for environment: {env_name}")
        current_sha = gitlab_client.get_environment_commit(PROJECT_ID, env_name)
        print(f"📌 Current deployment: {current_sha[:8]}")

        print(f"🔍 Comparing with {to_ref}...")
        commits = gitlab_client.get_commits_between(PROJECT_ID, current_sha, to_ref)

        formatter.format_changelog(commits, PROJECT_ID)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
