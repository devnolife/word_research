/**
 * Result Display Module
 * Handles displaying analysis results and data visualization
 */

class ResultDisplay {
  constructor() {
    this.currentResults = null;
    this.highlightingEnabled = false;

    this.initializeElements();
  }

  initializeElements() {
    // Summary cards
    this.summaryElements = {
      plagiarismScore: document.getElementById('plagiarism-score'),
      plagiarismStatus: document.getElementById('plagiarism-status'),
      modifiedSentences: document.getElementById('modified-sentences'),
      modificationStatus: document.getElementById('modification-status'),
      qualityScore: document.getElementById('quality-score'),
      qualityStatus: document.getElementById('quality-status')
    };

    // Statistics
    this.statsElements = {
      wordCount: document.getElementById('word-count'),
      paragraphCount: document.getElementById('paragraph-count'),
      pageCount: document.getElementById('page-count'),
      readingTime: document.getElementById('reading-time')
    };

    // Content panels
    this.contentPanels = {
      plagiarismResults: document.getElementById('plagiarism-results'),
      paraphrasingResults: document.getElementById('paraphrasing-results'),
      originalContent: document.getElementById('original-content'),
      paraphrasedContent: document.getElementById('paraphrased-content')
    };
  }

  displayResults(results) {
    this.currentResults = results;

    // Update summary cards
    this.updateSummaryCards(results);

    // Update document statistics
    this.updateDocumentStats(results);

    // Update detailed panels
    this.updatePlagiarismPanel(results.plagiarism);
    this.updateParaphrasingPanel(results.paraphrasing);
    this.updateComparisonView(results);

    console.log('Results displayed successfully');
  }

  updateSummaryCards(results) {
    // Plagiarism Score
    if (results.plagiarism && this.summaryElements.plagiarismScore) {
      this.summaryElements.plagiarismScore.textContent = `${results.plagiarism.score}%`;
      this.summaryElements.plagiarismStatus.textContent = results.plagiarism.status;

      // Update card color based on score
      const plagiarismCard = this.summaryElements.plagiarismScore.closest('.summary-card');
      this.updateCardStatus(plagiarismCard, results.plagiarism.score, 'plagiarism');
    }

    // Modified Sentences
    if (results.paraphrasing && this.summaryElements.modifiedSentences) {
      this.summaryElements.modifiedSentences.textContent = results.paraphrasing.sentencesModified;
      this.summaryElements.modificationStatus.textContent = results.paraphrasing.status;
    }

    // Quality Score
    if (results.quality && this.summaryElements.qualityScore) {
      this.summaryElements.qualityScore.textContent = results.quality.score;
      this.summaryElements.qualityStatus.textContent = results.quality.status;

      // Update card color based on score
      const qualityCard = this.summaryElements.qualityScore.closest('.summary-card');
      this.updateCardStatus(qualityCard, results.quality.score, 'quality');
    }
  }

  updateCardStatus(card, score, type) {
    if (!card) return;

    // Remove existing status classes
    card.classList.remove('status-excellent', 'status-good', 'status-warning', 'status-danger');

    let statusClass = 'status-good';

    if (type === 'plagiarism') {
      if (score >= 30) statusClass = 'status-danger';
      else if (score >= 15) statusClass = 'status-warning';
      else statusClass = 'status-excellent';
    } else if (type === 'quality') {
      if (score >= 90) statusClass = 'status-excellent';
      else if (score >= 75) statusClass = 'status-good';
      else if (score >= 60) statusClass = 'status-warning';
      else statusClass = 'status-danger';
    }

    card.classList.add(statusClass);
  }

  updateDocumentStats(results) {
    if (results.document) {
      const stats = results.document;

      if (this.statsElements.wordCount) {
        this.statsElements.wordCount.textContent = this.formatNumber(stats.words);
      }
      if (this.statsElements.paragraphCount) {
        this.statsElements.paragraphCount.textContent = this.formatNumber(stats.paragraphs);
      }
      if (this.statsElements.pageCount) {
        this.statsElements.pageCount.textContent = this.formatNumber(stats.pages);
      }
      if (this.statsElements.readingTime) {
        this.statsElements.readingTime.textContent = `${Math.round(stats.readingTime)} min`;
      }
    }
  }

  updatePlagiarismPanel(plagiarismData) {
    if (!plagiarismData || !this.contentPanels.plagiarismResults) return;

    const container = this.contentPanels.plagiarismResults;
    container.innerHTML = '';

    if (plagiarismData.details && plagiarismData.details.length > 0) {
      // Create plagiarism details
      const detailsContainer = this.createPlagiarismDetails(plagiarismData.details);
      container.appendChild(detailsContainer);
    } else {
      // No plagiarism found
      const noPlagiarismDiv = document.createElement('div');
      noPlagiarismDiv.className = 'content-empty';
      noPlagiarismDiv.innerHTML = `
                <i class="fas fa-shield-alt"></i>
                <h4>No Plagiarism Detected</h4>
                <p>Your document appears to be original with no significant similarities found.</p>
            `;
      container.appendChild(noPlagiarismDiv);
    }
  }

