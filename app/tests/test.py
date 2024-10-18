import unittest
from random import randint
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.utils import constant
from app.utils.date_parse_utils import DateParseUtils
from main import app
import jwt

# Constants for your tests
SECRET_KEY = constant.secrets_key


class TestAdminAPIs(unittest.TestCase):

    def setUp(self):
        """Set up the TestClient and mock dependencies."""
        self.client = TestClient(app)
        self.admin_service_mock = patch('app.service.admin.admin_service').start()
        self.addCleanup(patch.stopall)

    def test_admin_register_success(self):
        """Test successful admin registration."""
        self.admin_service_mock.admin_register.return_value = {"success": True}
        num= randint(50,100)
        response = self.client.post("/admin/register", json={
          "firstname": "admin",
          "lastname": "admin lm",
          "email": f"admintest{num}@gmail.com",
          "password": "password",
          "is_deleted": False,
          "created_on": DateParseUtils.get_current_epoch(),
          "modified_on": DateParseUtils.get_current_epoch()
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response.json())

    def test_admin_register_missing_fields(self):
        """Test admin registration with missing fields."""
        response = self.client.post("/admin/register", json={})

        self.assertEqual(response.status_code, 422)  # Validation error

    def test_admin_register_user_exists(self):
        """Test admin registration when user already exists."""
        self.admin_service_mock.admin_register.side_effect = Exception("User already exists")
        response = self.client.post("/admin/register", json={
            "firstname": "admin",
            "lastname": "admin lm",
            "email": f"admintest@gmail.com",
            "password": "password"
        })

        self.assertEqual(response.status_code, 400)  # Assuming 400 for bad request
        self.assertIn('User already exists', response.json()['message'])


#### Video Upload Tests

class TestVideoAPIs(unittest.TestCase):

    def setUp(self):
        """Set up the TestClient and mock dependencies."""
        self.client = TestClient(app)
        self.video_service_mock = patch('app.service.video_ops.video_service.VideoService').start()
        self.addCleanup(patch.stopall)

    def create_test_token(self, role):
        """Helper function to create a test JWT token with the specified role."""
        token_data = {
            "email": "admin@gmail.com",
            "role": role
        }
        return jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    @patch('app.dao.user.user_dao.UserDAO.get_user_by_email_dao')
    def test_upload_video_success(self, mock_get_user_by_email_dao):
        """Test successful video upload for admin user."""
        # Mock user retrieval
        mock_get_user_by_email_dao.return_value = {"email": "test@example.com",
                                                   "role": "admin"}

        # Create a token for an admin user
        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}

        self.video_service_mock().upload_and_convert.return_value = {
            "video_id": 1}

        with open(
                '/home/dev1050/khushboo/Research/MI_task/videos/analysisplan-testing.mp4',
                'rb') as file:
            response = self.client.post("/video/upload", headers=headers,
                                        files={"file": file})

        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        self.assertIn('video_id', response.json()['data'])

    def test_upload_video_not_authenticated(self):
        """Test video upload without authentication."""
        headers = {"Authorization": ""}
        with open(
                '/home/dev1050/khushboo/Research/MI_task/videos/analysisplan-testing.mp4',
                'rb') as file:
            response = self.client.post("/video/upload", headers=headers,
                                        files={"file": file})
        self.assertEqual(response.status_code, 401)  # Assuming unauthorized


