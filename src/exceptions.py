"""
Custom exceptions for Word Research Analyzer
"""
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class DocumentProcessingError(Exception):
    """Base exception for document processing errors"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
        logger.error(f"DocumentProcessingError: {message}")


class FileValidationError(DocumentProcessingError):
    """Raised when file validation fails"""
    
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        message = f"File validation failed for '{file_path}': {reason}"
        super().__init__(message, {'file_path': file_path, 'reason': reason})


class DocumentParsingError(DocumentProcessingError):
    """Raised when document parsing fails"""
    
    def __init__(self, file_path: str, parsing_stage: str, original_error: Optional[Exception] = None):
        self.file_path = file_path
        self.parsing_stage = parsing_stage
        self.original_error = original_error
        
        message = f"Document parsing failed at stage '{parsing_stage}' for '{file_path}'"
        if original_error:
            message += f": {str(original_error)}"
            
        details = {
            'file_path': file_path,
            'parsing_stage': parsing_stage,
            'original_error': str(original_error) if original_error else None
        }
        
        super().__init__(message, details)


class ReconstructionError(DocumentProcessingError):
    """Raised when document reconstruction fails"""
    
    def __init__(self, reconstruction_stage: str, original_error: Optional[Exception] = None):
        self.reconstruction_stage = reconstruction_stage
        self.original_error = original_error
        
        message = f"Document reconstruction failed at stage '{reconstruction_stage}'"
        if original_error:
            message += f": {str(original_error)}"
            
        details = {
            'reconstruction_stage': reconstruction_stage,
            'original_error': str(original_error) if original_error else None
        }
        
        super().__init__(message, details)


class UnsupportedFormatError(FileValidationError):
    """Raised when file format is not supported"""
    
    def __init__(self, file_path: str, file_extension: str, supported_extensions: list):
        self.file_extension = file_extension
        self.supported_extensions = supported_extensions
        
        reason = f"Unsupported format '{file_extension}'. Supported formats: {', '.join(supported_extensions)}"
        super().__init__(file_path, reason)


class FileSizeError(FileValidationError):
    """Raised when file size exceeds limits"""
    
    def __init__(self, file_path: str, file_size_mb: float, max_size_mb: int):
        self.file_size_mb = file_size_mb
        self.max_size_mb = max_size_mb
        
        reason = f"File size {file_size_mb:.2f}MB exceeds maximum allowed size {max_size_mb}MB"
        super().__init__(file_path, reason)


class CorruptDocumentError(DocumentParsingError):
    """Raised when document appears to be corrupted"""
    
    def __init__(self, file_path: str, original_error: Optional[Exception] = None):
        super().__init__(file_path, "document_loading", original_error)
        self.message = f"Document '{file_path}' appears to be corrupted or unreadable"


class MemoryError(DocumentProcessingError):
    """Raised when processing exceeds memory limits"""
    
    def __init__(self, file_path: str, operation: str):
        self.file_path = file_path
        self.operation = operation
        
        message = f"Memory limit exceeded while processing '{file_path}' during operation '{operation}'"
        details = {'file_path': file_path, 'operation': operation}
        
        super().__init__(message, details)


class OutputError(DocumentProcessingError):
    """Raised when output generation fails"""
    
    def __init__(self, output_format: str, output_path: str, original_error: Optional[Exception] = None):
        self.output_format = output_format
        self.output_path = output_path
        self.original_error = original_error
        
        message = f"Failed to generate {output_format} output to '{output_path}'"
        if original_error:
            message += f": {str(original_error)}"
            
        details = {
            'output_format': output_format,
            'output_path': output_path,
            'original_error': str(original_error) if original_error else None
        }
        
        super().__init__(message, details)
