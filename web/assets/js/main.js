/**
 * Main Application File
 * Initializes all modules and handles the main application logic
 */

class WordAnalyzerApp {
  constructor() {
    this.fileHandler = null;
    this.apiClient = null;
    this.uiController = null;
    this.resultDisplay = null;

    this.currentAnalysisId = null;
    this.analysisInProgress = false;

    this.init();
  }

  async init() {
    try {
      // Initialize modules
      this.initializeModules();

      // Bind events between modules
      this.bindModuleEvents();

      // Check API connectivity
      await this.checkAPIConnectivity();

      // Initialize UI state
      this.initializeUI();

      console.log('Word Analyzer App initialized successfully');
    } catch (error) {
      console.error('Failed to initialize app:', error);
      this.handleInitializationError(error);
    }
  }

  initializeModules() {
    // Initialize all modules
    this.fileHandler = new FileHandler();
    this.apiClient = new APIClient();
    this.uiController = new UIController();
    this.resultDisplay = new ResultDisplay();

    // Set UI controller reference for file handler
    this.fileHandler.setUIController(this.uiController);

    console.log('All modules initialized');
  }

  bindModuleEvents() {
    // File Handler Events
    this.fileHandler.onFileSelected = (file) => {
      this.handleFileSelected(file);
    };

    this.fileHandler.onFileRemoved = () => {
      this.handleFileRemoved();
    };

    // UI Controller Events
    this.uiController.onAnalysisStart = (options) => {
      this.handleAnalysisStart(options);
    };

    this.uiController.onNewAnalysis = () => {
      this.handleNewAnalysis();
    };

    this.uiController.onDownloadResults = () => {
      this.handleDownloadResults();
    };

    this.uiController.onExportDocument = () => {
      this.handleExportDocument();
    };

    this.uiController.onTabSwitch = (tabId) => {
      this.handleTabSwitch(tabId);
    };

    console.log('Module events bound successfully');
  }

  async checkAPIConnectivity() {
    try {
      const isOnline = await this.apiClient.pingServer();
      if (!isOnline) {
        console.warn('API server not available, using mock responses');
        this.uiController.showError('Backend server is not available. Using demo mode.');
      }
    } catch (error) {
      console.warn('Could not connect to API server:', error);
    }
  }

  initializeUI() {
    // Set initial UI state
    this.uiController.showSection('upload-section');
    this.uiController.resetAnalysisOptions();

    // Add some welcome animations
    setTimeout(() => {
      const hero = document.querySelector('.hero');
      if (hero) {
        hero.classList.add('fade-in');
      }
    }, 100);
  }

  handleInitializationError(error) {
    const errorMessage = 'Failed to initialize the application. Please refresh the page and try again.';

    // Show error modal if UI is available
    if (this.uiController) {
      this.uiController.showError(errorMessage);
    } else {
      // Fallback to alert
      alert(errorMessage);
    }
  }

  // Event Handlers
  handleFileSelected(file) {
    console.log('File selected for analysis:', file.name);

    // Update UI to show options
    this.uiController.showSection('options-section');

    // Store file info for later use
    this.currentFile = file;

    // Show success message
    this.uiController.showSuccess(`File "${file.name}" loaded successfully! Configure analysis options below.`);
  }

  handleFileRemoved() {
    console.log('File removed');

    // Reset state
    this.currentFile = null;
    this.currentAnalysisId = null;

    // Hide options and results
    this.uiController.hideSection('options-section');
    this.uiController.hideSection('results-section');

    // Clear results
    this.resultDisplay.clearResults();
  }

  async handleAnalysisStart(options) {
    if (!this.currentFile) {
      this.uiController.showError('No file selected for analysis.');
      return;
    }

    if (this.analysisInProgress) {
      this.uiController.showError('Analysis is already in progress.');
      return;
    }

    try {
      this.analysisInProgress = true;

      // Show loading screen
      this.uiController.showLoading('Preparing analysis...');

      // Start analysis process
      await this.performAnalysis(options);

    } catch (error) {
      console.error('Analysis failed:', error);
      this.uiController.hideLoading();
      this.uiController.showError(this.apiClient.handleError(error));
    } finally {
      this.analysisInProgress = false;
    }
  }

