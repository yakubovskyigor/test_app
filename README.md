# TEST_APP
___

It is the wep application, that implement RESTful API endpoints for user registration, login, fetching user profile, updating user profile, and deleting the account.

## Installation

You can install this app on your working machine from source code:
```bash
# Step -- 1.
git clone --depth=1 --branch=main 'https://github.com/yakubovskyigor/test_app.git'

# Step -- 2.
cd ./test_app/

# Step -- 3.
pip install -r requirements.txt
```

## Usage

To test these API routes, you can use API tools such as curl, Postman, or Insomnia.

Sample requests for testing:

- User Registration:
```bash
curl -X POST -H "Content-Type: test_app/json" -d '{
    "username": "example_user",
    "email": "user@example.com",
    "password": "password123"
}' http://127.0.0.1:5000/registration
```

- User login:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "email": "user@example.com",
    "password": "password123"
}' http://127.0.0.1:5000/login
```

- Authentication verification:
```bash
curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:5000/is_login
```

- Getting a user profile:
```bash
curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:5000/users
```

- Updating the user profile:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{
    "username": "new_username",
    "password": "new_password"
}' http://127.0.0.1:5000/update_user/<user_id>
```

- Deleting a user:
```bash
curl -X DELETE http://127.0.0.1:5000/delete_user/<user_id>
```


