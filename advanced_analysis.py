"""
Advanced example demonstrating the complete document analysis workflow
This script shows all features of Phase 1 implementation
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.document_reader import DocumentReader
from src.config import DocumentConfig, ProcessingConfig
from src.logging_config import setup_logging, get_logger
from src.exceptions import (
    DocumentProcessingError, FileValidationError, DocumentParsingError,
    UnsupportedFormatError, FileSizeError, CorruptDocumentError
)


def analyze_document_comprehensive(file_path: str, output_dir: str = "outputs") -> dict:
    """
    Perform comprehensive document analysis with all available features
    
    Args:
        file_path: Path to the Word document
        output_dir: Directory to save analysis results
        
    Returns:
        dict: Complete analysis results
    """
    # Set up logging
    logger = setup_logging(log_level="INFO", console_logging=True)
    logger.info("Starting comprehensive document analysis")
    
    # Initialize configurations
    config = DocumentConfig()
    processing_config = ProcessingConfig()
    
    # Initialize reader
    reader = DocumentReader(config=config, processing_config=processing_config)
    
    # Initialize results structure
    analysis_results = {
        'metadata': {
            'analysis_timestamp': datetime.now().isoformat(),
            'file_path': str(file_path),
            'analysis_version': '1.0.0-phase1',
            'status': 'started'
        },
        'file_info': {},
        'document_metadata': {},
        'statistics': {},
        'content_analysis': {
            'paragraphs': [],
            'headings': [],
            'tables': [],
            'text_preview': '',
            'chapters': [],
            'chapter_structure': {}
        },
        'processing_log': [],
        'errors': []
    }
    
    try:
        # Step 1: Load and validate document
        logger.info(f"Loading document: {file_path}")
        analysis_results['processing_log'].append("Loading document...")
        
        success = reader.load_document(file_path)
        analysis_results['processing_log'].append("Document loaded successfully")
        
        # Step 2: Extract file information
        logger.info("Extracting file information")
        basic_info = reader.get_basic_info()
        analysis_results['file_info'] = basic_info.get('file_info', {})
        analysis_results['processing_log'].append("File information extracted")
        
        # Step 3: Extract document metadata
        logger.info("Extracting document metadata")
        doc_metadata = reader.get_document_metadata()
        analysis_results['document_metadata'] = doc_metadata
        analysis_results['processing_log'].append("Document metadata extracted")
        
        # Step 4: Calculate comprehensive statistics
        logger.info("Calculating document statistics")
        stats = reader.get_document_statistics()
        analysis_results['statistics'] = stats.to_dict()
        analysis_results['processing_log'].append("Statistics calculated")
        
        # Step 5: Extract structured content - Focus on chapter-by-chapter analysis
        logger.info("Identifying document structure and chapters")
        print("   🔍 Analyzing document structure...")
        headings = reader.identify_headings()
        analysis_results['content_analysis']['headings'] = [h.to_dict() for h in headings]
        
        # Organize content by chapters
        print("   📚 Organizing content by chapters...")
        chapters = extract_chapters_from_headings(headings, reader)
        analysis_results['content_analysis']['chapters'] = chapters
        analysis_results['content_analysis']['chapter_structure'] = generate_chapter_structure(chapters)
        analysis_results['processing_log'].append(f"Identified {len(chapters)} chapters/sections")
        print(f"   ✅ Found {len(chapters)} chapters/sections")
        
        # Extract paragraphs with chapter context
        logger.info("Extracting paragraphs with chapter context")
        print("   📝 Extracting paragraphs and assigning to chapters...")
        paragraphs = reader.extract_paragraphs()
        paragraphs_dicts = [p.to_dict() if hasattr(p, 'to_dict') else p for p in paragraphs]
        paragraphs_with_chapters = assign_paragraphs_to_chapters(paragraphs_dicts, chapters)
        analysis_results['content_analysis']['paragraphs'] = paragraphs_with_chapters
        analysis_results['processing_log'].append(f"Extracted {len(paragraphs)} paragraphs across chapters")
        print(f"   ✅ Processed {len(paragraphs)} paragraphs across chapters")
        
        # Extract tables with chapter context
        logger.info("Extracting tables with chapter context")
        print("   📋 Extracting tables and assigning to chapters...")
        tables = reader.extract_tables_basic()
        tables_dicts = [t.to_dict() if hasattr(t, 'to_dict') else t for t in tables]
        tables_with_chapters = assign_tables_to_chapters(tables_dicts, chapters)
        analysis_results['content_analysis']['tables'] = tables_with_chapters
        analysis_results['processing_log'].append(f"Extracted {len(tables)} tables across chapters")
        print(f"   ✅ Processed {len(tables)} tables across chapters")
        
        # Step 6: Extract raw text for preview
        logger.info("Extracting text content")
        raw_text = reader.extract_raw_text()
        # Store preview (first 1000 characters)
        analysis_results['content_analysis']['text_preview'] = raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text
        analysis_results['content_analysis']['total_text_length'] = len(raw_text)
        analysis_results['processing_log'].append("Text content extracted")
        
        # Step 7: Generate analysis summary
        summary = generate_analysis_summary(analysis_results)
        analysis_results['summary'] = summary
        analysis_results['processing_log'].append("Analysis summary generated")
        
        # Step 8: Save results to files
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save JSON results
        json_file = output_path / f"analysis_{Path(file_path).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        analysis_results['output_files'] = [str(json_file)]
        analysis_results['processing_log'].append(f"Results saved to {json_file}")
        
        # Mark as successful
        analysis_results['metadata']['status'] = 'completed'
        analysis_results['metadata']['completion_timestamp'] = datetime.now().isoformat()
        
        logger.info("Comprehensive analysis completed successfully")
        
    except FileValidationError as e:
        error_info = {'type': 'FileValidationError', 'message': str(e), 'details': e.details}
        analysis_results['errors'].append(error_info)
        analysis_results['metadata']['status'] = 'failed'
        logger.error(f"File validation error: {e}")
        
    except UnsupportedFormatError as e:
        error_info = {'type': 'UnsupportedFormatError', 'message': str(e), 'supported_formats': e.supported_extensions}
        analysis_results['errors'].append(error_info)
        analysis_results['metadata']['status'] = 'failed'
        logger.error(f"Unsupported format error: {e}")
        
    except CorruptDocumentError as e:
        error_info = {'type': 'CorruptDocumentError', 'message': str(e)}
        analysis_results['errors'].append(error_info)
        analysis_results['metadata']['status'] = 'failed'
        logger.error(f"Corrupt document error: {e}")
        
    except DocumentProcessingError as e:
        error_info = {'type': 'DocumentProcessingError', 'message': str(e), 'details': e.details}
        analysis_results['errors'].append(error_info)
        analysis_results['metadata']['status'] = 'failed'
        logger.error(f"Document processing error: {e}")
        
    except Exception as e:
        error_info = {'type': 'UnexpectedError', 'message': str(e)}
        analysis_results['errors'].append(error_info)
        analysis_results['metadata']['status'] = 'failed'
        logger.error(f"Unexpected error: {e}")
    
    return analysis_results


def generate_analysis_summary(results: dict) -> dict:
    """
    Generate a summary of the analysis results
    
    Args:
        results: Analysis results dictionary
        
    Returns:
        dict: Analysis summary
    """
    stats = results.get('statistics', {})
    content = results.get('content_analysis', {})
    metadata = results.get('document_metadata', {})
    
    return {
        'document_overview': {
            'title': metadata.get('title', 'Untitled'),
            'author': metadata.get('author', 'Unknown'),
            'total_words': stats.get('total_words', 0),
            'total_pages': stats.get('total_pages', 0),
            'reading_time_minutes': stats.get('reading_time_minutes', 0),
            'complexity_score': stats.get('complexity_score', 0)
        },
        'structure_analysis': {
            'total_paragraphs': len(content.get('paragraphs', [])),
            'total_headings': len(content.get('headings', [])),
            'total_tables': len(content.get('tables', [])),
            'total_chapters': len(content.get('chapters', [])),
            'heading_levels': get_heading_level_distribution(content.get('headings', [])),
            'average_paragraph_length': calculate_average_paragraph_length(content.get('paragraphs', [])),
            'chapter_structure': content.get('chapter_structure', {})
        },
        'content_metrics': {
            'total_sentences': stats.get('total_sentences', 0),
            'characters_with_spaces': stats.get('total_characters', 0),
            'characters_without_spaces': stats.get('total_characters_no_spaces', 0),
            'average_words_per_sentence': calculate_average_words_per_sentence(stats),
            'estimated_reading_level': estimate_reading_level(stats)
        },
        'quality_indicators': {
            'has_title': bool(metadata.get('title')),
            'has_author': bool(metadata.get('author')),
            'has_headings': len(content.get('headings', [])) > 0,
            'has_tables': len(content.get('tables', [])) > 0,
            'structure_score': calculate_structure_score(content)
        }
    }


def get_heading_level_distribution(headings: list) -> dict:
    """Get distribution of heading levels"""
    distribution = {}
    for heading in headings:
        level = heading.get('level', 1)
        distribution[f'level_{level}'] = distribution.get(f'level_{level}', 0) + 1
    return distribution


def calculate_average_paragraph_length(paragraphs: list) -> float:
    """Calculate average paragraph length in words"""
    if not paragraphs:
        return 0.0
    
    total_words = sum(len(p.get('text', '').split()) for p in paragraphs)
    return round(total_words / len(paragraphs), 2)


def calculate_average_words_per_sentence(stats: dict) -> float:
    """Calculate average words per sentence"""
    words = stats.get('total_words', 0)
    sentences = stats.get('total_sentences', 0)
    
    if sentences == 0:
        return 0.0
    
    return round(words / sentences, 2)


def estimate_reading_level(stats: dict) -> str:
    """Estimate reading level based on statistics"""
    avg_words_per_sentence = calculate_average_words_per_sentence(stats)
    complexity = stats.get('complexity_score', 0)
    
    if complexity <= 3:
        return "Elementary"
    elif complexity <= 5:
        return "Middle School"
    elif complexity <= 7:
        return "High School"
    elif complexity <= 9:
        return "College"
    else:
        return "Graduate"


def calculate_structure_score(content: dict) -> float:
    """Calculate a structure quality score (0-10)"""
    headings = content.get('headings', [])
    paragraphs = content.get('paragraphs', [])
    tables = content.get('tables', [])
    
    score = 0.0
    
    # Points for having headings
    if headings:
        score += 3.0
        
        # Bonus for good heading hierarchy
        levels = [h.get('level', 1) for h in headings]
        if 1 in levels:  # Has top-level headings
            score += 1.0
        if len(set(levels)) > 1:  # Has multiple levels
            score += 1.0
    
    # Points for reasonable paragraph count
    if 5 <= len(paragraphs) <= 100:
        score += 2.0
    elif len(paragraphs) > 0:
        score += 1.0
    
    # Points for having tables (shows structured data)
    if tables:
        score += 1.5
    
    # Points for good paragraph-to-heading ratio
    if headings and paragraphs:
        ratio = len(paragraphs) / len(headings)
        if 3 <= ratio <= 10:  # Good structure
            score += 1.5
    
    return round(min(score, 10.0), 2)


def print_analysis_summary(results: dict):
    """Print a formatted summary of the analysis"""
    status = results['metadata']['status']
    
    if status == 'failed':
        print("❌ Analysis failed!")
        for error in results.get('errors', []):
            print(f"   Error: {error['message']}")
        return
    
    summary = results.get('summary', {})
    overview = summary.get('document_overview', {})
    structure = summary.get('structure_analysis', {})
    metrics = summary.get('content_metrics', {})
    quality = summary.get('quality_indicators', {})
    
    print("📄 COMPREHENSIVE DOCUMENT ANALYSIS")
    print("=" * 50)
    
    print(f"\\n📋 Document Overview:")
    print(f"   Title: {overview.get('title', 'N/A')}")
    print(f"   Author: {overview.get('author', 'N/A')}")
    print(f"   Words: {overview.get('total_words', 0):,}")
    print(f"   Pages: {overview.get('total_pages', 0)}")
    print(f"   Reading Time: {overview.get('reading_time_minutes', 0):.1f} minutes")
    print(f"   Complexity Score: {overview.get('complexity_score', 0):.1f}/10")
    
    print(f"\\n🏗️  Structure Analysis:")
    print(f"   Chapters: {structure.get('total_chapters', 0)}")
    print(f"   Paragraphs: {structure.get('total_paragraphs', 0)}")
    print(f"   Headings: {structure.get('total_headings', 0)}")
    print(f"   Tables: {structure.get('total_tables', 0)}")
    print(f"   Avg Paragraph Length: {structure.get('average_paragraph_length', 0)} words")
    
    # Chapter structure details
    chapter_struct = structure.get('chapter_structure', {})
    if chapter_struct:
        print(f"   Subsections: {chapter_struct.get('total_subsections', 0)}")
        print(f"   Avg Subsections/Chapter: {chapter_struct.get('average_subsections_per_chapter', 0)}")
    
    print(f"\\n📊 Content Metrics:")
    print(f"   Sentences: {metrics.get('total_sentences', 0)}")
    print(f"   Avg Words/Sentence: {metrics.get('average_words_per_sentence', 0)}")
    print(f"   Estimated Reading Level: {metrics.get('estimated_reading_level', 'Unknown')}")
    
    print(f"\\n✅ Quality Indicators:")
    print(f"   Has Title: {'Yes' if quality.get('has_title') else 'No'}")
    print(f"   Has Author: {'Yes' if quality.get('has_author') else 'No'}")
    print(f"   Has Headings: {'Yes' if quality.get('has_headings') else 'No'}")
    print(f"   Has Tables: {'Yes' if quality.get('has_tables') else 'No'}")
    print(f"   Structure Score: {quality.get('structure_score', 0):.1f}/10")
    
    print("\\n" + "=" * 50)
    print("✅ Analysis completed successfully!")


def extract_chapters_from_headings(headings: list, reader) -> list:
    """
    Extract chapters/sections from document headings
    
    Args:
        headings: List of heading objects
        reader: DocumentReader instance
        
    Returns:
        list: List of chapter objects with content
    """
    chapters = []
    current_chapter = None
    
    for i, heading in enumerate(headings):
        heading_dict = heading.to_dict() if hasattr(heading, 'to_dict') else heading
        
        # Consider level 1 and 2 headings as main chapters
        if heading_dict.get('level', 1) <= 2:
            # Save previous chapter if exists
            if current_chapter:
                chapters.append(current_chapter)
            
            # Start new chapter
            current_chapter = {
                'chapter_number': len(chapters) + 1,
                'title': heading_dict.get('text', '').strip(),
                'level': heading_dict.get('level', 1),
                'start_position': heading_dict.get('position', 0),
                'subsections': [],
                'content_preview': '',
                'word_count': 0,
                'paragraph_count': 0,
                'table_count': 0
            }
        else:
            # Add as subsection to current chapter
            if current_chapter:
                subsection = {
                    'title': heading_dict.get('text', '').strip(),
                    'level': heading_dict.get('level', 3),
                    'position': heading_dict.get('position', 0)
                }
                current_chapter['subsections'].append(subsection)
    
    # Don't forget the last chapter
    if current_chapter:
        chapters.append(current_chapter)
    
    # If no chapters found based on headings, create a single chapter
    if not chapters:
        chapters.append({
            'chapter_number': 1,
            'title': 'Main Content',
            'level': 1,
            'start_position': 0,
            'subsections': [],
            'content_preview': '',
            'word_count': 0,
            'paragraph_count': 0,
            'table_count': 0
        })
    
    return chapters


def generate_chapter_structure(chapters: list) -> dict:
    """
    Generate a structure overview of chapters
    
    Args:
        chapters: List of chapter objects
        
    Returns:
        dict: Chapter structure information
    """
    structure = {
        'total_chapters': len(chapters),
        'chapter_titles': [ch['title'] for ch in chapters],
        'chapters_with_subsections': len([ch for ch in chapters if ch['subsections']]),
        'total_subsections': sum(len(ch['subsections']) for ch in chapters),
        'average_subsections_per_chapter': 0,
        'chapter_levels': {}
    }
    
    if structure['total_chapters'] > 0:
        structure['average_subsections_per_chapter'] = round(
            structure['total_subsections'] / structure['total_chapters'], 2
        )
    
    # Count chapter levels
    for chapter in chapters:
        level = chapter['level']
        structure['chapter_levels'][f'level_{level}'] = structure['chapter_levels'].get(f'level_{level}', 0) + 1
    
    return structure


def assign_paragraphs_to_chapters(paragraphs: list, chapters: list) -> list:
    """
    Assign paragraphs to their respective chapters based on order
    
    Args:
        paragraphs: List of paragraph objects/dicts
        chapters: List of chapter objects
        
    Returns:
        list: List of paragraphs with chapter information
    """
    if not chapters:
        return paragraphs
    
    paragraphs_with_chapters = []
    total_paragraphs = len(paragraphs)
    
    # Distribute paragraphs evenly across chapters based on their order
    paragraphs_per_chapter = max(1, total_paragraphs // len(chapters))
    
    for i, paragraph in enumerate(paragraphs):
        # Ensure paragraph is a dict
        if hasattr(paragraph, 'to_dict'):
            para_dict = paragraph.to_dict()
        elif isinstance(paragraph, dict):
            para_dict = paragraph.copy()
        else:
            # Create basic dict from object attributes
            para_dict = {
                'index': getattr(paragraph, 'index', i),
                'text': getattr(paragraph, 'text', str(paragraph)),
                'position': getattr(paragraph, 'position', i)
            }
        
        # Determine chapter based on paragraph order
        chapter_index = min(i // paragraphs_per_chapter, len(chapters) - 1)
        assigned_chapter = chapters[chapter_index]
        
        # Add chapter information to paragraph
        para_dict['chapter_number'] = assigned_chapter['chapter_number']
        para_dict['chapter_title'] = assigned_chapter['title']
        
        # Update chapter statistics
        assigned_chapter['paragraph_count'] += 1
        assigned_chapter['word_count'] += len(para_dict.get('text', '').split())
        
        # Set content preview if not set
        if not assigned_chapter['content_preview'] and para_dict.get('text', '').strip():
            text = para_dict['text'][:200]
            assigned_chapter['content_preview'] = text + "..." if len(para_dict['text']) > 200 else text
        
        paragraphs_with_chapters.append(para_dict)
    
    return paragraphs_with_chapters


def assign_tables_to_chapters(tables: list, chapters: list) -> list:
    """
    Assign tables to their respective chapters based on order
    
    Args:
        tables: List of table objects/dicts
        chapters: List of chapter objects
        
    Returns:
        list: List of tables with chapter information
    """
    if not chapters or not tables:
        return tables
    
    tables_with_chapters = []
    total_tables = len(tables)
    
    # Distribute tables across chapters
    tables_per_chapter = max(1, total_tables // len(chapters))
    
    for i, table in enumerate(tables):
        # Ensure table is a dict
        if hasattr(table, 'to_dict'):
            table_dict = table.to_dict()
        elif isinstance(table, dict):
            table_dict = table.copy()
        else:
            # Create basic dict from object attributes
            table_dict = {
                'index': getattr(table, 'index', i),
                'rows': getattr(table, 'rows', 0),
                'columns': getattr(table, 'columns', 0),
                'position': getattr(table, 'position', i * 100)
            }
        
        # Determine chapter based on table order
        chapter_index = min(i // tables_per_chapter, len(chapters) - 1)
        assigned_chapter = chapters[chapter_index]
        
        # Add chapter information to table
        table_dict['chapter_number'] = assigned_chapter['chapter_number']
        table_dict['chapter_title'] = assigned_chapter['title']
        
        # Update chapter statistics
        assigned_chapter['table_count'] += 1
        
        tables_with_chapters.append(table_dict)
    
    return tables_with_chapters


def print_chapter_analysis(results: dict):
    """Print detailed chapter-by-chapter analysis"""
    chapters = results.get('content_analysis', {}).get('chapters', [])
    chapter_structure = results.get('content_analysis', {}).get('chapter_structure', {})
    
    if not chapters:
        print("\\n📚 No chapters detected in document")
        return
    
    print("\\n📚 CHAPTER-BY-CHAPTER ANALYSIS")
    print("=" * 50)
    
    print(f"\\n📊 Structure Overview:")
    print(f"   Total Chapters: {chapter_structure.get('total_chapters', 0)}")
    print(f"   Total Subsections: {chapter_structure.get('total_subsections', 0)}")
    print(f"   Avg Subsections per Chapter: {chapter_structure.get('average_subsections_per_chapter', 0)}")
    
    # Show chapter titles overview
    print(f"\\n📖 Chapter Overview:")
    print("-" * 30)
    main_chapters = [ch for ch in chapters if ch['level'] == 1]
    for chapter in main_chapters[:10]:  # Show first 10 main chapters
        print(f"   • {chapter['title']} ({chapter['word_count']} words, {chapter['paragraph_count']} paragraphs)")
    
    if len(main_chapters) > 10:
        print(f"   ... and {len(main_chapters) - 10} more chapters")
    
    print(f"\\n📖 Detailed Chapter Analysis:")
    print("-" * 30)
    
    # Show detailed analysis for first 5 chapters
    for i, chapter in enumerate(chapters[:5]):
        print(f"\\nChapter {chapter['chapter_number']}: {chapter['title']}")
        print(f"   Level: {chapter['level']}")
        print(f"   Words: {chapter['word_count']:,}")
        print(f"   Paragraphs: {chapter['paragraph_count']}")
        print(f"   Tables: {chapter['table_count']}")
        
        if chapter['subsections']:
            print(f"   Subsections ({len(chapter['subsections'])}):")
            for subsection in chapter['subsections'][:3]:  # Show first 3 subsections
                print(f"     • {subsection['title']}")
            if len(chapter['subsections']) > 3:
                print(f"     ... and {len(chapter['subsections']) - 3} more")
        
        if chapter['content_preview']:
            preview = chapter['content_preview'][:150] + "..." if len(chapter['content_preview']) > 150 else chapter['content_preview']
            print(f"   Preview: {preview}")
        
        print()
    
    if len(chapters) > 5:
        print(f"\\n   ... and {len(chapters) - 5} more chapters with detailed content")
        print("   (See full analysis in the saved JSON file)")
    
    # Summary statistics by chapter level
    level_stats = {}
    for chapter in chapters:
        level = chapter['level']
        if level not in level_stats:
            level_stats[level] = {'count': 0, 'total_words': 0, 'total_paragraphs': 0}
        level_stats[level]['count'] += 1
        level_stats[level]['total_words'] += chapter['word_count']
        level_stats[level]['total_paragraphs'] += chapter['paragraph_count']
    
    print(f"\\n📊 Statistics by Level:")
    print("-" * 25)
    for level in sorted(level_stats.keys()):
        stats = level_stats[level]
        avg_words = stats['total_words'] / stats['count'] if stats['count'] > 0 else 0
        print(f"   Level {level}: {stats['count']} sections, avg {avg_words:.0f} words each")


def main():
    """Main function for the advanced analysis example"""
    if len(sys.argv) != 2:
        print("Usage: python advanced_analysis.py <path_to_document>")
        print("\\nExample:")
        print("  python advanced_analysis.py sample_docs/research_paper.docx")
        return
    
    file_path = sys.argv[1]
    
    print("🔬 Advanced Document Analysis - Word Research Analyzer")
    print("Phase 1: Complete Feature Demonstration")
    print()
    
    # Perform comprehensive analysis
    results = analyze_document_comprehensive(file_path)
    
    # Print summary
    print_analysis_summary(results)
    
    # Print detailed chapter analysis
    print_chapter_analysis(results)
    
    # Show output file location
    if 'output_files' in results and results['output_files']:
        print(f"\\n📁 Detailed results saved to: {results['output_files'][0]}")


if __name__ == "__main__":
    main()