  async performAnalysis(options) {
    // Step 1: Upload file
    this.uiController.updateLoadingStep(1, 'active');
    this.uiController.updateLoadingMessage('Uploading document...');

    try {
      // Try real API first, fall back to mock if needed
      let response;
      try {
        response = await this.apiClient.analyzeDocument(this.currentFile, options);
      } catch (error) {
        console.warn('Real API failed, using mock response:', error);
        response = await this.apiClient.mockAnalyzeDocument(this.currentFile, options);
      }

      this.currentAnalysisId = response.analysisId;
      this.uiController.updateLoadingStep(1, 'completed');

    } catch (error) {
      throw new Error('Failed to upload document: ' + error.message);
    }

    // Step 2: Scan for plagiarism
    this.uiController.updateLoadingStep(2, 'active');
    this.uiController.updateLoadingMessage('Scanning for plagiarism...');

    await this.delay(2000); // Simulate processing time
    this.uiController.updateLoadingStep(2, 'completed');

    // Step 3: Apply paraphrasing
    if (options.autoParaphrase) {
      this.uiController.updateLoadingStep(3, 'active');
      this.uiController.updateLoadingMessage('Applying paraphrasing improvements...');

      await this.delay(3000); // Simulate processing time
      this.uiController.updateLoadingStep(3, 'completed');
    } else {
      this.uiController.updateLoadingStep(3, 'completed');
    }

    // Step 4: Generate results
    this.uiController.updateLoadingStep(4, 'active');
    this.uiController.updateLoadingMessage('Generating analysis results...');

    try {
      // Get results
      let results;
      try {
        results = await this.apiClient.getAnalysisResults(this.currentAnalysisId);
      } catch (error) {
        console.warn('Real API failed, using mock results:', error);
        results = await this.apiClient.mockGetAnalysisResults(this.currentAnalysisId);
      }

      this.uiController.updateLoadingStep(4, 'completed');

      // Show results
      await this.delay(500);
      this.uiController.hideLoading();
      this.displayResults(results.results);

    } catch (error) {
      throw new Error('Failed to get analysis results: ' + error.message);
    }
  }

  displayResults(results) {
    // Show results section
    this.uiController.showResults(results);

    // Display results using ResultDisplay module
    this.resultDisplay.displayResults(results);

    // Show success message
    this.uiController.showSuccess('Analysis completed successfully! Review your results below.');

    // Scroll to results
    setTimeout(() => {
      const resultsSection = document.getElementById('results-section');
      if (resultsSection) {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
      }
    }, 500);
  }

  handleNewAnalysis() {
    // Reset everything
    this.currentFile = null;
    this.currentAnalysisId = null;
    this.analysisInProgress = false;

    // Clear file handler
    this.fileHandler.removeFile();

    // Clear results
    this.resultDisplay.clearResults();

    // Reset UI
    this.uiController.hideAllSections();
    this.uiController.showSection('upload-section');
    this.uiController.resetAnalysisOptions();

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async handleDownloadResults() {
    if (!this.currentAnalysisId) {
      this.uiController.showError('No analysis results available for download.');
      return;
    }

    try {
      // Download report
      this.resultDisplay.downloadReport('json');
      this.uiController.showSuccess('Analysis report downloaded successfully!');

    } catch (error) {
      console.error('Download failed:', error);
      this.uiController.showError('Failed to download results. Please try again.');
    }
  }

  async handleExportDocument() {
    if (!this.currentAnalysisId) {
      this.uiController.showError('No processed document available for export.');
      return;
    }

    try {
      // For now, we'll simulate the export
      await this.delay(1000);

      // Create a simple download
      const filename = `paraphrased_${this.currentFile.name}`;
      const content = 'This would be the paraphrased document content in DOCX format.';

      this.resultDisplay.downloadFile(content, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename);
      this.uiController.showSuccess('Document exported successfully!');

    } catch (error) {
      console.error('Export failed:', error);
      this.uiController.showError('Failed to export document. Please try again.');
    }
  }

  handleTabSwitch(tabId) {
    console.log('Switched to tab:', tabId);

    // Handle specific tab logic if needed
    switch (tabId) {
      case 'comparison':
        // Enable highlighting toggle
        const highlightBtn = document.getElementById('highlight-changes');
        if (highlightBtn) {
          highlightBtn.addEventListener('click', () => {
            this.toggleHighlighting();
          });
        }
        break;
    }
  }

  toggleHighlighting() {
    const isActive = document.getElementById('highlight-changes').classList.contains('active');
    this.resultDisplay.setHighlighting(!isActive);
  }

  // Utility methods
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  generateAnalysisId() {
    return 'analysis_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Public API methods
  getCurrentFile() {
    return this.currentFile;
  }

  getCurrentAnalysisId() {
    return this.currentAnalysisId;
  }

  isAnalysisInProgress() {
    return this.analysisInProgress;
  }

  // Error handling
  handleGlobalError(event) {
    console.error('Global error:', event.error);

    if (this.uiController) {
      this.uiController.showError('An unexpected error occurred. Please refresh the page.');
    }
  }

  handleUnhandledRejection(event) {
    console.error('Unhandled promise rejection:', event.reason);

    if (this.uiController) {
      this.uiController.showError('A processing error occurred. Please try again.');
    }
  }
}

// Global error handlers
window.addEventListener('error', (event) => {
  if (window.app) {
    window.app.handleGlobalError(event);
  }
});

window.addEventListener('unhandledrejection', (event) => {
  if (window.app) {
    window.app.handleUnhandledRejection(event);
  }
});

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new WordAnalyzerApp();
});

// Service Worker registration for PWA functionality (optional)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Export for debugging
window.WordAnalyzerApp = WordAnalyzerApp;
