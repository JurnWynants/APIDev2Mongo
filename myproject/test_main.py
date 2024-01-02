import requests
import json




def test_create_user_endpoint():
    user_data = {
        "email": "test@test.be",
        "password": "testpassword",
    }


    response = requests.post('http://127.0.0.1:8000/users/', json=user_data)


    assert response.status_code == 200


    created_user = response.json()
    assert created_user['email'] == user_data['email']
    assert 'id' in created_user


headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

request_data = {
    "grant_type": "",
    "username": "test@test.be",
    "password": "testpassword",
    "scope": "",
    "client_id": "",
    "client_secret": ""
}

token_request = requests.post("http://localhost:8000/token", data=request_data, headers=headers)

# Extract the access token from the response
response_data = token_request.json()
access_token = response_data.get("access_token", "")

# Include the access token in the headers for subsequent requests
headers_with_token = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}


def test_read_users_endpoint():
    response = requests.get('http://127.0.0.1:8000/users/')
    assert response.status_code == 200

    users_list = response.json()
    assert isinstance(users_list, list)


    for user in users_list:
        assert "id" in user
        assert "email" in user
        assert "books" in user
        assert "is_active" in user

def test_read_user_endpoint():

    user_id = 1
    response = requests.get(f'http://127.0.0.1:8000/users/{user_id}')

    assert response.status_code == 200

    user = response.json()

    assert user['id'] == user_id
    assert 'email' in user
    assert 'books' in user
    assert "is_active" in user

def test_create_book_for_user_endpoint():

    book_data = {
        "title": "Sample Book",
        "description": "Sample Description",
        "releaseyear": 0

    }

    user_id = 1

    response = requests.post(
        f'http://127.0.0.1:8000/users/{user_id}/books/',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(book_data)
    )

    assert response.status_code == 200


    created_book = response.json()


    assert created_book['title'] == book_data['title']
    assert created_book['description'] == book_data['description']
    assert created_book['releaseyear'] == book_data['releaseyear']



    assert 'id' in created_book
    assert 'owner_id' in created_book and created_book['owner_id'] == user_id



def test_read_books_endpoint():

    response = requests.get(
        'http://127.0.0.1:8000/books/',
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 200
    books_list = response.json()
    assert isinstance(books_list, list)

    for book in books_list:
        assert 'title' in book
        assert 'releaseyear' in book
        assert 'description' in book

def test_delete_book_endpoint():
    book_id = 1

    delete_book_response = requests.delete(f"http://localhost:8000/books/{1}", headers=headers_with_token)
    assert delete_book_response.status_code == 200
    books_list = delete_book_response.json()


def test_delete_user_endpoint():

    user_id= 1

    response = requests.delete(
        f'http://127.0.0.1:8000/users/{user_id}',
        headers=headers_with_token
    )

    assert response.status_code == 200
    deleted_user = response.json()

    assert 'id' in deleted_user
    assert 'email' in deleted_user
    assert 'books' in deleted_user
    assert 'is_active' in deleted_user

