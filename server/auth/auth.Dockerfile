FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
ENV APP_SECRET="W10_ESD_Breakdowns"
ENV FACEBOOK_OAUTH_ID="207392055310912"
ENV FACEBOOK_OAUTH_SECRET="85f92b197a5c9b7cad6cdeb19809e86a"
COPY ./invokes.py ./auth.py ./
CMD [ "python", "./auth.py" ]