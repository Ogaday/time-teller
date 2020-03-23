FROM python:3.8

# TODO: Create app user

WORKDIR /opt

COPY time_teller.py /opt/time_teller.py

ENTRYPOINT ["python"]
CMD ["-m", "time_teller"]
