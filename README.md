# UltraSpeedReader

A Python-based speed reading application built with Kivy, designed to help users read text faster using Rapid Serial Visual Presentation (RSVP).

## Project Roadmap & To-Do List

### 🛠 Phase 1: Debugging & Stability
- [ ] [cite_start]**Fix KV Loading Warning**: Resolve the issue where `speedread.kv` is loaded multiple times to prevent side effects[cite: 77].
- [ ] [cite_start]**Fix UI Overlap**: Correct the bug where the slider's old value overlaps with the new value, making the label unreadable[cite: 78].
- [ ] [cite_start]**Code Simplification**: Refactor and simplify error-prone sections of the codebase[cite: 77].

### 🚀 Phase 2: Core Features
- [ ] [cite_start]**Smart Resume**: specific implementation to save the current word index in `config.json` and resume reading from that exact spot[cite: 79].
- [ ] [cite_start]**Punctuation Pacing**: Implement variable delays for punctuation (e.g., longer pauses for periods `.`, medium for semi-colons `;`, short for commas `,`) to improve comprehension[cite: 78].
- [ ] [cite_start]**JSON Configuration**: Ensure all user settings (WPM, last position) are robustly saved and loaded via `config.json`[cite: 79].

### ✨ Phase 3: Advanced Polishing
- [ ] [cite_start]**Visual Anchoring**: Implement a feature to split words and highlight the middle letter (or middle -1) in red to center the user's focus[cite: 79].
- [ ] [cite_start]**Mobile Optimization**: Testing and layout adjustments for phone screens[cite: 79].
- [ ] [cite_start]**App Store Prep**: Final preparations for App Store implementation[cite: 79].

### 📝 Documentation
- [ ] Update README with feature descriptions.