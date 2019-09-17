FROM python:3-alpine
RUN apk add --update \
    vim \
  && rm -rf /var/cache/apk/*
RUN pip install requests
COPY entrypoint.py /
CMD ["/usr/local/bin/python","entrypoint.py"]
