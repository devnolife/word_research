"""
Test cases for DocumentReader class
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.document_reader import DocumentReader, DocumentStats, ParagraphInfo, HeadingInfo, TableInfo
from src.config import DocumentConfig, ProcessingConfig

class TestDocumentReader:
    """Test cases for DocumentReader"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.config = DocumentConfig()
        self.processing_config = ProcessingConfig()
        self.reader = DocumentReader(self.config, self.processing_config)
        self.sample_doc_path = Path(__file__).parent.parent / "sample_docs" / "research_paper.docx"
    
    def test_init(self):
        """Test DocumentReader initialization"""
        assert self.reader.config is not None
        assert self.reader.processing_config is not None
        assert self.reader.document is None
        assert self.reader.file_path is None
        assert self.reader.is_loaded is False
    
    def test_validate_file_nonexistent(self):
        """Test validation of non-existent file"""
        with pytest.raises(Exception):  # Should raise FileValidationError
            self.reader.validate_file("nonexistent.docx")
    
    def test_validate_file_unsupported_format(self):
        """Test validation of unsupported file format"""
        # Create temporary file with wrong extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name
        
        try:
            with pytest.raises(Exception):  # Should raise UnsupportedFormatError
                self.reader.validate_file(tmp_path)
        finally:
            os.unlink(tmp_path)
    
    def test_get_basic_info_not_loaded(self):
        """Test get_basic_info when document not loaded"""
        result = self.reader.get_basic_info()
        assert result == {}
    
    def test_extract_raw_text_not_loaded(self):
        """Test extract_raw_text when document not loaded"""
        result = self.reader.extract_raw_text()
        assert result == ""
    
    def test_get_document_metadata_not_loaded(self):
        """Test get_document_metadata when document not loaded"""
        result = self.reader.get_document_metadata()
        assert result == {}
    
    def test_extract_paragraphs_not_loaded(self):
        """Test extract_paragraphs when document not loaded"""
        result = self.reader.extract_paragraphs()
        assert result == []
    
    def test_identify_headings_not_loaded(self):
        """Test identify_headings when document not loaded"""
        result = self.reader.identify_headings()
        assert result == []
    
    def test_extract_tables_basic_not_loaded(self):
        """Test extract_tables_basic when document not loaded"""
        result = self.reader.extract_tables_basic()
        assert result == []
    
    def test_get_document_statistics_not_loaded(self):
        """Test get_document_statistics when document not loaded"""
        result = self.reader.get_document_statistics()
        assert isinstance(result, DocumentStats)
        assert result.total_paragraphs == 0
        assert result.total_words == 0
    
    def test_load_sample_document(self):
        """Test loading the actual sample document"""
        if not self.sample_doc_path.exists():
            pytest.skip(f"Sample document not found: {self.sample_doc_path}")
        
        # Load the document
        success = self.reader.load_document(self.sample_doc_path)
        assert success is True
        assert self.reader.is_loaded is True
        
        # Test basic info
        basic_info = self.reader.get_basic_info()
        assert isinstance(basic_info, dict)
        assert basic_info['words'] > 0
        assert basic_info['paragraphs'] > 0
        
        # Test metadata
        metadata = self.reader.get_document_metadata()
        assert isinstance(metadata, dict)
        
        # Test text extraction
        raw_text = self.reader.extract_raw_text()
        assert isinstance(raw_text, str)
        assert len(raw_text) > 0
        
        # Test paragraph extraction
        paragraphs = self.reader.extract_paragraphs()
        assert isinstance(paragraphs, list)
        assert len(paragraphs) > 0
        
        # Test heading extraction
        headings = self.reader.identify_headings()
        assert isinstance(headings, list)
        
        # Test table extraction
        tables = self.reader.extract_tables_basic()
        assert isinstance(tables, list)
        
        # Test statistics
        stats = self.reader.get_document_statistics()
        assert isinstance(stats, DocumentStats)
        assert stats.total_words > 0
        assert stats.reading_time_minutes > 0
        assert 0 <= stats.complexity_score <= 10

class TestDocumentStats:
    """Test cases for DocumentStats"""
    
    def test_init_default(self):
        """Test DocumentStats default initialization"""
        stats = DocumentStats()
        assert stats.total_paragraphs == 0
        assert stats.total_words == 0
        assert stats.total_characters == 0
    
    def test_to_dict(self):
        """Test DocumentStats to_dict method"""
        stats = DocumentStats(
            total_paragraphs=5,
            total_words=100,
            total_characters=500
        )
        result = stats.to_dict()
        
        assert isinstance(result, dict)
        assert result['total_paragraphs'] == 5
        assert result['total_words'] == 100
        assert result['total_characters'] == 500

class TestParagraphInfo:
    """Test cases for ParagraphInfo"""
    
    def test_init(self):
        """Test ParagraphInfo initialization"""
        para = ParagraphInfo(
            index=0,
            text="Test paragraph",
            style_name="Normal"
        )
        
        assert para.index == 0
        assert para.text == "Test paragraph"
        assert para.style_name == "Normal"
        assert para.is_heading is False
    
    def test_to_dict(self):
        """Test ParagraphInfo to_dict method"""
        para = ParagraphInfo(
            index=1,
            text="Test heading",
            style_name="Heading 1",
            is_heading=True,
            heading_level=1
        )
        
        result = para.to_dict()
        assert isinstance(result, dict)
        assert result['index'] == 1
        assert result['text'] == "Test heading"
        assert result['is_heading'] is True
        assert result['heading_level'] == 1

class TestHeadingInfo:
    """Test cases for HeadingInfo"""
    
    def test_init(self):
        """Test HeadingInfo initialization"""
        heading = HeadingInfo(
            index=0,
            text="Chapter 1",
            level=1,
            style_name="Heading 1",
            paragraph_index=5
        )
        
        assert heading.index == 0
        assert heading.text == "Chapter 1"
        assert heading.level == 1
        assert heading.style_name == "Heading 1"
        assert heading.paragraph_index == 5
    
    def test_to_dict(self):
        """Test HeadingInfo to_dict method"""
        heading = HeadingInfo(
            index=0,
            text="Chapter 1",
            level=1,
            style_name="Heading 1",
            paragraph_index=5
        )
        
        result = heading.to_dict()
        assert isinstance(result, dict)
        assert result['text'] == "Chapter 1"
        assert result['level'] == 1

class TestTableInfo:
    """Test cases for TableInfo"""
    
    def test_init(self):
        """Test TableInfo initialization"""
        table = TableInfo(
            index=0,
            rows=3,
            columns=2,
            data=[["A", "B"], ["C", "D"], ["E", "F"]]
        )
        
        assert table.index == 0
        assert table.rows == 3
        assert table.columns == 2
        assert len(table.data) == 3
    
    def test_to_dict(self):
        """Test TableInfo to_dict method"""
        table = TableInfo(
            index=0,
            rows=2,
            columns=2,
            data=[["A", "B"], ["C", "D"]]
        )
        
        result = table.to_dict()
        assert isinstance(result, dict)
        assert result['rows'] == 2
        assert result['columns'] == 2
        assert result['data'] == [["A", "B"], ["C", "D"]]

if __name__ == "__main__":
    pytest.main([__file__])
