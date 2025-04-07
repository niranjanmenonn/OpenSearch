# OpenSearch
A privacy-focused, intelligent search engine with advanced features including concept mapping and system control capabilities. Built with Flask and modern web technologies, it provides encrypted search results, content summarization, and visual concept maps to enhance information discovery while maintaining user privacy.

Features

Privacy-First Architecture: Query obfuscation, encryption of search results, and secure session management
Multi-Modal Search: Integrated web, image, and video search capabilities
AI-Powered Insights: Content summarization, entity extraction, and topic identification
Interactive Concept Maps: Visual representation of search concepts and relationships
News Aggregation: Real-time news from multiple sources categorized by topic
System Controls: Integrated brightness and volume controls for Windows systems

Technical Stack

Backend: Flask with security enhancements (Talisman, CSP headers)
NLP Processing: spaCy and NLTK for natural language understanding
Data Visualization: Graphviz for concept mapping
Encryption: Fernet symmetric encryption with PBKDF2HMAC key derivation
External APIs: Google Custom Search API for search results
Frontend: Responsive design with modern JavaScript

Security Features

Content Security Policy (CSP) implementation
Query obfuscation to prevent tracking
Encryption of sensitive data
Secure session management
Sanitized API calls

System Requirements

Python 3.7+
Windows OS (for brightness and volume control features)
