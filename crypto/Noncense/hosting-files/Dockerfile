FROM ubuntu:22.04
RUN apt update -y
RUN apt install -y socat python3 python3-pip

RUN pip3 install cryptography 

WORKDIR /app
COPY program.py .
COPY key.txt .
COPY nonce.txt .
COPY flag1.txt .
COPY flag2.txt .

EXPOSE 1337

CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:python3 -u /app/program.py"]