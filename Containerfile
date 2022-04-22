FROM registry.access.redhat.com/ubi8/python-39:latest
WORKDIR $HOME
COPY requirements.txt $HOME
RUN pip3 install -r requirements.txt
RUN mkdir $HOME/app
COPY app/ $HOME/app
COPY entrypoint.sh $HOME
ENV PORT=8000
CMD ["./entrypoint.sh"]
