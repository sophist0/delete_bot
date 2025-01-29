FROM python:3.12
RUN mkdir ./delete_bot
WORKDIR ./delete_bot
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD delete_user_data.py .
ADD base_util.py .
ADD bot_methods.py .
ADD script_constants.py .
ADD config.txt .
RUN mkdir logs
COPY tests .
# CMD ["python3", "./delete_user_data.py"]
# CMD ["python3", "-m", "pytest"]
CMD ["sh", "-c", "${DOCKER_CMD}"]