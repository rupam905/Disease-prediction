import os, time
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from src.helper import download_embeddings
from src.prompt import system_prompt

from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --------------------------------------------------------------------
# 0.  ENV + LangChain initialisation
# --------------------------------------------------------------------
load_dotenv()
os.environ["OPENAI_API_KEY"]   = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"]  = os.getenv("OPENAI_API_BASE")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

embeddings = download_embeddings()
docsearch  = PineconeVectorStore.from_existing_index(
    index_name="medi-chatbot",
    embedding=embeddings,
)
retriever = docsearch.as_retriever(
    search_type="similarity", search_kwargs={"k": 3}
)

chat_model = ChatOpenAI(
    model="compound-beta-mini",
    temperature=0.2,
    max_tokens=200,
)

prompt  = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human",  "{input}")
])

qa_chain  = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# --------------------------------------------------------------------
# 1.  FastAPI application
# --------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Medi-Chatbot")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",          # url_for('static', path=...) uses this name
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------
# 2.  Routes
# --------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=PlainTextResponse)
async def chat(msg: str = Form(...)):
    answer = rag_chain.invoke({"input": msg})["answer"]
    print(f"[{time.strftime('%H:%M:%S')}] Q: {msg}\nA: {answer}\n")
    return answer

@app.get("/ping")
async def ping():
    return {"status": "ok", "ts": int(time.time())}

# --------------------------------------------------------------------
# 3.  Local launch
# --------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
