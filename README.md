# The Unofficial Guide — Project 1

## Domain

My system covers student reviews and experiences about the UT Austin MSDS program, including courses, workload, difficulty, professors, admissions, and preparation tips. This knowledge is valuable because official program pages explain requirements, but they do not show what students actually experience in classes. Student opinions about course difficulty, workload, professor responsiveness, and time management are spread across unofficial sites, Reddit-style discussions, and course review notes.

---

## Document Sources

| #  | Source                              | Type                       | URL or file path                    |
| -- | ----------------------------------- | -------------------------- | ----------------------------------- |
| 1  | MSDS Hub                            | Student review site        | documents/msds_hub.txt              |
| 2  | UT MSDS Overview                    | Official program info      | documents/ut_msds_overview.txt      |
| 3  | Reddit workload thread              | Student discussion         | documents/reddit_workload.txt       |
| 4  | Reddit difficulty thread            | Student discussion         | documents/reddit_difficulty.txt     |
| 5  | Reddit professor interaction thread | Student discussion         | documents/reddit_professors.txt     |
| 6  | Reddit full-time job thread         | Student discussion         | documents/reddit_fulltime_job.txt   |
| 7  | Reddit course reviews thread        | Student discussion         | documents/reddit_course_reviews.txt |
| 8  | Reddit admissions thread            | Student discussion         | documents/reddit_admissions.txt     |
| 9  | Coursicle SDS 313                   | Course information / notes | documents/coursicle_sds313.txt      |
| 10 | Coursicle SDS 322E                  | Course information / notes | documents/coursicle_sds322e.txt     |

---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Why these choices fit your documents:**
Most of my documents are short student reviews, course notes, and discussion-style comments. I chose 800 characters because it is large enough to keep one student comment or course review section together, but small enough to avoid mixing too many unrelated ideas. I used 150 characters of overlap so important information would not be lost if it appeared near a chunk boundary. I also cleaned the documents manually before chunking by removing website navigation, buttons, empty text, and unnecessary formatting.

**Final chunk count:** 16 chunks

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` from `sentence-transformers`

**Production tradeoff reflection:**
I chose this model because it runs locally, is free, and is fast enough for a small class project. If I were deploying this system for real students, I would compare it with stronger embedding models that may perform better on informal student reviews and course-specific language. I would consider accuracy, context length, latency, cost, multilingual support, and whether the model should run locally or through an API.

---

## Grounded Generation

**System prompt grounding instruction:**
My system tells the LLM to answer only from the retrieved documents. The prompt includes this instruction:

```text
You are answering questions using ONLY the retrieved documents below.

Rules:
- Do not use outside knowledge.
- If the documents do not contain enough information, say: "I don't have enough information on that."
- Cite the source filenames used in your answer.
```

**How source attribution is surfaced in the response:**
The system passes the retrieved chunks to the LLM with their source filenames. The final answer includes cited source filenames, and the Gradio interface also shows a separate “Sources Retrieved” box listing the files used for retrieval.

---
## Sample Chunks

### Chunk 1 — reddit_workload.txt

```
Thread: How much time does the UT Austin MSDS program require each week?

Student A:
For most courses, I spend between 10 and 15 hours per week. During project-heavy weeks, that can increase to 20 hours or more.
```

### Chunk 2 — reddit_difficulty.txt

```
Thread: Which MSDS courses are the hardest?

Student A:
Deep Learning was the most difficult course I took because of the mathematical concepts and project requirements.

Student B:
Advanced Predictive Models required significant effort and independent study.
```

### Chunk 3 — coursicle_sds313.txt

```
Course: SDS 313 - Elementary Statistical Methods

Topics:
- Descriptive statistics
- Probability
- Hypothesis testing
- Confidence intervals
```

### Chunk 4 — reddit_fulltime_job.txt

```
Many students successfully work full-time.
One course per semester is often recommended.
Recorded lectures provide flexibility.
```

### Chunk 5 — msds_hub.txt

```
Course: Advanced Predictive Models (DSC 383)

Pros:
- Cool material not seen elsewhere

