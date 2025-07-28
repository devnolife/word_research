"""
Utility functions for Word Research Analyzer
"""
import os
import re
from pathlib import Path
from typing import Union, Dict, Any, Optional
from datetime import datetime
import hashlib

def validate_file_path(file_path: Union[str, Path]) -> bool:
    """
    Validate if file path exists and is accessible
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if file exists and is readable
    """
    path = Path(file_path)
    return path.exists() and path.is_file() and os.access(path, os.R_OK)

def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to the file
        
    Returns:
        int: File size in bytes, 0 if file doesn't exist
    """
    try:
        return Path(file_path).stat().st_size
    except (OSError, FileNotFoundError):
        return 0

def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Get file extension in lowercase
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: File extension including the dot (e.g., '.docx')
    """
    return Path(file_path).suffix.lower()

def is_supported_format(file_path: Union[str, Path], supported_extensions: list) -> bool:
    """
    Check if file format is supported
    
    Args:
        file_path: Path to the file
        supported_extensions: List of supported extensions
        
    Returns:
        bool: True if format is supported
    """
    extension = get_file_extension(file_path)
    return extension in [ext.lower() for ext in supported_extensions]

def generate_output_filename(
    original_filename: str, 
    output_format: str, 
    timestamp: bool = True,
    suffix: Optional[str] = None
) -> str:
    """
    Generate output filename based on original filename and format
    
    Args:
        original_filename: Original file name
        output_format: Target output format
        timestamp: Whether to include timestamp
        suffix: Optional suffix to add
        
    Returns:
        str: Generated output filename
    """
    base_name = Path(original_filename).stem
    
    # Clean filename for output
    base_name = re.sub(r'[^\w\-_\.]', '_', base_name)
    
    parts = [base_name]
    
    if suffix:
        parts.append(suffix)
        
    if timestamp:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        parts.append(timestamp_str)
    
    filename = '_'.join(parts) + f'.{output_format}'
    return filename

def calculate_file_hash(file_path: Union[str, Path]) -> str:
    """
    Calculate MD5 hash of a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: MD5 hash of the file
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (OSError, FileNotFoundError):
        return ""

def ensure_output_directory(output_path: Union[str, Path]) -> bool:
    """
    Ensure output directory exists, create if necessary
    
    Args:
        output_path: Path to output directory or file
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        path = Path(output_path)
        if path.suffix:  # It's a file path
            path = path.parent
        path.mkdir(parents=True, exist_ok=True)
        return True
    except OSError:
        return False

def clean_text(text: str, preserve_whitespace: bool = False) -> str:
    """
    Clean text content by removing extra whitespace and special characters
    
    Args:
        text: Input text to clean
        preserve_whitespace: Whether to preserve original whitespace
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    if preserve_whitespace:
        # Only remove null characters and other problematic chars
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
    else:
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove problematic characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
        return text.strip()

def format_bytes(size_bytes: int) -> str:
    """
    Format byte size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"
