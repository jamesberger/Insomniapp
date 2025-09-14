# Insomniapp

A comprehensive cognitive assessment tool for measuring mental performance across multiple domains. Designed for researchers, educators, and individuals interested in understanding how sleep, stress, and other factors affect cognitive function.

**Author:** James Berger  
**License:** GNU General Public License v3.0  
**Issues:** Please report any issues or bugs by [opening a GitHub issue](https://github.com/jamesberger/Insomniapp/issues)

## Table of Contents

- [What is Insomniapp?](#what-is-insomniapp)
- [Available Tests](#available-tests)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
  - [Prerequisites](#prerequisites)
  - [Python Installation](#python-installation)
  - [Verification](#verification)
- [Installation & Setup](#installation--setup)
  - [Step 1: Download the Application](#step-1-download-the-application)
  - [Step 2: Install Python (if not already installed)](#step-2-install-python-if-not-already-installed)
  - [Step 3: Run the Application](#step-3-run-the-application)
    - [Windows](#windows)
    - [macOS](#macos)
    - [Linux](#linux)
  - [Step 4: Install Graphing Features (Optional)](#step-4-install-graphing-features-optional)
- [Terminal Latency Calibration](#terminal-latency-calibration)
  - [Why Calibration Matters](#why-calibration-matters)
  - [How to Calibrate](#how-to-calibrate)
  - [Platform-Specific Calibration Methods](#platform-specific-calibration-methods)
  - [Terminal Application Compatibility](#terminal-application-compatibility)
- [Usage Instructions](#usage-instructions)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [Performance Benchmarks](#performance-benchmarks)
  - [Expected Score Ranges](#expected-score-ranges)
  - [Sleep Impact on Performance](#sleep-impact-on-performance)
- [Best Practices for Assessment](#best-practices-for-assessment)
- [Research Applications](#research-applications)
  - [Sleep Deprivation Studies](#sleep-deprivation-studies)
  - [Circadian Rhythm Studies](#circadian-rhythm-studies)
  - [Practice Effect Studies](#practice-effect-studies)
- [Data Management](#data-management)
  - [File Storage](#file-storage)
  - [Privacy and Security](#privacy-and-security)
- [Technical Support](#technical-support)
- [Scientific Applications](#scientific-applications)

## What is Insomniapp?

Insomniapp is a cognitive testing suite that provides standardized assessments of mental performance. The application measures various cognitive domains including processing speed, working memory, attention, and executive function. It's particularly valuable for tracking how sleep deprivation and other lifestyle factors impact cognitive performance.

## Available Tests

1. **Reaction Time Test** - Measures processing speed and alertness through visual-motor response tasks
2. **Digit Span Test** - Assesses working memory capacity using forward digit recall
3. **Mental Math Test** - Evaluates processing speed and arithmetic ability under time pressure
4. **Word Recall Test** - Tests memory encoding and retrieval through verbal learning tasks
5. **Stroop Test** - Measures attention and cognitive inhibition using color-word interference
6. **Sustained Attention Test** - Evaluates focus and mental endurance through serial subtraction

## Key Features

- **Automated Data Collection**: All test results are automatically saved with precise timestamps
- **Statistical Analysis**: Comprehensive performance tracking with trend analysis
- **Sleep Correlation**: Built-in sleep logging to correlate rest patterns with cognitive performance
- **Historical Tracking**: Long-term data storage for longitudinal studies and personal monitoring

## System Requirements

### Prerequisites
- **Python 3.6 or higher** (Python 3.8+ recommended)
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: 50MB free space

### Python Installation

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and **ensure "Add Python to PATH" is checked**
3. Complete the installation

**macOS:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer package
3. Verify installation in Terminal

**Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Verification
Test your Python installation:
```bash
python3 --version
```
Expected output: `Python 3.x.x`

## Installation & Setup

### Step 1: Download the Application
1. **Download the repository**: Click the green "Code" button and download as ZIP
2. **Extract the ZIP file** to a folder on your computer (e.g., Desktop or Documents)

### Step 2: Install Python (if not already installed)
Follow the Python installation instructions in the System Requirements section above.

### Step 3: Run the Application

#### Windows
1. **Open Command Prompt**:
   - Press `Windows + R`, type `cmd`, press Enter
   - Or search "Command Prompt" in the Start menu

2. **Navigate to the application folder**:
   ```cmd
   cd C:\path\to\Insomniapp
   ```
   (Replace with your actual folder path)

3. **Run the application**:
   ```cmd
   python insomniapp.py
   ```
   (If that doesn't work, try `py insomniapp.py`)

#### macOS
1. **Open Terminal**:
   - Press `Cmd + Space`, type "Terminal", press Enter
   - Or go to Applications > Utilities > Terminal

2. **Navigate to the application folder**:
   ```bash
   cd /path/to/Insomniapp
   ```
   (Replace with your actual folder path)

3. **Run the application**:
   ```bash
   python3 insomniapp.py
   ```

#### Linux
1. **Open Terminal**:
   - Press `Ctrl + Alt + T`
   - Or search "Terminal" in your applications

2. **Navigate to the application folder**:
   ```bash
   cd /path/to/Insomniapp
   ```
   (Replace with your actual folder path)

3. **Run the application**:
   ```bash
   python3 insomniapp.py
   ```

### Step 4: Install Graphing Features (Optional)

**Important**: The application works fully without matplotlib, but **graphing and visualization features will not be available**. You will only see text-based results and summaries.

To enable graphing features:

#### Windows
```cmd
pip install matplotlib
```

#### macOS/Linux
```bash
pip3 install matplotlib
```

**Note**: After installing matplotlib, restart the application to access graphing features. Without matplotlib, you can still:
- Take all cognitive tests
- View text-based results
- Track performance over time
- Export data
- Use all core functionality

**What you'll miss without matplotlib**:
- Visual trend graphs
- Performance charts
- Graphical data analysis

## Terminal Latency Calibration

### Why Calibration Matters
For accurate reaction time measurements, Insomniapp can calibrate your terminal's input latency. This accounts for the delay between when you press a key and when the application receives it, ensuring precise timing measurements.

### How to Calibrate
1. **Run the application**: `python3 insomniapp.py`
2. **Select option 11**: "Calibrate Terminal Latency" from the main menu
3. **Follow the on-screen instructions** for your platform

### Platform-Specific Calibration Methods

#### Windows
- **PowerShell SendKeys** (recommended): Automated calibration using PowerShell
- **Manual calibration**: Fallback method if PowerShell automation fails
- **Best compatibility**: Works well with Command Prompt, PowerShell, and most Windows terminals

#### macOS
- **AppleScript automation**: Uses system automation to send keystrokes
- **Requires permissions**: You may need to grant Accessibility permissions to Terminal/iTerm2
- **Best compatibility**: Works excellently with Terminal.app and iTerm2

#### Linux
- **Manual calibration**: Measures your natural reaction time to key presses
- **Universal compatibility**: Works with all Linux terminal applications
- **Most reliable**: No automation dependencies, works consistently across all environments

### Terminal Application Compatibility

**Excellent compatibility**:
- Windows: Command Prompt, PowerShell, Windows Terminal
- macOS: Terminal.app, iTerm2
- Linux: All standard terminal applications (GNOME Terminal, Konsole, etc.)

**Good compatibility**:
- VS Code integrated terminal (all platforms)
- Cursor integrated terminal (all platforms)

**Note**: The calibration system automatically detects your platform and terminal environment, selecting the most appropriate method for optimal accuracy.

## Usage Instructions

1. **Launch the application**: Execute `python3 insomniapp.py`
2. **Select assessment**: Choose from the available cognitive tests (1-6)
3. **Follow test protocols**: Each test provides specific instructions
4. **Review results**: Performance data is automatically recorded
5. **Monitor trends**: Use historical data for longitudinal analysis

## Troubleshooting

### Common Issues

**"Python not found" or "command not found"**
- Verify Python installation (see System Requirements above)
- Try alternative commands: `python` or `py` (Windows)
- Ensure Python is added to your system PATH

**"No module named matplotlib"**
- This is expected if matplotlib is not installed
- Install with: `pip3 install matplotlib` (optional)
- Application functions normally without matplotlib

**Application fails to start**
- Verify you're in the correct directory containing `insomniapp.py`
- Test Python functionality: `python3 -c "print('Python is working')"`
- Check file permissions and Python version compatibility

## Performance Benchmarks

### Expected Score Ranges
- **Reaction Time**: 0.200-0.300 seconds (lower values indicate better performance)
- **Digit Span**: 6-8 digits (higher values indicate better working memory)
- **Mental Math**: 15-25 problems in 60 seconds (higher values indicate better processing speed)
- **Word Recall**: 60-80% accuracy (higher percentages indicate better memory encoding/retrieval)
- **Stroop Test**: 85-95% accuracy (higher percentages indicate better cognitive inhibition)
- **Sustained Attention**: 90%+ accuracy (higher percentages indicate better sustained focus)

### Sleep Impact on Performance
- **<6 hours sleep**: Significant performance degradation expected
- **6-7 hours sleep**: Moderate performance impact may be observed
- **8+ hours sleep**: Optimal performance baseline

## Best Practices for Assessment

1. **Establish Baseline**: Conduct initial assessments when well-rested (8+ hours sleep)
2. **Maintain Consistency**: Test at consistent times of day to control for circadian effects
3. **Document Sleep Patterns**: Log sleep duration to correlate with performance metrics
4. **Control Environment**: Use consistent, distraction-free testing environment
5. **Longitudinal Tracking**: Regular assessments enable trend analysis and pattern recognition

## Research Applications

### Sleep Deprivation Studies
1. **Baseline Phase**: Assess performance after 8+ hours of sleep
2. **Intervention Phase**: Test after 6 hours of sleep
3. **Acute Deprivation**: Test after 4 hours of sleep
4. **Analysis**: Compare performance metrics across sleep conditions

### Circadian Rhythm Studies
- Conduct assessments at multiple time points (9 AM, 2 PM, 8 PM)
- Analyze performance variations across different times of day

### Practice Effect Studies
- Daily assessments over extended periods
- Measure learning curves and performance stabilization

## Data Management

### File Storage
- Results are stored locally in `insomniapp_results.json`
- Data remains on your local system and is not transmitted externally
- Files can be backed up, archived, or deleted as needed

### Privacy and Security
- All data collection occurs locally on your device
- No external data transmission or cloud storage
- Users maintain complete control over their assessment data

## Technical Support

For technical issues:
1. Review the Troubleshooting section above
2. Verify Python installation and version compatibility
3. Check system requirements and file permissions
4. Ensure proper directory navigation and file access

## Scientific Applications

Insomniapp is suitable for:
- Educational research on sleep and cognition
- Personal performance monitoring
- Sleep hygiene studies
- Cognitive assessment in controlled environments
- Longitudinal tracking of cognitive performance