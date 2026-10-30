# Supply a digest in PYTHON_BASE after the target's first successful build.
ARG PYTHON_BASE=python:3.12-slim-bookworm
FROM ${PYTHON_BASE}
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    CTI_LAB_ROOT=/opt/cti-lab JUPYTER_CONFIG_DIR=/tmp/jupyter-config \
    JUPYTER_DATA_DIR=/tmp/jupyter-data JUPYTER_RUNTIME_DIR=/tmp/jupyter-runtime
WORKDIR /opt/cti-lab
COPY requirements.lock /tmp/requirements.lock
COPY wheelhouse/ /wheels/
RUN python -m pip install --no-index --find-links=/wheels -r /tmp/requirements.lock
COPY . /opt/cti-lab/
RUN python -m pip install --no-deps --no-build-isolation . \
    && groupadd --gid 1000 lab && useradd --uid 1000 --gid 1000 --create-home lab \
    && chown -R lab:lab /opt/cti-lab
USER 1000:1000
EXPOSE 8888
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
    CMD python scripts/healthcheck.py
CMD ["python", "scripts/serve.py"]
