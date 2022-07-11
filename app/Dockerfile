FROM centos:7


RUN yum -y update \
    && yum -y install python3 \
    && yum -y install which

COPY requirments.txt /tmp
RUN pip3 install -r /tmp/requirments.txt 

RUN useradd -d /home/senpow -p senpow -m senpow \
     && echo 'root ALL=(ALL) ALL' >> /etc/sudoers \ 
     && echo 'senpow ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER senpow
WORKDIR /home/senpow

RUN mkdir -m755 templates \
    && mkdir -m755 static 
COPY ./templates/* /home/senpow/templates/
COPY ./static/* /home/senpow/static/

COPY app.py /tmp

RUN cp /tmp/app.py /home/senpow \
     && chmod +x app.py \
     && pwd \
     && ls \
     && ls ./templates \
     && ls ./static 

EXPOSE 5000
CMD ["/home/senpow/app.py"]
ENTRYPOINT ["python3"]
