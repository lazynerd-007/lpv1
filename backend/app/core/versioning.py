"""
API versioning and compatibility management for LemonNPie Backend API
"""
from typing import Dict, Any, List, Optional
from enum import Enum
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import re
from datetime import datetime, date


class APIVersion(str, Enum):
    """Supported API versions"""
    V1 = "v1"
    # Future versions can be added here
    # V2 = "v2"


class VersionStatus(str, Enum):
    """Version status indicators"""
    CURRENT = "current"
    SUPPORTED = "supported"
    DEPRECATED = "deprecated"
    SUNSET = "sunset"


class APIVersionManager:
    """Manages API versioning and compatibility"""
    
    # Version configuration
    VERSIONS = {
        APIVersion.V1: {
            "status": VersionStatus.CURRENT,
            "release_date": "2024-01-01",
            "sunset_date": None,
            "description": "Initial release with core functionality",
            "breaking_changes": [],
            "deprecated_features": []
        }
        # Future versions configuration
        # APIVersion.V2: {
        #     "status": VersionStatus.SUPPORTED,
        #     "release_date": "2024-06-01",
        #     "sunset_date": None,
        #     "description": "Enhanced search and analytics features",
        #     "breaking_changes": [
        #         "Changed pagination response format",
        #         "Removed deprecated user fields"
        #     ],
        #     "deprecated_features": [
        #         "Legacy search endpoint"
        #     ]
        # }
    }
    
    # Default version when none specified
    DEFAULT_VERSION = APIVersion.V1
    
    # Minimum supported version
    MIN_SUPPORTED_VERSION = APIVersion.V1
    
    @classmethod
    def get_version_from_request(cls, request: Request) -> APIVersion:
        """
        Extract API version from request
        
        Version can be specified in:
        1. URL path: /api/v1/endpoint
        2. Accept header: Accept: application/vnd.lemonnpie.v1+json
        3. Custom header: X-API-Version: v1
        4. Query parameter: ?version=v1
        """
        # 1. Check URL path
        path_version = cls._extract_version_from_path(request.url.path)
        if path_version:
            return path_version
        
        # 2. Check Accept header
        accept_header = request.headers.get("accept", "")
        accept_version = cls._extract_version_from_accept_header(accept_header)
        if accept_version:
            return accept_version
        
        # 3. Check custom header
        header_version = request.headers.get("x-api-version")
        if header_version:
            try:
                return APIVersion(header_version.lower())
            except ValueError:
                pass
        
        # 4. Check query parameter
        query_version = request.query_params.get("version")
        if query_version:
            try:
                return APIVersion(query_version.lower())
            except ValueError:
                pass
        
        # Return default version
        return cls.DEFAULT_VERSION
    
    @classmethod
    def _extract_version_from_path(cls, path: str) -> Optional[APIVersion]:
        """Extract version from URL path"""
        match = re.search(r'/api/(v\d+)/', path)
        if match:
            version_str = match.group(1)
            try:
                return APIVersion(version_str)
            except ValueError:
                pass
        return None
    
    @classmethod
    def _extract_version_from_accept_header(cls, accept_header: str) -> Optional[APIVersion]:
        """Extract version from Accept header"""
        # Format: application/vnd.lemonnpie.v1+json
        match = re.search(r'application/vnd\.lemonnpie\.(v\d+)\+json', accept_header)
        if match:
            version_str = match.group(1)
            try:
                return APIVersion(version_str)
            except ValueError:
                pass
        return None
    
    @classmethod
    def validate_version(cls, version: APIVersion) -> bool:
        """Validate if version is supported"""
        if version not in cls.VERSIONS:
            return False
        
        version_info = cls.VERSIONS[version]
        return version_info["status"] in [VersionStatus.CURRENT, VersionStatus.SUPPORTED]
    
    @classmethod
    def get_version_info(cls, version: APIVersion) -> Dict[str, Any]:
        """Get detailed information about a version"""
        if version not in cls.VERSIONS:
            raise ValueError(f"Unknown version: {version}")
        
        return cls.VERSIONS[version]
    
    @classmethod
    def get_all_versions_info(cls) -> Dict[str, Any]:
        """Get information about all versions"""
        return {
            "current_version": cls.DEFAULT_VERSION,
            "supported_versions": [
                {
                    "version": version,
                    **info
                }
                for version, info in cls.VERSIONS.items()
                if info["status"] in [VersionStatus.CURRENT, VersionStatus.SUPPORTED]
            ],
            "deprecated_versions": [
                {
                    "version": version,
                    **info
                }
                for version, info in cls.VERSIONS.items()
                if info["status"] == VersionStatus.DEPRECATED
            ]
        }
    
    @classmethod
    def create_version_headers(cls, version: APIVersion) -> Dict[str, str]:
        """Create version-related response headers"""
        version_info = cls.get_version_info(version)
        
        headers = {
            "X-API-Version": version.value,
            "X-API-Version-Status": version_info["status"].value
        }
        
        # Add deprecation warning if applicable
        if version_info["status"] == VersionStatus.DEPRECATED:
            headers["Deprecation"] = "true"
            if version_info.get("sunset_date"):
                headers["Sunset"] = version_info["sunset_date"]
        
        return headers


