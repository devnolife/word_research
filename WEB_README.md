# Word Research Analyzer - Web Frontend

A modern web-based frontend application for document analysis, plagiarism detection, and automatic paraphrasing.

## 🌟 Features

### Core Functionality
- **File Upload**: Drag & drop or browse to upload Word documents (.docx, .doc)
- **Plagiarism Detection**: Scan documents for potential plagiarism issues
- **Automatic Paraphrasing**: Rephrase content to improve originality
- **Structure Analysis**: Analyze document organization and layout
- **Quality Metrics**: Assess writing quality and readability

### User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations
- **Real-time Progress**: Live updates during document processing
- **Interactive Dashboard**: Comprehensive results with tabbed interface
- **Side-by-side Comparison**: Original vs paraphrased content view

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Install Web Server Dependencies**
   ```bash
   pip install -r web_requirements.txt
   ```

2. **Start the Web Server**
   ```bash
   python app.py
   ```

3. **Access the Application**
   Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
web/
├── index.html              # Main application page
├── assets/
│   ├── css/
│   │   ├── main.css         # Core styles
│   │   ├── components.css   # Component styles
│   │   └── responsive.css   # Mobile responsiveness
│   └── js/
│       ├── file-handler.js  # File upload logic
│       ├── api-client.js    # Backend API communication
│       ├── ui-controller.js # Interface state management
│       ├── result-display.js # Results visualization
│       └── main.js          # Main application logic
app.py                      # Flask web server
web_requirements.txt        # Web dependencies
```

## 🔧 Configuration

### File Upload Settings
- **Max File Size**: 100MB
- **Supported Formats**: .docx, .doc
- **Upload Method**: Drag & drop or file browser

### Analysis Options
- **Plagiarism Detection**: Check for content similarities
- **Auto Paraphrasing**: Three intensity levels (Light, Moderate, Heavy)
- **Structure Analysis**: Document organization assessment
- **Quality Metrics**: Readability and clarity evaluation

## 💻 Usage Guide

### 1. Upload Document
- Drag and drop your Word document onto the upload area
- Or click "Browse Files" to select a document
- File will be validated and preview shown

### 2. Configure Analysis
- Select desired analysis options:
  - ✅ Plagiarism Detection (recommended)
  - ✅ Automatic Paraphrasing (recommended)
  - ⬜ Structure Analysis (optional)
  - ⬜ Quality Metrics (optional)
- Choose paraphrasing intensity if enabled
- Click "Start Analysis"

### 3. Monitor Progress
- Real-time progress indicator shows processing steps:
  1. **Uploading**: Document upload to server
  2. **Scanning**: Plagiarism detection analysis
  3. **Paraphrasing**: Content improvement processing
  4. **Complete**: Results generation

### 4. Review Results
- **Summary Cards**: Quick overview of key metrics
- **Detailed Tabs**: In-depth analysis results
  - **Overview**: Document statistics
  - **Plagiarism**: Similarity findings
  - **Paraphrasing**: Content improvements
  - **Comparison**: Side-by-side view

### 5. Export Results
- Download analysis report (JSON format)
- Export improved document (Word format)
- Save comparison highlights

## 🎨 Design Guidelines

### Visual Design
- **Color Scheme**: Professional blues and grays
- **Typography**: Inter font family for clarity
- **Icons**: Font Awesome for consistency
- **Animations**: Smooth transitions and loading states

### User Experience
- **Progressive Disclosure**: Show options step by step
- **Clear Feedback**: Success/error messages and progress indicators
- **Accessibility**: ARIA labels and keyboard navigation
- **Mobile-First**: Responsive design for all devices

## 🔌 API Endpoints

### Core Endpoints
- `POST /api/analyze` - Start document analysis
- `GET /api/analysis/{id}/status` - Check analysis progress
- `GET /api/analysis/{id}/results` - Get analysis results
- `GET /api/analysis/{id}/download` - Download processed document

### Health Check
- `GET /api/health` - Server health and status

## 🛠️ Development

### Frontend Architecture
- **Modular Design**: Separate modules for different functionality
- **Event-Driven**: Communication between modules via events
- **Error Handling**: Comprehensive error catching and user feedback
- **Progressive Enhancement**: Works with basic functionality, enhanced with JavaScript

### Key Components

1. **FileHandler**: Manages file upload, validation, and drag & drop
2. **APIClient**: Handles server communication with retry logic
3. **UIController**: Manages interface state and user interactions
4. **ResultDisplay**: Visualizes analysis results and comparisons
5. **Main App**: Coordinates all modules and handles application flow

### Browser Compatibility
- **Modern Browsers**: Chrome 60+, Firefox 60+, Safari 12+, Edge 79+
- **Mobile Browsers**: iOS Safari 12+, Chrome Mobile 60+
- **Features Used**: Fetch API, CSS Grid, Flexbox, ES6 modules

## 🐛 Troubleshooting

### Common Issues

**File Upload Fails**
- Check file size (max 100MB)
- Ensure file format is .docx or .doc
- Verify internet connection

**Analysis Doesn't Start**
- Refresh the page and try again
- Check browser console for errors
- Ensure backend server is running

**Results Not Loading**
- Wait for analysis to complete
- Check server status at `/api/health`
- Try with a smaller document

### Debug Mode
Enable browser developer tools to see detailed logging and error messages.

## 🚀 Deployment

### Development Server
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress (Windows)
waitress-serve --host 0.0.0.0 --port 5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r web_requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📋 Requirements

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for processing
- **Network**: Internet connection for API communication

### Browser Requirements
- **JavaScript**: Must be enabled
- **Local Storage**: For temporary data storage
- **File API**: For drag & drop functionality

## 🔒 Security

### File Upload Security
- File type validation on both client and server
- File size limits to prevent DoS attacks
- Secure filename handling
- Temporary file cleanup

### API Security
- CORS configuration for cross-origin requests
- Request size limits
- Error message sanitization

## 📈 Performance

### Optimization Features
- **Lazy Loading**: Results loaded on demand
- **File Streaming**: Large file handling
- **Progress Tracking**: Real-time progress updates
- **Caching**: Browser caching for static assets

### Performance Tips
- Use smaller documents for faster processing
- Enable browser caching
- Close unused browser tabs during analysis

## 🆘 Support

### Getting Help
1. Check this README for common solutions
2. Review browser console for error messages
3. Verify backend server is running
4. Check network connectivity

### Reporting Issues
Include the following information:
- Browser and version
- Operating system
- File type and size
- Error messages or console logs
- Steps to reproduce the issue

## 📄 License

This project is part of the Word Research Analyzer system. See the main project README for license information.

---

**Word Research Analyzer Web Frontend** - Making document analysis accessible through a modern web interface.
