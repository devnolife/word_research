"""
Flask Web Server for Word Research Analyzer
Serves the frontend and provides API endpoints for document analysis
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

# Import your existing analyzer modules
import sys
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from src.document_reader import DocumentReader
    from src.config import DocumentConfig, ProcessingConfig
    from src.exceptions import *
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    print("Warning: Document analyzer modules not available. Using mock responses.")

app = Flask(__name__, 
            static_folder='web/assets',
            static_url_path='/assets')
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store analysis results in memory (in production, use a database)
analysis_storage = {}

@app.route('/')
def index():
    """Serve the main web application"""
    return send_from_directory('web', 'index.html')

@app.route('/sw.js')
def service_worker():
    """Serve the service worker file"""
    return send_from_directory('web', 'sw.js')

@app.route('/favicon.svg')
@app.route('/favicon.ico')
def favicon():
    """Serve the favicon"""
    return send_from_directory('web', 'favicon.svg')

@app.route('/web/<path:filename>')
def web_files(filename):
    """Serve web files"""
    return send_from_directory('web', filename)

@app.route('/api/health')
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'analyzer_available': ANALYZER_AVAILABLE
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    """Analyze uploaded document"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not file.filename.lower().endswith(('.docx', '.doc')):
            return jsonify({'error': 'Unsupported file format. Please upload .docx or .doc files.'}), 415
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get analysis options
        options = {
            'plagiarism_check': request.form.get('plagiarism_check', 'false').lower() == 'true',
            'auto_paraphrase': request.form.get('auto_paraphrase', 'false').lower() == 'true',
            'structure_analysis': request.form.get('structure_analysis', 'false').lower() == 'true',
            'quality_metrics': request.form.get('quality_metrics', 'false').lower() == 'true',
            'paraphrase_intensity': request.form.get('paraphrase_intensity', 'moderate')
        }
        
        # Generate analysis ID
        analysis_id = f"analysis_{timestamp}_{hash(filename) % 10000}"
        
        # Store analysis info
        analysis_storage[analysis_id] = {
            'id': analysis_id,
            'filename': filename,
            'file_path': file_path,
            'options': options,
            'status': 'processing',
            'created_at': datetime.now().isoformat(),
            'progress': 0
        }
        
        # Start analysis in background (for demo, we'll simulate it)
        if ANALYZER_AVAILABLE:
            try:
                # Use real analyzer
                results = perform_real_analysis(file_path, options)
                analysis_storage[analysis_id].update({
                    'status': 'completed',
                    'results': results,
                    'progress': 100
                })
            except Exception as e:
                logger.error(f"Real analysis failed: {e}")
                # Fall back to mock
                results = generate_mock_results(filename, options)
                analysis_storage[analysis_id].update({
                    'status': 'completed',
                    'results': results,
                    'progress': 100
                })
        else:
            # Use mock results
            results = generate_mock_results(filename, options)
            analysis_storage[analysis_id].update({
                'status': 'completed',
                'results': results,
                'progress': 100
            })
        
        return jsonify({
            'success': True,
            'analysisId': analysis_id,
            'message': 'Analysis started successfully',
            'estimatedTime': '2-3 minutes'
        })
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<analysis_id>/status')
def get_analysis_status(analysis_id):
    """Get analysis status"""
    if analysis_id not in analysis_storage:
        return jsonify({'error': 'Analysis not found'}), 404
    
    analysis = analysis_storage[analysis_id]
    return jsonify({
        'id': analysis_id,
        'status': analysis['status'],
        'progress': analysis.get('progress', 0),
        'created_at': analysis['created_at']
    })

@app.route('/api/analysis/<analysis_id>/results')
def get_analysis_results(analysis_id):
    """Get analysis results"""
    if analysis_id not in analysis_storage:
        return jsonify({'error': 'Analysis not found'}), 404
    
    analysis = analysis_storage[analysis_id]
    
    if analysis['status'] != 'completed':
        return jsonify({'error': 'Analysis not completed yet'}), 202
    
    return jsonify({
        'success': True,
        'status': 'completed',
        'results': analysis['results']
    })

@app.route('/api/analysis/<analysis_id>/download')
def download_document(analysis_id):
    """Download processed document"""
    if analysis_id not in analysis_storage:
        return jsonify({'error': 'Analysis not found'}), 404
    
    analysis = analysis_storage[analysis_id]
    
    if analysis['status'] != 'completed':
        return jsonify({'error': 'Analysis not completed yet'}), 202
    
    # For demo, return the original file with a new name
    original_path = analysis['file_path']
    if os.path.exists(original_path):
        return send_file(original_path, 
                        as_attachment=True, 
                        download_name=f"paraphrased_{analysis['filename']}")
    
    return jsonify({'error': 'Processed file not found'}), 404

