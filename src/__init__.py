"""
Word Research Analyzer - Python backend for analyzing Word document structure
"""

from .document_reader import DocumentReader, DocumentStats, ParagraphInfo, HeadingInfo, TableInfo
from .config import (
    DEFAULT_DOCUMENT_CONFIG, 
    DEFAULT_OUTPUT_CONFIG, 
    DEFAULT_PROCESSING_CONFIG,
    DocumentConfig,
    OutputConfig,
    ProcessingConfig
)

__version__ = "0.1.0"
__author__ = "Word Research Analyzer Team"
__description__ = "Python backend for analyzing Word document structure in research context"

__all__ = [
    'DocumentReader',
    'DocumentStats',
    'ParagraphInfo', 
    'HeadingInfo',
    'TableInfo',
    'DocumentConfig',
    'OutputConfig', 
    'ProcessingConfig',
    'DEFAULT_DOCUMENT_CONFIG',
    'DEFAULT_OUTPUT_CONFIG',
    'DEFAULT_PROCESSING_CONFIG'
]
