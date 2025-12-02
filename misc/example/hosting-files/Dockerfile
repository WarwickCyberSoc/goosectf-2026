FROM ubuntu:22.04
RUN apt-get update --fix-missing && \
 apt-get install -y socat python3 && \
 rm -rf /var/lib/apt/lists/*
RUN groupadd -r ctf && useradd -r -g ctf ctf

ADD --chown=ctf hello.py /home/ctf/
RUN chown -R root:ctf /home/ctf
RUN chmod 440 /home/ctf/flag.txt
RUN chmod 750 /home/ctf/level2

USER ctf
WORKDIR /home/ctf
EXPOSE 1337
ENTRYPOINT ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:python3 hello.py"]