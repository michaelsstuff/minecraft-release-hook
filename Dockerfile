FROM python:3-alpine
RUN pip install requests
COPY entrypoint.py /root/
WORKDIR /root/
CMD ["/usr/local/bin/python","entrypoint.py"]