#### Video Download Tests

    def test_download_video_not_found(self):
        """Test video download when video is not found."""
        self.video_service_mock().get_video_path_by_id.return_value = None
        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}
        response = self.client.get("/video/download/99",headers=headers)

        self.assertEqual(response.status_code, 404) # Video not found

    def test_download_video_blocked(self):
        """Test successful video block."""

        # Create a token for an admin user
        token = self.create_test_token(
            role="admin")  # Ensure the role is admin
        headers = {"Authorization": token}

        # Call the download endpoint
        response = self.client.get("/video/download/1", headers=headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 403)


    @patch('app.utils.authentication_check.login_required')
    def test_download_video_unauthorized(self, mock_login_required):
        """Test unauthorized video download."""
        mock_login_required.return_value = None  # Allow access as a regular user

        # Mock the service but not provide the necessary permissions
        self.video_service_mock().get_video_path_by_id.return_value = '/home/dev1050/khushboo/Research/MI_task/videos/analysisplan-testing.mp4'

        # Create a token for a non-admin user
        token = self.create_test_token(
            role="user")  # Ensure the role is "user"
        headers = {"Authorization": token}

        # Make the request to download the video
        response = self.client.get("/video/download/1", headers=headers)

        # Assert that the response is unauthorized
        self.assertEqual(response.status_code, 401)

    @patch('app.utils.authentication_check.login_required')
    def test_search_video_success(self, mock_login_required):
        """Test successful video search."""
        mock_login_required.return_value = None

        # Simulate videos found
        self.video_service_mock.search_videos_by_metadata.return_value = [
            {"id": 1, "file_name": "analysis"}
        ]

        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}

        response = self.client.get("video/search/?search_keyword=1",
                                   headers=headers)

        # Expect a 200 OK since the video matches the search
        self.assertEqual(response.status_code, 200)

    @patch('app.utils.authentication_check.login_required')
    def test_search_video_not_found(self, mock_login_required):
        """Test video search when no results are found."""
        mock_login_required.return_value = None

        # Simulate no videos found
        self.video_service_mock.search_videos_by_metadata.return_value = []

        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}

        response = self.client.get("video/search/?search_keyword=Nonexistent",
                                   headers=headers)

        # Expect a 404 Not Found since no videos match the search
        self.assertEqual(response.status_code, 404)


    @patch('app.utils.authentication_check.login_required')
    def test_block_video_success(self, mock_login_required):
        """Test successful video blocking."""
        mock_login_required.return_value = None

        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}
        video_id = 10
        self.video_service_mock.block_video.return_value = True

        response = self.client.post(f"video/block/{video_id}",headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['data']['video_id'], video_id)

    @patch('app.utils.authentication_check.login_required')
    def test_block_video_not_found(self, mock_login_required):
        """Test blocking a video that does not exist."""
        mock_login_required.return_value = None

        video_id = 999
        self.video_service_mock.block_video.return_value = False
        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}
        response = self.client.post(f"video/block/{video_id}", headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json()['success'])
        self.assertIn('Video Not Found!', response.json()['message'])

    @patch('app.utils.authentication_check.login_required')
    def test_unblock_video_success(self, mock_login_required):
        """Test successful video unblocking."""
        mock_login_required.return_value = None
        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}
        video_id = 1
        self.video_service_mock.unblock_video.return_value = True

        response = self.client.post(f"/video/unblock/{video_id}", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['data']['video_id'], video_id)

    @patch('app.utils.authentication_check.login_required')
    def test_unblock_video_not_found(self, mock_login_required):
        """Test unblocking a video that does not exist."""
        mock_login_required.return_value = None

        token = self.create_test_token(role="admin")
        headers = {"Authorization": token}
        video_id = 999
        self.video_service_mock.unblock_video.return_value = False

        response = self.client.post(f"video/unblock/{video_id}",headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json()['success'])
        self.assertIn('Video Not Found!', response.json()['message'])

#### User Registration Tests
class TestUserAPIs(unittest.TestCase):

    def setUp(self):
        """Set up the TestClient and mock dependencies."""
        self.client = TestClient(app)
        self.user_service_mock = patch(
            'app.service.user.user_service').start()
        self.addCleanup(patch.stopall)

    def test_user_register_success(self):
        """Test successful user registration."""
        self.user_service_mock.user_register.return_value = {"success": True}
        num= randint(50,100)
        response = self.client.post("/user/register", json={
            "firstname": "user",
            "lastname": "test",
            "email": f"usertest{num}@gmail.com",
            "password": "password",
            "is_deleted":False,
            "created_on":DateParseUtils.get_current_epoch(),
            "modified_on":DateParseUtils.get_current_epoch()
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response.json())

    def test_user_register_missing_fields(self):
        """Test user registration with missing fields."""
        response = self.client.post("/user/register", json={})

        self.assertEqual(response.status_code, 422)  # Validation error

    def test_user_register_user_exists(self):
        """Test user registration when user already exists."""
        self.user_service_mock.user_register.side_effect = Exception("User already exists")

        response = self.client.post("/user/register", json={
            "firstname": "user",
            "lastname": "test",
            "email": "usertest@gmail.com",
            "password": "password"
        })

        self.assertEqual(response.status_code, 400)  # Assuming 400 for bad request
        self.assertIn('User already exists', response.json()['message'])

if __name__ == '__main__':
    unittest.main()
