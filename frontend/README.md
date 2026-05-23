# HR Assistant — Frontend

Professional, WhatsApp-style chat UI built on top of the existing `RAGService`
in [`main.py`](../main.py). The backend is reused as-is — this layer only
imports `RAGService` and renders the chat.

## Brand
- Background: `#FFFFFF`
- Green:  `#00E676`
- Purple: `#8A5CF6`
- Pink:   `#FF2D95`
- Gradient: `#00E676 → #8A5CF6 → #FF2D95`

## Run

From the **project root** (one level above this folder):

```bash
pip install streamlit
streamlit run frontend/app.py
```

Streamlit opens at <http://localhost:8501>.

## Notes
- Make sure your `.env` (with `OPENAI_API_KEY`) sits at the project root —
  `RAGService` loads it the same way the CLI does.
- The first launch will build/load the Chroma DB (`hr_db/`) just like
  `python main.py` does.
- Click **Clear conversation** in the sidebar to reset the chat history.
