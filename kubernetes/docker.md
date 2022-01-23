to put your docker image in hub.docker.com
1. docker image build -t todoapp:v1.0
2. docker login --username=yourUserName  
3. docker tag todoapp:v1.0 yourUserName/todoapp:v1.0
4. docker push yourUsername/todoapp:v1.0