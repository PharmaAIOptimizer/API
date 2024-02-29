# PAPO API

## API Calls
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