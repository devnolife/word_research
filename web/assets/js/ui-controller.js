/**
 * UI Controller Module
 * Manages UI state, navigation, and user interactions
 */

class UIController {
  constructor() {
    this.currentSection = 'home';
    this.modals = {
      error: null,
      success: null
    };

    this.initializeElements();
    this.bindEvents();
  }

  initializeElements() {
    // Sections
    this.sections = {
      upload: document.getElementById('upload-section'),
      options: document.getElementById('options-section'),
      loading: document.getElementById('loading-section'),
      results: document.getElementById('results-section')
    };

    // Modals
    this.modals.error = document.getElementById('error-modal');
    this.modals.success = document.getElementById('success-modal');

    // Modal elements
    this.errorMessage = document.getElementById('error-message');
    this.successMessage = document.getElementById('success-message');

    // Navigation
    this.navLinks = document.querySelectorAll('.nav-link');

    // Analysis options
    this.analysisOptions = {
      plagiarismCheck: document.getElementById('plagiarism-check'),
      autoParaphrase: document.getElementById('auto-paraphrase'),
      structureAnalysis: document.getElementById('structure-analysis'),
      qualityMetrics: document.getElementById('quality-metrics')
    };

    this.intensityOptions = document.querySelectorAll('input[name="intensity"]');
    this.startAnalysisBtn = document.getElementById('start-analysis');

    // Results elements
    this.newAnalysisBtn = document.getElementById('new-analysis');
    this.downloadResultsBtn = document.getElementById('download-results');

    // Tab system
    this.tabButtons = document.querySelectorAll('.tab-btn');
    this.tabPanels = document.querySelectorAll('.tab-panel');

    // Loading steps
    this.loadingSteps = document.querySelectorAll('.step');
    this.loadingMessage = document.getElementById('loading-message');

    // Comparison controls
    this.highlightChangesBtn = document.getElementById('highlight-changes');
    this.exportDocumentBtn = document.getElementById('export-document');
  }