  createPlagiarismDetails(details) {
    const container = document.createElement('div');
    container.className = 'plagiarism-details';

    details.forEach((detail, index) => {
      const detailItem = document.createElement('div');
      detailItem.className = 'plagiarism-item';

      const similarity = detail.similarity || 0;
      const severityClass = this.getPlagiarismSeverity(similarity);

      detailItem.innerHTML = `
                <div class="plagiarism-header">
                    <span class="similarity-badge ${severityClass}">${similarity}% Similar</span>
                    <span class="source">${detail.source || 'Unknown Source'}</span>
                </div>
                <div class="plagiarism-text">
                    <strong>Flagged Text:</strong>
                    <p>${detail.text}</p>
                </div>
            `;

      container.appendChild(detailItem);
    });

    return container;
  }

  getPlagiarismSeverity(similarity) {
    if (similarity >= 80) return 'severity-high';
    if (similarity >= 60) return 'severity-medium';
    return 'severity-low';
  }

  updateParaphrasingPanel(paraphrasingData) {
    if (!paraphrasingData || !this.contentPanels.paraphrasingResults) return;

    const container = this.contentPanels.paraphrasingResults;
    container.innerHTML = '';

    if (paraphrasingData.changes && paraphrasingData.changes.length > 0) {
      // Create paraphrasing changes
      const changesContainer = this.createParaphrasingChanges(paraphrasingData.changes);
      container.appendChild(changesContainer);
    } else {
      // No changes made
      const noChangesDiv = document.createElement('div');
      noChangesDiv.className = 'content-empty';
      noChangesDiv.innerHTML = `
                <i class="fas fa-edit"></i>
                <h4>No Paraphrasing Applied</h4>
                <p>The document was already well-written and required no modifications.</p>
            `;
      container.appendChild(noChangesDiv);
    }
  }

  createParaphrasingChanges(changes) {
    const container = document.createElement('div');
    container.className = 'paraphrasing-changes';

    changes.slice(0, 10).forEach((change, index) => { // Show first 10 changes
      const changeItem = document.createElement('div');
      changeItem.className = 'paraphrasing-item';

      const confidence = Math.round((change.confidence || 0) * 100);
      const confidenceClass = confidence >= 80 ? 'confidence-high' :
        confidence >= 60 ? 'confidence-medium' : 'confidence-low';

      changeItem.innerHTML = `
                <div class="change-header">
                    <span class="change-number">Change ${index + 1}</span>
                    <span class="confidence-badge ${confidenceClass}">${confidence}% Confidence</span>
                </div>
                <div class="change-comparison">
                    <div class="original-text">
                        <label>Original:</label>
                        <p>${change.original}</p>
                    </div>
                    <div class="paraphrased-text">
                        <label>Improved:</label>
                        <p>${change.paraphrased}</p>
                    </div>
                </div>
            `;

      container.appendChild(changeItem);
    });

    if (changes.length > 10) {
      const moreChanges = document.createElement('div');
      moreChanges.className = 'more-changes';
      moreChanges.innerHTML = `
                <p>And ${changes.length - 10} more improvements...</p>
            `;
      container.appendChild(moreChanges);
    }

    return container;
  }

  updateComparisonView(results) {
    // This would be implemented to show side-by-side comparison
    // For now, we'll add placeholder content

    if (this.contentPanels.originalContent) {
      this.contentPanels.originalContent.innerHTML = `
                <div class="content-loading">
                    <i class="fas fa-spinner fa-spin"></i>
                    <p>Loading original content...</p>
                </div>
            `;
    }

    if (this.contentPanels.paraphrasedContent) {
      this.contentPanels.paraphrasedContent.innerHTML = `
                <div class="content-loading">
                    <i class="fas fa-spinner fa-spin"></i>
                    <p>Loading paraphrased content...</p>
                </div>
            `;
    }

    // Simulate loading content
    setTimeout(() => {
      this.loadComparisonContent(results);
    }, 1500);
  }

