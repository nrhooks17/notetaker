FROM python:3.11-alpine3.18

# set the working directory
WORKDIR /opt/webapps/notetaker

RUN apk add bash vim curl

# copy over all files
COPY . .

#install dependencies from requirements file
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