  bindEvents() {
    // Navigation
    this.navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        this.handleNavigation(link.getAttribute('href'));
      });
    });

    // Analysis options - auto paraphrase dependency
    this.analysisOptions.autoParaphrase.addEventListener('change', () => {
      this.toggleIntensitySelector();
    });

    // Start analysis button
    this.startAnalysisBtn.addEventListener('click', () => {
      this.handleStartAnalysis();
    });

    // New analysis button
    this.newAnalysisBtn.addEventListener('click', () => {
      this.handleNewAnalysis();
    });

    // Download results button
    this.downloadResultsBtn.addEventListener('click', () => {
      this.handleDownloadResults();
    });

    // Tab system
    this.tabButtons.forEach(button => {
      button.addEventListener('click', () => {
        this.switchTab(button.getAttribute('data-tab'));
      });
    });

    // Modal close events
    this.bindModalEvents();

    // Comparison controls
    if (this.highlightChangesBtn) {
      this.highlightChangesBtn.addEventListener('click', () => {
        this.toggleHighlights();
      });
    }

    if (this.exportDocumentBtn) {
      this.exportDocumentBtn.addEventListener('click', () => {
        this.handleExportDocument();
      });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      this.handleKeyboardShortcuts(e);
    });
  }

  bindModalEvents() {
    // Error modal
    const errorCloseBtn = document.getElementById('error-modal-close');
    const errorOkBtn = document.getElementById('error-modal-ok');

    if (errorCloseBtn) {
      errorCloseBtn.addEventListener('click', () => this.hideModal('error'));
    }
    if (errorOkBtn) {
      errorOkBtn.addEventListener('click', () => this.hideModal('error'));
    }

    // Success modal
    const successCloseBtn = document.getElementById('success-modal-close');
    const successOkBtn = document.getElementById('success-modal-ok');

    if (successCloseBtn) {
      successCloseBtn.addEventListener('click', () => this.hideModal('success'));
    }
    if (successOkBtn) {
      successOkBtn.addEventListener('click', () => this.hideModal('success'));
    }

    // Close modals on backdrop click
    Object.values(this.modals).forEach(modal => {
      if (modal) {
        modal.addEventListener('click', (e) => {
          if (e.target === modal) {
            this.hideAllModals();
          }
        });
      }
    });

    // Close modals on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.hideAllModals();
      }
    });
  }

  // Section Management
  showSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
      section.style.display = 'block';
      section.classList.add('fade-in-up');
      this.currentSection = sectionId;
    }
  }

  hideSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
      section.style.display = 'none';
      section.classList.remove('fade-in-up');
    }
  }

  hideAllSections() {
    Object.values(this.sections).forEach(section => {
      if (section) {
        section.style.display = 'none';
        section.classList.remove('fade-in-up');
      }
    });
  }

  // Navigation
  handleNavigation(href) {
    const targetId = href.replace('#', '');

    // Update active nav link
    this.navLinks.forEach(link => link.classList.remove('active'));
    document.querySelector(`[href="${href}"]`).classList.add('active');

    // Handle specific navigation
    switch (targetId) {
      case 'home':
        this.showHomeView();
        break;
      case 'features':
        this.showFeaturesView();
        break;
      case 'help':
        this.showHelpView();
        break;
    }
  }

  showHomeView() {
    this.hideAllSections();
    this.showSection('upload-section');
  }

  showFeaturesView() {
    // This could scroll to a features section or show a features modal
    console.log('Show features view');
  }

  showHelpView() {
    // This could show a help modal or navigate to help page
    console.log('Show help view');
  }

  // Analysis Options
  getAnalysisOptions() {
    const selectedIntensity = document.querySelector('input[name="intensity"]:checked');

    return {
      plagiarismCheck: this.analysisOptions.plagiarismCheck.checked,
      autoParaphrase: this.analysisOptions.autoParaphrase.checked,
      structureAnalysis: this.analysisOptions.structureAnalysis.checked,
      qualityMetrics: this.analysisOptions.qualityMetrics.checked,
      paraphraseIntensity: selectedIntensity ? selectedIntensity.value : 'moderate'
    };
  }

  toggleIntensitySelector() {
    const intensitySelector = document.getElementById('intensity-selector');
    if (this.analysisOptions.autoParaphrase.checked) {
      intensitySelector.style.display = 'block';
    } else {
      intensitySelector.style.display = 'none';
    }
  }

  handleStartAnalysis() {
    const options = this.getAnalysisOptions();
    console.log('Starting analysis with options:', options);

    // Trigger analysis start event
    this.onAnalysisStart(options);
  }

  handleNewAnalysis() {
    this.hideAllSections();
    this.showSection('upload-section');
    this.resetAnalysisOptions();

    // Trigger new analysis event
    this.onNewAnalysis();
  }

  resetAnalysisOptions() {
    this.analysisOptions.plagiarismCheck.checked = true;
    this.analysisOptions.autoParaphrase.checked = true;
    this.analysisOptions.structureAnalysis.checked = false;
    this.analysisOptions.qualityMetrics.checked = false;

    const moderateIntensity = document.getElementById('moderate');
    if (moderateIntensity) {
      moderateIntensity.checked = true;
    }

    this.toggleIntensitySelector();
  }

  // Loading Management
  showLoading(message = 'Preparing analysis...') {
    this.hideAllSections();
    this.showSection('loading-section');
    this.updateLoadingMessage(message);
    this.resetLoadingSteps();
  }

  hideLoading() {
    this.hideSection('loading-section');
  }

  updateLoadingMessage(message) {
    if (this.loadingMessage) {
      this.loadingMessage.textContent = message;
    }
  }

  updateLoadingStep(stepNumber, status = 'active') {
    // Reset all steps
    this.loadingSteps.forEach(step => {
      step.classList.remove('active', 'completed');
    });

    // Update steps up to current
    for (let i = 1; i <= stepNumber; i++) {
      const step = document.getElementById(`step-${i}`);
      if (step) {
        if (i === stepNumber && status === 'active') {
          step.classList.add('active');
        } else if (i < stepNumber) {
          step.classList.add('completed');
        }
      }
    }

    // Complete current step if specified
    if (status === 'completed') {
      const currentStep = document.getElementById(`step-${stepNumber}`);
      if (currentStep) {
        currentStep.classList.remove('active');
        currentStep.classList.add('completed');
      }
    }
  }

  resetLoadingSteps() {
    this.loadingSteps.forEach(step => {
      step.classList.remove('active', 'completed');
    });
  }

  // Tab Management
  switchTab(tabId) {
    // Update tab buttons
    this.tabButtons.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

    // Update tab panels
    this.tabPanels.forEach(panel => panel.classList.remove('active'));
    document.getElementById(`${tabId}-panel`).classList.add('active');

    // Trigger tab switch event
    this.onTabSwitch(tabId);
  }

  // Modal Management
  showModal(type, message) {
    const modal = this.modals[type];
    const messageElement = type === 'error' ? this.errorMessage : this.successMessage;

    if (modal && messageElement) {
      messageElement.textContent = message;
      modal.classList.add('show');
    }
  }

  hideModal(type) {
    const modal = this.modals[type];
    if (modal) {
      modal.classList.remove('show');
    }
  }

  hideAllModals() {
    Object.values(this.modals).forEach(modal => {
      if (modal) {
        modal.classList.remove('show');
      }
    });
  }

  showError(message) {
    this.showModal('error', message);
  }

  showSuccess(message) {
    this.showModal('success', message);
  }

  // Results Management
  showResults(results) {
    this.hideAllSections();
    this.showSection('results-section');

    // This will be handled by ResultDisplay module
    this.onResultsReady(results);
  }

  handleDownloadResults() {
    console.log('Download results clicked');
    this.onDownloadResults();
  }

  // Comparison View
  toggleHighlights() {
    const isActive = this.highlightChangesBtn.classList.contains('active');

    if (isActive) {
      this.highlightChangesBtn.classList.remove('active');
      this.hideHighlights();
    } else {
      this.highlightChangesBtn.classList.add('active');
      this.showHighlights();
    }
  }

  showHighlights() {
    const changes = document.querySelectorAll('.highlight-added, .highlight-removed');
    changes.forEach(element => {
      element.style.display = 'inline';
    });
  }

  hideHighlights() {
    const changes = document.querySelectorAll('.highlight-added, .highlight-removed');
    changes.forEach(element => {
      element.style.display = 'none';
    });
  }

  handleExportDocument() {
    console.log('Export document clicked');
    this.onExportDocument();
  }

  // Keyboard Shortcuts
  handleKeyboardShortcuts(e) {
    // Ctrl/Cmd + Enter to start analysis
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      if (this.currentSection === 'options-section') {
        this.handleStartAnalysis();
      }
    }

    // Ctrl/Cmd + N for new analysis
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
      e.preventDefault();
      this.handleNewAnalysis();
    }
  }

  // Utility Methods
  addLoadingClass(element) {
    if (element) {
      element.classList.add('loading');
    }
  }

  removeLoadingClass(element) {
    if (element) {
      element.classList.remove('loading');
    }
  }

  disableButton(button) {
    if (button) {
      button.disabled = true;
      button.classList.add('disabled');
    }
  }

  enableButton(button) {
    if (button) {
      button.disabled = false;
      button.classList.remove('disabled');
    }
  }

  // Event Callbacks (to be overridden by main app)
  onAnalysisStart(options) {
    console.log('Analysis start event:', options);
  }

  onNewAnalysis() {
    console.log('New analysis event');
  }

  onResultsReady(results) {
    console.log('Results ready event:', results);
  }

  onDownloadResults() {
    console.log('Download results event');
  }

  onExportDocument() {
    console.log('Export document event');
  }

  onTabSwitch(tabId) {
    console.log('Tab switch event:', tabId);
  }
}

// Export for use in other modules
window.UIController = UIController;
