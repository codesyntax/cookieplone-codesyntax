import pytest


def test_project_template_overridden(merged_repository_config):
    """Verify that the project template title is our custom one."""
    assert merged_repository_config is not None
    project = merged_repository_config["templates"]["project"]
    assert project["title"] == "CodeSyntax's Plone projects"


def test_project_layers(template_layers):
    """Verify that the project template has at least two layers (upstream + ours)."""
    assert "project" in template_layers
    layers = template_layers["project"]
    # Upstream + downstream
    assert len(layers) >= 2
    # The last layer should be from our local repo
    downstream_repo, _ = layers[-1]
    assert "cookieplone-codesyntax" in downstream_repo


def test_bake_project(bake_from_local):
    """Test baking the project template."""
    result = bake_from_local(
        "project",
        extra_context={
            "project_title": "Test Project",
            "project_slug": "test-project",
            "description": "A test project",
            "author": "CodeSyntax",
            "email": "info@codesyntax.com",
        },
    )
    assert result.exit_code == 0, result.exception
    assert result.project_path.is_dir()
    # Check for some expected file in the baked project
    assert (result.project_path / "README.md").exists()


def test_subtemplate_availability(merged_repository_config):
    """Verify that the subtemplate is present and hidden."""
    assert "sub/project_settings" in merged_repository_config["templates"]
    sub = merged_repository_config["templates"]["sub/project_settings"]
    assert sub["hidden"] is True
