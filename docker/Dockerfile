FROM python:3.11.1-bullseye as base

######################################### [build] ########################

FROM base as build

ENV LC_ALL=C.UTF-8
ENV DOCKER_UID=1000
ENV PIPENV_VENV_IN_PROJECT=1
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gettext \
        locales \
        sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    dpkg-reconfigure locales && \
      locale-gen C.UTF-8 && \
      /usr/sbin/update-locale LANG=C.UTF-8 && \
    useradd -u $DOCKER_UID -ms /bin/bash -d /app appuser

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
ENV PATH=/app/.venv/bin:/root/.local/bin:$PATH
RUN pip3 install --user pipenv && \
    pipenv sync --dev
COPY src /app/

RUN export DJANGO_SECRET_KEY=unused-but-must-be-present && \
    python3 /app/manage.py collectstatic --noinput && \
    python3 /app/manage.py compilemessages && \
    unset DJANGO_SECRET_KEY

######################################### [app] ########################

FROM base as app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV DJANGO_SETTINGS_MODULE=generic_vote.settings
ENV DOCKER_UID=1000
ENV PATH=/app/.venv/bin:/root/.local/bin:$PATH

# From GitHub Actions
ARG BUILD_DATE
ARG GITHUB_SHA
ENV BUILD_DATE=$BUILD_DATE
ENV GITHUB_SHA=$GITHUB_SHA

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        rsync \
        vim \
        sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /run/generic_vote /static_files && \
    chown -R $DOCKER_UID:$DOCKER_UID /run/generic_vote /static_files && \
    useradd -u $DOCKER_UID -ms /bin/bash -d /app appuser

COPY docker/entrypoint.sh /usr/local/bin/entrypoint

COPY --from=build --chown=appuser /app /app

RUN chmod +x /usr/local/bin/entrypoint

WORKDIR /app

USER appuser

ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD [""]
