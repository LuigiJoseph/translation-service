FROM python:3.12



WORKDIR /model-api


# installing dep
RUN pip install flask flask-restx torch transformers SentencePiece


COPY . . 


# exposing port 
EXPOSE 5000

CMD [ "python", "model-api.py"]

#Ins for building and running docker images 

# 1- in terminal run this command to build image---> docker build -t translation-service .

# 2- run this to start the flask app ---> docker run --rm -d -p 5000:5000 translation-service:latest

# 3- go to link http://localhost:5000 NOTE-: make sure there are no other severs running on this port

#you can build images and run container via search above with commands >docker build , >docker run