# Project Structure Overview

```
ESG_Chatbot
├─ chatbot.py  
├─ config                                             # Main chatbot program (Gradio interface)
│  ├─ config.ini                                      # Configuration files include API keys
│  ├─ __init__.py
├─ Data                                               # Data resources
│  ├─ after_process                                   # Processed data                   
│  │  ├─ base.csv                                     # Core company dataset
│  │  ├─ keywords.csv                                 # the result of keyword extraction
│  │  └─ sentiment_results.csv                        # the result of sentiment analysis
│  └─ source_file                                     # Original data
├─ exports                                            # Conversation exports
│  ├─ chat_1745854069.md
│  ├─ chat_1745879183.md
│  └─ chat_1745933998.md
├─ llm                                                # LLM core components
│  ├─ agent_process.py                                # Agent process  
│  ├─ __init__.py
├─ src        
│  └─ keyword                                         # The method implement of Keyword Extraction 
│     ├─ bert.py                
│     ├─ llm.py                 
│     ├─ main.py                
│     ├─ README.md              
│     ├─ requirements.txt       
│     └─ textrank.py            
├─ README.md
└─ sessions                                           # Sessiosn data  
   └─ latest_session.json
```

# Core Module Specifications

## 1. Chatbot Main Program (chatbot.py)

• Gradio-based interactive interface

• Key Features:

  • Multi-turn conversation management (Markdown support)

  • Dynamic model parameter control (temperature/model selection)

  • File preview system (auto-encoding detection)

  • Session persistence & export (JSON/Markdown)

## 2. LLM Agent Engine (agent_process.py)

• LangChain-powered agent architecture:

```python
Agent Architecture
  ┌─────────────────┐        ┌───────────────────┐
  │ Fuzzy Matcher    │◄─┤     │ Data Query Tool    │
  └─────────────────┘        └───────────────────┘
           ▲                        ▲
           │                        │
  ┌─────────────────┐        ┌───────────────────┐
  │ Ranking Generator │◄─┤     │ Field Explainer    │
  └─────────────────┘        └───────────────────┘
           ▲
           │
  ┌─────────────────┐
  │ Agent Controller  │
  └─────────────────┘
```

• Core Capabilities:

  • Company name fuzzy matching (fuzzywuzzy)

  • Multi-dimensional data retrieval (ESG/SDG scores, risk metrics)

  • Dynamic ranking generation (any numeric column)

  • Field explanation system

### 3. Data Layer

• Core dataset includes:

```python
Columns = [
    'Symbol', 'Name', 'Address', 'Sector', 'Industry',
    'Full Time Employees', 'Description', 'Total ESG Risk score',
    'Environment Risk Score', 'Governance Risk Score', 'Social Risk Score',
    'Controversy Level', 'Controversy Score', 'ESG Risk Percentile',
    'ESG Risk Level', 'SDG Score', 'topic', 'keywords'
]
```

• Extendable with:

  • Annual report text analysis results

  • Social media sentiment analysis

  • SDG score prediction outputs

### 4. System Features

• Hybrid reasoning architecture:

```python
Processing Flow
User Query → 
[Local Agent] → Data Retrieval/Calculation → 
[LLM Inference] → Result Integration → 
[Gradio Rendering] → Visual Output
```

• Supports Alibaba's Qwen model series and Deepseek's LLM

• Stream processing (stream=True) for real-time responses

### 5. Keyword Extraction

• Multi-method extraction architecture(src/keyword):

```python
Keyword Extraction Pipeline
  ┌───────────────┐       ┌───────────────┐       ┌─────────────┐
  │ TextRank      │       │ BERT-Enhanced │       │ LLM Analyst │
  │ (RAKE Algorithm)│◄─┤  │ (KeyBERT)     │◄─┤    │ (Qwen-Long) │
  └───────────────┘       └───────────────┘       └─────────────┘
           │                       │                       │
           ▼                       ▼                       ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                Unified Output Processor                       │
  │ • JSON Standardization  • Spell Checking  • Blacklist Filter  │
  │ • Quality Validation                                         │
  └───────────────────────────────────────────────────────────────┘
```

Core Capabilities  
TextRank Rapid Extraction  
• RAKE algorithm with NLTK preprocessing  
• Automatic long-phrase filtering (`max_words=3`)  
• Processing speed: 2 million words/minute  

BERT Semantic Enhancement  
• Based on `distilbert-base-nli-mean-tokens` model  
• Triple filtering mechanism: POS filtering (Nouns/Proper Nouns), Spell validation (SpellChecker), Custom blacklist (500+ noise words)