"""
Cloudinary service for image upload and management
"""
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from typing import Dict, Optional, Any
import logging
from app.core.config import settings
from app.core.exceptions import LemonPieException

logger = logging.getLogger(__name__)


class CloudinaryService:
    """Service for handling image uploads and management with Cloudinary"""
    
    def __init__(self):
        """Initialize Cloudinary configuration"""
        self._configured = False
        
        if all([
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET
        ]):
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True
            )
            self._configured = True
            logger.info("Cloudinary service initialized successfully")
        else:
            logger.warning(
                "Cloudinary configuration is incomplete. Image upload functionality will be disabled. "
                "Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET "
                "environment variables to enable image uploads."
            )
    
    def _check_configuration(self):
        """Check if Cloudinary is properly configured"""
        if not self._configured:
            raise LemonPieException(
                "Cloudinary is not configured. Please set CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET environment variables.",
                status_code=503
            )
    
    async def upload_image(
        self, 
        file_data: bytes, 
        folder: str = "lemonnpie",
        public_id: Optional[str] = None,
        transformation: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload image to Cloudinary with automatic optimization
        
        Args:
            file_data: Image file data as bytes
            folder: Cloudinary folder to store the image
            public_id: Optional custom public ID for the image
            transformation: Optional transformation parameters
            
        Returns:
            Dictionary containing upload result with URLs and metadata
            
        Raises:
            LemonPieException: If upload fails
        """
        self._check_configuration()
        
        try:
            upload_options = {
                "folder": folder,
                "resource_type": "image",
                "format": "webp",  # Convert to WebP for better compression
                "quality": "auto:good",  # Automatic quality optimization
                "fetch_format": "auto",  # Automatic format selection
                "overwrite": True,  # Allow overwriting existing images
                "invalidate": True,  # Invalidate CDN cache
            }
            
            if public_id:
                upload_options["public_id"] = public_id
            
            if transformation:
                upload_options["transformation"] = transformation
            
            logger.info(f"Uploading image to folder: {folder}")
            result = cloudinary.uploader.upload(file_data, **upload_options)
            
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "width": result["width"],
                "height": result["height"],
                "format": result["format"],
                "bytes": result["bytes"],
                "created_at": result["created_at"]
            }
            
        except Exception as e:
            logger.error(f"Failed to upload image to Cloudinary: {str(e)}")
            raise LemonPieException(
                f"Image upload failed: {str(e)}",
                status_code=500
            )
    
    def get_optimized_url(
        self, 
        public_id: str, 
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: str = "fill",
        quality: str = "auto:good",
        format: str = "auto"
    ) -> str:
        """
        Generate optimized image URL with transformations
        
        Args:
            public_id: Cloudinary public ID of the image
            width: Target width in pixels
            height: Target height in pixels
            crop: Crop mode (fill, fit, scale, etc.)
            quality: Image quality setting
            format: Image format (auto, webp, jpg, png)
            
        Returns:
            Optimized image URL
        """
        try:
            transformation = {
                "quality": quality,
                "fetch_format": format
            }
            
            if width:
                transformation["width"] = width
            if height:
                transformation["height"] = height
            if width or height:
                transformation["crop"] = crop
            
            url, _ = cloudinary_url(public_id, **transformation)
            return url
            
        except Exception as e:
            logger.error(f"Failed to generate optimized URL: {str(e)}")
            # Return original URL as fallback
            url, _ = cloudinary_url(public_id)
            return url
    
    def get_responsive_urls(self, public_id: str) -> Dict[str, str]:
        """
        Generate multiple responsive image URLs for different screen sizes
        
        Args:
            public_id: Cloudinary public ID of the image
            
        Returns:
            Dictionary with different sized URLs
        """
        return {
            "thumbnail": self.get_optimized_url(
                public_id, width=150, height=150, crop="thumb"
            ),
            "small": self.get_optimized_url(
                public_id, width=300, height=225, crop="fill"
            ),
            "medium": self.get_optimized_url(
                public_id, width=600, height=450, crop="fill"
            ),
            "large": self.get_optimized_url(
                public_id, width=1200, height=900, crop="fill"
            ),
            "original": self.get_optimized_url(public_id)
        }
    
    async def delete_image(self, public_id: str) -> bool:
        """
        Delete image from Cloudinary
        
        Args:
            public_id: Cloudinary public ID of the image to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        self._check_configuration()
        
        try:
            logger.info(f"Deleting image with public_id: {public_id}")
            result = cloudinary.uploader.destroy(public_id)
            success = result.get("result") == "ok"
            
            if success:
                logger.info(f"Successfully deleted image: {public_id}")
            else:
                logger.warning(f"Failed to delete image: {public_id}, result: {result}")
                
            return success
            
        except Exception as e:
            logger.error(f"Error deleting image {public_id}: {str(e)}")
            return False
    
    def validate_image_file(self, content_type: str, file_size: int) -> None:
        """
        Validate image file type and size
        
        Args:
            content_type: MIME type of the file
            file_size: Size of the file in bytes
            
        Raises:
            LemonPieException: If validation fails
        """
        # Check file type
        allowed_types = [
            "image/jpeg", "image/jpg", "image/png", 
            "image/webp", "image/gif", "image/bmp"
        ]
        
        if content_type not in allowed_types:
            raise LemonPieException(
                f"Invalid file type. Allowed types: {', '.join(allowed_types)}",
                status_code=400
            )
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB in bytes
        if file_size > max_size:
            raise LemonPieException(
                f"File size too large. Maximum allowed size is {max_size // (1024 * 1024)}MB",
                status_code=400
            )
    
    def extract_public_id_from_url(self, url: str) -> Optional[str]:
        """
        Extract public ID from Cloudinary URL
        
        Args:
            url: Cloudinary image URL
            
        Returns:
            Public ID if found, None otherwise
        """
        try:
            # Cloudinary URLs typically have format:
            # https://res.cloudinary.com/{cloud_name}/image/upload/{transformations}/{public_id}.{format}
            if "cloudinary.com" not in url:
                return None
            
            # Split by '/' and find the part after 'upload'
            parts = url.split('/')
            upload_index = -1
            
            for i, part in enumerate(parts):
                if part == "upload":
                    upload_index = i
                    break
            
            if upload_index == -1 or upload_index + 1 >= len(parts):
                return None
            
            # The public ID might have transformations before it
            # Look for the last part that doesn't contain transformation parameters
            for i in range(upload_index + 1, len(parts)):
                part = parts[i]
                # Skip transformation parameters (they contain underscores and specific patterns)
                if not any(char in part for char in ['c_', 'w_', 'h_', 'q_', 'f_']):
                    # Remove file extension
                    public_id = part.split('.')[0]
                    # Reconstruct full path from folder structure
                    folder_parts = parts[upload_index + 1:i]
                    if folder_parts:
                        return '/'.join(folder_parts + [public_id])
                    return public_id
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract public ID from URL {url}: {str(e)}")
            return None


# Global instance
cloudinary_service = CloudinaryService()