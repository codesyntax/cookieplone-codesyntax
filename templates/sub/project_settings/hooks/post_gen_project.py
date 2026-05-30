"""Post generation hook."""

import json
from collections import OrderedDict
from pathlib import Path

from binaryornot.check import is_binary
from cookieplone import generator
from cookieplone.utils import console, npm, plone, post_gen
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


POST_GEN_TO_REMOVE: dict[str, list[str]] = {
    "devops": [
        "devops/.env_dist",
        "devops/.gitignore",
        "devops/ansible.cfg",
        "devops/etc",
        "devops/inventory",
        "devops/Makefile",
        "devops/playbooks",
        "devops/requirements",
        "devops/tasks",
        "devops/README.md",
    ],
}

TEMPLATES_FOLDER: str = "templates"


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
