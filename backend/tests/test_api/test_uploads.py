"""
Tests for image upload endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import io
from PIL import Image

from app.main import app
from app.services.cloudinary_service import cloudinary_service


client = TestClient(app)


@pytest.fixture
def mock_image_file():
    """Create a mock image file for testing"""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


@pytest.fixture
def auth_headers():
    """Mock authentication headers"""
    return {"Authorization": "Bearer test-token"}


class TestUploadEndpoints:
    """Test image upload endpoints"""
    
    def test_get_upload_limits(self):
        """Test getting upload limits endpoint"""
        response = client.get("/api/v1/uploads/limits")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "max_file_size_mb" in data["data"]
        assert "allowed_formats" in data["data"]
        assert data["data"]["max_file_size_mb"] == 10
    
    @patch('app.auth.dependencies.get_current_user')
    @patch.object(cloudinary_service, 'upload_image')
    @patch.object(cloudinary_service, 'get_responsive_urls')
    @patch.object(cloudinary_service, 'validate_image_file')
    def test_upload_avatar_success(
        self, 
        mock_validate, 
        mock_responsive_urls, 
        mock_upload, 
        mock_get_user,
        mock_image_file
    ):
        """Test successful avatar upload"""
        # Mock user
        mock_user = MagicMock()
        mock_user.id = "test-user-id"
        mock_get_user.return_value = mock_user
        
        # Mock Cloudinary responses
        mock_upload.return_value = {
            "public_id": "lemonnpie/avatars/user_test-user-id",
            "url": "https://res.cloudinary.com/test/image/upload/test.jpg",
            "width": 400,
            "height": 400,
            "format": "jpg",
            "bytes": 12345
        }
        
        mock_responsive_urls.return_value = {
            "thumbnail": "https://res.cloudinary.com/test/image/upload/c_thumb,w_150,h_150/test.jpg",
            "small": "https://res.cloudinary.com/test/image/upload/c_fill,w_300,h_225/test.jpg",
            "medium": "https://res.cloudinary.com/test/image/upload/c_fill,w_600,h_450/test.jpg",
            "large": "https://res.cloudinary.com/test/image/upload/c_fill,w_1200,h_900/test.jpg",
            "original": "https://res.cloudinary.com/test/image/upload/test.jpg"
        }
        
        # Test upload
        response = client.post(
            "/api/v1/uploads/avatar",
            files={"file": ("test.jpg", mock_image_file, "image/jpeg")},
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Avatar uploaded successfully"
        assert "public_id" in data["data"]
        assert "url" in data["data"]
        assert "responsive_urls" in data["data"]
        
        # Verify mocks were called
        mock_validate.assert_called_once()
        mock_upload.assert_called_once()
        mock_responsive_urls.assert_called_once()
    
    @patch('app.auth.dependencies.get_current_user')
    def test_upload_avatar_invalid_file_type(self, mock_get_user):
        """Test avatar upload with invalid file type"""
        mock_user = MagicMock()
        mock_user.id = "test-user-id"
        mock_get_user.return_value = mock_user
        
        # Create a text file instead of image
        text_file = io.BytesIO(b"This is not an image")
        
        response = client.post(
            "/api/v1/uploads/avatar",
            files={"file": ("test.txt", text_file, "text/plain")},
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 400
    
    @patch('app.auth.dependencies.require_admin')
    @patch.object(cloudinary_service, 'upload_image')
    @patch.object(cloudinary_service, 'get_responsive_urls')
    @patch.object(cloudinary_service, 'validate_image_file')
    def test_upload_movie_poster_success(
        self, 
        mock_validate, 
        mock_responsive_urls, 
        mock_upload, 
        mock_require_admin,
        mock_image_file
    ):
        """Test successful movie poster upload by admin"""
        # Mock admin user
        mock_admin = MagicMock()
        mock_admin.id = "admin-user-id"
        mock_admin.role = "admin"
        mock_require_admin.return_value = mock_admin
        
        # Mock Cloudinary responses
        mock_upload.return_value = {
            "public_id": "lemonnpie/posters/movie_test-movie-id",
            "url": "https://res.cloudinary.com/test/image/upload/poster.jpg",
            "width": 800,
            "height": 1200,
            "format": "jpg",
            "bytes": 54321
        }
        
        mock_responsive_urls.return_value = {
            "thumbnail": "https://res.cloudinary.com/test/image/upload/c_thumb,w_150,h_150/poster.jpg",
            "small": "https://res.cloudinary.com/test/image/upload/c_fill,w_300,h_225/poster.jpg",
            "medium": "https://res.cloudinary.com/test/image/upload/c_fill,w_600,h_450/poster.jpg",
            "large": "https://res.cloudinary.com/test/image/upload/c_fill,w_1200,h_900/poster.jpg",
            "original": "https://res.cloudinary.com/test/image/upload/poster.jpg"
        }
        
        # Test upload
        response = client.post(
            "/api/v1/uploads/movie-poster",
            files={"file": ("poster.jpg", mock_image_file, "image/jpeg")},
            data={"movie_id": "test-movie-id"},
            headers={"Authorization": "Bearer admin-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Movie poster uploaded successfully"
        assert "movie_id" in data["data"]
        
        # Verify mocks were called
        mock_validate.assert_called_once()
        mock_upload.assert_called_once()
        mock_responsive_urls.assert_called_once()
    
    def test_get_image_urls_responsive(self):
        """Test getting responsive image URLs"""
        with patch.object(cloudinary_service, 'get_responsive_urls') as mock_responsive:
            mock_responsive.return_value = {
                "thumbnail": "https://res.cloudinary.com/test/image/upload/c_thumb,w_150,h_150/test.jpg",
                "small": "https://res.cloudinary.com/test/image/upload/c_fill,w_300,h_225/test.jpg",
                "medium": "https://res.cloudinary.com/test/image/upload/c_fill,w_600,h_450/test.jpg",
                "large": "https://res.cloudinary.com/test/image/upload/c_fill,w_1200,h_900/test.jpg",
                "original": "https://res.cloudinary.com/test/image/upload/test.jpg"
            }
            
            response = client.get("/api/v1/uploads/image/test-public-id/urls")
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "responsive_urls" in data["data"]
            mock_responsive.assert_called_once_with("test-public-id")
    
    def test_get_image_urls_custom_dimensions(self):
        """Test getting image URLs with custom dimensions"""
        with patch.object(cloudinary_service, 'get_optimized_url') as mock_optimized:
            mock_optimized.return_value = "https://res.cloudinary.com/test/image/upload/c_fill,w_500,h_300/test.jpg"
            
            response = client.get(
                "/api/v1/uploads/image/test-public-id/urls",
                params={"width": 500, "height": 300, "crop": "fill"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "optimized_url" in data["data"]
            assert "parameters" in data["data"]
            
            mock_optimized.assert_called_once_with(
                public_id="test-public-id",
                width=500,
                height=300,
                crop="fill",
                quality="auto:good",
                format="auto"
            )