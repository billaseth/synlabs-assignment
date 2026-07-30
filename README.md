markdown
# Synlabs GenAI Engineering Take-Home Assignment

This repository contains the solution for the Synlabs GenAI take-home assignment, featuring a local offline RAG application and an automated LLM-as-Judge evaluation pipeline.

---

## Project Structure

```text
synlabs-take-home-assignment/
├── problem_1_rag/
│   ├── data/
│   │   └── sample.txt
│   ├── chroma_db/
│   ├── ingest.py
│   └── app.py
│
└── problem_2_judge/
    ├── test_suite.json
    └── judge.py

```

---

## Problem 1: Free & Local RAG Application (`problem_1_rag/`)

An offline Retrieval-Augmented Generation system built using ChromaDB for local vector storage, retrieval, and grounded answer generation with source citations.

### Execution Instructions:

1. Navigate to the RAG directory:
```bash
cd problem_1_rag

```


2. Ingest documents into the vector store:
```bash
python ingest.py

```


3. Run the application:
```bash
python app.py

```



---

## Problem 2: LLM-as-Judge Evaluation Pipeline (`problem_2_judge/`)

An evaluation framework that assesses test cases against quality criteria, computes automated scoring, tracks pass rates, and includes checks for position bias mitigation.

### Execution Instructions:

1. Navigate to the Judge directory:
```bash
cd problem_2_judge

```


2. Run the evaluation pipeline:
```bash
python judge.py

```



---



```

```
