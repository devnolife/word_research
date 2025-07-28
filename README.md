# Word Research Analyzer

A Python backend for analyzing Word document structure in research context. This project provides preprocessing capabilities for research documents before further analysis.

## 🚀 Current Status: Phase 1 - COMPLETED ✅

### ✅ Fully Implemented Features (Phase 1A & 1B)

**🎯 ALL Phase 1 requirements have been successfully implemented and tested!**

#### Core Methods (Phase 1A) - ✅ COMPLETE

- **`load_document(file_path)`** - ✅ Load Word files (.docx) with comprehensive error handling
- **`validate_file(file_path)`** - ✅ Validate format and existence with custom exceptions
- **`get_basic_info()`** - ✅ Basic stats: paragraphs, words, characters, tables, headings
- **`extract_raw_text()`** - ✅ Extract all raw text content with cleaning
- **`get_document_metadata()`** - ✅ Document metadata (author, dates, title, etc.)

#### Advanced Methods (Phase 1B) - ✅ COMPLETE

- **`extract_paragraphs()`** - ✅ Extract paragraphs with complete structure info
- **`identify_headings()`** - ✅ Identify headings and their levels with hierarchy
- **`extract_tables_basic()`** - ✅ Basic table information with data extraction
- **`get_document_statistics()`** - ✅ Comprehensive statistics with reading time and complexity

#### 🔧 Additional Implementation Features

- **Comprehensive Error Handling** - ✅ Custom exception classes with detailed logging
- **Advanced Logging System** - ✅ Rotating file logs with configurable levels
- **Document Complexity Analysis** - ✅ Sophisticated scoring algorithm (0-10 scale)
- **Reading Time Calculation** - ✅ Accurate estimates based on word count
- **File Size Validation** - ✅ Configurable limits with detailed error messages
- **Type Hints & Documentation** - ✅ Complete type annotations and docstrings
- **Comprehensive Test Suite** - ✅ 19 unit tests covering all functionality
- **JSON Output Generation** - ✅ Structured data export for further processing

## 📁 Project Structure

```
word_research_analyzer/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── document_reader.py          # ✅ Core document reader (IMPLEMENTED)
│   ├── document_reconstructor.py   # 🔄 Phase 2
│   ├── text_cleaner.py            # 🔄 Phase 2
│   ├── output_formatters.py       # 🔄 Phase 2
│   ├── config.py                  # ✅ Configuration (IMPLEMENTED)
│   └── utils.py                   # ✅ Utilities (IMPLEMENTED)
├── tests/
│   ├── __init__.py
│   ├── test_document_reader.py     # ✅ Basic tests (IMPLEMENTED)
│   └── test_reconstructor.py       # 🔄 Phase 2
├── templates/
│   ├── markdown_template.md        # ✅ Markdown template
│   ├── html_template.html          # ✅ HTML template
│   └── json_schema.json           # ✅ JSON schema
├── outputs/                        # Output directory
├── sample_docs/                    # Sample documents directory
├── requirements.txt                # ✅ Dependencies
├── README.md                       # ✅ This file
├── .gitignore                     # 🔄 To be created
└── main.py                        # ✅ Demo script (IMPLEMENTED)
```

## 🛠️ Installation & Setup

### 1. Create Virtual Environment (Recommended)

#### For Windows Users

Create and activate a virtual environment to isolate project dependencies:

```powershell
# Navigate to project directory
cd d:\devnolife\word_research_analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1
```

**Alternative activation methods for Windows:**

```cmd
# Using Command Prompt (cmd)
venv\Scripts\activate.bat

# Using Git Bash
source venv/Scripts/activate
```

#### For Linux/Mac Users

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**💡 Important Notes for Windows Users:**

- **PowerShell Execution Policy**: If you get an execution policy error when activating the virtual environment, run PowerShell as Administrator and execute:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **Deactivate Virtual Environment**: To deactivate the virtual environment when you're done:

  ```powershell
  deactivate
  ```

- **Verify Virtual Environment**: You'll know the virtual environment is active when you see `(venv)` at the beginning of your command prompt.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python main.py --help
```

## 🎯 Usage

### Quick Start Demo

```bash
# Analyze a Word document
python main.py path/to/your/document.docx
```

### Python API Usage

```python
from src import DocumentReader, DocumentConfig, ProcessingConfig

# Initialize the reader
config = DocumentConfig()
processing_config = ProcessingConfig()
reader = DocumentReader(config=config, processing_config=processing_config)

# Load and analyze document
if reader.load_document("document.docx"):
    # Get basic information
    basic_info = reader.get_basic_info()
    print(f"Words: {basic_info['words']}")
    print(f"Paragraphs: {basic_info['paragraphs']}")
    
    # Extract text content
    raw_text = reader.extract_raw_text()
    
    # Get document metadata
    metadata = reader.get_document_metadata()
    
    # Analyze structure
    headings = reader.identify_headings()
    tables = reader.extract_tables_basic()
    paragraphs = reader.extract_paragraphs()
    
    # Get comprehensive statistics
    stats = reader.get_document_statistics()
