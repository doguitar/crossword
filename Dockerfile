FROM python:2

WORKDIR /usr/src/app

RUN mkdir -p /data/config/ /data/crosswords

COPY cherrypy/ ./cherrypy/
COPY db/ ./db/
COPY downloaders/ ./downloaders/
COPY html/ ./html/
COPY mako/ ./mako/
COPY manager/ ./manager/
COPY markupsafe/ ./markupsafe/
COPY puzpy/ ./puzpy/
COPY host.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4567

# run the application
CMD ["python", "./host.py"]  