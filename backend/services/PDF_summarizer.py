import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
import re 


load_dotenv()

# === CONFIG ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
CHUNK_SIZE = 7000
CHUNK_OVERLAP = 200
MAX_PARALLEL = 10   

llm = ChatGroq(model=MODEL_NAME, api_key=SecretStr(GROQ_API_KEY) if GROQ_API_KEY else None)

prompt_template = """
You are an expert summarizer. Summarize the following tutorial or educational transcript clearly and accurately.

Guidelines:
- Use English only, under 600 words.
- Explain concepts, steps, logic, and examples.
- Exclude code, personal remarks, or unrelated info.
- Use clear section titles and bullet points.
- Keep it concise, direct, and faithful to the text.

Content:
{text}

Final Summary:
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

def clean_transcript_text(full_text: str) -> str:
    """
    Remove common English and Hindi filler words, repeated spaces, and extra punctuation from the transcript.
    """
    filler_words_en = r"\b(uh|um|erm|like|you know|so|yeah|basically|actually|right|I mean|kinda|sorta|well)\b"
    
    filler_words_hi = r"\b(अच्छा|हम्म|मतलब|चलिए|चलो|ठीक है|अरे|उफ़|ओह|सुनो|जानते हो|वैसे|देखो|बस|तो|हाँ|है ना|यानी|क्या कहते हैं|वैसे तो)\b"
    
    fillers = f"({filler_words_en}|{filler_words_hi})"
    
    cleaned = re.sub(fillers, "", full_text, flags=re.IGNORECASE)
    
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def clean_pdf_text(text):
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"-\s+", "", text)  
    text = re.sub(r"Page \d+ of \d+", "", text)
    text = re.sub(r"\d+\s?\n?", "", text) 
    text = text.strip()
    return text

def chunk_content(pdf_docs , chunk_size=CHUNK_SIZE):
    raw_text = " ".join([doc.page_content for doc in pdf_docs]) 
    cleaned_text = clean_pdf_text(clean_transcript_text(raw_text))
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=CHUNK_OVERLAP)
    docs = splitter.create_documents([cleaned_text])
    return [doc.page_content for doc in docs]

# creating summarization chain 
summarization_chain = prompt | llm | StrOutputParser()

async def safe_summarize(text: str) -> str:
    try:
        if not text.strip():
            return "No content found."
        return await summarization_chain.ainvoke({"text": text})
    except Exception as e:
        msg = str(e)
        return f"Failed to summarize: {msg}"

# batch processing for speedup of summarization
# i am sending a chunks of transcripts in a batch of 10 so they summarize parallaly 
async def summarize_chunks(chunks: list[str]):
    results = []
    sem = asyncio.Semaphore(MAX_PARALLEL)
    # sending a chunk for summarization 
    async def worker(chunk):
        async with sem:
            return await safe_summarize(chunk)

    for i in range(0, len(chunks), MAX_PARALLEL):
        batch = chunks[i:i+MAX_PARALLEL]  # batch will store first 10 chunks, then next 10 chunks and so on 
        batch_results = await asyncio.gather(*[worker(c) for c in batch]) #running all requests together 
        results.extend(batch_results)
        # small delay between batches to prevent rate limiting
        if len(chunks) > MAX_PARALLEL:
            await asyncio.sleep(0.5)

    return results

async def summarize_long_pdf(pdf_docs: list) -> str:
    chunks = chunk_content(pdf_docs)
    print(f" {len(chunks)} chunks created from PDF content.")

    if not chunks:
        return "No content found."

    chunk_summaries = await summarize_chunks(chunks)

    while chunk_summaries and len(" ".join(chunk_summaries).split()) > 6000:
        grouped = [
            " ".join(chunk_summaries[i:i+3])
            for i in range(0, len(chunk_summaries), 3)
        ]
        print(f"🔁 Compressing summaries into {len(grouped)} groups...")
        chunk_summaries = await summarize_chunks(grouped)

    final_summary = await safe_summarize(" ".join(chunk_summaries))
    return final_summary.strip()
