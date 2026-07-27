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
- ⛔ Groq and Jina API calls could NOT be tested in this sandbox — their domains
  aren't reachable from here. This is expected and not a bug in the code.

## What you need to do on your own machine

### 1. Get free API keys
- **Groq**: console.groq.com → sign in → API Keys → Create API Key
- **Jina**: jina.ai → sign in → get API key (generous free tier)

### 2. Fill in `.env`
Replace the placeholders in `.env` with your real keys:
```
GROQ_API_KEY=gsk_your_real_key
JINA_API_KEY=jina_your_real_key
```

### 3. Run it
```bash
cd groq_rag_practice
source venv/bin/activate        # Windows: venv\Scripts\activate
python rag_practice.py
```

You should see: environment loaded → document loaded → 6 chunks →
FAISS indexed → a raw similarity search result → the LLM ready → three
sample questions asked and answered by the agent, using the `search_policy`
tool to ground its answers in `data/policies.txt`.

## Try asking it yourself
Add your own questions at the bottom of `rag_practice.py`, e.g.:
- "Can I return an opened electronics item after 10 days?"
- "How is the reorder quantity calculated?"
- "What happens if a supplier pays late?"

## What to notice while you run this (teaching points)
- The **system prompt explicitly forbids** the assistant from promising a
  refund directly — this is the safety-guardrail pattern from Phase 2,
  now doing real work in an agent's instructions, not just a lecture point.
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
