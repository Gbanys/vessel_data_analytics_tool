FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get -y install curl

RUN curl -LsS https://aka.ms/InstallAzureCLIDeb | bash && rm -rf /var/lib/apt/lists/*

COPY . /home/vessel_data_analytics_tool
WORKDIR /home/vessel_data_analytics_tool

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]