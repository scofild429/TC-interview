
docker ps -aq | xargs docker stop
docker ps -aq | xargs docker rm
sudo docker image ls -q | xargs docker rmi
docker build -t streamlit-interview .
docker run -p 8501:8501 streamlit-interview:latest
