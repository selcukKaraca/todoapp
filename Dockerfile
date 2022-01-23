FROM python:alpine
RUN mkdir /app /app/templates
WORKDIR /app
COPY requirements.txt /app 
COPY app.py /app 
COPY templates /app/templates
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
