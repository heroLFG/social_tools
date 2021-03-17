FROM python:3
WORKDIR /application
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install ffmpeg -y
EXPOSE 5000
# COPY . .
CMD ["flask", "run"]