Cons:
- Lots of self-study required
- Course organization was poor
```
---
## Retrieval Test Results

### Query 1

**Question:** Which courses are the hardest?

Top Retrieved Chunks:

1. reddit_difficulty.txt
2. reddit_course_reviews.txt
3. msds_hub.txt

Why relevant:
The retrieved chunks directly discuss course difficulty and specifically mention Deep Learning and Advanced Predictive Models as challenging courses.

---

### Query 2

**Question:** How many hours per week do students spend?

Top Retrieved Chunks:

1. reddit_workload.txt
2. reddit_fulltime_job.txt
3. reddit_workload.txt (second chunk)

Why relevant:
The retrieved chunks contain direct workload estimates, including 10–15 hours per week and 20+ hours during project-heavy weeks.

---

### Query 3

**Question:** What do students say about Advanced Predictive Models?

Top Retrieved Chunks:

1. reddit_course_reviews.txt
2. msds_hub.txt
3. coursicle_sds313.txt

Observation:
The correct Advanced Predictive Models review was retrieved but not ranked first, demonstrating a retrieval weakness.

---

## Example Responses

### Example 1

**Question**

```text
Which courses are the hardest?
```

**Answer**

```text
According to student reviews, Deep Learning and Advanced Predictive Models are frequently considered the most difficult courses in the UT Austin MSDS program. Students describe Deep Learning as mathematically challenging and project-intensive, while Advanced Predictive Models requires significant independent study and effort.

Sources:
reddit_difficulty.txt
reddit_course_reviews.txt
msds_hub.txt
```

---

### Example 2

**Question**

```text
How many hours per week do students spend?
```

**Answer**

```text
Students commonly report spending between 10 and 20 hours per week on coursework. During project-heavy weeks, the workload can increase beyond 20 hours. Students working full-time often recommend taking one course at a time and maintaining consistent study habits.

Sources:
reddit_workload.txt
reddit_fulltime_job.txt
```

---

### Example 3 (Out-of-Scope Query)

**Question**

```text
What is the best dining hall at UT Austin?
```

**Answer**

```text
I don't have enough information on that.

The retrieved documents contain information about the UT Austin MSDS program, including courses, workload, professors, and student experiences, but they do not contain information about dining halls.

Sources:
No relevant sources retrieved.
```
---
## Query Interface

### Input

The system provides a text box where users can enter natural-language questions about the UT Austin MSDS program. Users can ask about course difficulty, workload, professor interaction, admissions, and student experiences.

Example inputs:

```text
Which courses are the hardest?

How many hours per week do students spend?

What do students say about Advanced Predictive Models?

Can students complete the program while working full-time?
```

### Output

The interface returns two outputs:

1. **Grounded Answer** – A response generated by the LLM using only the retrieved documents.
2. **Sources Retrieved** – A list of document filenames used during retrieval and answer generation.

### Interface Technology

The user interface was implemented using **Gradio**. The backend connects to a ChromaDB vector store, retrieves relevant chunks using sentence embeddings, and sends the retrieved context to a Groq-hosted LLM for grounded answer generation.

### Sample Interaction

**User Query**

```text
What do students say about Advanced Predictive Models?
```

**System Response**

```text
Students describe Advanced Predictive Models as an interesting course with useful material and active professors. However, several reviews mention that the course requires significant self-study and that assignment expectations can be unclear. Some students also reported concerns about course organization.

