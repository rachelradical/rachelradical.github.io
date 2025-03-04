# Anomaly Storyteller AI – Project Summary
Overview:
The Anomaly Storyteller AI is a Python-based analytics tool designed to detect and explain anomalies in barcode scan data. The project integrates data science, machine learning, and AI-generated storytelling to analyze ID scan anomalies across multiple store locations.

**Instructions**
1. Run generate_dataset.py to generate the sample datasets for anomaly detection. This step could be replaced with providing real-world data!
2. Go through the anomaly_detection jupyter notebook and run each section. This performs the neccessary data analysis and organization.
3. Run storyteller.py to prompt Chat GPT 3.5 turbo to use the data analysis and context data to provide likely explanations for the anomalies, highlighting which anomalies should be investigated for fraud.

Key Features:
Data Generation & Simulation – Generates realistic barcode scan data with embedded anomalies.
Multi-Factor Anomaly Detection – Identifies irregularities using statistical methods (e.g., Z-scores, checksum validation).
AI-Powered Storytelling – Uses OpenAI's GPT-3.5 Turbo to generate contextual explanations for detected anomalies.
Optimized API Calls – Batches API requests to minimize costs while maintaining insightful analysis.
Data Visualization & Reporting – Produces graphical representations of anomalies for easier interpretation.

Technical Highlights:
Python & Pandas – Data manipulation and statistical analysis.
Machine Learning Techniques – Detecting frequency-based anomalies using statistical modeling.
API Integration – Uses OpenAI’s GPT model to contextualize anomalies.
Efficient Data Pipelines – Process automation, data cleaning, and structured reporting.

How It Works:
Data Simulation: Generates a month’s worth of scan data with realistic transaction patterns.
Anomaly Detection: Flags unusual scan behaviors (e.g., repeated scans, invalid ID patterns).
AI Storytelling: Summarizes anomalies into human-readable explanations with possible causes.
Final Report: Merges insights into a structured JSON file for further analysis.

Potential Applications:
Fraud Detection: Identifying fraudulent ID use in retail transactions.
Business Intelligence: Understanding store traffic and operational inefficiencies.
Machine Learning Research: Extending the pipeline to incorporate predictive analytics for anomaly forecasting.
