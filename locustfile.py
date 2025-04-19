from locust import HttpUser, task, between, tag
import random

class ApiPerformanceTest(HttpUser):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = {
            'user_id': random.randint(1, 10),
            'post_id': random.randint(1, 100),
            'album_id': random.randint(1, 100),
            'todo_id': random.randint(1, 200)
        }

    def on_start(self):
        print("Load test started")
        
    def on_stop(self):
        print("Load test completed")

    @tag('posts', 'get')
    @task
    def fetch_posts(self):
        with self.client.get("/posts/", name="Get all posts", catch_response=True) as response:
            self._validate_response(response, expected_fields=[], is_list=True)

    @tag('posts', 'get')
    @task
    def fetch_single_post(self):
        with self.client.get(f"/posts/{self.test_data['post_id']}", name="Get single post", catch_response=True) as response:
            self._validate_response(response, expected_fields=['id', 'title'])

    @tag('posts', 'post')
    @task(3)
    def add_new_post(self):
        payload = {
            "userId": self.test_data['user_id'],
            "title": f"New post {random.randint(1, 100)}",
            "body": f"Post content {random.randint(1, 100)}"
        }
        with self.client.post("/posts/", json=payload, name="Create post", catch_response=True) as response:
            self._validate_response(response, expected_fields=['id'], status_code=201)

    @tag('posts', 'put')
    @task(2)
    def modify_post(self):
        payload = {
            "id": self.test_data['post_id'],
            "title": f"Updated post {random.randint(1, 100)}",
            "body": "Updated content",
            "userId": self.test_data['user_id']
        }
        with self.client.put(f"/posts/{self.test_data['post_id']}", json=payload, name="Update post", catch_response=True) as response:
            self._validate_response(response)

    @tag('posts', 'delete')
    @task(1)
    def remove_post(self):
        with self.client.delete(f"/posts/{self.test_data['post_id']}", name="Delete post", catch_response=True) as response:
            self._validate_response(response)

    @tag('comments', 'get')
    @task(2)
    def fetch_post_comments(self):
        with self.client.get(f"/posts/{self.test_data['post_id']}/comments", name="Get post comments", catch_response=True) as response:
            self._validate_response(response, is_list=True)

    @tag('users', 'get')
    @task(1)
    def fetch_user(self):
        with self.client.get(f"/users/{self.test_data['user_id']}", name="Get user", catch_response=True) as response:
            self._validate_response(response, expected_fields=['name', 'email'])

    @tag('todos', 'get')
    @task(1)
    def fetch_user_todos(self):
        with self.client.get(f"/users/{self.test_data['user_id']}/todos", name="Get user todos", catch_response=True) as response:
            self._validate_response(response, is_list=True)

    @tag('albums', 'get')
    @task(1)
    def fetch_albums(self):
        with self.client.get("/albums", name="Get albums", catch_response=True) as response:
            self._validate_response(response, is_list=True, min_length=1)

    @tag('photos', 'get')
    @task(1)
    def fetch_album_photos(self):
        with self.client.get(f"/albums/{self.test_data['album_id']}/photos", name="Get album photos", catch_response=True) as response:
            self._validate_response(response, is_list=True, check_items=['albumId', 'url'])

    @tag('todos', 'post')
    @task(1)
    def create_todo(self):
        payload = {
            "userId": self.test_data['user_id'],
            "title": f"Todo {random.randint(1, 100)}",
            "completed": random.choice([True, False])
        }
        with self.client.post("/todos", json=payload, name="Create todo", catch_response=True) as response:
            self._validate_response(response, expected_fields=['id'], status_code=201)

    @tag('todos', 'put')
    @task(1)
    def update_todo(self):
        payload = {
            "userId": self.test_data['user_id'],
            "id": self.test_data['todo_id'],
            "title": f"Updated todo {random.randint(1, 100)}",
            "completed": True
        }
        with self.client.put(f"/todos/{self.test_data['todo_id']}", json=payload, name="Update todo", catch_response=True) as response:
            self._validate_response(response)

    def _validate_response(self, response, expected_fields=None, status_code=200, is_list=False, min_length=0, check_items=None):
        if expected_fields is None:
            expected_fields = []
            
        if response.status_code != status_code:
            response.failure(f"Unexpected status: {response.status_code} (expected {status_code})")
            return

        try:
            json_data = response.json()
        except ValueError:
            response.failure("Invalid JSON response")
            return

        if is_list:
            if not isinstance(json_data, list):
                response.failure("Expected list in response")
                return
            if len(json_data) < min_length:
                response.failure(f"List too small: {len(json_data)} items (expected {min_length})")
                return
            if check_items and json_data:
                for item in json_data[:5]:
                    if not all(key in item for key in check_items):
                        response.failure(f"Missing required fields: {check_items}")
                        return
        else:
            if expected_fields and not all(field in json_data for field in expected_fields):
                response.failure(f"Missing required fields: {expected_fields}")
                return

        response.success()