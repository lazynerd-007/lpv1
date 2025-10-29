"""
Image upload endpoints for LemonNPie Backend API
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging
from uuid import UUID

from app.auth.dependencies import get_current_user, require_admin
from app.models.user import User
from app.services.cloudinary_service import cloudinary_service
from app.core.exceptions import LemonPieException

logger = logging.getLogger(__name__)

router = APIRouter(tags=["uploads"])


@router.post("/avatar", response_model=Dict[str, Any])
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload user avatar image
    
    - **file**: Image file to upload (JPEG, PNG, WebP, GIF, BMP)
    - **Returns**: Upload result with URLs and metadata
    """
    try:
        # Validate file
        if not file.content_type:
            raise HTTPException(400, "File content type is required")
        
        file_data = await file.read()
        cloudinary_service.validate_image_file(file.content_type, len(file_data))
        
        # Upload to Cloudinary with user-specific folder and public ID
        folder = f"lemonnpie/avatars"
        public_id = f"user_{current_user.id}"
        
        # Apply avatar-specific transformations
        transformation = {
            "width": 400,
            "height": 400,
            "crop": "fill",
            "gravity": "face",  # Focus on face if detected
            "quality": "auto:good"
        }
        
        result = await cloudinary_service.upload_image(
            file_data=file_data,
            folder=folder,
            public_id=public_id,
            transformation=transformation
        )
        
        # Generate responsive URLs for different use cases
        responsive_urls = cloudinary_service.get_responsive_urls(result["public_id"])
        
        logger.info(f"Avatar uploaded successfully for user {current_user.id}")
        
        return {
            "success": True,
            "message": "Avatar uploaded successfully",
            "data": {
                "public_id": result["public_id"],
                "url": result["url"],
                "responsive_urls": responsive_urls,
                "metadata": {
                    "width": result["width"],
                    "height": result["height"],
                    "format": result["format"],
                    "size_bytes": result["bytes"]
                }
            }
        }
        
    except LemonPieException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error uploading avatar for user {current_user.id}: {str(e)}")
        raise HTTPException(500, "Internal server error during file upload")


@router.post("/movie-poster", response_model=Dict[str, Any])
async def upload_movie_poster(
    file: UploadFile = File(...),
    movie_id: UUID = Form(...),
    current_user: User = Depends(require_admin)
):
    """
    Upload movie poster image (Admin only)
    
    - **file**: Image file to upload (JPEG, PNG, WebP, GIF, BMP)
    - **movie_id**: ID of the movie this poster belongs to
    - **Returns**: Upload result with URLs and metadata
    """
    try:
        # Validate file
        if not file.content_type:
            raise HTTPException(400, "File content type is required")
        
        file_data = await file.read()
        cloudinary_service.validate_image_file(file.content_type, len(file_data))
        
        # Upload to Cloudinary with movie-specific folder and public ID
        folder = f"lemonnpie/posters"
        public_id = f"movie_{movie_id}"
        
        # Apply poster-specific transformations
        transformation = {
            "width": 800,
            "height": 1200,
            "crop": "fill",
            "quality": "auto:good"
        }
        
        result = await cloudinary_service.upload_image(
            file_data=file_data,
            folder=folder,
            public_id=public_id,
            transformation=transformation
        )
        
        # Generate responsive URLs for different use cases
        responsive_urls = cloudinary_service.get_responsive_urls(result["public_id"])
        
        logger.info(f"Movie poster uploaded successfully for movie {movie_id} by admin {current_user.id}")
        
        return {
            "success": True,
            "message": "Movie poster uploaded successfully",
            "data": {
                "public_id": result["public_id"],
                "url": result["url"],
                "movie_id": str(movie_id),
                "responsive_urls": responsive_urls,
                "metadata": {
                    "width": result["width"],
                    "height": result["height"],
                    "format": result["format"],
                    "size_bytes": result["bytes"]
                }
            }
        }
        
    except LemonPieException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error uploading movie poster for movie {movie_id}: {str(e)}")
        raise HTTPException(500, "Internal server error during file upload")


@router.delete("/image/{public_id:path}")
async def delete_image(
    public_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete an image from Cloudinary
    
    - **public_id**: Cloudinary public ID of the image to delete
    - **Returns**: Deletion result
    
    Note: Users can only delete their own avatars, admins can delete any image
    """
    try:
        # Check permissions
        is_admin = current_user.role in ["admin", "moderator"]
        is_user_avatar = public_id.startswith(f"lemonnpie/avatars/user_{current_user.id}")
        
        if not is_admin and not is_user_avatar:
            raise HTTPException(
                403, 
                "You can only delete your own avatar images"
            )
        
        # Delete from Cloudinary
        success = await cloudinary_service.delete_image(public_id)
        
        if success:
            logger.info(f"Image {public_id} deleted successfully by user {current_user.id}")
            return {
                "success": True,
                "message": "Image deleted successfully",
                "public_id": public_id
            }
        else:
            raise HTTPException(404, "Image not found or could not be deleted")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting image {public_id}: {str(e)}")
        raise HTTPException(500, "Internal server error during image deletion")


@router.get("/image/{public_id:path}/urls")
async def get_image_urls(
    public_id: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: str = "fill",
    quality: str = "auto:good",
    format: str = "auto"
):
    """
    Generate optimized image URLs for a given public ID
    
    - **public_id**: Cloudinary public ID of the image
    - **width**: Target width in pixels (optional)
    - **height**: Target height in pixels (optional)
    - **crop**: Crop mode (fill, fit, scale, etc.)
    - **quality**: Image quality setting
    - **format**: Image format (auto, webp, jpg, png)
    - **Returns**: Optimized URLs
    """
    try:
        if width or height:
            # Generate single optimized URL with specified dimensions
            optimized_url = cloudinary_service.get_optimized_url(
                public_id=public_id,
                width=width,
                height=height,
                crop=crop,
                quality=quality,
                format=format
            )
            
            return {
                "success": True,
                "data": {
                    "optimized_url": optimized_url,
                    "parameters": {
                        "width": width,
                        "height": height,
                        "crop": crop,
                        "quality": quality,
                        "format": format
                    }
                }
            }
        else:
            # Generate responsive URLs for different screen sizes
            responsive_urls = cloudinary_service.get_responsive_urls(public_id)
            
            return {
                "success": True,
                "data": {
                    "responsive_urls": responsive_urls
                }
            }
            
    except Exception as e:
        logger.error(f"Error generating URLs for image {public_id}: {str(e)}")
        raise HTTPException(500, "Internal server error generating image URLs")


@router.get("/limits")
async def get_upload_limits():
    """
    Get file upload limits and allowed formats
    
    - **Returns**: Upload configuration and limits
    """
    return {
        "success": True,
        "data": {
            "max_file_size_mb": 10,
            "allowed_formats": [
                "image/jpeg",
                "image/jpg", 
                "image/png",
                "image/webp",
                "image/gif",
                "image/bmp"
            ],
            "avatar_dimensions": {
                "recommended": "400x400",
                "max": "2000x2000"
            },
            "poster_dimensions": {
                "recommended": "800x1200",
                "max": "2000x3000"
            }
        }
    }