# syntax=docker/dockerfile:1
ARG PYTHON_VERSION={{ cookiecutter.__python_version }}
FROM plone/server-builder:uv-${PYTHON_VERSION} AS builder

RUN apt-get update && apt-get install -y --no-install-recommends openssh-client git swig libssl-dev && rm -rf /var/lib/apt/lists/*

COPY . /src
WORKDIR /src

# Install package
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=mx.ini,target=mx.ini \
    --mount=type=ssh,id=default \
    GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    uv tool run mxdev[uv] -c mx.ini && \
    uv sync \
        --no-dev \
        --no-group test \
        --group container \
        --no-editable

RUN if [ -d /src/sources/cs.dxfeatured/src/cs ]; then \
        for sp in /app/lib/python*/site-packages; do \
            mkdir -p "$sp/cs" && \
            cp -r /src/sources/cs.dxfeatured/src/cs/. "$sp/cs/"; \
        done; \
    fi

RUN for d in \
        /app/lib/python*/site-packages/ftw_blueprints-*.dist-info \
        /app/lib/python*/site-packages/collective_blueprint_jsonmigrator-*.dist-info \
        /app/lib/python*/site-packages/collective.jsonmigrator-*.dist-info; do \
        if [ -f "$d/entry_points.txt" ]; then rm -f "$d/entry_points.txt"; fi; \
    done

# Move skeleton files to /app
RUN <<EOT
    mv /app_skeleton/* /app
    rm -Rf /app_skeleton
    chmod +x /app/docker-entrypoint.sh
    mv scripts/create_site.py /app/scripts/create_site.py
EOT

# Compile translation files
RUN <<EOT
    /app/bin/python /compile_mo.py
EOT

FROM plone/server-prod-config:uv-${PYTHON_VERSION}

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-backend" \
      org.label-schema.description="{{ cookiecutter.title }} backend image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

# Copy the pre-built `/app` directory to the runtime container
# and change the ownership to user app and group app in one step.
COPY --from=builder --chown=500:500 /app /app

RUN <<EOT
    ln -s /data /app/var
    chown -R 500:500 /data
EOT
