from dotenv import load_dotenv
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough , RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import ConversationalRetrievalChain, RetrievalQA

class ChatBot():
    load_dotenv()
    embeddings = HuggingFaceEmbeddings()
    INDEX_NAME = "chatbotqa-index"
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    retriver = docsearch.as_retriever(search_kwargs={"k": 3})
    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    llm = HuggingFaceHub(
    repo_id=repo_id, 
    model_kwargs={"temperature": 0.8, "top_k": 50}, 
    huggingfacehub_api_token=os.getenv('HUGGING_FACE_API_TOKEN')
    )
    template = """Use the following pieces of context to answer the question. Please follow the following rules:
1. Only share the final answer in the "result".
2. If you don't know the answer, don't try to make up an answer. Just say "I can't find the final answer but you may want to check the following links".
3. If you find the answer, write the answer in a concise way with five sentences maximum.

{context}

Question: {question}

Helpful Answer:
"""

    prompt = PromptTemplate(
    template=template, 
    input_variables=["context", "question"]
    )
    retrievalQA = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriver,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt, "verbose":False}
)


