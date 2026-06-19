\# Project 1: Advanced Rule-Based AI Chatbot Logic Engine



\## 📌 Project Overview

This project delivers a production-grade, rule-based chatbot framework designed under the \*\*Input-Process-Output (IPO)\*\* model guidelines. It serves as a deterministic "White Box" control layer, executing predictable data transformations without hallucination risks.



Rather than relying on static, hardcoded conditional branches inside the main execution file, this architecture decouples the core decision logic from the data layer by sourcing intents directly from an external JSON-based knowledge base.



\### 🌟 Advanced Features Implemented:

1\. \*\*Dynamic State \& Memory Integration:\*\* Tracks user profile states (such as names) persistently across the runtime loop to inject contextual markers into outbound responses.

2\. \*\*Decoupled Knowledge Layer (`intents.json`):\*\* Manages responses and trigger keywords independently, allowing the system to scale without modifying execution logic.

3\. \*\*List-Based Keyword Verification:\*\* Utilizes short-circuiting sequence matching (`any()`) to match human intent variables seamlessly.

4\. \*\*Variational Feedback Matrix:\*\* Employs randomized payload retrieval arrays to provide dynamic conversation flow variants instead of rigid responses.



\---



\## 📂 System Architecture \& Directory Layout



```text

rule\_based\_chatbot/

│

├── chatbot.py          # Main execution engine (Input handling, state tracking, \& control flow)

└── intents.json        # External declarative data registry containing intents and keywords

