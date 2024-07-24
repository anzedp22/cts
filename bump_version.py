import subprocess


def get_latest_tag():
    try:
        latest_tag = (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"]
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        latest_tag = None
    return latest_tag


def get_commit_messages_since_latest_tag(latest_tag):
    commit_range = f"{latest_tag}..HEAD"
    commit_messages = (
        subprocess.check_output(
            ["git", "log", commit_range, "--pretty=format:%s"]
        )
        .decode()
        .split("\n")
    )
    return commit_messages


def determine_version_bump(commit_messages):
    bump_type = "patch"
    for message in commit_messages:
        if "BREAKING CHANGE" in message:
            bump_type = "major"
            break
        elif message.startswith("feat"):
            bump_type = "minor"
    return bump_type


def read_version(file_path="version.txt"):
    with open(file_path, "r") as file:
        version = file.read().strip().lstrip("v")
    return version


def write_version(version, file_path="version.txt"):
    with open(file_path, "w") as file:
        file.write(f"v{version}")


def increment_version(version, part):
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        major += 1
        minor, patch = 0, 0
    elif part == "minor":
        minor += 1
        patch = 0

    elif part == "patch":

        patch += 1
    return f"{major}.{minor}.{patch}"


def main():
    latest_tag = get_latest_tag()
    if latest_tag is None:
        latest_tag = "v1.0.0"
        version = latest_tag.strip().lstrip("v")
        write_version(version)
        print(f"New version: v{version}")

    else:
        commit_messages = get_commit_messages_since_latest_tag(latest_tag)
        version_bump = determine_version_bump(commit_messages)
        current_version = read_version()
        new_version = increment_version(current_version, version_bump)
        write_version(new_version)
        print(f"Version updated from v{current_version} to v{new_version}")


if __name__ == "__main__":
    main()
