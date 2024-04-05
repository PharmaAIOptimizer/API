# PAPO API

How to run the API locally:
1. Clone repo
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

## API Calls

    API PUBLIC IP:  100.26.146.163

### Hello World
```bash
curl -X GET "http://127.0.0.1:8000/"
```

### User
#### Create User
```bash
curl -X POST "http://127.0.0.1:8000/user" -H "Content-Type: application/json" -d "{\"username\":\"person\", \"password\":\"password\", \"email\":\"email@mail.com\"}"
```

#### Get User by ID
```bash
curl -X GET "http://127.0.0.1:8000/user?id=1"
````

#### Get User by Username
```bash
curl -X GET "http://127.0.0.1:8000/user?username=person"
```

#### Delete User
```bash
curl -X POST "http://127.0.0.1:8000/delete_user?id=4"
```

# Deploying to AWS EC2

Log into your AWS account and create an EC2 instance (`t2.micro`), using the latest stable
Ubuntu Linux AMI.

[SSH into the instance](https://aws.amazon.com/blogs/compute/new-using-amazon-ec2-instance-connect-for-ssh-access-to-your-ec2-instances/) and run these commands to update the software repository and install
our dependencies.

```bash
sudo apt-get update
sudo apt install -y python3-pip nginx
```

Clone the FastAPI server app (or create your `main.py` in Python).

```bash
git clone https://github.com/pixegami/fastapi-tutorial.git
```

Add the FastAPI configuration to NGINX's folder. Create a file called `fastapi_nginx` (like the one in this repository).

```bash
sudo vim /etc/nginx/sites-enabled/fastapi_nginx
```

And put this config into the file (replace the IP address with your EC2 instance's public IP):

```
server {
    listen 80;   
    server_name <YOUR_EC2_IP>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```


Start NGINX.

```bash
sudo service nginx restart
```

Start FastAPI.

```bash
cd fastapi-tutorial
python3 -m uvicorn main:app
```

Update EC2 security-group settings for your instance to allow HTTP traffic to port 80.

Now when you visit your public IP of the instance, you should be able to access your API.
