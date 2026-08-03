# EchoMatch 2.0 System Architecture & Data Flow

This document details the components, data flow, and evaluation touchpoints of EchoMatch 2.0.

```mermaid
graph TD
    %% 1. Input Section
    subgraph Inputs ["1. Input Layer"]
        UserQuery["User Natural Language Query (UI/CLI)"]
        EvalRunner["Automated Evaluator (evaluate.py)"]
    end

    %% 2. Processing Section
    subgraph Processing ["2. Processing & Reasoning Layer"]
        IG["Input Guardrail (LLM Checker)"]
        
        subgraph RAG ["RAG Component"]
            DB[(Song Catalog: songs.csv)]
            Retriever["Context Retriever (Serializes songs)"]
        end
        
        subgraph AgenticLoop ["Agentic Workflow"]
            RecAgent["Recommendation Agent (LLM)"]
            DraftRec["Draft JSON Recommendations"]
            CritiqueAgent["Critique & Verification Agent (LLM)"]
            Correction["Self-Correction Step"]
        end
    end

    %% 3. Output Section
    subgraph Outputs ["3. Output Layer"]
        FinalRecs["Verified Song Recommendations & Explanations"]
        ErrorBlock["Safe Blocked Response"]
    end

    %% 4. Human & Testing Loops
    subgraph FeedbackLoops ["4. Human & Verification Layer"]
        HumanUI["Human Visual Inspection (Streamlit UI Logs)"]
        EvalReport["Evaluation Suite Reports (evaluation_report.md)"]
    end

    %% Data Flow Connections
    UserQuery --> IG
    EvalRunner --> IG
    
    IG -- "Blocked (Off-topic/Jailbreak)" --> ErrorBlock
    IG -- "Passed (Safe & Relevant)" --> Retriever
    
    DB --> Retriever
    Retriever -- "In-context RAG Data" --> RecAgent
    
    RecAgent --> DraftRec
    DraftRec --> CritiqueAgent
    
    CritiqueAgent -- "Fails Validation (Hallucination/Mismatch)" --> Correction
    Correction --> RecAgent
    
    CritiqueAgent -- "Approved" --> FinalRecs
    
    %% Inspection & Evaluation Flow
    FinalRecs --> HumanUI
    ErrorBlock --> HumanUI
    
    FinalRecs --> EvalReport
    ErrorBlock --> EvalReport
```

## Component Definitions

1. **Input Guardrail**: Blocks jailbreaks, prompt injections, and off-topic prompts.
2. **Context Retriever (RAG)**: Serializes the 20-song catalog from `data/songs.csv` and injects it as context into the prompt, ensuring the AI only recommends existing songs.
3. **Recommendation Agent**: Reasons over the user's mood, genre, and acoustic requests to select the best songs from the catalog context.
4. **Critique Agent**: Detects hallucinations (checks returned IDs against the database) and flags severe matches mismatches.
5. **Automated Evaluator**: The CLI test runner that programmatically inspects outcomes to log passing rates.
6. **Human Interaction (Streamlit UI)**: Exposes the step-by-step agent logs so users can inspect *why* a song was recommended and review the system's decisions.
