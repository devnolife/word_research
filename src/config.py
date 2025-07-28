"""
Configuration module for Word Research Analyzer
"""
from dataclasses import dataclass
from typing import Dict, Any, List
from pathlib import Path

@dataclass
class DocumentConfig:
    """Configuration for document processing"""
    supported_extensions: List[str] = None
    max_file_size_mb: int = 100
    encoding: str = 'utf-8'
    output_formats: List[str] = None
    
    def __post_init__(self):
        if self.supported_extensions is None:
            self.supported_extensions = ['.docx', '.doc']
        if self.output_formats is None:
            self.output_formats = ['json', 'markdown', 'html', 'txt']

@dataclass
class OutputConfig:
    """Configuration for output formatting"""
    base_output_dir: str = 'outputs'
    create_subdirs: bool = True
    timestamp_files: bool = True
    preserve_formatting: bool = True
    include_metadata: bool = True

@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    extract_images: bool = False
    extract_tables: bool = True
    extract_headers_footers: bool = True
    analyze_styles: bool = True
    detect_language: bool = False
    
# Default configurations
DEFAULT_DOCUMENT_CONFIG = DocumentConfig()
DEFAULT_OUTPUT_CONFIG = OutputConfig()
DEFAULT_PROCESSING_CONFIG = ProcessingConfig()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / 'src'
TEMPLATES_DIR = PROJECT_ROOT / 'templates'
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'
SAMPLE_DOCS_DIR = PROJECT_ROOT / 'sample_docs'
TESTS_DIR = PROJECT_ROOT / 'tests'
