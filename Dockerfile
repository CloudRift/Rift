from python:2.7

RUN mkdir /home/Rift
WORKDIR /home/Rift
COPY requirements.txt /home/Rift/requirements.txt
COPY test-requirements.txt /home/Rift/test-requirements.txt
RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt
RUN rm requirements.txt
RUN rm test-requirements.txt
COPY . /home/Rift/
RUN adduser --disabled-password --gecos '' rift-worker
