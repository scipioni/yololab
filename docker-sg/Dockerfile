FROM deciai/super-gradients:latest
ENV JUPYTER_TOKEN xyz
ENV CRASH_HANDLER=FALSE

WORKDIR /tmp

COPY requirements.txt requirements.txt
RUN pip install nvidia-pyindex
RUN pip3 --no-cache-dir install -U -r requirements.txt


#WORKDIR /ultralytics
#RUN python3 -m venv venv --system-site-packages
#RUN venv/bin/python -m ipykernel install --user --name=ultralytics
#RUN venv/bin/pip --no-cache-dir install -U ultralytics 
#COPY requirements.deciai.txt requirements.txt
#RUN venv/bin/pip install -r requirements.txt

WORKDIR /notebooks

#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
