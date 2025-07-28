"""
Main entry point for Word Research Analyzer
Demonstrates the core functionality of the document reader with comprehensive error handling
"""

import sys
from pathlib import Path
from src import DocumentReader, DocumentConfig, ProcessingConfig
from src.exceptions import (
    DocumentProcessingError, FileValidationError, DocumentParsingError,
    UnsupportedFormatError, FileSizeError, CorruptDocumentError, MemoryError
)
from src.logging_config import setup_logging, get_logger

def demonstrate_document_analysis(file_path: str):
    """
    Demonstrate the document analysis capabilities with comprehensive error handling
    
    Args:
        file_path: Path to the Word document to analyze
    """
    # Set up logging
    logger = setup_logging(log_level="INFO", console_logging=False)
    
    print("=" * 60)
    print("Word Research Analyzer - Document Analysis Demo")
    print("=" * 60)
    
    # Initialize the document reader
    config = DocumentConfig()
    processing_config = ProcessingConfig()
    reader = DocumentReader(config=config, processing_config=processing_config)
    
    print(f"\nAnalyzing document: {file_path}")
    print("-" * 40)
    
    # Load the document with proper error handling
    try:
        success = reader.load_document(file_path)
        print("✅ Document loaded successfully!")
        logger.info(f"Document loaded successfully: {file_path}")
        
    except FileValidationError as e:
        print(f"❌ File validation failed: {e.reason}")
        logger.error(f"File validation failed: {e}")
        return False
        
    except UnsupportedFormatError as e:
        print(f"❌ Unsupported file format: {e.file_extension}")
        print(f"   Supported formats: {', '.join(e.supported_extensions)}")
        logger.error(f"Unsupported format: {e}")
        return False
        
    except FileSizeError as e:
        print(f"❌ File too large: {e.file_size_mb:.2f}MB (max: {e.max_size_mb}MB)")
        logger.error(f"File size error: {e}")
        return False
        
    except CorruptDocumentError as e:
        print("❌ Document appears to be corrupted or unreadable")
        print("   Please try opening the file in Microsoft Word to verify it's valid")
        logger.error(f"Corrupt document: {e}")
        return False
        
    except MemoryError as e:
        print("❌ Document too large for available memory")
        print("   Try processing a smaller document or increase available memory")
        logger.error(f"Memory error: {e}")
        return False
        
    except DocumentProcessingError as e:
        print(f"❌ Document processing error: {e.message}")
        logger.error(f"Document processing error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected error: {e}")
        return False
    
    # Get basic information
    print("\n📊 BASIC INFORMATION")
    print("-" * 20)
    basic_info = reader.get_basic_info()
    
    file_info = basic_info.get('file_info', {})
    print(f"File name: {file_info.get('name', 'Unknown')}")
    print(f"File size: {file_info.get('size_formatted', 'Unknown')}")
    print(f"File extension: {file_info.get('extension', 'Unknown')}")
    print(f"Paragraphs: {basic_info.get('paragraphs', 0)}")
    print(f"Words: {basic_info.get('words', 0)}")
    print(f"Characters: {basic_info.get('characters', 0)}")
    print(f"Characters (no spaces): {basic_info.get('characters_no_spaces', 0)}")
    print(f"Tables: {basic_info.get('tables', 0)}")
    print(f"Headings: {basic_info.get('headings', 0)}")
    
    # Get document metadata
    print("\n📋 DOCUMENT METADATA")
    print("-" * 20)
    metadata = reader.get_document_metadata()
    
    for key, value in metadata.items():
        if value:  # Only show non-empty values
            print(f"{key.title()}: {value}")
    
    # Get detailed statistics
    print("\n📈 DETAILED STATISTICS")
    print("-" * 20)
    stats = reader.get_document_statistics()
    stats_dict = stats.to_dict()
    
    for key, value in stats_dict.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"{formatted_key}: {value}")
    
    # Show headings structure
    print("\n📑 DOCUMENT STRUCTURE - HEADINGS")
    print("-" * 20)
    headings = reader.identify_headings()
    
    if headings:
        for heading in headings:
            indent = "  " * (heading.level - 1) if heading.level > 0 else ""
            print(f"{indent}• Level {heading.level}: {heading.text[:60]}...")
    else:
        print("No headings found in the document")
    
    # Show table information
    print("\n📋 TABLES INFORMATION")
    print("-" * 20)
    tables = reader.extract_tables_basic()
    
    if tables:
        for table in tables:
            print(f"Table {table.index + 1}: {table.rows} rows × {table.columns} columns")
            if table.style_name:
                print(f"  Style: {table.style_name}")
            # Show first few cells as preview
            if table.data and len(table.data) > 0:
                preview_row = table.data[0][:3]  # First 3 cells of first row
                preview = " | ".join([cell[:20] + "..." if len(cell) > 20 else cell for cell in preview_row])
                print(f"  Preview: {preview}")
    else:
        print("No tables found in the document")
    
    # Extract and show text preview
    print("\n📄 TEXT CONTENT PREVIEW")
    print("-" * 20)
    raw_text = reader.extract_raw_text()
    
    if raw_text:
        # Show first 500 characters
        preview = raw_text[:500]
        if len(raw_text) > 500:
            preview += "..."
        print(preview)
    else:
        print("No text content found")
    
    print("\n" + "=" * 60)
    print("Analysis completed successfully! ✅")
    print("=" * 60)
    
    return True

def main():
    """Main function"""
    print("Word Research Analyzer - Phase 1: Document Reading Foundation")
    
    if len(sys.argv) != 2:
        print("\nUsage: python main.py <path_to_word_document>")
        print("\nExample:")
        print("  python main.py sample_docs/research_paper.docx")
        print("  python main.py \"C:/Documents/my_document.docx\"")
        
        # Show available sample documents if any
        sample_docs_dir = Path("sample_docs")
        if sample_docs_dir.exists():
            sample_files = list(sample_docs_dir.glob("*.docx"))
            if sample_files:
                print(f"\nAvailable sample documents in {sample_docs_dir}:")
                for sample_file in sample_files:
                    print(f"  - {sample_file.name}")
        
        return
    
    file_path = sys.argv[1]
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File '{file_path}' not found!")
        return
    
    # Perform the analysis
    try:
        demonstrate_document_analysis(file_path)
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")
        print("\nPlease check:")
        print("- The file is a valid Word document (.docx)")
        print("- The file is not corrupted")
        print("- You have read permissions for the file")
        print("- Check the logs directory for more detailed error information")

if __name__ == "__main__":
    main()