  loadComparisonContent(results) {
    const sampleOriginal = `
            This is a sample paragraph from the original document. It contains the text as it was 
            originally written by the author. The content may have some areas that could be improved 
            for clarity and originality.
            
            Another paragraph follows here with more content that demonstrates the original writing 
            style and structure of the document.
        `;

    const sampleParaphrased = `
            This represents a sample paragraph from the original document. It includes the text as it was 
            initially composed by the author. The material may contain certain sections that could be enhanced 
            for better clarity and uniqueness.
            
            A subsequent paragraph appears here with additional content that illustrates the initial writing 
            approach and organization of the document.
        `;

    if (this.contentPanels.originalContent) {
      this.contentPanels.originalContent.innerHTML = this.formatContentForDisplay(sampleOriginal);
    }

    if (this.contentPanels.paraphrasedContent) {
      this.contentPanels.paraphrasedContent.innerHTML = this.formatContentForDisplay(sampleParaphrased, true);
    }
  }

  formatContentForDisplay(content, isParaphrased = false) {
    // Split content into paragraphs
    const paragraphs = content.trim().split('\n\n');

    return paragraphs.map(paragraph => {
      if (isParaphrased && this.highlightingEnabled) {
        // Add highlighting for changes (this would be more sophisticated in real implementation)
        return `<p>${this.addChangeHighlights(paragraph)}</p>`;
      }
      return `<p>${paragraph.trim()}</p>`;
    }).join('');
  }

  addChangeHighlights(text) {
    // Simple highlighting simulation
    return text
      .replace(/represents/g, '<span class="highlight-added">represents</span>')
      .replace(/includes/g, '<span class="highlight-added">includes</span>')
      .replace(/initially composed/g, '<span class="highlight-added">initially composed</span>')
      .replace(/material/g, '<span class="highlight-added">material</span>')
      .replace(/enhanced/g, '<span class="highlight-added">enhanced</span>')
      .replace(/uniqueness/g, '<span class="highlight-added">uniqueness</span>');
  }

  // Utility methods
  formatNumber(number) {
    if (number >= 1000000) {
      return (number / 1000000).toFixed(1) + 'M';
    } else if (number >= 1000) {
      return (number / 1000).toFixed(1) + 'K';
    }
    return number.toString();
  }

  formatPercentage(value, decimals = 1) {
    return `${value.toFixed(decimals)}%`;
  }

  formatTime(minutes) {
    if (minutes < 60) {
      return `${Math.round(minutes)} min`;
    } else {
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = Math.round(minutes % 60);
      return `${hours}h ${remainingMinutes}m`;
    }
  }

  // Animation methods
  animateNumber(element, targetValue, duration = 1000) {
    if (!element) return;

    const startValue = 0;
    const startTime = performance.now();

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      const currentValue = startValue + (targetValue - startValue) * this.easeOutCubic(progress);
      element.textContent = Math.round(currentValue);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }

  easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  // Export functionality
  generateReport() {
    if (!this.currentResults) return null;

    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        plagiarismScore: this.currentResults.plagiarism?.score || 0,
        modifiedSentences: this.currentResults.paraphrasing?.sentencesModified || 0,
        qualityScore: this.currentResults.quality?.score || 0
      },
      details: this.currentResults
    };

    return report;
  }

  downloadReport(format = 'json') {
    const report = this.generateReport();
    if (!report) return;

    let content, mimeType, filename;

    switch (format) {
      case 'json':
        content = JSON.stringify(report, null, 2);
        mimeType = 'application/json';
        filename = `analysis-report-${Date.now()}.json`;
        break;
      case 'csv':
        content = this.convertToCSV(report);
        mimeType = 'text/csv';
        filename = `analysis-report-${Date.now()}.csv`;
        break;
      default:
        content = JSON.stringify(report, null, 2);
        mimeType = 'application/json';
        filename = `analysis-report-${Date.now()}.json`;
    }

    this.downloadFile(content, mimeType, filename);
  }

  convertToCSV(report) {
    const headers = ['Metric', 'Value', 'Status'];
    const rows = [
      ['Plagiarism Score', `${report.summary.plagiarismScore}%`, report.details.plagiarism?.status || ''],
      ['Modified Sentences', report.summary.modifiedSentences, report.details.paraphrasing?.status || ''],
      ['Quality Score', report.summary.qualityScore, report.details.quality?.status || '']
    ];

    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    return csvContent;
  }

  downloadFile(content, mimeType, filename) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  }

  // Highlighting control
  setHighlighting(enabled) {
    this.highlightingEnabled = enabled;

    if (this.currentResults) {
      this.updateComparisonView(this.currentResults);
    }
  }

  clearResults() {
    this.currentResults = null;

    // Clear all content panels
    Object.values(this.contentPanels).forEach(panel => {
      if (panel) panel.innerHTML = '';
    });

    // Reset summary cards
    Object.values(this.summaryElements).forEach(element => {
      if (element) element.textContent = '0';
    });

    // Reset stats
    Object.values(this.statsElements).forEach(element => {
      if (element) element.textContent = '0';
    });
  }
}

// Export for use in other modules
window.ResultDisplay = ResultDisplay;