```

## 📊 Features Overview

### Document Analysis Capabilities

| Feature | Status | Description |
|---------|--------|-------------|
| **File Validation** | ✅ | Validates file format, existence, and size |
| **Basic Statistics** | ✅ | Word count, paragraph count, character count |
| **Metadata Extraction** | ✅ | Author, title, creation date, etc. |
| **Raw Text Extraction** | ✅ | Clean text content extraction |
| **Heading Detection** | ✅ | Identifies headings and their hierarchy levels |
| **Table Analysis** | ✅ | Basic table structure and content |
| **Paragraph Analysis** | ✅ | Detailed paragraph information with formatting |
| **Document Statistics** | ✅ | Comprehensive document metrics |

### Data Structures

#### DocumentStats

```python
@dataclass
class DocumentStats:
    total_paragraphs: int
    total_words: int
    total_characters: int
    total_characters_no_spaces: int
    total_sentences: int
    total_pages: int
    total_sections: int
    total_tables: int
    total_images: int
    total_headings: int
```

#### ParagraphInfo

```python
@dataclass
class ParagraphInfo:
    index: int
    text: str
    style_name: str
    is_heading: bool
    heading_level: Optional[int]
    alignment: Optional[str]
    bold: bool
    italic: bool
    underline: bool
    font_size: Optional[float]
    font_name: Optional[str]
```

#### HeadingInfo

```python
@dataclass
class HeadingInfo:
    index: int
    text: str
    level: int
    style_name: str
    paragraph_index: int
```

#### TableInfo

```python
@dataclass
class TableInfo:
    index: int
    rows: int
    columns: int
    data: List[List[str]]
    style_name: Optional[str]
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_document_reader.py

# Run with verbose output
pytest tests/ -v
```

## 📝 Configuration

### DocumentConfig

- `supported_extensions`: File formats to process (default: ['.docx', '.doc'])
- `max_file_size_mb`: Maximum file size limit (default: 100MB)
- `encoding`: Text encoding (default: 'utf-8')
- `output_formats`: Supported output formats

### ProcessingConfig

- `extract_images`: Include image analysis (default: False)
- `extract_tables`: Include table analysis (default: True)
- `extract_headers_footers`: Include headers/footers (default: True)
- `analyze_styles`: Analyze style information (default: True)

## 🎯 Example Output

### Console Output

```
==========================================
Word Research Analyzer - Document Analysis Demo
==========================================

Analyzing document: research_paper.docx
----------------------------------------
✅ Document loaded successfully!

📊 BASIC INFORMATION
--------------------
File name: research_paper.docx
File size: 245.7 KB
Paragraphs: 127
Words: 4,523
Characters: 28,945
Tables: 3
Headings: 12

📋 DOCUMENT METADATA
--------------------
Title: Machine Learning in Healthcare Research
Author: Dr. Jane Smith
Created: 2024-01-15T09:30:00
Modified: 2024-01-20T14:22:00

📑 DOCUMENT STRUCTURE - HEADINGS
--------------------------------
• Level 1: Introduction
  • Level 2: Background and Literature Review
  • Level 2: Methodology
    • Level 3: Data Collection
    • Level 3: Model Training
• Level 1: Results and Discussion
  • Level 2: Performance Metrics
• Level 1: Conclusion
```

## 🔮 Upcoming Features (Phase 2+)

### Phase 2: Advanced Analysis

- **Document Reconstruction** - Rebuild document structure
- **Advanced Text Cleaning** - Academic text normalization
- **Output Formatters** - JSON, Markdown, HTML export
- **Citation Extraction** - Academic citation detection
- **Image Analysis** - Extract and analyze embedded images

### Phase 3: Research-Specific Features

- **Reference Management** - Bibliography analysis
- **Section Classification** - Automatic section type detection
- **Content Analysis** - Research methodology identification
- **Cross-Reference Detection** - Internal document references

## 📋 Requirements

### Python Dependencies

- `python-docx>=0.8.11` - Word document processing
- `python-magic>=0.4.27` - File type detection
- `pathlib2>=2.3.7` - Path handling
- `dataclasses>=0.8` - Data structures
- `typing-extensions>=4.0.0` - Type hints

### Development Dependencies

- `pytest>=7.0.0` - Testing framework
- `black>=22.0.0` - Code formatting
- `flake8>=5.0.0` - Code linting
- `mypy>=0.991` - Type checking

## 🤝 Contributing

This is Phase 1 of the project. Current focus is on:

1. Testing the core document reader functionality
2. Performance optimization
3. Error handling improvements
4. Documentation enhancements

## 📄 License

This project is developed for research document preprocessing and analysis.

## 🆘 Support

### Common Issues

1. **"Document not loaded" error**
   - Check file exists and is readable
   - Verify file is a valid .docx format
   - Ensure file size is under 100MB

2. **Import errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Performance issues**
   - Large documents may take time to process
   - Consider splitting very large documents

4. **Windows Virtual Environment Issues**
   - **PowerShell execution policy error**: Run PowerShell as Administrator and execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
   - **"venv is not recognized"**: Make sure you're in the correct project directory and Python is properly installed
   - **Activation script not found**: Verify the virtual environment was created successfully with `python -m venv venv`
   - **Permission denied**: Ensure you have write permissions in the project directory

### Getting Help

For issues or questions about Phase 1 implementation:

1. Check the test files for usage examples
2. Review the main.py demo script
3. Verify your document format and structure
4. For Windows-specific issues, ensure virtual environment is properly activated (you should see `(venv)` in your prompt)

---

**🎉 Phase 1 Complete!** The document reading foundation is fully implemented and ready for use. Start analyzing your Word documents today!
