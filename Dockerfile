FROM azuresdk/azure-cli-python:2.0.14

RUN mkdir perisher
RUN mkdir exports
WORKDIR perisher

COPY ["requirements.txt", "requirements.txt"]
RUN pip install --ignore-install --upgrade -r requirements.txt

RUN mkdir modules
COPY ["modules", "modules"]
COPY ["run.py", "run.py"]

ENTRYPOINT python run.py
