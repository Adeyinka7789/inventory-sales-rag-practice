# Inventory & Sales RAG Practice — Groq + Jina + FAISS

Practice build following the free-tier stack: **Groq** (LLM, free tier),
**Jina** (embeddings, free tier), **FAISS** (local vector store, free).
Same workflow as the reference video — rebuilt on Inventory & Sales
policy data instead of HR, so this is genuinely yours to teach from.

## What's been verified already
- ✅ Project scaffolded, dependencies installed (`requirements.txt` pinned)
- ✅ `.env` / `.gitignore` wired correctly — secrets never get tracked by git
- ✅ Data loading + chunking confirmed working (6 clean chunks from `data/policies.txt`)
- ✅ FAISS vector store + retriever wiring confirmed working (structural test)
- ✅ Full end-to-end run on Windows / Python 3.13: Jina embedded the chunks,
  FAISS persisted them to `faiss_index/`, and Groq answered from retrieved
  policy text (bulk-discount tiers, Net 30/45 terms, the 7-day electronics
  window) — so the answers are genuinely grounded, not improvised.
- ✅ Persistence confirmed both ways: first run builds and saves the index,
  every run after prints "loading it (no re-embedding)".

## What you need to do on your own machine

### 1. Get free API keys
- **Groq**: console.groq.com → sign in → API Keys → Create API Key
- **Jina**: jina.ai → sign in → get API key (generous free tier)

### 2. Create `.env`
`.env` is gitignored and is **not** in this repo — create it yourself in the
repo root, next to `config.py`, with your real keys:
```
GROQ_API_KEY=gsk_your_real_key
JINA_API_KEY=jina_your_real_key
```
`config.check_api_keys()` runs before anything else in `rag_practice.py`, so a
missing key fails immediately with a clear message rather than halfway through
building the index.

### 3. Create the venv and install
```bash
cd inventory-sales-rag-practice
python -m venv venv
source venv/bin/activate            # Windows PowerShell: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Run it
```bash
python rag_practice.py
```

Run it from the **repo root** — `config.py` uses relative paths
(`data/policies.txt`, `faiss_index`), so running from anywhere else
fails with a `FileNotFoundError` in the loader.

On the first run you should see "No saved vector store found — building one
from scratch" (that's the one time Jina gets paid), then a `>` prompt. Every
run after that says "Found a saved vector store on disk — loading it".

## Try asking it yourself
`rag_practice.py` ends in an interactive loop — type a question at the `>`
prompt, press Enter on a blank line to quit. Things worth trying:
- "Can I return an opened electronics item after 10 days?"
- "How is the reorder quantity calculated?"
- "What happens if a supplier pays late?"

Note that each question is a **fresh conversation** — `ask_assistant` sends a
single user message, so a follow-up like "what about 200 units?" won't know
what you were just talking about. Adding memory means carrying the message
history across turns (LangGraph checkpointers); that's a deliberate next step,
not an oversight.

## What to notice while you run this (teaching points)
- The "never promise a refund directly" guardrail lives in **`data/policies.txt`,
  not in the system prompt** — `config.SYSTEM_PROMPT` only says "use the tool".
  So the rule reaches the model as *retrieved data*, and holds only when that
  chunk is actually retrieved. In practice it works (ask about a late order and
  the assistant routes to a manager instead of promising money back), but it's
  worth showing trainees that a guardrail in the corpus is at the mercy of the
  retriever, whereas one in the system prompt is present on every single call.
  Good live demo: move the rule into `SYSTEM_PROMPT` and discuss the tradeoff.
- `create_agent` is LangChain's newer, higher-level way to build an agent —
  compare this to the raw `tools_schema` + manual loop from the Build
  Guide's Phase 5. Teach the raw version first so trainees understand
  what `create_agent` is doing for them underneath.
- `langchain-community` is flagged as being sunset in favor of standalone
  integration packages (e.g. `langchain-jina`, `langchain-groq` already is
  one). Worth mentioning to trainees that the ecosystem moves fast —
  checking a package's current recommended import path is a real, ongoing
  AI-engineering skill, not a one-time lesson.

## Where this plugs into the Django app
This exact pattern — `TextLoader` → `RecursiveCharacterTextSplitter` →
embeddings → `FAISS`/Chroma → `create_agent` with a `search_policy` tool —
is the LangChain-framework version of what the Build Guide's Step 8-9
built with raw OpenAI calls and Chroma. Once you're comfortable with both,
decide which one to actually teach: raw code teaches the concepts more
transparently; `create_agent` ships faster. Many instructors teach raw
first, then show this as "the shortcut, now that you know what's really
happening."