class VersionCompatibilityHandler:
    """Handles backward compatibility between API versions"""
    
    @classmethod
    def transform_response_for_version(
        cls, 
        response_data: Dict[str, Any], 
        target_version: APIVersion,
        endpoint: str
    ) -> Dict[str, Any]:
        """
        Transform response data for backward compatibility
        """
        # For now, v1 is the only version, so no transformation needed
        # Future versions would implement transformation logic here
        
        if target_version == APIVersion.V1:
            return cls._transform_to_v1(response_data, endpoint)
        
        return response_data
    
    @classmethod
    def _transform_to_v1(cls, data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Transform response to v1 format"""
        # V1 is the base format, no transformation needed
        return data
    
    @classmethod
    def validate_request_for_version(
        cls,
        request_data: Dict[str, Any],
        target_version: APIVersion,
        endpoint: str
    ) -> Dict[str, Any]:
        """
        Validate and transform request data for version compatibility
        """
        if target_version == APIVersion.V1:
            return cls._validate_v1_request(request_data, endpoint)
        
        return request_data
    
    @classmethod
    def _validate_v1_request(cls, data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Validate request for v1 compatibility"""
        # V1 validation logic
        return data


def version_middleware(request: Request, call_next):
    """
    Middleware to handle API versioning
    """
    async def middleware(request: Request):
        # Extract version from request
        version = APIVersionManager.get_version_from_request(request)
        
        # Validate version
        if not APIVersionManager.validate_version(version):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "unsupported_version",
                    "message": f"API version {version} is not supported",
                    "supported_versions": list(APIVersionManager.VERSIONS.keys()),
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "path": request.url.path
                }
            )
        
        # Add version to request state
        request.state.api_version = version
        
        # Process request
        response = await call_next(request)
        
        # Add version headers to response
        version_headers = APIVersionManager.create_version_headers(version)
        for header, value in version_headers.items():
            response.headers[header] = value
        
        return response
    
    return middleware


class MigrationGuide:
    """Provides migration guidance between API versions"""
    
    MIGRATION_GUIDES = {
        # Future migration guides would be added here
        # "v1_to_v2": {
        #     "title": "Migrating from v1 to v2",
        #     "description": "Guide for upgrading from API v1 to v2",
        #     "breaking_changes": [
        #         {
        #             "change": "Pagination format updated",
        #             "old_format": {"page": 1, "per_page": 20, "total": 100},
        #             "new_format": {"page": 1, "size": 20, "total": 100, "pages": 5},
        #             "migration_steps": [
        #                 "Update pagination parsing logic",
        #                 "Use 'size' instead of 'per_page'",
        #                 "Handle new 'pages' field"
        #             ]
        #         }
        #     ],
        #     "deprecated_features": [
        #         {
        #             "feature": "Legacy search endpoint",
        #             "replacement": "New advanced search endpoint",
        #             "timeline": "Deprecated in v2, removed in v3"
        #         }
        #     ],
        #     "new_features": [
        #         "Enhanced analytics endpoints",
        #         "Improved search capabilities",
        #         "Real-time notifications"
        #     ]
        # }
    }
    
    @classmethod
    def get_migration_guide(cls, from_version: str, to_version: str) -> Dict[str, Any]:
        """Get migration guide between versions"""
        guide_key = f"{from_version}_to_{to_version}"
        return cls.MIGRATION_GUIDES.get(guide_key, {})
    
    @classmethod
    def get_all_migration_guides(cls) -> Dict[str, Any]:
        """Get all available migration guides"""
        return cls.MIGRATION_GUIDES


def create_version_info_endpoint():
    """Create endpoint for version information"""
    
    def get_api_versions():
        """
        Get API version information
        
        Returns information about all supported API versions, including:
        - Current version
        - Supported versions with status
        - Deprecated versions with sunset dates
        - Migration guides
        """
        return {
            "api_name": "LemonNPie Backend API",
            "version_info": APIVersionManager.get_all_versions_info(),
            "versioning_strategy": {
                "type": "URL path versioning",
                "format": "/api/{version}/endpoint",
                "alternatives": [
                    "Accept header: application/vnd.lemonnpie.{version}+json",
                    "Custom header: X-API-Version: {version}",
                    "Query parameter: ?version={version}"
                ]
            },
            "compatibility": {
                "backward_compatibility": "Maintained for one major version",
                "deprecation_policy": "6 months notice before removal",
                "breaking_changes": "Only in major version updates"
            },
            "migration_guides": MigrationGuide.get_all_migration_guides(),
            "support": {
                "documentation": "https://docs.lemonnpie.com/api/versioning",
                "contact": "api-support@lemonnpie.com"
            }
        }
    
    return get_api_versions