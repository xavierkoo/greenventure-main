FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./mission.py ./invokes.py ./
CMD [ "python", "./mission.py" ]
