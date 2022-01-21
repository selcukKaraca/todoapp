FROM python:alpine
RUN mkdir /app /app/templates
WORKDIR /app
ADD requirements.txt /app && ADD app.py /app && COPY templates /app/templates
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
