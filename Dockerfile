FROM python:3.12-alpine
WORKDIR /gypso_app
COPY requirements.txt .
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# ENV PYTHONPATH "${PYTHONPATH}:/usr/src/gypso_app"
# COPY . .
# ENTRYPOINT ["python", "manage.py", "runserver"]
EXPOSE 8000