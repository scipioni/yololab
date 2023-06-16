#ARG OPENCV_VERSION=4.7.0

#FROM yololab/opencv:${OPENCV_VERSION}

ARG CUDA_VERSION=11.6.1
FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-runtime-ubuntu20.04

ARG ENV=development
ARG PYTHON=3.9
# ARG PYPI_URL=https://pypi.csgalileo.org/simple
# ARG PYPI_USERNAME=galileo
# ARG PYPI_PASSWORD

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  DEBIAN_FRONTEND=noninteractive \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

# serve per cv2.imshow
RUN if [ "$ENV" = "development" ]; then \
  apt-get update && \
  apt-get install -y -q --no-install-recommends libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 && \
  rm -rf /var/lib/apt/lists/*; fi

COPY ./deadsnakes/deadsnakes_ubuntu_ppa.gpg /etc/apt/trusted.gpg.d/deadsnakes_ubuntu_ppa.gpg
COPY ./deadsnakes/deadsnakes-ubuntu-ppa-focal.list /etc/apt/sources.list.d/deadsnakes-ubuntu-ppa-focal.list

RUN apt-get update

#RUN apt-get remove -y python3.8
#RUN apt-get -y autoremove

RUN apt-get install -y -q --no-install-recommends \
  python${PYTHON} \
  python${PYTHON}-dev \
  python${PYTHON}-venv

RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON} 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON} 1

RUN python${PYTHON} -m ensurepip
RUN python${PYTHON} -m pip install --upgrade wheel




RUN python${PYTHON} -m pip install wheel pdm
RUN pdm config python.use_venv false
#RUN pdm config pypi.extra.url ${PYPI_URL}
#RUN pdm config pypi.extra.username ${PYPI_USERNAME}
#RUN pdm config pypi.extra.password ${PYPI_PASSWORD}

WORKDIR /project
COPY pyproject.toml pdm.lock README.md ./

RUN pdm install --prod --no-lock --no-editable --no-isolation
RUN pdm install -G gpu --no-lock --no-editable --no-isolation
#RUN pdm install -G $ENV --no-lock --no-editable --no-isolation


WORKDIR /app
COPY ./yololab ./yololab
RUN mkdir -p /app/pkgs
RUN bash -c "cp -a /project/__pypackages__/3*/* /app/pkgs"

ENV PYTHONPATH=/app/pkgs/lib:/app:$PYTHONPATH
ENV PATH=/app/pkgs/bin:$PATH
