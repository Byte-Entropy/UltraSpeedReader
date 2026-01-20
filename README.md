# UltraSpeedReader

A Python-based speed reading application built with Kivy, designed to help users read text faster using Rapid Serial Visual Presentation (RSVP).

## Project Roadmap & To-Do List

### 🛠 Phase 1: Debugging & Stability
- [ ] **Fix KV Loading Warning**: Resolve the issue where `speedread.kv` is loaded multiple times to prevent side effects.
- [ ] **Fix UI Overlap**: Correct the bug where the slider's old value overlaps with the new value, making the label unreadable.
- [ ] **Code Simplification**: Refactor and simplify error-prone sections of the codebase.

### 🚀 Phase 2: Core Features
- [ ] **Smart Resume**: specific implementation to save the current word index in `config.json` and resume reading from that exact spot.
- [ ] **Punctuation Pacing**: Implement variable delays for punctuation (e.g., longer pauses for periods `.`, medium for semi-colons `;`, short for commas `,`) to improve comprehension.
- [ ] **JSON Configuration**: Ensure all user settings (WPM, last position) are robustly saved and loaded via `config.json`.

### ✨ Phase 3: Advanced Polishing
- [ ] **Visual Anchoring**: Implement a feature to split words and highlight the middle letter (or middle -1) in red to center the user's focus.
- [ ] **Mobile Optimization**: Testing and layout adjustments for phone screens.
- [ ] **App Store Prep**: Final preparations for App Store implementation.

### 📝 Documentation
- [ ] Update README with feature descriptions.