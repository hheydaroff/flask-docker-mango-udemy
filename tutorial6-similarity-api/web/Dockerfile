#Pull the image of Python
FROM python:3
#Select the working directory on container
WORKDIR /usr/src/app
#Copy the requirements to the container
COPY requirements.txt .
#install the modules from requirements
RUN pip3 install --no-cache-dir -r requirements.txt
#copy all files from repo to container working directory
COPY . .
# import spacy model
RUN pip3 install ./en_core_web_sm-2.3.1.tar.gz
#Run the app
CMD ["python3", "app.py"]
