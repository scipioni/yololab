FROM ultralytics/ultralytics
ENV JUPYTER_TOKEN xyz


WORKDIR /tmp

COPY requirements.txt requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt


#WORKDIR /deciai
#RUN python3 -m venv venv --system-site-packages
#RUN venv/bin/python -m ipykernel install --user --name=deciai
#COPY requirements.deciai.txt requirements.txt
#RUN venv/bin/pip install -r requirements.txt

WORKDIR /notebooks

#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
