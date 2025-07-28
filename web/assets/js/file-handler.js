/**
 * File Handler Module
 * Handles file upload, validation, and drag & drop functionality
 */

class FileHandler {
  constructor(uiController = null) {
    this.currentFile = null;
    this.maxFileSize = 100 * 1024 * 1024; // 100MB
    this.allowedExtensions = ['.docx', '.doc'];
    this.uploadProgress = 0;
    this.uiController = uiController;

    this.initializeElements();
    this.bindEvents();
  }

  initializeElements() {
    // Get DOM elements
    this.uploadArea = document.getElementById('upload-area');
    this.fileInput = document.getElementById('file-input');
    this.browseBtn = document.getElementById('browse-btn');
    this.filePreview = document.getElementById('file-preview');
    this.fileName = document.getElementById('file-name');
    this.fileSize = document.getElementById('file-size');
    this.removeFileBtn = document.getElementById('remove-file');
    this.uploadProgress = document.getElementById('upload-progress');
    this.progressFill = document.getElementById('progress-fill');
    this.progressText = document.getElementById('progress-text');
  }

  bindEvents() {
    // File input change event
    this.fileInput.addEventListener('change', (e) => {
      this.handleFileSelect(e.target.files[0]);
    });

    // Browse button click
    this.browseBtn.addEventListener('click', (e) => {
      e.preventDefault();
      this.fileInput.click();
    });

    // Upload area click
    this.uploadArea.addEventListener('click', () => {
      if (!this.currentFile) {
        this.fileInput.click();
      }
    });

    // Drag and drop events
    this.uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      this.uploadArea.classList.add('dragover');
    });

    this.uploadArea.addEventListener('dragleave', (e) => {
      e.preventDefault();
      if (!this.uploadArea.contains(e.relatedTarget)) {
        this.uploadArea.classList.remove('dragover');
      }
    });

    this.uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      this.uploadArea.classList.remove('dragover');

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.handleFileSelect(files[0]);
      }
    });

    // Remove file button
    this.removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.removeFile();
    });
  }

  handleFileSelect(file) {
    if (!file) return;

    // Validate file
    const validation = this.validateFile(file);
    if (!validation.valid) {
      if (this.uiController) {
        this.uiController.showError(validation.message);
      } else {
        console.error(validation.message);
      }
      return;
    }

    // Set current file
    this.currentFile = file;

    // Show file preview
    this.showFilePreview(file);

    // Hide upload area, show options
    this.uploadArea.style.display = 'none';
    if (this.uiController) {
      this.uiController.showSection('options-section');
    }

    // Trigger file selected event
    this.onFileSelected(file);
  }

  validateFile(file) {
    // Check file type
    const extension = this.getFileExtension(file.name);
    if (!this.allowedExtensions.includes(extension.toLowerCase())) {
      return {
        valid: false,
        message: `Unsupported file type. Please upload a ${this.allowedExtensions.join(' or ')} file.`
      };
    }

    // Check file size
    if (file.size > this.maxFileSize) {
      const maxSizeMB = this.maxFileSize / (1024 * 1024);
      return {
        valid: false,
        message: `File too large. Maximum size allowed is ${maxSizeMB}MB.`
      };
    }

    // Check if file is corrupted (basic check)
    if (file.size === 0) {
      return {
        valid: false,
        message: 'File appears to be empty or corrupted.'
      };
    }

    return { valid: true };
  }

  getFileExtension(filename) {
    return filename.substring(filename.lastIndexOf('.'));
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  showFilePreview(file) {
    this.fileName.textContent = file.name;
    this.fileSize.textContent = this.formatFileSize(file.size);
    this.filePreview.style.display = 'block';
    this.filePreview.classList.add('fade-in');
  }

  hideFilePreview() {
    this.filePreview.style.display = 'none';
    this.filePreview.classList.remove('fade-in');
  }

  removeFile() {
    this.currentFile = null;
    this.fileInput.value = '';

    // Hide file preview and options
    this.hideFilePreview();
    if (this.uiController) {
      this.uiController.hideSection('options-section');
    }

    // Show upload area
    this.uploadArea.style.display = 'block';

    // Reset upload progress
    this.resetProgress();

    // Trigger file removed event
    this.onFileRemoved();
  }

  showProgress() {
    this.uploadProgress.style.display = 'block';
  }

  hideProgress() {
    this.uploadProgress.style.display = 'none';
  }

  updateProgress(percentage) {
    this.uploadProgress = Math.min(100, Math.max(0, percentage));
    this.progressFill.style.width = `${this.uploadProgress}%`;
    this.progressText.textContent = `${Math.round(this.uploadProgress)}%`;
  }

  resetProgress() {
    this.uploadProgress = 0;
    this.updateProgress(0);
    this.hideProgress();
  }

  simulateUpload(callback) {
    this.showProgress();
    let progress = 0;

    const interval = setInterval(() => {
      progress += Math.random() * 15;

      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        this.updateProgress(progress);

        setTimeout(() => {
          if (callback) callback();
        }, 500);
      } else {
        this.updateProgress(progress);
      }
    }, 200);
  }

  getCurrentFile() {
    return this.currentFile;
  }

  hasFile() {
    return this.currentFile !== null;
  }

  getFileInfo() {
    if (!this.currentFile) return null;

    return {
      name: this.currentFile.name,
      size: this.currentFile.size,
      sizeFormatted: this.formatFileSize(this.currentFile.size),
      type: this.currentFile.type,
      extension: this.getFileExtension(this.currentFile.name),
      lastModified: new Date(this.currentFile.lastModified)
    };
  }

  // Event callbacks (to be overridden)
  onFileSelected(file) {
    console.log('File selected:', file.name);
    // This can be overridden by other modules
  }

  onFileRemoved() {
    console.log('File removed');
    // This can be overridden by other modules
  }

  onUploadProgress(percentage) {
    console.log('Upload progress:', percentage + '%');
    // This can be overridden by other modules
  }

  onUploadComplete() {
    console.log('Upload complete');
    // This can be overridden by other modules
  }

  onUploadError(error) {
    console.error('Upload error:', error);
    // This can be overridden by other modules
  }

  // Method to set UI controller reference
  setUIController(uiController) {
    this.uiController = uiController;
  }
}

// Export for use in other modules
window.FileHandler = FileHandler;
