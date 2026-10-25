"""Post generation hook."""

import json
import re
from collections import OrderedDict
from datetime import date
from pathlib import Path

from binaryornot.check import is_binary
from cookieplone import generator
from cookieplone.utils import console, npm, plone, post_gen
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


POST_GEN_TO_REMOVE: dict[str, list[str]] = {
    "devops": [
        "devops",
    ],
}

TEMPLATES_FOLDER: str = "templates"


def configure_repoplone_release(context: OrderedDict, *args: tuple, **kwargs: dict):
    """Configure the repoplone release pipeline used by GitLab CI.

    GitLab projects do not have a GitHub release to create, so the
    `gh_release` step is omitted. The `git` step is also omitted: the CI job
    commits and pushes only after the container images have been promoted, so
    a failed image push does not leave a published tag behind.
    """
    path = Path("repository.toml")
    if not path.is_file():
        return

    content = path.read_text()
    if "[repository.release]" in content:
        return

    if not content.endswith("\n"):
        content += "\n"
    content += """
[repository.release]
steps = [
    "changelog",
    "version",
    "repository",
    "release_backend",
    "release_frontend",
]
"""
    path.write_text(content)


def set_initial_calver_version(context: OrderedDict, *args: tuple, **kwargs: dict):
    """Seed version.txt with today's date when the repository uses calver.

    The project template ships a semver seed (``__version_package``). With
    calver, repoplone expects a value like ``YYYYMMDD.N`` so the first release
    becomes ``YYYYMMDD.1`` instead of a semver-derived value.
    """
    repository_path = Path("repository.toml")
    version_path = Path("version.txt")
    if not (repository_path.is_file() and version_path.is_file()):
        return

    repository_content = repository_path.read_text()
    if not re.search(
        r'^\s*version_format\s*=\s*"calver"\s*$', repository_content, re.MULTILINE
    ):
        return

    current_version = version_path.read_text().strip()
    seed_version = str(context.get("__version_package", "")).strip()
    if seed_version and current_version != seed_version:
        # Do not overwrite a version that was already released or managed.
        return

    version_path.write_text(date.today().strftime("%Y%m%d") + ".0\n")


def modify_pyprojecttoml_dependency(context: OrderedDict, *args: tuple, **kwargs: dict):
    new_content = []
    with open(Path("backend") / "pyproject.toml") as fp:
        in_dependencies = False
        for line in fp.readlines():
            if in_dependencies and line == "]\n":
                in_dependencies = False
                new_content.append("]")
            elif in_dependencies:
                continue

            elif not in_dependencies and line.startswith("dependencies = ["):
                new_content.append(line)
                new_content.append('"Plone",')
                if context.get("postgres", False):
                    new_content.append('"zodb_pgjsonb",')
                    new_content.append('"plone.pgcatalog",')
                    if context.get("thumbor"):
                        new_content.append('"plone-pgthumbor",')

                if not context.get("feature_headless", False):
                    new_content.append('"z3c.jbot",')

                in_dependencies = True
            else:
                new_content.append(line)

    with open(Path("backend") / "pyproject.toml", "w") as fp:
        fp.writelines(new_content)


def configure_repository_urls(
    context: OrderedDict, *args: tuple, **kwargs: dict
):
    """Use the container registry answer to choose GitHub or GitLab URLs."""
    if context.get("container_registry") != "gitlab":
        return

    organization = context.get("github_organization")
    project_slug = context.get("__project_slug") or context.get("project_slug")
    if not organization or not project_slug:
        return

    old_http = f"https://github.com/{organization}/{project_slug}"
    new_http = f"https://gitlab.com/{organization}/{project_slug}"
    old_git = f"git@github.com:{organization}/{project_slug}"
    new_git = f"git@gitlab.com:{organization}/{project_slug}"
    badge = re.compile(
        re.escape(old_http) + r"/actions/workflows/[^/]+/badge\.svg"
    )

    for path in Path(".").rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if is_binary(str(path)):
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        new_text = badge.sub(f"{new_http}/badges/main/pipeline.svg", text)
        new_text = re.sub(
            re.escape(old_http) + r"/actions/workflows/[^)\s]+",
            f"{new_http}/-/pipelines",
            new_text,
        )
        new_text = new_text.replace(old_http, new_http)
        new_text = new_text.replace(old_git, new_git)
        new_text = new_text.replace(f"{new_http}/issues", f"{new_http}/-/issues")
        new_text = new_text.replace(
            "Specific GitHub Workflows are triggered based on changes in each "
            "codebase (refer to .github/workflows).",
            "Specific GitLab CI jobs are triggered based on changes in each "
            "codebase (refer to .gitlab-ci.yml).",
        )
        if new_text != text:
            path.write_text(new_text)


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""

    actions: list[post_gen.PostGenAction] = [
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "devops"),
            "title": "Remove Ansible files",
            "enabled": True,
        },
        {
            "handler": modify_pyprojecttoml_dependency,
            "title": "Modify pyproject.toml dependencies",
            "enabled": True,
        },
        {
            "handler": configure_repoplone_release,
            "title": "Configure repoplone release pipeline",
            "enabled": True,
        },
        {
            "handler": set_initial_calver_version,
            "title": "Set initial calver version",
            "enabled": True,
        },
        {
            "handler": configure_repository_urls,
            "title": "Configure GitLab repository URLs",
            "enabled": True,
        },
    ]
    return actions


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # Action handlers
    post_gen.run_post_gen_actions(context, output_dir, action_handlers(context))

    msg = """
        [bold blue]{{ cookiecutter.title }}[/bold blue]

        Now, code it, create a git repository, push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New project was generated",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
