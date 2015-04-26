FROM python:2.7.9
MAINTAINER brian@projectweekend.net
RUN apt-get update && apt-get -y install libxml2-dev libxslt-dev libjpeg-dev zlib1g-dev libpng12-dev
ADD . /src/
WORKDIR /src
RUN pip install ipython && pip install -r requirements.txt
RUN curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python
CMD ["python", "parser.py"]
