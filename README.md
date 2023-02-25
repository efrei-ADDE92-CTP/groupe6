# groupe6
By conserving wildlife, we're ensuring that future generations can enjoy our natural world.

![image](https://user-images.githubusercontent.com/57401552/210325880-fd86a618-3812-471a-82f3-6dd79716f01c.png)

---
### Preliminary preparation

````bash
WSL2 :
toto@DESKTOP-OBTCMJQ:/mnt/c/Windows/system32$

$ cd ../..
toto@DESKTOP-OBTCMJQ:/mnt/c$

$ cd Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet
toto@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet$

$ source MYVENV/bin/activate
(MYVENV) toto@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/M2/APPLICATIONS_OF_BIG_DATA_2/projet$
````

---
### *Python* dependencies to install

````python
$ pip install matplotlib==3.5.3
$ pip install numpy==1.21.6
$ pip install pandas==1.3.5         ou sudo apt-get install python3-pandas
$ pip install scikit-learn==1.0.2
$ pip install starlette             for the web parts
$ pip install pydantic              for the data parts
$ pip install fastapi
$ pip install "uvicorn[standard]"   ASGI server for production
$ pip install -r requirements.txt
$ pip install scipy==1.7.3
$ pip install contourpy==1.0.6
$ pip install prometheus_client
$ pip install starlette
$ pip install starlette-exporter
$ pip install wheel
$ pip install hey                    ou sudo apt install hey
$ pip freeze > requirements.txt
````

---
### Create a *main.py* file
* See the *main.py* file on the repository.

---
### Configuration of a *Dockerfile*

````docker
FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /projet
WORKDIR /projet

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# CMD ["bash", "-c", "uvicorn main:api_router --host 0.0.0.0 --port 5000"] on Windows
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "main:api_router"]
````

---
### Docker commands to build and run the project and to test the program

````bash
$ docker build --tag files . # Build the image


$ docker run -p 8080:5000 -it --rm files # run the image
Or
$ docker run -it --network host --rm files # all ports mapped by the container are locally mapped

# In another CLI terminal :
$ curl --request POST --url 'http://localhost:8080/predict' --header 'content-type: application/json' --data '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
Or
$ curl 'http://localhost:8080/predict' -H 'content-type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
````

---
### Publish an image on the DockerHub

````bash
$ docker login --username=antoinearthur
Password : *******
Login Succeeded

$ docker images
REPOSITORY                                  TAG       IMAGE ID       CREATED        SIZE
files                                       latest    2161bac8e4e0   40 hours ago   1.04GB

$ docker tag 2161bac8e4e0 antoinearthur/app_big_data_docker_project
$ docker images
REPOSITORY                                  TAG       IMAGE ID       CREATED        SIZE
antoinearthur/app_big_data_docker_project   latest    2161bac8e4e0   40 hours ago   1.04GB
files                                       latest    2161bac8e4e0   40 hours ago   1.04GB

$ docker push antoinearthur/app_big_data_docker_project
````

* Our image, tagged with *app_big_data_docker_project*, is uploaded on the DockerHub, at the following address : https://hub.docker.com/r/antoinearthur/app_big_data_docker_project


---
### Run the image and test the program yet again

````bash
$ docker run -p 8080:5000 -it --rm antoinearthur/app_big_data_docker_project

# In another CLI terminal :
$ curl 'http://localhost:8080/predict' -H 'content-type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
````

---
### Testing the application's scalability

````python
$ pip install wheel
$ pip install hey                    ou sudo apt install hey
$ pip freeze > requirements.txt
````

* We chose the *`hey`* library, easy to implement, and sufficient for our use case (only one docker image to test).
* See the *test_charge.py* file on the repository.

````bash
$ docker run -p 8080:5000 -it --rm files
Or
$ docker run -p 8080:5000 -it --rm antoinearthur/app_big_data_docker_project
````

````python
# In another CLI terminal :
$ python test_charge.py
````

* On the first CLI terminal :
````bash
INFO:     172.17.0.1:36380 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     172.17.0.1:36234 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     172.17.0.1:36384 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     172.17.0.1:35866 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
````

* On the second CLI terminal :
````bash
Summary:
  Total:        7.2684 secs
  Slowest:      0.1666 secs
  Fastest:      0.0014 secs
  Average:      0.0718 secs
  Requests/sec: 1375.8257

  Total data:   810000 bytes
  Size/request: 81 bytes

Response time histogram:
  0.001 [1]     |
  0.018 [32]    |
  0.034 [214]   |■■
  0.051 [376]   |■■■■
  0.067 [4101]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.084 [3552]  |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.101 [743]   |■■■■■■■
  0.117 [659]   |■■■■■■
  0.134 [123]   |■
  0.150 [99]    |■
  0.167 [100]   |■


Latency distribution:
  10% in 0.0587 secs
  25% in 0.0611 secs
  50% in 0.0682 secs
  75% in 0.0775 secs
  90% in 0.0990 secs
  95% in 0.1085 secs
  99% in 0.1542 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0005 secs, 0.0014 secs, 0.1666 secs
  DNS-lookup:   0.0002 secs, 0.0000 secs, 0.0530 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0045 secs
  resp wait:    0.0711 secs, 0.0013 secs, 0.1387 secs
  resp read:    0.0001 secs, 0.0000 secs, 0.0057 secs

Status code distribution:
  [422] 10000 responses
````

* Interpretation of the results : ***complete***

---
### Get the Endpoint API of your Azure Container App
***complete***