Sources:
msds_hub.txt
reddit_difficulty.txt
reddit_course_reviews.txt
```

**Sources Retrieved**

```text
msds_hub.txt
reddit_difficulty.txt
reddit_course_reviews.txt
```

---

## Evaluation Report

| # | Question                                                   | Expected answer                                                                                                                                             | System response (summarized)                                                                                                                                                                       | Retrieval quality  | Response accuracy  |
| - | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------ |
| 1 | Which courses are the hardest?                             | Deep Learning and Advanced Predictive Models are frequently described as difficult courses.                                                                 | The system identified Deep Learning as the most difficult course and Advanced Predictive Models as another challenging course requiring significant effort and independent study.                  | Relevant           | Accurate           |
| 2 | How many hours per week do students spend?                 | Students generally spend between 10 and 20 hours per week, depending on course load and projects.                                                           | The system retrieved workload discussions showing students spend 10–15 hours per week normally and up to 20+ hours during project-heavy periods.                                                   | Relevant           | Accurate           |
| 3 | What do students say about Advanced Predictive Models?     | Students describe it as interesting but requiring significant self-study, with mixed opinions about course organization.                                    | The system reported that students found the course interesting and useful but requiring self-study. It also retrieved reviews mentioning poor organization and unclear assignment expectations.    | Partially relevant | Partially accurate |
| 4 | Can students complete the program while working full-time? | Yes. Students commonly report that the program is manageable while working full-time if they take a reasonable course load and manage their time carefully. | The system retrieved discussions stating that many students successfully complete the program while working full-time, often recommending one course per semester and emphasizing time management. | Relevant           | Accurate           |
| 5 | What is the best dining hall at UT Austin?                 | The system should not answer because the documents contain no information about dining halls.                                                               | The system indicates that it does not have enough information because the retrieved documents focus on the MSDS program rather than campus dining.                                                 | Off-target         | Accurate           |

**Retrieval quality:** Relevant / Partially relevant / Off-target

**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
What do students say about Advanced Predictive Models?

**What the system returned:**
The system returned useful information about Advanced Predictive Models, including comments about workload, self-study requirements, and course organization. However, the most specific course review was not ranked first among the retrieved results.

**Root cause (tied to a specific pipeline stage):**
This was primarily a retrieval-stage issue. The embedding model retrieved broader course review documents before retrieving the most relevant Advanced Predictive Models review. Because semantic similarity focused on general course-review language, the exact course-specific chunk was ranked below more general discussion chunks.

**What I would change to fix it:**
I would improve metadata by attaching course names and course codes to every chunk. I would also implement hybrid retrieval that combines semantic search with keyword matching so exact terms such as "Advanced Predictive Models" and "DSC 383" receive higher ranking priority.

---

## Spec Reflection

**One way the spec helped you during implementation:**
The planning document helped me make clear decisions before coding. Because I already chose my chunk size, overlap, embedding model, and top-k value, it was easier to build the pipeline step by step instead of changing everything while coding. The architecture diagram also helped me understand the order of the system: documents, chunks, embeddings, retrieval, then generation.

**One way your implementation diverged from the spec, and why:**
My original chunking approach used fixed character chunks, but I later improved it to chunk more cleanly around paragraphs. I made this change because one retrieved chunk started in the middle of a sentence, which made the result less readable. The final approach still used the same general chunk size and overlap idea, but it produced cleaner chunks.

---

## AI Usage

**Instance 1**

* *What I gave the AI:* I gave the AI my project instructions, planning template, and chosen domain about UT Austin MSDS student reviews.
* *What it produced:* It helped me draft the planning document, including the domain, document list, chunking strategy, retrieval approach, architecture, and evaluation questions.
* *What I changed or overrode:* I adjusted the sources and documents based on the actual text files I collected manually, especially from MSDS Hub and student-style discussion files.

**Instance 2**

* *What I gave the AI:* I gave the AI my chunking strategy and asked for code to load documents, split them into chunks, and save them for embedding.
* *What it produced:* It produced the first version of `chunker.py`, plus later improvements to save `chunks.txt` and add source metadata.
* *What I changed or overrode:* I tested the output and noticed one chunk started in the middle of a sentence, so I improved the chunking approach to respect paragraph boundaries and include source/title metadata.

**Instance 3**

* *What I gave the AI:* I gave the AI my Milestone 4 and Milestone 5 requirements.
* *What it produced:* It helped create `embed_store.py`, `retrieval_test.py`, `query.py`, and `app.py`.
* *What I changed or overrode:* I tested the retrieval results myself, improved chunking when retrieval was not ideal, and updated the Gradio app to look cleaner and be easier to use in a demo.

---

## Demo Video

[Watch the demo video on Loom](https://www.loom.com/share/cff9a88855684b3a9537ecec1c82e149)

The video demonstrates:
- The Gradio query interface
- Retrieval and grounded generation
- Multiple successful queries
- A documented failure case
- Evaluation results and project reflection