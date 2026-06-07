# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Student reviews and experiences about UT Austin MSDS courses, professors, workload, and preparation tips.

This knowledge is valuable because official UT Austin pages explain degree requirements and course descriptions, but they do not always explain what students actually experience. Students often want to know which courses feel difficult, how much time the program takes, how professors interact with students, and what skills they should prepare before starting. This information is hard to find because it is spread across Reddit posts, unofficial review sites, course review pages, and student discussions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source                                           | Description                                                                          | URL or location                                                                |
| -- | ------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| 1  | MSDS Hub                                         | Unofficial student-created MSDS course review and planning site                      | https://msdshub.com/                                                           |
| 2  | UT Austin MSDS official page                     | Official program information, curriculum, and degree requirements                    | https://cdso.utexas.edu/msds                                                   |
| 3  | Reddit MSDSO subreddit                           | General subreddit with student discussions about UT Austin MSDSO                     | https://www.reddit.com/r/MSDSO/                                                |
| 4  | Reddit MSDSO full-time job discussion            | Student discussion about doing UT Austin MSDS while working full-time                | https://www.reddit.com/r/MSDSO/search/?q=full%20time%20job&restrict_sr=1       |
| 5  | Reddit MSDSO workload discussion                 | Student comments about workload, time commitment, and course difficulty              | https://www.reddit.com/r/MSDSO/search/?q=workload&restrict_sr=1                |
| 6  | Reddit MSDSO course difficulty discussion        | Student discussions about which MSDS courses are harder or easier                    | https://www.reddit.com/r/MSDSO/search/?q=difficulty&restrict_sr=1              |
| 7  | Reddit MSDSO professor interaction discussion    | Student comments about professor communication, office hours, and online interaction | https://www.reddit.com/r/MSDSO/search/?q=professor%20interaction&restrict_sr=1 |
| 8  | Reddit MSDSO course review discussion            | Student reviews and opinions about specific MSDS courses                             | https://www.reddit.com/r/MSDSO/search/?q=course%20review&restrict_sr=1         |
| 9  | Coursicle UT Austin SDS courses                  | Course review pages for UT Austin Statistics and Data Science courses                | https://www.coursicle.com/utexas/courses/SDS/                                  |
| 10 | UT Austin Statistics and Data Science department | Official department information for SDS courses and academic context                 | https://stat.utexas.edu/                                                       |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Reasoning:**
Most of my sources are student reviews, Reddit comments, and short course descriptions. An 800-character chunk is large enough to keep one student opinion or short explanation together, but small enough to avoid combining too many unrelated comments in the same chunk. The 150-character overlap will help prevent important details from being lost when a useful sentence is split between two chunks.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` using `sentence-transformers`

**Top-k:** 4

**Production tradeoff reflection:**
For this project, `all-MiniLM-L6-v2` is a good choice because it is free, fast, and runs locally. If this system were used by real students, I would compare it with stronger embedding models that may understand informal student language better and retrieve more accurate results. I would also consider context length, accuracy, latency, cost, and whether the model can handle noisy Reddit posts and course review language.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question                                                                     | Expected answer                                                                                                                                                                                    |
| - | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Can students complete the UT Austin MSDS program while working full-time?    | Student sources should say that it is possible, but students usually recommend managing the workload carefully and often taking one course at a time.                                              |
| 2 | What do students say about workload in the UT Austin MSDS program?           | Student sources should say that workload depends on the course, with some classes requiring more weekly time than others.                                                                          |
| 3 | What do students say about professor interaction in the online MSDS program? | Student sources should say that interaction may happen through office hours, discussion boards, TAs, or learning assistants, but direct professor interaction can be limited in an online program. |
| 4 | What is MSDS Hub useful for?                                                 | The system should say that MSDS Hub is useful for unofficial course reviews, workload information, course planning, and student perspectives.                                                      |
| 5 | What should new students prepare before starting UT Austin MSDS?             | The system should mention preparation in Python, statistics, math, data science basics, and time management, depending on what the retrieved sources support.                                      |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Student reviews may be subjective and inconsistent. One student may describe a course as easy while another student may describe the same course as difficult, so the system must avoid presenting one opinion as a fact for everyone.

2. Source attribution may be difficult if documents are not stored with clear metadata. Since this project requires citations, each chunk needs to keep the original source name and URL so the final answer can show where the information came from.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
Document Ingestion
Python loads text files / scraped source documents from the documents folder
        |
        v
Chunking
Custom Python chunk_text() function
Chunk size: 800 characters
Overlap: 150 characters
        |
        v
Embedding + Vector Store
sentence-transformers creates embeddings using all-MiniLM-L6-v2
ChromaDB stores chunks, embeddings, source names, and URLs
        |
        v
Retrieval
User question is embedded
System retrieves top 4 most relevant chunks from ChromaDB
        |
        v
Generation
Groq LLM generates an answer using only the retrieved chunks
Final answer includes source citations
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will use ChatGPT to help me write Python code that loads my source documents from the `documents` folder and splits them into chunks. I will give ChatGPT my Documents section and Chunking Strategy section, including the 800-character chunk size and 150-character overlap. I expect it to produce a document loading function and a `chunk_text()` function. I will verify the output by printing sample chunks and checking that each chunk is readable, not empty, and connected to the correct source.

**Milestone 4 — Embedding and retrieval:**
I will use ChatGPT to help me implement embeddings using `sentence-transformers` and store the chunks in ChromaDB. I will give ChatGPT my Retrieval Approach section, including the embedding model `all-MiniLM-L6-v2` and top-k value of 4. I expect it to produce code that embeds chunks, stores metadata, and retrieves the four most relevant chunks for a user question. I will verify the output by asking my evaluation questions and checking whether the retrieved chunks are related to the question.

**Milestone 5 — Generation and interface:**
I will use ChatGPT to help me create a simple command-line interface where a user can type a question and receive a grounded answer. I will give ChatGPT my Evaluation Plan and require that the generated answers use only retrieved chunks and include citations. I expect it to produce code that sends retrieved context to the Groq LLM and returns an answer with source attribution. I will verify the system by running my five evaluation questions and marking each result as accurate, partially accurate, or inaccurate.
