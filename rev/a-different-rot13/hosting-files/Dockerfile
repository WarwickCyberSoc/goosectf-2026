FROM ubuntu:22.04
RUN apt-get update --fix-missing && \
 apt-get install -y socat gcc-multilib && \
 rm -rf /var/lib/apt/lists/*
RUN groupadd -r ctf && useradd -r -g ctf ctf

ADD --chown=ctf rot_13_or_smth_else flag.txt /home/ctf/
RUN chown -R root:ctf /home/ctf
RUN chmod 440 /home/ctf/flag.txt
RUN chmod 750 /home/ctf/rot_13_or_smth_else

USER ctf
WORKDIR /home/ctf
EXPOSE 1337
ENTRYPOINT ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./rot_13_or_smth_else,stderr"]