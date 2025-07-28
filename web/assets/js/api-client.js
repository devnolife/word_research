/**
 * API Client Module
 * Handles communication with the backend API
 */

class APIClient {
  constructor() {
    this.baseURL = window.location.origin;
    this.apiURL = this.baseURL + '/api';
    this.timeout = 300000; // 5 minutes
    this.retryAttempts = 3;
    this.retryDelay = 1000; // 1 second
  }

  /**
   * Make HTTP request with retry logic
   */
  async makeRequest(url, options = {}) {
    const defaultOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: this.timeout,
      ...options
    };

    for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), defaultOptions.timeout);

        const response = await fetch(url, {
          ...defaultOptions,
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          return await response.json();
        } else {
          return await response.text();
        }

      } catch (error) {
        console.error(`API request attempt ${attempt} failed:`, error);

        if (attempt === this.retryAttempts) {
          throw error;
        }

        // Wait before retrying
        await this.delay(this.retryDelay * attempt);
      }
    }
  }

  /**
   * Upload file with progress tracking
   */
  async uploadFile(file, options = {}, progressCallback = null) {
    return new Promise((resolve, reject) => {
      const formData = new FormData();
      formData.append('file', file);

      // Add analysis options
      if (options.plagiarismCheck !== undefined) {
        formData.append('plagiarism_check', options.plagiarismCheck);
      }
      if (options.autoParaphrase !== undefined) {
        formData.append('auto_paraphrase', options.autoParaphrase);
      }
      if (options.structureAnalysis !== undefined) {
        formData.append('structure_analysis', options.structureAnalysis);
      }
      if (options.qualityMetrics !== undefined) {
        formData.append('quality_metrics', options.qualityMetrics);
      }
      if (options.paraphraseIntensity) {
        formData.append('paraphrase_intensity', options.paraphraseIntensity);
      }

      const xhr = new XMLHttpRequest();

      // Progress tracking
      if (progressCallback) {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            progressCallback(percentComplete);
          }
        });
      }

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            resolve(response);
          } catch (error) {
            reject(new Error('Invalid JSON response'));
          }
        } else {
          reject(new Error(`Upload failed: ${xhr.status} ${xhr.statusText}`));
        }
      });

      xhr.addEventListener('error', () => {
        reject(new Error('Upload failed: Network error'));
      });

      xhr.addEventListener('timeout', () => {
        reject(new Error('Upload failed: Request timeout'));
      });

      xhr.timeout = this.timeout;
      xhr.open('POST', `${this.apiURL}/analyze`, true);
      xhr.send(formData);
    });
  }

  /**
   * Start document analysis
   */
  async analyzeDocument(file, options = {}) {
    try {
      const analysisOptions = {
        plagiarismCheck: options.plagiarismCheck || false,
        autoParaphrase: options.autoParaphrase || false,
        structureAnalysis: options.structureAnalysis || false,
        qualityMetrics: options.qualityMetrics || false,
        paraphraseIntensity: options.paraphraseIntensity || 'moderate'
      };

      console.log('Starting analysis with options:', analysisOptions);

      const response = await this.uploadFile(file, analysisOptions, (progress) => {
        console.log(`Upload progress: ${progress}%`);
      });

      return response;

    } catch (error) {
      console.error('Analysis failed:', error);
      throw new Error(`Analysis failed: ${error.message}`);
    }
  }

  /**
   * Get analysis status
   */
  async getAnalysisStatus(analysisId) {
    try {
      const response = await this.makeRequest(`${this.apiURL}/analysis/${analysisId}/status`);
      return response;
    } catch (error) {
      console.error('Failed to get analysis status:', error);
      throw error;
    }
  }

  /**
   * Get analysis results
   */
  async getAnalysisResults(analysisId) {
    try {
      const response = await this.makeRequest(`${this.apiURL}/analysis/${analysisId}/results`);
      return response;
    } catch (error) {
      console.error('Failed to get analysis results:', error);
      throw error;
    }
  }

  /**
   * Download processed document
   */
  async downloadDocument(analysisId, format = 'docx') {
    try {
      const url = `${this.apiURL}/analysis/${analysisId}/download?format=${format}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Download failed: ${response.status} ${response.statusText}`);
      }

      const blob = await response.blob();
      return blob;
    } catch (error) {
      console.error('Download failed:', error);
      throw error;
    }
  }

  /**
   * Get plagiarism report
   */
  async getPlagiarismReport(analysisId) {
    try {
      const response = await this.makeRequest(`${this.apiURL}/analysis/${analysisId}/plagiarism`);
      return response;
    } catch (error) {
      console.error('Failed to get plagiarism report:', error);
      throw error;
    }
  }

  /**
   * Get paraphrasing details
   */
  async getParaphrasingDetails(analysisId) {
    try {
      const response = await this.makeRequest(`${this.apiURL}/analysis/${analysisId}/paraphrasing`);
      return response;
    } catch (error) {
      console.error('Failed to get paraphrasing details:', error);
      throw error;
    }
  }

  /**
   * Mock API responses for testing (when backend is not available)
   */
  async mockAnalyzeDocument(file, options = {}) {
    console.log('Using mock API responses');

    // Simulate upload progress
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          analysisId: 'mock-' + Date.now(),
          message: 'Analysis started successfully',
          estimatedTime: '2-3 minutes'
        });
      }, 1000);
    });
  }

  async mockGetAnalysisResults(analysisId) {
    console.log('Using mock analysis results');

    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          status: 'completed',
          results: {
            plagiarism: {
              score: 15,
              status: 'Low Risk',
              details: [
                {
                  text: 'This is a sample sentence that might have plagiarism.',
                  similarity: 85,
                  source: 'Academic Database'
                }
              ]
            },
            paraphrasing: {
              sentencesModified: 42,
              status: 'Significant Improvements',
              changes: [
                {
                  original: 'Original sentence text here.',
                  paraphrased: 'Improved sentence text here.',
                  confidence: 0.92
                }
              ]
            },
            quality: {
              score: 87,
              status: 'Excellent',
              metrics: {
                readability: 85,
                clarity: 89,
                coherence: 88
              }
            },
            document: {
              words: 3918,
              paragraphs: 204,
              pages: 16,
              readingTime: 19.59
            }
          }
        });
      }, 2000);
    });
  }

  /**
   * Utility functions
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  isOnline() {
    return navigator.onLine;
  }

  async pingServer() {
    try {
      const response = await fetch(`${this.apiURL}/health`, {
        method: 'GET',
        timeout: 5000
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  /**
   * Error handling
   */
  handleError(error) {
    console.error('API Error:', error);

    if (error.name === 'AbortError') {
      return 'Request timeout. Please try again.';
    }

    if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
      return 'Network error. Please check your internet connection.';
    }

    if (error.message.includes('413')) {
      return 'File too large. Please upload a smaller file.';
    }

    if (error.message.includes('415')) {
      return 'Unsupported file format. Please upload a .docx or .doc file.';
    }

    if (error.message.includes('500')) {
      return 'Server error. Please try again later.';
    }

    return error.message || 'An unexpected error occurred.';
  }
}

// Export for use in other modules
window.APIClient = APIClient;