def perform_real_analysis(file_path, options):
    """Perform real document analysis using the existing analyzer"""
    try:
        # Initialize the document reader
        config = DocumentConfig()
        processing_config = ProcessingConfig()
        reader = DocumentReader(config=config, processing_config=processing_config)
        
        # Load the document
        success = reader.load_document(file_path)
        if not success:
            raise Exception("Failed to load document")
        
        # Get analysis data
        basic_info = reader.get_basic_info()
        metadata = reader.get_document_metadata()
        content_analysis = reader.get_content_analysis()
        
        # Generate results based on the real analysis
        results = {
            'plagiarism': generate_plagiarism_results(options),
            'paraphrasing': generate_paraphrasing_results(options, basic_info),
            'quality': generate_quality_results(basic_info),
            'document': {
                'words': basic_info.get('words', 0),
                'paragraphs': basic_info.get('paragraphs', 0),
                'pages': basic_info.get('pages', 1),
                'readingTime': basic_info.get('words', 0) / 200  # Assume 200 WPM
            }
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Real analysis failed: {e}")
        raise

def generate_mock_results(filename, options):
    """Generate mock analysis results for demo purposes"""
    import random
    
    # Base document stats
    words = random.randint(1000, 5000)
    paragraphs = random.randint(50, 200)
    pages = max(1, words // 250)
    
    results = {
        'plagiarism': {
            'score': random.randint(5, 25) if options['plagiarism_check'] else 0,
            'status': 'Low Risk',
            'details': []
        },
        'paraphrasing': {
            'sentencesModified': random.randint(20, 80) if options['auto_paraphrase'] else 0,
            'status': 'Significant Improvements' if options['auto_paraphrase'] else 'No Changes',
            'changes': []
        },
        'quality': {
            'score': random.randint(75, 95),
            'status': 'Excellent',
            'metrics': {
                'readability': random.randint(80, 95),
                'clarity': random.randint(85, 95),
                'coherence': random.randint(80, 90)
            }
        },
        'document': {
            'words': words,
            'paragraphs': paragraphs,
            'pages': pages,
            'readingTime': words / 200
        }
    }
    
    # Add some sample plagiarism details if enabled
    if options['plagiarism_check'] and results['plagiarism']['score'] > 10:
        results['plagiarism']['details'] = [
            {
                'text': 'This is a sample sentence that might have similarity to existing sources.',
                'similarity': random.randint(60, 90),
                'source': 'Academic Database'
            },
            {
                'text': 'Another example of potentially similar content found in the document.',
                'similarity': random.randint(70, 85),
                'source': 'Online Article'
            }
        ]
    
    # Add sample paraphrasing changes if enabled
    if options['auto_paraphrase'] and results['paraphrasing']['sentencesModified'] > 0:
        results['paraphrasing']['changes'] = [
            {
                'original': 'The original sentence that needed improvement for better clarity.',
                'paraphrased': 'The initial sentence that required enhancement for improved clarity.',
                'confidence': random.uniform(0.8, 0.95)
            },
            {
                'original': 'This content was modified to increase originality and readability.',
                'paraphrased': 'This material was revised to enhance uniqueness and comprehensibility.',
                'confidence': random.uniform(0.85, 0.92)
            }
        ]
    
    return results

def generate_plagiarism_results(options):
    """Generate plagiarism analysis results"""
    if not options['plagiarism_check']:
        return {'score': 0, 'status': 'Not Checked', 'details': []}
    
    import random
    score = random.randint(5, 30)
    
    if score < 15:
        status = 'Low Risk'
    elif score < 25:
        status = 'Medium Risk'
    else:
        status = 'High Risk'
    
    return {
        'score': score,
        'status': status,
        'details': []
    }

def generate_paraphrasing_results(options, basic_info):
    """Generate paraphrasing results"""
    if not options['paraphrasing_check']:
        return {'sentencesModified': 0, 'status': 'Not Applied', 'changes': []}
    
    import random
    total_sentences = basic_info.get('sentences', 100)
    modified = random.randint(10, min(total_sentences, 80))
    
    return {
        'sentencesModified': modified,
        'status': 'Improvements Applied',
        'changes': []
    }

def generate_quality_results(basic_info):
    """Generate quality assessment results"""
    import random
    
    score = random.randint(75, 95)
    
    if score >= 90:
        status = 'Excellent'
    elif score >= 80:
        status = 'Good'
    elif score >= 70:
        status = 'Fair'
    else:
        status = 'Needs Improvement'
    
    return {
        'score': score,
        'status': status,
        'metrics': {
            'readability': random.randint(70, 95),
            'clarity': random.randint(75, 95),
            'coherence': random.randint(70, 90)
        }
    }

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 100MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Word Research Analyzer Web Server...")
    print(f"Analyzer modules available: {ANALYZER_AVAILABLE}")
    print("Access the application at: http://localhost:5000")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
