FROM python:3.7
LABEL maintainer="coryphanta@mail.ru"
COPY . .
WORKDIR .
RUN pip install -r requirements.txt
EXPOSE 8180
CMD python run_server.py
