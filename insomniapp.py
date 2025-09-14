#!/usr/bin/env python3
"""
Insomniapp
A comprehensive battery of insomniapp tests to assess mental sharpness
with result tracking and historical analysis.
"""

import time
import random
import json
import os
from datetime import datetime, date, timedelta
import subprocess
import platform
import statistics
# matplotlib import moved to where it is needed to avoid backend issues
from typing import Dict, List, Any
from collections import defaultdict
import threading
import sys

class InsomniappSuite:
    def __init__(self):
        self.results_file = "insomniapp_results.json"
        self.sleep_file = "sleep_log.json"
        self.calibration_file = "terminal_latency.json"
        self.results = self.load_results()
        self.sleep_log = self.load_sleep_log()
        self.terminal_calibration = self.load_terminal_calibration()
        self._word_bank: List[str] = []
    
    def get_test_info(self, test_name: str) -> Dict[str, str]:
        """Get scoring information and benchmarks for each test type"""
        test_info = {
            'Reaction Time': {
                'description': 'Response Speed Test (Inverted Display)',
                'score_type': 'Reaction speed score (higher is better on graph)',
                'good_range': 'Excellent: <0.200s | Good: 0.200-0.300s | Fair: 0.300-0.400s | Poor: >0.400s',
                'lower_better': False
            },
            'Digit Span': {
                'description': 'Working Memory Capacity',
                'score_type': 'Maximum digits recalled correctly',
                'good_range': 'Excellent: 8+ digits | Good: 6-7 digits | Average: 5-6 digits | Below Avg: <5 digits',
                'lower_better': False
            },
            'Mental Math': {
                'description': 'Processing Speed & Arithmetic (Time-Based) - Inverted Display',
                'score_type': 'Average time per problem with penalties (higher is better on graph)',
                'good_range': 'Excellent: <6.5s | Good: 6.5-11s | Average: 11-15.5s | Poor: >15.5s',
                'lower_better': False
            },
            'Word Recall': {
                'description': 'Memory Encoding & Retrieval',
                'score_type': 'Percentage of words correctly recalled',
                'good_range': 'Excellent: 80%+ | Good: 65-79% | Average: 50-64% | Below Avg: <50%',
                'lower_better': False
            },
            'Stroop Test': {
                'description': 'Attention & Cognitive Inhibition (Triple Interference + Time Pressure) - Inverted Display',
                'score_type': 'Response speed score (higher is better on graph)',
                'good_range': 'Excellent: <1.5s | Good: 1.5-2.0s | Average: 2.0-2.5s | Poor: >2.5s',
                'lower_better': False
            },
            'Sustained Attention': {
                'description': 'Focus & Mental Endurance (Speed-Based) - Inverted Display',
                'score_type': 'Attention speed score (higher is better on graph)',
                'good_range': 'Excellent: <3s | Good: 3-5s | Average: 5-8s | Poor: >8s',
                'lower_better': False
            }
        }
        return test_info.get(test_name, {
            'description': 'Cognitive Assessment',
            'score_type': 'Test score',
            'good_range': 'Ranges vary by test type',
            'lower_better': False
        })
        
    def load_results(self) -> Dict[str, List[Dict]]:
        """Load previous test results from file"""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}
    
    def save_results(self):
        """Save results to file"""
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def load_sleep_log(self) -> Dict[str, Dict]:
        """Load sleep log from file"""
        if os.path.exists(self.sleep_file):
            try:
                with open(self.sleep_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}
    
    def save_sleep_log(self):
        """Save sleep log to file"""
        with open(self.sleep_file, 'w') as f:
            json.dump(self.sleep_log, f, indent=2)
    
    def log_sleep(self, date_str: str, hours: int, minutes: int):
        """Log sleep duration for a specific date"""
        self.sleep_log[date_str] = {
            'hours': hours,
            'minutes': minutes,
            'total_minutes': hours * 60 + minutes
        }
        self.save_sleep_log()
    
    def get_sleep_for_date(self, date_obj: date) -> str:
        """Get formatted sleep string for a specific date"""
        date_str = date_obj.strftime('%Y-%m-%d')
        if date_str in self.sleep_log:
            sleep_data = self.sleep_log[date_str]
            return f"{sleep_data['hours']}h {sleep_data['minutes']}m"
        return "No sleep data"
    
    def get_sleep_for_graph_label(self, date_obj: date) -> str:
        """Get compact sleep string for graph x-axis labels"""
        date_str = date_obj.strftime('%Y-%m-%d')
        if date_str in self.sleep_log:
            sleep_data = self.sleep_log[date_str]
            return f"Sleep\n{sleep_data['hours']}h{sleep_data['minutes']:02d}m"
        return "Sleep\nN/A"
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_performance_bands(self, test_name: str) -> Dict[str, tuple]:
        """Get performance bands for color-coding graphs with equal 25% sizing"""
        test_info = self.get_test_info(test_name)
        lower_better = test_info['lower_better']
        
        # Define performance bands with equal 25% height distribution
        bands = {}
        
        if test_name == 'Reaction Time':
            # Set fixed range 0.2-1.0 (inverted), each band gets 25% (0.2 each)
            # Note: These bands are inverted (1.0 - original_time) so higher is better
            bands = {
                'poor': (0.2, 0.4),      # Original: 0.6-0.8s (slowest)
                'average': (0.4, 0.6),   # Original: 0.4-0.6s
                'good': (0.6, 0.8),      # Original: 0.2-0.4s
                'excellent': (0.8, 1.0)  # Original: 0.0-0.2s (fastest)
            }
        elif test_name == 'Digit Span':
            # Set fixed range 0-16 digits, each band gets 25% (4 digits each)
            bands = {
                'poor': (0, 4),
                'average': (4, 8),
                'good': (8, 12),
                'excellent': (12, 16)
            }
        elif test_name == 'Mental Math':
            # Set fixed range 2-20s per problem (inverted), each band gets 25% (4.5s each)
            # Note: These bands are inverted (22.0 - original_time) so higher is better
            # Based on realistic two-digit addition: 2-8s base + penalties
            bands = {
                'poor': (2.0, 6.5),       # Original: 15.5-20s (slowest with penalties)
                'average': (6.5, 11.0),   # Original: 11-15.5s
                'good': (11.0, 15.5),     # Original: 6.5-11s
                'excellent': (15.5, 20.0) # Original: 2-6.5s (fastest)
            }
        elif test_name == 'Stroop Test':
            # Set fixed range 1-5 (inverted), each band gets 25% (1 each)
            # Note: These bands are inverted (5.0 - original_time) so higher is better
            bands = {
                'poor': (1.0, 2.0),      # Original: 3.0-4.0s (slowest)
                'average': (2.0, 3.0),   # Original: 2.0-3.0s
                'good': (3.0, 4.0),      # Original: 1.0-2.0s
                'excellent': (4.0, 5.0)  # Original: 0.0-1.0s (fastest)
            }
        elif test_name == 'Sustained Attention':
            # Set fixed range 1-13 (inverted), each band gets 25% (3 each)
            # Note: These bands are inverted (13.0 - original_time) so higher is better
            bands = {
                'poor': (1.0, 4.0),      # Original: 9.0-12.0s (slowest)
                'average': (4.0, 7.0),   # Original: 6.0-9.0s
                'good': (7.0, 10.0),     # Original: 3.0-6.0s
                'excellent': (10.0, 13.0) # Original: 0.0-3.0s (fastest)
            }
        elif test_name == 'Word Recall':
            # Set fixed range 0-100%, each band gets 25% (25% each)
            bands = {
                'poor': (0, 25),
                'average': (25, 50),
                'good': (50, 75),
                'excellent': (75, 100)
            }
        
        return bands

    def _get_adaptive_y_range(self, test_name: str, data_values: list) -> tuple:
        """Get adaptive y-axis range based on actual data values for the week"""
        performance_bands = self.get_performance_bands(test_name)
        
        if not data_values or not performance_bands:
            # Fallback to fixed ranges if no data
            if test_name == 'Reaction Time':
                return (0.2, 1.0)  # Inverted range for better display
            elif test_name == 'Digit Span':
                return (0, 16)
            elif test_name == 'Mental Math':
                return (2.0, 20.0)  # Inverted range for better display
            elif test_name == 'Stroop Test':
                return (1.0, 5.0)  # Inverted range for better display
            elif test_name == 'Sustained Attention':
                return (1.0, 13.0)  # Inverted range for better display
            else:  # Percentage tests (Word Recall)
                return (0, 100)
        
        # Find min and max values from actual data
        min_val = min(data_values)
        max_val = max(data_values)
        
        # Determine which performance bands the data spans
        bands_in_range = []
        for band_name, (band_min, band_max) in performance_bands.items():
            if (min_val < band_max and max_val >= band_min):
                bands_in_range.append((band_name, band_min, band_max))
        
        if not bands_in_range:
            # Fallback if no bands found
            padding = (max_val - min_val) * 0.1 if max_val != min_val else 1
            return (min_val - padding, max_val + padding)
        
        # Use the range that encompasses all bands with data
        y_min = min(band_min for _, band_min, _ in bands_in_range)
        y_max = max(band_max for _, _, band_max in bands_in_range)
        
        return (y_min, y_max)

    def _get_active_performance_bands(self, test_name: str, y_min: float, y_max: float) -> dict:
        """Get only the performance bands that are visible in the current y-axis range"""
        all_bands = self.get_performance_bands(test_name)
        active_bands = {}
        
        for band_name, (band_min, band_max) in all_bands.items():
            # Include band if it overlaps with the visible range
            if band_min < y_max and band_max > y_min:
                # Clip the band to the visible range
                visible_min = max(band_min, y_min)
                visible_max = min(band_max, y_max)
                active_bands[band_name] = (visible_min, visible_max)
        
        return active_bands

    # ===== Terminal latency calibration =====
    def _terminal_signature(self) -> Dict[str, str]:
        """Identify the current terminal/computer environment to key a calibration entry."""
        term_prog = os.environ.get('TERM_PROGRAM', '')
        term_prog_ver = os.environ.get('TERM_PROGRAM_VERSION', '')
        shell = os.environ.get('SHELL', '')
        return {
            'os': platform.system(),
            'os_version': platform.release(),
            'python': platform.python_version(),
            'terminal_program': term_prog,
            'terminal_version': term_prog_ver,
            'shell': shell,
        }

    def _terminal_signature_key(self) -> str:
        sig = self._terminal_signature()
        key = f"{sig['os']}|{sig['terminal_program']}|{sig['terminal_version']}|{sig['shell']}"
        return key

    def load_terminal_calibration(self) -> Dict[str, Dict[str, float]]:
        """Load terminal latency calibrations from file."""
        if os.path.exists(self.calibration_file):
            try:
                with open(self.calibration_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}

    # ===== Word bank support =====
    def get_word_bank(self) -> List[str]:
        """Return a large list of simple words from an internal word bank only.
        No system dictionary files are read.
        """
        if self._word_bank:
            return self._word_bank

        words: List[str] = [
            # Common objects, nature, animals, actions, colors, and simple nouns
            'apple','chair','table','spoon','bottle','pocket','window','door','floor','ceiling',
            'mountain','valley','river','ocean','island','desert','forest','meadow','garden','harbor',
            'cloud','storm','breeze','rain','thunder','lightning','sunrise','sunset','shadow','stone',
            'purple','yellow','orange','green','blue','red','silver','golden','copper','white',
            'castle','bridge','tower','village','market','street','path','road','tunnel','station',
            'pencil','notebook','paper','letter','envelope','mirror','ladder','bucket','basket','blanket',
            'candle','lamp','lantern','clock','watch','compass','camera','keychain','wallet','ticket',
            'coffee','tea','sugar','pepper','ginger','onion','garlic','tomato','potato','carrot',
            'banana','orange','lemon','grapes','peach','berry','melon','coconut','almond','peanut',
            'penguin','tiger','zebra','monkey','rabbit','kitten','puppy','parrot','dolphin','whale',
            'sparrow','eagle','falcon','owl','fox','bear','camel','yak','horse','sheep',
            'violin','piano','drums','trumpet','flute','guitar','singer','dancer','artist','poetry',
            'rocket','planet','saturn','comet','meteor','orbit','spaceship','astronaut','helmet','telescope',
            'bridge','harbor','anchor','sailor','captain','harvest','plow','tractor','barn','pasture',
            'garden','shovel','rake','hose','fence','gate','porch','balcony','curtain','sofa',
            'wallet','ticket','passport','luggage','airplane','airport','runway','window','seat','aisle',
            'spring','summer','autumn','winter','morning','evening','midnight','noon','breakfast','dinner',
            'kit','map','route','trail','camp','tent','cabin','fire','marshmallow','riverbank',
            'paint','brush','canvas','museum','gallery','sculpture','statue','poem','novel','writer',
            'engine','piston','hammer','wrench','screw','bolt','scissors','needle','thread','fabric'
        ]

        # Deduplicate and shuffle for variety
        words = sorted(set(words))
        random.shuffle(words)
        self._word_bank = words
        return self._word_bank

    def save_terminal_calibration(self):
        with open(self.calibration_file, 'w') as f:
            json.dump(self.terminal_calibration, f, indent=2)

    def get_active_baseline_seconds(self) -> float:
        """Return the median baseline (seconds) for the active terminal if available, else 0.0."""
        key = self._terminal_signature_key()
        entry = self.terminal_calibration.get(key)
        if entry and 'median_ms' in entry:
            return entry['median_ms'] / 1000.0
        return 0.0

    def calibrate_terminal_latency(self, trial_count: int = 50):
        """Run terminal latency calibration for the current platform and terminal."""
        print("\n=== TERMINAL LATENCY CALIBRATION ===")
        
        if platform.system() == 'Darwin':
            self._calibrate_macos_terminal(trial_count)
        elif platform.system() == 'Windows':
            self._calibrate_windows_terminal(trial_count)
        else:
            self._calibrate_manual_terminal(trial_count)
    
    def _calibrate_macos_terminal(self, trial_count: int = 50):
        """macOS terminal calibration using AppleScript"""
        print("macOS detected - Using AppleScript automation")
        print("This will send an automated Return key to the current terminal and measure how long")
        print("it takes for Python input() to receive it. Ensure this window is focused and grant")
        print("Accessibility permissions to Terminal/iTerm2 and your Python interpreter if prompted.")
        print(f"Trials to run: {trial_count}")
        input("Press ENTER to begin...")

        samples = []
        errors = 0
        for i in range(1, trial_count + 1):
            try:
                print(f"Trial {i}/{trial_count}: GO!", flush=True)
                t0 = time.time()
                # Send Return to frontmost app using AppleScript
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to keystroke return'
                ], check=True)
                _ = input()
                dt = time.time() - t0
                samples.append(dt)
                # Brief pacing delay to avoid spamming
                time.sleep(0.05)
            except subprocess.CalledProcessError:
                errors += 1
                print("AppleScript failed to send keystroke. Check Accessibility permissions.")
                break
            except KeyboardInterrupt:
                print("Calibration interrupted.")
                break

        self._save_calibration_results(samples, "AppleScript automation")
    
    def _calibrate_windows_terminal(self, trial_count: int = 50):
        """Windows terminal calibration with multiple methods"""
        print("Windows detected - Multiple calibration methods available")
        print()
        print("CALIBRATION METHODS:")
        print("1. PowerShell SendKeys automation (recommended)")
        print("2. Manual timing calibration")
        print("3. Back to main menu")
        
        choice = input("Select calibration method (1-3): ").strip()
        
        if choice == '1':
            self._calibrate_windows_sendkeys(trial_count)
        elif choice == '2':
            self._calibrate_manual_terminal(trial_count)
        elif choice == '3':
            return
        else:
            print("Invalid choice.")
    
    def _calibrate_windows_sendkeys(self, trial_count: int = 50):
        """Windows calibration using PowerShell SendKeys"""
        print("\n--- PowerShell SendKeys Calibration ---")
        print("This method uses PowerShell to send keystrokes to the current window.")
        print("Make sure this terminal window stays focused during calibration.")
        print(f"Trials to run: {trial_count}")
        
        # Test if PowerShell SendKeys works
        print("\nTesting PowerShell SendKeys capability...")
        try:
            # Create a PowerShell script that sends Enter key
            ps_script = '''
            Add-Type -AssemblyName System.Windows.Forms
            Start-Sleep -Milliseconds 500
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
            '''
            
            # Test the PowerShell command
            result = subprocess.run([
                'powershell', '-Command', ps_script
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                print("PowerShell SendKeys test failed. Falling back to manual calibration.")
                self._calibrate_manual_terminal(trial_count)
                return
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print("PowerShell SendKeys not available. Falling back to manual calibration.")
            self._calibrate_manual_terminal(trial_count)
            return
        
        print("PowerShell SendKeys test successful!")
        input("Press ENTER to begin calibration...")

        samples = []
        errors = 0
        
        for i in range(1, trial_count + 1):
            try:
                print(f"Trial {i}/{trial_count}: GO!", flush=True)
                t0 = time.time()
                
                # Send Enter key using PowerShell
                subprocess.run([
                    'powershell', '-Command',
                    '''
                    Add-Type -AssemblyName System.Windows.Forms
                    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
                    '''
                ], check=True, capture_output=True)
                
                _ = input()
                dt = time.time() - t0
                samples.append(dt)
                # Brief pacing delay
                time.sleep(0.1)
                
            except subprocess.CalledProcessError:
                errors += 1
                print("PowerShell SendKeys failed.")
                if errors >= 3:
                    print("Too many errors. Stopping calibration.")
                    break
            except KeyboardInterrupt:
                print("Calibration interrupted.")
                break

        self._save_calibration_results(samples, "PowerShell SendKeys")
    
    def _calibrate_manual_terminal(self, trial_count: int = 25):
        """Manual calibration method for any platform"""
        print("\n--- Manual Calibration ---")
        print("This method measures your natural reaction time to pressing Enter.")
        print("When you see 'GO!', press ENTER as quickly as possible.")
        print("This provides a baseline for your terminal's input latency.")
        print(f"Trials to run: {trial_count}")
        input("Press ENTER when ready to begin...")

        samples = []
        
        for i in range(1, trial_count + 1):
            try:
                print(f"\nTrial {i}/{trial_count}")
                print("Get ready...")
                
                # Random delay between 1-3 seconds
                time.sleep(random.uniform(1.0, 3.0))
                
                print("GO! Press ENTER NOW!")
                t0 = time.time()
                _ = input()
                dt = time.time() - t0
                samples.append(dt)
                
                print(f"Response time: {dt*1000:.1f} ms")
                
            except KeyboardInterrupt:
                print("Calibration interrupted.")
                break

        self._save_calibration_results(samples, "Manual timing")
    
    def _save_calibration_results(self, samples, method_name):
        """Save calibration results to file"""
        if not samples:
            print("No samples recorded.")
            return

        samples_ms = [s * 1000.0 for s in samples]
        samples_ms.sort()
        median_ms = statistics.median(samples_ms)
        p10_ms = samples_ms[int(max(0, round(0.10 * (len(samples_ms) - 1))))]
        p90_ms = samples_ms[int(max(0, round(0.90 * (len(samples_ms) - 1))))]

        sig = self._terminal_signature()
        key = self._terminal_signature_key()
        self.terminal_calibration[key] = {
            'median_ms': round(median_ms, 1),
            'p10_ms': round(p10_ms, 1),
            'p90_ms': round(p90_ms, 1),
            'samples': len(samples_ms),
            'method': method_name,
            'timestamp': datetime.now().isoformat(),
            'env': sig,
        }
        self.save_terminal_calibration()

        print(f"\nCalibration complete using {method_name}:")
        print(f"  Median: {median_ms:.1f} ms  (p10: {p10_ms:.1f} ms, p90: {p90_ms:.1f} ms)")
        print(f"  Samples: {len(samples_ms)}")
        print(f"  Saved for: {sig['terminal_program']} on {sig['os']} {sig['os_version']}")
        
        if method_name == "Manual timing":
            print(f"  Note: Manual calibration includes human reaction time (~150-300ms)")
            print(f"        This baseline will be subtracted from reaction time tests.")
        
        input("\nPress Enter to continue...")
    
    def record_result(self, test_name: str, score: float, details: Dict = None):
        """Record a test result with timestamp"""
        if test_name not in self.results:
            self.results[test_name] = []
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'details': details or {}
        }
        
        self.results[test_name].append(result)
        self.save_results()
    
    def display_results(self, test_name: str):
        """Display historical results for a specific test"""
        if test_name not in self.results or not self.results[test_name]:
            print(f"\nNo previous results found for {test_name}")
            input("\nPress Enter to return to results menu...")
            return
        
        # Get test information for header
        test_info = self.get_test_info(test_name)
        
        print(f"\n=== {test_name} Results History ===")
        print(f"Description: {test_info['description']}")
        print(f"Score: {test_info['score_type']}")
        print(f"Benchmarks: {test_info['good_range']}")
        print("-" * 60)
        
        results = self.results[test_name]
        
        for i, result in enumerate(results[-10:], 1):  # Show last 10 results
            timestamp = datetime.fromisoformat(result['timestamp'])
            result_date = timestamp.date()
            sleep_info = self.get_sleep_for_date(result_date)

            if test_name == 'Reaction Time':
                # Prefer stored adjusted value; else adjust using current baseline
                adjusted = None
                if result.get('details') and 'adjusted_average_s' in result['details']:
                    adjusted = result['details']['adjusted_average_s']
                else:
                    adjusted = max(0.0, result['score'] - self.get_active_baseline_seconds())
                print(f"{i:2d}. {timestamp.strftime('%Y-%m-%d %H:%M')} - Score (adjusted): {adjusted:.3f} s [raw: {result['score']:.3f} s] | Sleep: {sleep_info}")
            else:
                print(f"{i:2d}. {timestamp.strftime('%Y-%m-%d %H:%M')} - Score: {result['score']:.3f} | Sleep: {sleep_info}")
            if result['details']:
                for key, value in result['details'].items():
                    print(f"     {key}: {value}")
        
        if len(results) > 1:
            if test_name == 'Reaction Time':
                scores = []
                for r in results:
                    if r.get('details') and 'adjusted_average_s' in r['details']:
                        scores.append(r['details']['adjusted_average_s'])
                    else:
                        scores.append(max(0.0, r['score'] - self.get_active_baseline_seconds()))
            else:
                scores = [r['score'] for r in results]
            print(f"\nStatistics:")
            print(f"  Average: {sum(scores)/len(scores):.3f}")
            if test_info['lower_better']:
                print(f"  Best (lowest): {min(scores):.3f}")
            else:
                print(f"  Best (highest): {max(scores):.3f}")
            print(f"  Latest: {scores[-1]:.3f}")
        
        input("\nPress Enter to return to results menu...")
    
    def wait_for_keypress(self):
        """Wait for any key press (cross-platform)"""
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def reaction_time_test(self):
        """Simple reaction time test"""
        self.clear_screen()
        print("=== REACTION TIME TEST ===")
        print("Press ENTER as quickly as possible when you see 'GO!'")
        print("Press Ctrl+C to exit test without saving data")
        print()
        print("Ready to start?")
        input("Press Enter when you're ready to begin...")
        print()
        print("Get ready...")
        
        times = []
        trials = 5
        
        try:
            for trial in range(1, trials + 1):
                print(f"\nTrial {trial}/{trials}")
                print("Wait for it...")
                
                # Random delay between 1-4 seconds
                time.sleep(random.uniform(1.0, 4.0))
                
                print("GO! Press ENTER NOW!")
                start_time = time.time()
                
                input()  # Wait for Enter key
                reaction_time = time.time() - start_time
                adjusted = reaction_time - self.get_active_baseline_seconds()
                times.append(reaction_time)
                
                print(f"Reaction time: {reaction_time:.3f} s  (adjusted: {max(adjusted, 0):.3f} s)")
            
            # Only calculate and save results if all trials completed
            average_time = sum(times) / len(times)
            baseline = self.get_active_baseline_seconds()
            avg_adjusted = max(0.0, average_time - baseline)
        
        except KeyboardInterrupt:
            self.clear_screen()
            print("=== TEST INTERRUPTED ===")
            print("Reaction time test was cancelled. No data saved.")
            input("\nPress Enter to return to main menu...")
            self.clear_screen()
            return
        
        # Clear screen and show results
        self.clear_screen()
        print("=== REACTION TIME TEST RESULTS ===")
        print(f"Average reaction time: {average_time:.3f} seconds")
        print(f"Adjusted average: {avg_adjusted:.3f} seconds (after {baseline*1000:.1f}ms baseline)")
        print(f"Best time: {min(times):.3f} seconds")
        print(f"Worst time: {max(times):.3f} seconds")
        print(f"Trials completed: {trials}")
        
        self.record_result("Reaction Time", average_time, {
            'trials': trials,
            'times': [round(t, 3) for t in times],
            'adjusted_average_s': round(avg_adjusted, 3),
            'baseline_ms': round(baseline * 1000.0, 1)
        })
        
        input("\nPress Enter to continue...")
        self.clear_screen()
    
    def digit_span_test(self):
        """Working memory digit span test"""
        self.clear_screen()
        print("=== DIGIT SPAN TEST ===")
        print("I'll show you a sequence of digits.")
        print("Memorize them, then type them back in the same order.")
        print("Press Ctrl+C to exit test without saving data")
        
        input("\nPress Enter when you're ready to start...")
        
        span_length = 3
        max_span = 0
        
        try:
            while span_length <= 10:
                print(f"\nTesting span length: {span_length}")
                
                # Generate random digits
                digits = [random.randint(0, 9) for _ in range(span_length)]
                digit_string = ' '.join(map(str, digits))
                
                print(f"Memorize these digits: {digit_string}")
                time.sleep(span_length * 0.8)  # Give time to memorize
                
                # Clear screen to prevent looking back
                self.clear_screen()
                print("=== DIGIT SPAN TEST ===")
                print("Enter the digits in order (no spaces): ", end="")
                
                try:
                    user_input = input().strip()
                    correct_answer = ''.join(map(str, digits))
                    
                    if user_input == correct_answer:
                        print("Correct!")
                        max_span = span_length
                        span_length += 1
                    else:
                        print(f"Incorrect. The correct answer was: {correct_answer}")
                        break
                except ValueError:
                    print("Invalid input. Test ended.")
                    break
        
        except KeyboardInterrupt:
            self.clear_screen()
            print("=== TEST INTERRUPTED ===")
            print("Digit span test was cancelled. No data saved.")
            input("\nPress Enter to return to main menu...")
            self.clear_screen()
            return
        
        # Clear screen and show results
        self.clear_screen()
        print("=== DIGIT SPAN TEST RESULTS ===")
        print(f"Your digit span: {max_span} digits")
        print(f"This measures your working memory capacity.")
        
        self.record_result("Digit Span", max_span, {
            'max_digits_recalled': max_span
        })
        
        input("\nPress Enter to continue...")
        self.clear_screen()
    
    def mental_math_test(self):
        """Processing speed mental math test with time-based scoring"""
        self.clear_screen()
        print("=== MENTAL MATH TEST ===")
        print("Solve as many addition problems as you can in 60 seconds!")
        print("Your score will be based on average time per problem.")
        print("Incorrect answers add a 10-second time penalty.")
        print("Press Ctrl+C to exit test without saving data")
        print("Press ENTER to start...")
        input()
        
        start_time = time.time()
        correct = 0
        total = 0
        test_completed = False
        problem_times = []
        penalty_time = 0  # Track total penalty time for incorrect answers
        
        print("\nSTART!")
        
        try:
            while time.time() - start_time < 60:
                num1 = random.randint(10, 99)
                num2 = random.randint(10, 99)
                correct_answer = num1 + num2
                
                remaining_time = 60 - (time.time() - start_time)
                if remaining_time <= 0:
                    break
                    
                print(f"\nTime remaining: {remaining_time:.1f}s")
                print(f"{num1} + {num2} = ", end="")
                
                try:
                    start_problem = time.time()
                    user_answer = int(input())
                    end_problem = time.time()
                    
                    problem_time = end_problem - start_problem
                    total += 1
                    
                    if user_answer == correct_answer:
                        correct += 1
                        problem_times.append(problem_time)
                        print("✓ Correct!")
                    else:
                        # Add penalty time (10 seconds) for incorrect answer
                        problem_times.append(problem_time + 10.0)
                        penalty_time += 10.0
                        print(f"✗ Wrong. Answer was {correct_answer} (+10s penalty)")
                        
                except ValueError:
                    # Invalid input also gets penalty
                    end_problem = time.time()
                    problem_time = end_problem - start_problem
                    problem_times.append(problem_time + 10.0)
                    penalty_time += 10.0
                    print("Invalid input, skipping... (+10s penalty)")
                    total += 1
            
            # Mark as completed if we exited the loop naturally (time expired)
            test_completed = True
            
        except KeyboardInterrupt:
            self.clear_screen()
            print("=== TEST INTERRUPTED ===")
            print("Mental math test was cancelled. No data saved.")
            input("\nPress Enter to return to main menu...")
            self.clear_screen()
            return
        
        # Only proceed with results if test completed
        if not test_completed:
            return
            
        # Calculate time-based scoring
        if problem_times:
            avg_time_per_problem = sum(problem_times) / len(problem_times)
        else:
            avg_time_per_problem = 60.0  # Fallback if no problems attempted
            
        accuracy = (correct / total * 100) if total > 0 else 0
        score = avg_time_per_problem  # Primary score is now average time per problem
        
        # Clear screen and show results
        self.clear_screen()
        print("=== MENTAL MATH TEST RESULTS ===")
        print(f"Problems attempted: {total}")
        print(f"Correct answers: {correct}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Penalty time added: {penalty_time:.1f}s")
        print(f"Average time per problem: {avg_time_per_problem:.2f}s")
        print(f"This measures processing speed and arithmetic accuracy.")
        
        self.record_result("Mental Math", score, {
            'problems_attempted': total,
            'correct_answers': correct,
            'accuracy_percent': round(accuracy, 1),
            'avg_time_per_problem': round(avg_time_per_problem, 2),
            'penalty_time': round(penalty_time, 1),
            'time_limit': 60
        })
        
        input("\nPress Enter to continue...")
        self.clear_screen()
    
    def word_recall_test(self):
        """Memory word list recall test"""
        # Build a larger pool of simple words (cached and filtered from system dictionary when available)
        words = self.get_word_bank()
        
        self.clear_screen()
        print("=== WORD RECALL TEST ===")
        print("I'll show you a list of words to memorize.")
        print("Press Ctrl+C to exit test without saving data")
        print()
        print("Ready to start?")
        input("Press Enter when you're ready to begin...")
        
        # Select random words
        sample_size = 12 if len(words) >= 12 else min(12, len(words))
        test_words = random.sample(words, sample_size)
        
        try:
            print(f"\nMemorize these {len(test_words)} words:")
            for i, word in enumerate(test_words, 1):
                print(f"{i:2d}. {word}")
            
            print(f"\nStudy for 30 seconds...")
            time.sleep(30)
            
            # Clear screen to prevent looking back
            self.clear_screen()
            print("=== WORD RECALL TEST ===")
            print("Now write down as many words as you can remember.")
            print("Enter one word per line. Press ENTER on empty line to finish.")
            
            recalled_words = []
            while True:
                word = input("Word: ").strip().lower()
                if not word:
                    break
                recalled_words.append(word)
                
        except KeyboardInterrupt:
            self.clear_screen()
            print("=== TEST INTERRUPTED ===")
            print("Word recall test was cancelled. No data saved.")
            input("\nPress Enter to return to main menu...")
            self.clear_screen()
            return
        
        # Score the recall
        correct_recalls = sum(1 for word in recalled_words if word in [w.lower() for w in test_words])
        total_words = len(test_words)
        score = (correct_recalls / total_words) * 100
        
        # Clear screen and show results
        self.clear_screen()
        print("=== WORD RECALL TEST RESULTS ===")
        print(f"Words to remember: {total_words}")
        print(f"Words recalled: {len(recalled_words)}")
        print(f"Correct recalls: {correct_recalls}")
        print(f"Accuracy: {score:.1f}%")
        print(f"This measures memory encoding and retrieval.")
        
        # Show missed words
        missed = [word for word in test_words if word.lower() not in recalled_words]
        if missed:
            print(f"Missed words: {', '.join(missed)}")
        
        self.record_result("Word Recall", score, {
            'total_words': total_words,
            'words_recalled': len(recalled_words),
            'correct_recalls': correct_recalls
        })
        
        input("\nPress Enter to continue...")
        self.clear_screen()
    
    def stroop_test(self):
        """Enhanced Stroop test with time pressure - color naming interference"""
        colors = ['red', 'blue', 'green', 'yellow']
        color_codes = {
            'red': 'r',
            'blue': 'b', 
            'green': 'g',
            'yellow': 'y'
        }
        
        # High-contrast ANSI color codes (bold + 256-color) for terminal display
        # Text colors
        ansi_text_colors = {
            'red': '\033[1;38;5;196m',    # Bright red text
            'blue': '\033[1;38;5;21m',    # Bright blue text
            'green': '\033[1;38;5;46m',   # Neon green text
            'yellow': '\033[1;38;5;226m'  # Bright yellow text
        }
        # Background colors
        ansi_bg_colors = {
            'red': '\033[48;5;196m',      # Red background
            'blue': '\033[48;5;21m',      # Blue background
            'green': '\033[48;5;46m',     # Green background
            'yellow': '\033[48;5;226m'    # Yellow background
        }
        reset_color = '\033[0m'
        
        self.clear_screen()
        print("=== TRIPLE INTERFERENCE STROOP TEST ===")
        print("You'll see color words with TRIPLE INTERFERENCE:")
        print("1. Word meaning (e.g., 'BLUE')")
        print("2. Text color (e.g., red text)")  
        print("3. Background color (e.g., green background)")
        print("")
        print("Type the first letter of the TEXT COLOR (not the word or background)!")
        print("TIME LIMIT: You have 3 seconds per trial - respond quickly!")
        print("Press Ctrl+C to exit test without saving data")
        print(f"\nResponse keys: r=red, b=blue, g=green, y=yellow")
        
        # Show legend and examples with triple interference
        print("\nColor legend:")
        print(f"  {ansi_text_colors['red']}RED TEXT{reset_color}  {ansi_text_colors['blue']}BLUE TEXT{reset_color}  {ansi_text_colors['green']}GREEN TEXT{reset_color}  {ansi_text_colors['yellow']}YELLOW TEXT{reset_color}")
        print(f"\nExample: {ansi_bg_colors['green']}{ansi_text_colors['red']}BLUE{reset_color} = word 'BLUE' in RED text on GREEN background → type 'r' for red text")
        print(f"Example: {ansi_bg_colors['yellow']}{ansi_text_colors['blue']}RED{reset_color} = word 'RED' in BLUE text on YELLOW background → type 'b' for blue text")
        
        print(f"\nREMEMBER: You have only 3 seconds per trial!")
        print("Press ENTER to start...")
        input()
        
        correct = 0
        total = 0
        times = []
        test_completed = False
        
        print("\nSTART!")
        
        try:
            timeouts = 0
            for trial in range(25):  # Increased trials for better assessment
                # Triple interference: word, text color, and background color all different
                word = random.choice(colors)
                text_color = random.choice([c for c in colors if c != word])
                # Background color different from both word and text color
                available_bg_colors = [c for c in colors if c != word and c != text_color]
                bg_color = random.choice(available_bg_colors)
                
                print(f"\nTrial {trial + 1}/25")
                
                # Display the word with triple interference (background + text color)
                colored_word = f"{ansi_bg_colors[bg_color]}{ansi_text_colors[text_color]}{word.upper()}{reset_color}"
                print(f"Word: {colored_word}")
                
                print(f"TEXT Color? ({'/'.join(color_codes.values())}): ", end="", flush=True)
                
                start_time = time.time()
                
                # Implement time pressure with timeout
                response = ""
                try:
                    import select
                    import sys
                    if hasattr(select, 'select'):
                        # Unix-like systems
                        ready, _, _ = select.select([sys.stdin], [], [], 3.0)  # 3 second timeout
                        if ready:
                            response = sys.stdin.readline().strip().lower()
                        else:
                            print("\n⏰ Time's up!")
                            timeouts += 1
                    else:
                        # Fallback for systems without select
                        response = input().strip().lower()
                except:
                    # Fallback to regular input if select fails
                    response = input().strip().lower()
                
                response_time = time.time() - start_time
                times.append(response_time)
                
                total += 1
                if response and response == color_codes[text_color]:
                    correct += 1
                    if response_time <= 3.0:
                        print("✓ Correct!")
                    else:
                        print("✓ Correct (but slow)")
                elif response_time > 3.0 or not response:
                    print(f"⏰ Too slow! Answer was '{color_codes[text_color]}' for {text_color} text")
                else:
                    print(f"✗ Wrong. Correct answer was '{color_codes[text_color]}' for {text_color} text")
            
            # Mark as completed if all trials finished
            test_completed = True
            
        except KeyboardInterrupt:
            self.clear_screen()
            print("=== TEST INTERRUPTED ===")
            print("Stroop test was cancelled. No data saved.")
            input("\nPress Enter to return to main menu...")
            self.clear_screen()
            return
        
        # Only proceed if test completed
        if not test_completed:
            return
            
        accuracy = (correct / total * 100) if total > 0 else 0
        avg_time = sum(times) / len(times) if times else 0
        
        # Clear screen and show results
        self.clear_screen()
        print("=== ENHANCED STROOP TEST RESULTS ===")
        print(f"Trials completed: {total}")
        print(f"Correct responses: {correct}")
        print(f"Timeouts (>3s): {timeouts}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Average response time: {avg_time:.3f} seconds")
        fast_responses = sum(1 for t in times if t <= 3.0)
        print(f"Responses within 3s: {fast_responses}/{total} ({fast_responses/total*100:.1f}%)")
        print(f"This triple-interference test measures attention and cognitive inhibition under extreme pressure.")
        print(f"Triple interference (word + text color + background) creates maximum cognitive conflict.")
        print(f"Time pressure particularly challenges sleep-deprived cognitive control.")
        
        # Use average response time as primary score (lower is better)
        self.record_result("Stroop Test", avg_time, {
            'accuracy_percent': round(accuracy, 1),
            'average_response_time': round(avg_time, 3),
            'timeouts': timeouts,
            'fast_responses': fast_responses,
            'time_pressure_accuracy': round(fast_responses/total*100, 1) if total > 0 else 0,
            'trials_completed': total
        })
        
        input("\nPress Enter to continue...")
        self.clear_screen()
    
    def sustained_attention_test(self):
        """Count backwards by a random increment from 100 down to the last non-negative number"""
        self.clear_screen()
        print("=== SUSTAINED ATTENTION TEST ===")
        
        # Randomly select counting increment
        counting_options = [3, 7, 11, 13, 17, 19]
        count_by = random.choice(counting_options)
        
        print(f"Count backwards from 100 by {count_by}s (100, {100-count_by}, {100-count_by*2}, ...)")
        print("I'll track your accuracy and speed. The test ends automatically when the sequence is complete.")
        print("Press Ctrl+C to exit test without saving data")
        print()
        print("Ready to start?")
        input("Press Enter when you're ready to begin...")
        
        start_number = 100
        correct_sequence = []
        
        # Pre-calculate correct sequence
        num = start_number
        while num >= 0:
            correct_sequence.append(num)
            num -= count_by
        
        print(f"\nStart with: {start_number}")
        print("Next number: ", end="")
        
        start_time = time.time()
        correct = 0
        total = 0
        position = 1  # Start from second number
        test_completed = False
        
        try:
            while position < len(correct_sequence):
                try:
                    user_input = input().strip()
                    if user_input.lower() == 'done':
                        break
                    
                    user_number = int(user_input)
                    expected = correct_sequence[position]
                    
                    total += 1
                    if user_number == expected:
                        correct += 1
                        if position + 1 < len(correct_sequence):
                            print("✓ Correct! Next: ", end="")
                        else:
                            print("✓ Correct! Sequence complete.")
                    else:
                        if position + 1 < len(correct_sequence):
                            print(f"✗ Wrong. Expected {expected}. Next: ", end="")
                        else:
                            print(f"✗ Wrong. Expected {expected}. Sequence complete.")
                    
                    position += 1
                    
                except ValueError:
                    print("Invalid input. Enter a number or 'done': ", end="")
            
            # Mark as completed if we finished the sequence or user said 'done'
            test_completed = True
            
        except KeyboardInterrupt:
            self.clear_screen()
            print("=== TEST INTERRUPTED ===")
            print("Sustained attention test was cancelled. No data saved.")
            input("\nPress Enter to return to main menu...")
            self.clear_screen()
            return
        
        # Only proceed if test completed
        if not test_completed:
            return
            
        elapsed_time = time.time() - start_time
        accuracy = (correct / total * 100) if total > 0 else 0
        # Calculate average time per correct answer (primary score - lower is better)
        avg_time_per_correct = (elapsed_time / correct) if correct > 0 else elapsed_time
        
        # Clear screen and show results
        self.clear_screen()
        print("=== SUSTAINED ATTENTION TEST RESULTS ===")
        print(f"Counting by: {count_by}s from {start_number}")
        print(f"Numbers attempted: {total}")
        print(f"Correct: {correct}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Time taken: {elapsed_time:.1f} seconds")
        print(f"Average time per attempt: {elapsed_time/total:.2f} seconds" if total > 0 else "")
        print(f"Average time per correct answer: {avg_time_per_correct:.2f} seconds")
        print(f"This measures focus, mental endurance, and processing speed under sustained effort.")
        
        # Use average time per correct answer as primary score (lower is better)
        self.record_result("Sustained Attention", avg_time_per_correct, {
            'accuracy_percent': round(accuracy, 1),
            'numbers_attempted': total,
            'correct_answers': correct,
            'time_taken': round(elapsed_time, 1),
            'avg_time_per_attempt': round(elapsed_time/total, 2) if total > 0 else 0,
            'avg_time_per_correct': round(avg_time_per_correct, 2),
            'start_value': start_number,
            'count_by': count_by,
            'end_value': correct_sequence[-1],
            'sequence_length': len(correct_sequence)
        })
        
        input("\nPress Enter to continue...")
        self.clear_screen()
    
    def display_all_results(self):
        """Display summary of all test results grouped by date"""
        print("\n=== ALL RESULTS SUMMARY ===")
        
        if not self.results:
            print("No test results available yet.")
            return
        
        # Group all results by date across all tests
        all_dates = set()
        for test_results in self.results.values():
            for result in test_results:
                result_date = datetime.fromisoformat(result['timestamp']).date()
                all_dates.add(result_date)
        
        if not all_dates:
            print("No test results available yet.")
            return
        
        # Sort dates (most recent first)
        sorted_dates = sorted(all_dates, reverse=True)
        
        print(f"Results available for {len(sorted_dates)} different dates:\n")
        
        # Scoring legend: show what each test measures and benchmark ranges
        print("SCORING LEGEND")
        print("-" * 40)
        legend_tests = [
            "Reaction Time",
            "Digit Span",
            "Mental Math",
            "Word Recall",
            "Stroop Test",
            "Sustained Attention",
        ]
        for legend_test in legend_tests:
            info = self.get_test_info(legend_test)
            print(f"{legend_test}:")
            print(f"  Measures: {info['description']}")
            print(f"  Score: {info['score_type']}")
            print(f"  Benchmarks: {info['good_range']}")
        print()
        
        for result_date in sorted_dates:
            sleep_info = self.get_sleep_for_date(result_date)
            print(f"Date: {result_date.strftime('%Y-%m-%d (%A)')} | Sleep: {sleep_info}")
            print("-" * 40)
            
            date_has_results = False
            
            for test_name, test_results in self.results.items():
                # Get results for this specific date
                date_results = [
                    r for r in test_results 
                    if datetime.fromisoformat(r['timestamp']).date() == result_date
                ]
                
                if date_results:
                    date_has_results = True
                    if test_name == 'Reaction Time':
                        scores = []
                        for r in date_results:
                            if r.get('details') and 'adjusted_average_s' in r['details']:
                                scores.append(r['details']['adjusted_average_s'])
                            else:
                                scores.append(max(0.0, r['score'] - self.get_active_baseline_seconds()))
                    else:
                        scores = [r['score'] for r in date_results]
                    avg_score = sum(scores) / len(scores)
                    
                    # Show number of attempts and average for the day
                    if len(date_results) == 1:
                        print(f"  {test_name}: {scores[0]:.3f} (1 attempt)")
                    else:
                        print(f"  {test_name}: {avg_score:.3f} avg ({len(date_results)} attempts)")
                        print(f"    Range: {min(scores):.3f} - {max(scores):.3f}")
            
            if not date_has_results:
                print("  No test results for this date")
            
            print()  # Empty line between dates
        
        # Overall statistics
        print("OVERALL STATISTICS")
        print("=" * 40)
        
        for test_name, test_results in self.results.items():
            if test_results:
                if test_name == 'Reaction Time':
                    scores = []
                    for r in test_results:
                        if r.get('details') and 'adjusted_average_s' in r['details']:
                            scores.append(r['details']['adjusted_average_s'])
                        else:
                            scores.append(max(0.0, r['score'] - self.get_active_baseline_seconds()))
                else:
                    scores = [r['score'] for r in test_results]
                latest = test_results[-1]
                timestamp = datetime.fromisoformat(latest['timestamp'])
                
                # Get test information for header
                test_info = self.get_test_info(test_name)
                
                print(f"\n{test_name} ({test_info['description']})")
                print(f"   Score Type: {test_info['score_type']}")
                print(f"   Benchmarks: {test_info['good_range']}")
                print(f"   Results:")
                print(f"     Total attempts: {len(test_results)}")
                print(f"     Overall average: {sum(scores)/len(scores):.3f}")
                if test_name == 'Reaction Time':
                    latest_adj = latest['details'].get('adjusted_average_s') if latest.get('details') else None
                    if latest_adj is None:
                        latest_adj = max(0.0, latest['score'] - self.get_active_baseline_seconds())
                    print(f"     Latest: {latest_adj:.3f} (adjusted) — raw {latest['score']:.3f} at {timestamp.strftime('%Y-%m-%d %H:%M')}")
                else:
                    print(f"     Latest: {latest['score']:.3f} ({timestamp.strftime('%Y-%m-%d %H:%M')})")
                
                if len(scores) > 1:
                    # Use test_info to determine if lower or higher is better
                    if test_info['lower_better']:
                        best_score = min(scores)
                        print(f"     Best (lowest): {best_score:.3f}")
                    else:
                        best_score = max(scores)
                        print(f"     Best (highest): {best_score:.3f}")
                
                # Show trend (last 3 vs first 3 if available)
                if len(scores) >= 6:
                    first_three = sum(scores[:3]) / 3
                    last_three = sum(scores[-3:]) / 3
                    if test_info['lower_better']:
                        trend = "improving" if last_three < first_three else "declining"
                        change = abs(last_three - first_three)
                    else:
                        trend = "improving" if last_three > first_three else "declining"
                        change = abs(last_three - first_three)
                    print(f"     Trend: {trend} ({change:.3f} change from first 3 to last 3)")
    
    def sleep_logging_menu(self):
        """Menu for logging sleep data"""
        print("\n=== SLEEP LOGGING ===")
        print("Log your sleep duration to correlate with cognitive performance.")
        
        # Get date input
        print("\nEnter date for sleep log:")
        print("1. Today")
        print("2. Yesterday") 
        print("3. Custom date (YYYY-MM-DD)")
        print("4. Back to main menu")
        
        choice = input("Select option (1-4): ").strip()
        
        target_date = None
        if choice == '1':
            target_date = date.today()
        elif choice == '2':
            target_date = date.today() - datetime.timedelta(days=1)
        elif choice == '3':
            while True:
                try:
                    date_input = input("Enter date (YYYY-MM-DD): ").strip()
                    target_date = datetime.strptime(date_input, '%Y-%m-%d').date()
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD (e.g., 2024-01-15)")
        elif choice == '4':
            return
        else:
            print("Invalid choice.")
            return
        
        if target_date is None:
            return
            
        # Get sleep duration input
        print(f"\nLogging sleep for {target_date.strftime('%Y-%m-%d (%A)')}")
        
        # Check if sleep data already exists for this date
        date_str = target_date.strftime('%Y-%m-%d')
        if date_str in self.sleep_log:
            existing = self.sleep_log[date_str]
            print(f"Current sleep data: {existing['hours']}h {existing['minutes']}m")
            if input("Overwrite existing data? (y/n): ").lower() != 'y':
                return
        
        while True:
            try:
                hours = int(input("Hours of sleep (0-24): ").strip())
                if 0 <= hours <= 24:
                    break
                else:
                    print("Hours must be between 0 and 24.")
            except ValueError:
                print("Please enter a valid number for hours.")
        
        while True:
            try:
                minutes = int(input("Additional minutes (0-59): ").strip())
                if 0 <= minutes <= 59:
                    break
                else:
                    print("Minutes must be between 0 and 59.")
            except ValueError:
                print("Please enter a valid number for minutes.")
        
        # Save the sleep data
        self.log_sleep(date_str, hours, minutes)
        
        total_hours = hours + minutes / 60
        print(f"\n✅ Sleep logged: {hours}h {minutes}m ({total_hours:.1f} hours total) for {target_date.strftime('%Y-%m-%d')}")
        
        # Show correlation suggestion
        if total_hours < 6:
            print("💡 Note: Less than 6 hours of sleep may significantly impact cognitive performance.")
        elif total_hours < 7:
            print("💡 Note: 6-7 hours of sleep may show some cognitive performance impacts.")
        elif total_hours >= 8:
            print("💡 Note: 8+ hours of sleep typically supports optimal cognitive performance.")
    
    def weekly_trend_graphs(self):
        """Display ASCII line graphs showing weekly trends for each test"""
        print("\n=== WEEKLY TREND GRAPHS ===")
        
        # Check if matplotlib is available before proceeding
        if not self._check_matplotlib_available():
            return
        
        print("Choose a week to analyze:")
        print("1. Current week (Monday-Friday)")
        print("2. Enter a specific week date")
        print("3. Back to main menu")
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '3':
            return
        elif choice == '1':
            # Get current week's Monday
            today = date.today()
            days_since_monday = today.weekday()
            monday = today - timedelta(days=days_since_monday)
        elif choice == '2':
            while True:
                try:
                    date_input = input("Enter date (MM-DD-YY format, e.g., 01-15-24): ").strip()
                    month, day, year = map(int, date_input.split('-'))
                    year = 2000 + year if year < 50 else 1900 + year  # Handle 2-digit years
                    target_date = date(year, month, day)
                    # Get that week's Monday
                    days_since_monday = target_date.weekday()
                    monday = target_date - timedelta(days=days_since_monday)
                    break
                except ValueError:
                    print("Invalid date format. Please use MM-DD-YY (e.g., 01-15-24)")
        else:
            print("Invalid choice.")
            return
        
        # Generate the 5 weekdays (Monday-Friday)
        weekdays = [monday + timedelta(days=i) for i in range(5)]
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        print(f"\nWeek of {monday.strftime('%B %d, %Y')} - {weekdays[-1].strftime('%B %d, %Y')}")
        print("=" * 70)
        
        # Get all test types
        test_types = ["Reaction Time", "Digit Span", "Mental Math", "Word Recall", "Stroop Test", "Sustained Attention"]
        
        # Map test names to full menu titles for graph display
        test_title_map = {
            "Reaction Time": "Reaction Time Test",
            "Digit Span": "Digit Span Test (Working Memory)",
            "Mental Math": "Mental Math Test (Processing Speed)", 
            "Word Recall": "Word Recall Test (Memory)",
            "Stroop Test": "Stroop Test (Attention/Inhibition)",
            "Sustained Attention": "Sustained Attention Test (Random Counting)"
        }
        
        # Collect all test data for matplotlib graphing
        all_test_data = []
        
        for test_name in test_types:
            print(f"\n{test_name}")
            print("-" * 50)
            
            # Collect daily averages for this week
            daily_scores = []
            daily_labels = []
            
            # Check if test has any results at all
            if test_name not in self.results or not self.results[test_name]:
                print(f"   No historical data available for {test_name}")
                # Still add to graphing data with all None values
                daily_scores = [None] * 5
                daily_labels = [f"{weekday_names[i][:3]} (-)" for i in range(5)]
            else:
                for i, day in enumerate(weekdays):
                    day_results = [
                        r for r in self.results[test_name]
                        if datetime.fromisoformat(r['timestamp']).date() == day
                    ]
                    
                    if day_results:
                        if test_name == 'Reaction Time':
                            # Use adjusted values for reaction time
                            scores = []
                            for r in day_results:
                                if r.get('details') and 'adjusted_average_s' in r['details']:
                                    scores.append(r['details']['adjusted_average_s'])
                                else:
                                    scores.append(max(0.0, r['score'] - self.get_active_baseline_seconds()))
                        else:
                            scores = [r['score'] for r in day_results]
                        
                        avg_score = sum(scores) / len(scores)
                        daily_scores.append(avg_score)
                        daily_labels.append(f"{weekday_names[i][:3]} ({len(day_results)})")
                    else:
                        daily_scores.append(None)
                        daily_labels.append(f"{weekday_names[i][:3]} (-)")
            
            # Always collect data for matplotlib graphing (even if no data)
            all_test_data.append({
                'test_name': test_name,
                'weekdays': weekday_names,
                'weekdays_dates': weekdays,  # Add actual date objects
                'scores': daily_scores,
                'labels': daily_labels
            })
            
        
        # Generate matplotlib graphs
        self._display_matplotlib_graphs(all_test_data, monday, weekdays[-1], test_title_map)
    
    def _draw_ascii_graph(self, values, labels, test_name):
        """Draw an ASCII line graph with connected data points"""
        # Filter out None values for scaling
        valid_values = [v for v in values if v is not None]
        
        if not valid_values:
            print("   No data available for this week")
            return
        
        # Determine scale
        min_val = min(valid_values)
        max_val = max(valid_values)
        
        if min_val == max_val:
            # Flat line case
            print(f"   All values: {min_val:.3f}")
            graph_line = "   " + " ".join([f"{label:>8}" for label in labels])
            print(graph_line)
            print("   " + " ".join([f"{'●':>8}" if v is not None else f"{'-':>8}" for v in values]))
            return
        
        # Create graph matrix (5 rows x columns)
        graph_height = 5
        col_width = 8
        graph_matrix = []
        
        # Initialize matrix with spaces
        for row in range(graph_height):
            graph_matrix.append([' '] * (len(values) * col_width + 10))
        
        # Map values to row positions and mark data points
        data_points = []  # Store (col_center, row) for each valid value
        
        for i, val in enumerate(values):
            col_center = 3 + i * col_width + col_width // 2
            
            if val is not None:
                # Calculate which row this value belongs to
                val_ratio = (val - min_val) / (max_val - min_val)
                row = int((1 - val_ratio) * (graph_height - 1))
                row = max(0, min(graph_height - 1, row))
                
                # Mark the data point
                graph_matrix[row][col_center] = '●'
                data_points.append((col_center, row))
        
        # Draw connecting lines between adjacent data points
        for i in range(len(data_points) - 1):
            x1, y1 = data_points[i]
            x2, y2 = data_points[i + 1]
            
            # Draw line from (x1,y1) to (x2,y2)
            self._draw_line(graph_matrix, x1, y1, x2, y2)
        
        # Add value labels on the right
        for row in range(graph_height):
            row_threshold = max_val - (row * (max_val - min_val) / (graph_height - 1))
            # Convert row to string and add threshold label
            row_str = ''.join(graph_matrix[row][:len(values) * col_width + 3])
            print(f"   {row_str} {row_threshold:.3f}")
        
        # Print x-axis labels
        x_axis = "   " + "".join([f"{label:>8}" for label in labels])
        print(x_axis)
        
        # Print actual values
        value_line = "   " + "".join([f"{v:.3f}">8 if v is not None else f"{'---':>8}" for v in values])
        print(value_line)
        
        # Show improvement/decline
        if len(valid_values) >= 2:
            first_val = next(v for v in values if v is not None)
            last_val = next(v for v in reversed(values) if v is not None)
            
            test_info = self.get_test_info(test_name)
            if test_info['lower_better']:
                trend = "↗️ Improving" if last_val < first_val else "↘️ Declining" if last_val > first_val else "→ Stable"
            else:
                trend = "↗️ Improving" if last_val > first_val else "↘️ Declining" if last_val < first_val else "→ Stable"
            
            change = abs(last_val - first_val)
            print(f"   Week trend: {trend} (Δ {change:.3f})")
    
    def _check_matplotlib_available(self) -> bool:
        """Check if matplotlib is available and provide installation guidance if not"""
        try:
            import matplotlib
            return True
        except ImportError:
            print("\n" + "="*60)
            print("                MATPLOTLIB NOT INSTALLED")
            print("="*60)
            print()
            print("[ERROR] The Weekly Trend Graphs feature requires matplotlib to display")
            print("        professional-quality charts and graphs.")
            print()
            print("INSTALLATION INSTRUCTIONS:")
            print("-" * 25)
            
            # Detect which Python command is being used
            python_cmd = self._detect_python_command()
            
            print(f"1. Install matplotlib using {python_cmd}:")
            print(f"   {python_cmd} -m pip install matplotlib")
            print()
            print("2. Alternative installation methods:")
            print("   - Using pip directly: pip install matplotlib")
            print("   - Using conda: conda install matplotlib")
            print()
            print("WHAT MATPLOTLIB PROVIDES:")
            print("- Interactive graphs that you can zoom and pan")
            print("- High-quality PNG files saved automatically")
            print("- Color-coded performance bands")
            print("- Professional chart formatting")
            print("- Sleep correlation visualizations")
            print()
            print("After installation, restart this program and try again.")
            print("="*60)
            
            input("\nPress Enter to return to main menu...")
            return False
    
    def _detect_python_command(self) -> str:
        """Detect which Python command is being used to run this script"""
        import sys
        import os
        
        # Get the executable path
        python_exe = sys.executable
        
        # Extract just the filename
        python_name = os.path.basename(python_exe).lower()
        
        # Common Python command variations
        if 'python3' in python_name:
            return 'python3'
        elif 'python' in python_name:
            return 'python'
        else:
            # Fallback - return the full path
            return python_exe
    
    def _detect_gui_environment(self) -> bool:
        """Detect if we're running in a GUI-capable environment"""
        # Check various indicators of GUI availability
        
        # 1. Check DISPLAY environment variable (Linux/macOS X11)
        if os.environ.get('DISPLAY'):
            return True
        
        # 2. Check if we're in Windows with a desktop session
        if platform.system() == 'Windows':
            # Check for interactive session
            session_name = os.environ.get('SESSIONNAME', '').lower()
            
            # Admin PowerShell and some terminals may have limited GUI access
            # Check if we're running as admin (common cause of GUI issues)
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if is_admin:
                    print("   Detected admin privileges - GUI may be limited")
                    # Admin sessions often have GUI restrictions
                    return False
            except:
                pass
            
            # Check if we have access to GUI libraries with a real test
            try:
                import tkinter
                root = tkinter.Tk()
                root.withdraw()  # Hide the window
                # Try to actually use the GUI
                root.update()
                root.destroy()
                return True
            except Exception as e:
                print(f"   GUI test failed: {e}")
                return False
        
        # 3. Check for macOS GUI
        if platform.system() == 'Darwin':
            # Check if we're in a terminal that supports GUI
            if os.environ.get('TERM_PROGRAM') in ['iTerm.app', 'Terminal.app', 'vscode']:
                return True
        
        # 4. Check for common terminal environment indicators
        term_program = os.environ.get('TERM_PROGRAM', '').lower()
        term = os.environ.get('TERM', '').lower()
        
        # Known GUI-capable terminals (but not guaranteed)
        gui_terminals = ['vscode', 'cursor', 'iterm', 'terminal', 'hyper', 'alacritty']
        if any(gui_term in term_program for gui_term in gui_terminals):
            # Even these can have issues, so do a real test
            try:
                import tkinter
                root = tkinter.Tk()
                root.withdraw()
                root.update()
                root.destroy()
                return True
            except:
                return False
        
        # Known problematic terminals for GUI
        problematic_terms = ['screen', 'tmux']
        if any(prob_term in term for prob_term in problematic_terms):
            return False
        
        # 5. Detect specific terminal applications that commonly have GUI issues
        if ('tabby' in term_program or 
            os.environ.get('TABBY_CONFIG_DIRECTORY') or
            'powershell' in os.environ.get('PSModulePath', '').lower()):
            # These often have GUI limitations
            print("   Detected potentially GUI-limited terminal environment")
            return False
        
        # Default: be conservative and test for real GUI capability
        try:
            import tkinter
            root = tkinter.Tk()
            root.withdraw()
            root.update()
            root.destroy()
            return True
        except:
            return False
    
    def _draw_line(self, matrix, x1, y1, x2, y2):
        """Draw a line between two points in the ASCII matrix"""
        # Simple line drawing using Bresenham-like algorithm
        if x1 == x2:  # Vertical line
            start_y, end_y = (y1, y2) if y1 < y2 else (y2, y1)
            for y in range(start_y + 1, end_y):
                if 0 <= y < len(matrix) and 0 <= x1 < len(matrix[0]):
                    if matrix[y][x1] == ' ':
                        matrix[y][x1] = '│'
        elif y1 == y2:  # Horizontal line
            start_x, end_x = (x1, x2) if x1 < x2 else (x2, x1)
            for x in range(start_x + 1, end_x):
                if 0 <= y1 < len(matrix) and 0 <= x < len(matrix[0]):
                    if matrix[y1][x] == ' ':
                        matrix[y1][x] = '─'
        else:  # Diagonal line
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            
            x, y = x1, y1
            while True:
                if x == x2 and y == y2:
                    break
                    
                if 0 <= y < len(matrix) and 0 <= x < len(matrix[0]):
                    if matrix[y][x] == ' ':
                        # Choose appropriate line character based on direction
                        if abs(dx) > abs(dy):
                            matrix[y][x] = '─'
                        elif abs(dy) > abs(dx):
                            matrix[y][x] = '│'
                        else:
                            matrix[y][x] = '┼' if (sx * sy) > 0 else '┼'
                
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy
    
    def _display_matplotlib_graphs(self, test_data, start_date, end_date, test_title_map):
        """Display professional-quality graphs using matplotlib"""
        if not test_data:
            print("No data available for graphing.")
            return
        
        try:
            # Import matplotlib here to avoid backend issues
            import matplotlib
            
            # Detect if we're in a GUI-capable environment
            gui_available = self._detect_gui_environment()
            
            # Use appropriate backend for the platform with fallbacks
            backend_set = False
            if platform.system() == 'Darwin':  # macOS
                try:
                    matplotlib.use('macosx')
                    backend_set = True
                except:
                    pass
            elif platform.system() == 'Windows':
                # Try Windows-friendly backends in order of preference
                # If no GUI available, prioritize Agg (non-interactive)
                if gui_available:
                    backends_to_try = ['TkAgg', 'Qt5Agg', 'Agg']
                else:
                    backends_to_try = ['Agg', 'TkAgg', 'Qt5Agg']
                    print("   No GUI environment detected, prioritizing non-interactive backend")
                
                for backend in backends_to_try:
                    try:
                        matplotlib.use(backend, force=True)
                        backend_set = True
                        print(f"   Using matplotlib backend: {backend}")
                        break
                    except:
                        continue
            else:  # Linux and others
                if gui_available:
                    backends_to_try = ['Qt5Agg', 'TkAgg', 'Agg']
                else:
                    backends_to_try = ['Agg', 'Qt5Agg', 'TkAgg']
                
                for backend in backends_to_try:
                    try:
                        matplotlib.use(backend, force=True)
                        backend_set = True
                        break
                    except:
                        continue
            
            if not backend_set:
                print("   Warning: Could not set preferred backend, using matplotlib default")
            
            import matplotlib.pyplot as plt
            # Create figure with subplots (2 rows, 3 columns for 6 tests)
            fig, axes = plt.subplots(2, 3, figsize=(11.25, 7.5))
            fig.suptitle(f'Mental Performance Trends\n{start_date.strftime("%B %d")} - {end_date.strftime("%B %d, %Y")}', 
                        fontsize=12, fontweight='bold')
            
            # Set window title
            try:
                fig.canvas.manager.set_window_title('Insomniapp - Weekly Trends')
            except:
                pass  # Not all backends support this
            
            # Flatten axes array for easier indexing
            axes_flat = axes.flatten()
            
            for i, data in enumerate(test_data):
                if i >= 6:  # Safety check for max 6 tests
                    break
                    
                ax = axes_flat[i]
                test_name = data['test_name']
                weekdays = data['weekdays']
                scores = data['scores']
                
                # Prepare data for plotting (filter out None values)
                plot_days = []
                plot_scores = []
                
                for j, score in enumerate(scores):
                    if score is not None:
                        plot_days.append(j)
                        # Invert time-based scores for display (lower times = higher on graph)
                        if test_name == 'Reaction Time':
                            # Convert reaction time to inverted score (1.0 - score) so better times show higher
                            inverted_score = 1.0 - score
                            plot_scores.append(inverted_score)
                        elif test_name == 'Stroop Test':
                            # Convert response time to inverted score (5.0 - score) so better times show higher
                            # Using 5.0 as max since performance bands go to 4.0
                            inverted_score = 5.0 - score
                            plot_scores.append(inverted_score)
                        elif test_name == 'Sustained Attention':
                            # Convert time per correct to inverted score (13.0 - score) so better times show higher
                            # Using 13.0 as max since performance bands go to 12.0
                            inverted_score = 13.0 - score
                            plot_scores.append(inverted_score)
                        elif test_name == 'Mental Math':
                            # Convert average time per problem to inverted score (22.0 - score) so better times show higher
                            # Using 22.0 as max since performance bands go to 20.0
                            inverted_score = 22.0 - score
                            plot_scores.append(inverted_score)
                        else:
                            plot_scores.append(score)
                
                if plot_scores:
                    # Plot the line graph
                    ax.plot(plot_days, plot_scores, marker='o', linewidth=1.5, markersize=6, 
                           color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=1.5)
                    
                    # Customize the subplot
                    ax.set_title(test_title_map.get(test_name, test_name), fontsize=9, fontweight='bold', pad=12)
                    ax.set_xticks(range(5))
                    
                    # Create x-axis labels with sleep data
                    x_labels = []
                    for i, day_name in enumerate(weekdays):
                        day_date = data['weekdays_dates'][i]  # Get the actual date
                        sleep_info = self.get_sleep_for_graph_label(day_date)
                        x_labels.append(f"{day_name[:3]}\n{sleep_info}")
                    
                    ax.set_xticklabels(x_labels, rotation=0, ha='center', fontsize=7)
                    ax.grid(True, alpha=0.3, linestyle='--')
                    ax.set_ylabel('Score', fontsize=8)
                    
                    # Add performance bands on the right y-axis
                    performance_bands = self.get_performance_bands(test_name)
                    if performance_bands:
                        # Create a twin axis on the right
                        ax_right = ax.twinx()
                        
                        # Determine adaptive y-axis range based on actual data
                        y_min, y_max = self._get_adaptive_y_range(test_name, plot_scores)
                        
                        ax.set_ylim(y_min, y_max)
                        ax_right.set_ylim(y_min, y_max)
                        
                        # Color mapping
                        colors = {
                            'poor': '#FF4444',      # Red
                            'average': '#FF8C00',   # Orange  
                            'good': '#FFD700',      # Yellow/Gold
                            'excellent': '#32CD32'  # Green
                        }
                        
                        # Get only the active performance bands for this range
                        active_bands = self._get_active_performance_bands(test_name, y_min, y_max)
                        
                        # Add colored horizontal bands (only active ones)
                        for level, (visible_min, visible_max) in active_bands.items():
                            ax_right.axhspan(visible_min, visible_max, alpha=0.15, 
                                            color=colors.get(level, '#CCCCCC'), 
                                            zorder=0)
                        
                        # Add right y-axis labels
                        ax_right.set_ylabel('Performance Level', fontsize=8, rotation=270, labelpad=15)
                        
                        # Set right y-axis ticks at band boundaries (only active ones)
                        tick_positions = []
                        tick_labels = []
                        for level, (visible_min, visible_max) in active_bands.items():
                            mid_point = (visible_min + visible_max) / 2
                            tick_positions.append(mid_point)
                            tick_labels.append(level.title())
                        
                        ax_right.set_yticks(tick_positions)
                        ax_right.set_yticklabels(tick_labels, fontsize=6)
                        ax_right.tick_params(axis='y', colors='gray')
                    
                    # Add value labels on data points
                    for day, score in zip(plot_days, plot_scores):
                        ax.annotate(f'{score:.3f}', (day, score), textcoords="offset points", 
                                  xytext=(0,8), ha='center', fontsize=7, 
                                  bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    
                    # Show trend
                    if len(plot_scores) >= 2:
                        test_info = self.get_test_info(test_name)
                        first_val, last_val = plot_scores[0], plot_scores[-1]
                        
                        if test_info['lower_better']:
                            if last_val < first_val:
                                trend = "↗️ Improving"
                                trend_color = "lightgreen"
                            elif last_val > first_val:
                                trend = "↘️ Declining"
                                trend_color = "lightcoral"
                            else:
                                trend = "→ Stable"
                                trend_color = "lightyellow"
                        else:
                            if last_val > first_val:
                                trend = "↗️ Improving"
                                trend_color = "lightgreen"
                            elif last_val < first_val:
                                trend = "↘️ Declining"
                                trend_color = "lightcoral"
                            else:
                                trend = "→ Stable"
                                trend_color = "lightyellow"
                        
                        change = abs(last_val - first_val)
                        ax.text(0.02, 0.98, f"{trend}\nΔ {change:.3f}", transform=ax.transAxes,
                               fontsize=7, verticalalignment='top',
                               bbox=dict(boxstyle="round,pad=0.3", facecolor=trend_color, alpha=0.7))
                else:
                    # No data case
                    ax.text(0.5, 0.5, 'No data\nfor this week', transform=ax.transAxes, 
                           fontsize=9, ha='center', va='center', style='italic', color='gray')
                    ax.set_title(test_title_map.get(test_name, test_name), fontsize=9, fontweight='bold', pad=12)
                    ax.set_xticks(range(5))
                    
                    # Create x-axis labels with sleep data even for no-data case
                    x_labels = []
                    for i, day_name in enumerate(weekdays):
                        day_date = data['weekdays_dates'][i]  # Get the actual date
                        sleep_info = self.get_sleep_for_graph_label(day_date)
                        x_labels.append(f"{day_name[:3]}\n{sleep_info}")
                    
                    ax.set_xticklabels(x_labels, rotation=0, ha='center', fontsize=7)
                    
                    # Still show performance bands even with no data (use fixed ranges)
                    performance_bands = self.get_performance_bands(test_name)
                    if performance_bands:
                        # Use fixed ranges for no-data case
                        y_min, y_max = self._get_adaptive_y_range(test_name, [])
                        ax.set_ylim(y_min, y_max)
                        
                        # Create a twin axis on the right
                        ax_right = ax.twinx()
                        ax_right.set_ylim(y_min, y_max)
                        
                        # Color mapping
                        colors = {
                            'poor': '#FF4444',      # Red
                            'average': '#FF8C00',   # Orange  
                            'good': '#FFD700',      # Yellow/Gold
                            'excellent': '#32CD32'  # Green
                        }
                        
                        # Get active performance bands
                        active_bands = self._get_active_performance_bands(test_name, y_min, y_max)
                        
                        # Add colored horizontal bands (only active ones)
                        for level, (visible_min, visible_max) in active_bands.items():
                            ax_right.axhspan(visible_min, visible_max, alpha=0.15, 
                                            color=colors.get(level, '#CCCCCC'), 
                                            zorder=0)
                        
                        # Add right y-axis labels
                        ax_right.set_ylabel('Performance Level', fontsize=8, rotation=270, labelpad=15)
                        
                        # Set right y-axis ticks at band boundaries (only active ones)
                        tick_positions = []
                        tick_labels = []
                        for level, (visible_min, visible_max) in active_bands.items():
                            mid_point = (visible_min + visible_max) / 2
                            tick_positions.append(mid_point)
                            tick_labels.append(level.title())
                        
                        ax_right.set_yticks(tick_positions)
                        ax_right.set_yticklabels(tick_labels, fontsize=6)
                        ax_right.tick_params(axis='y', colors='gray')
            
            # Hide any unused subplots
            for i in range(len(test_data), 6):
                axes_flat[i].set_visible(False)
            
            # Adjust layout and display
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)  # Make room for the main title
            
            print("[GRAPHS] Opening interactive graphs in a new window...")
            print("   If no window appears, a PNG file will be saved and opened automatically.")
            print("   Close the graph window to return to the main menu.")
            
            # Force matplotlib to draw everything before showing
            fig.canvas.draw()
            
            # Try to bring window to front
            try:
                fig.canvas.manager.window.wm_attributes('-topmost', 1)
                fig.canvas.manager.window.wm_attributes('-topmost', 0)
            except:
                pass  # Not all backends support this
            
            # Save a backup PNG file
            backup_file = 'insomniapp_trends.png'
            plt.savefig(backup_file, dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"   Graphs saved to: {backup_file}")
            
            # Always try to show interactive plot, but handle failures gracefully
            interactive_success = False
            try:
                # Test if we can actually show plots in this environment
                test_backend = matplotlib.get_backend()
                if test_backend == 'Agg':
                    # Agg backend can't show interactive plots
                    print(f"   Using non-interactive backend ({test_backend}) - skipping interactive display")
                else:
                    plt.show(block=True)  # Block until window is closed
                    print("   Interactive window closed.")
                    interactive_success = True
            except Exception as e:
                print(f"   Interactive window failed to open: {e}")
                print("   This is common in some terminal environments (Tabby, Admin PowerShell, etc.)")
            
            # If interactive display failed or wasn't attempted, open the PNG file
            if not interactive_success:
                print("   Opening PNG file instead...")
                # Open the PNG file using platform-appropriate command
                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', backup_file], check=True)
                    elif platform.system() == 'Windows':
                        subprocess.run(['start', backup_file], shell=True, check=True)
                    else:  # Linux
                        subprocess.run(['xdg-open', backup_file], check=True)
                    print(f"   Opened {backup_file} in default image viewer.")
                    input("   Press Enter to continue...")
                except subprocess.CalledProcessError:
                    print(f"   Could not open {backup_file}. Please open it manually.")
            
        except ImportError:
            print("[ERROR] matplotlib is not installed. Please install it with:")
            print("   pip install matplotlib")
            print("   Falling back to text summary...")
            self._display_text_summary(test_data)
        except Exception as e:
            print(f"[ERROR] Error displaying graphs: {e}")
            print("   Falling back to text summary...")
            import traceback
            traceback.print_exc()  # Print full traceback for debugging
            self._display_text_summary(test_data)
    
    def _display_text_summary(self, test_data):
        """Fallback text summary if matplotlib fails"""
        print("\n=== WEEKLY PERFORMANCE SUMMARY ===")
        
        for data in test_data:
            test_name = data['test_name']
            scores = data['scores']
            labels = data['labels']
            
            print(f"\n{test_name}")
            print("-" * 30)
            
            valid_scores = [s for s in scores if s is not None]
            if valid_scores:
                for i, (score, label) in enumerate(zip(scores, labels)):
                    if score is not None:
                        print(f"  {label}: {score:.3f}")
                
                if len(valid_scores) >= 2:
                    first_val = next(s for s in scores if s is not None)
                    last_val = next(s for s in reversed(scores) if s is not None)
                    test_info = self.get_test_info(test_name)
                    
                    if test_info['lower_better']:
                        trend = "↗️ Improving" if last_val < first_val else "↘️ Declining" if last_val > first_val else "→ Stable"
                    else:
                        trend = "↗️ Improving" if last_val > first_val else "↘️ Declining" if last_val < first_val else "→ Stable"
                    
                    change = abs(last_val - first_val)
                    avg = sum(valid_scores) / len(valid_scores)
                    print(f"  Average: {avg:.3f} | {trend} (Δ {change:.3f})")
            else:
                print("  No data available for this week")
    
    def main_menu(self):
        """Main menu interface"""
        first_iteration = True
        while True:
            # Clear screen for all iterations except the first (to preserve welcome message)
            if not first_iteration:
                self.clear_screen()
            first_iteration = False
            
            print("\n" + "="*60)
            print("                        INSOMNIAPP")
            print("="*60)
            print()
            print("COGNITIVE TESTS:")
            print("  1. Reaction Time Test")
            print("  2. Digit Span Test (Working Memory)")
            print("  3. Mental Math Test (Processing Speed)")
            print("  4. Word Recall Test (Memory)")
            print("  5. Stroop Test (Attention/Inhibition)")
            print("  6. Sustained Attention Test (Random Counting)")
            print()
            print("RESULTS & ANALYSIS:")
            print("  7. View Test Results")
            print("  8. View All Results Summary")
            print("  9. Weekly Trend Graphs")
            print()
            print("OTHER FUNCTIONS:")
            print(" 10. Log Sleep Duration")
            print(" 11. Calibrate Terminal Latency")
            print(" 12. Exit")
            print("="*60)
            
            choice = input("Select option (1-12): ").strip()
            
            try:
                if choice == '1':
                    self.reaction_time_test()
                elif choice == '2':
                    self.digit_span_test()
                elif choice == '3':
                    self.mental_math_test()
                elif choice == '4':
                    self.word_recall_test()
                elif choice == '5':
                    self.stroop_test()
                elif choice == '6':
                    self.sustained_attention_test()
                elif choice == '7':
                    self.view_results_menu()
                elif choice == '8':
                    self.display_all_results()
                elif choice == '9':
                    self.weekly_trend_graphs()
                elif choice == '10':
                    self.sleep_logging_menu()
                elif choice == '11':
                    self.calibrate_terminal_latency()
                elif choice == '12':
                    print("Thank you for using Insomniapp!")
                    break
                else:
                    print("Invalid choice. Please select 1-12.")
                    
            except KeyboardInterrupt:
                print("\n\nTest interrupted. Returning to main menu...")
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Returning to main menu...")
    
    def view_results_menu(self):
        """Sub-menu for viewing historical results"""
        tests = [
            "Reaction Time", "Digit Span", "Mental Math", 
            "Word Recall", "Stroop Test", "Sustained Attention"
        ]
        
        print("\n=== VIEW RESULTS ===")
        for i, test in enumerate(tests, 1):
            print(f"{i}. {test}")
        print("7. Back to main menu")
        
        choice = input("Select test to view results (1-7): ").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= 6:
                self.display_results(tests[choice_num - 1])
            elif choice_num == 7:
                return
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

def main():
    """Main function to run Insomniapp"""
    # Clear screen on startup for a clean interface
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("Welcome to Insomniapp!")
    print("This program will help you assess your mental performance.")
    print("Results are automatically saved and you can track your progress over time.")
    
    suite = InsomniappSuite()
    suite.main_menu()

if __name__ == "__main__":
    main()