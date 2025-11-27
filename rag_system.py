import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

def get_loader_for_file(file_path):
    """
    Returns the appropriate document loader based on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    loaders = {
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.doc': Docx2txtLoader,
        '.txt': TextLoader,
        '.md': UnstructuredMarkdownLoader,
        '.csv': CSVLoader,
        '.xlsx': UnstructuredExcelLoader,
        '.xls': UnstructuredExcelLoader,
        '.html': UnstructuredHTMLLoader,
        '.htm': UnstructuredHTMLLoader,
    }
    
    loader_class = loaders.get(ext)
    if loader_class:
        return loader_class(file_path)
    else:
        print(f"Warning: Unsupported file type: {ext}")
        return None

def load_and_process_documents(file_paths=None, folder_path=None):
    """
    Loads documents from specified files or folder, splits them into chunks, and creates a vector store.
    Supports: PDF, DOCX, DOC, TXT, MD, CSV, XLSX, XLS, HTML
    """
    documents = []
    
    # Collect all file paths
    all_paths = []
    
    if file_paths:
        all_paths.extend(file_paths)
    
    if folder_path and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                all_paths.append(file_path)
    
    # Load documents
    for path in all_paths:
        if os.path.exists(path):
            loader = get_loader_for_file(path)
            if loader:
                try:
                    documents.extend(loader.load())
                    print(f"✓ Loaded: {os.path.basename(path)}")
                except Exception as e:
                    print(f"✗ Error loading {os.path.basename(path)}: {str(e)}")
        else:
            print(f"Warning: File not found: {path}")

    if not documents:
        raise ValueError("No documents loaded. Please add files to the 'documents' folder.")

    # Text Splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    texts = text_splitter.split_documents(documents)
    
    print(f"\n📚 Total documents loaded: {len(documents)}")
    print(f"📝 Total text chunks created: {len(texts)}")

    # Embeddings & Vector Store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    return vectorstore

def create_rag_chain(vectorstore):
    """
    Creates a RetrievalQA chain with the specific veterinary prompt.
    """
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0) # Using gpt-4o for better reasoning

    # Define the prompt template based on user requirements
    prompt_template = """수의학RAG

당신은 수의학 전문 어시스턴트입니다.

아래의 "컨텍스트"는 신뢰 가능한 수의학 자료(PDF, 가이드라인, 교과서, 논문)에서 
RAG 검색을 통해 가져온 내용입니다. 

당신의 규칙은 다음과 같습니다:

1) 반드시 "컨텍스트" 안의 정보만 사용해 답하세요.
2) 컨텍스트에서 확인되지 않는 내용은 절대 추측하거나 만들어내지 마세요.
3) 모르면 "해당 정보는 제공된 자료에서 확인할 수 없습니다"라고 답하세요.
4) 약물 용량, 투약 간격, 금기사항은 반드시 컨텍스트 근거를 기반으로만 말하세요.
5) 응급 상황(발작, 호흡곤란, 쇼크 등)이면 즉시 응급 동물병원 방문 권고를 포함하세요.
6) 항상 최종 문장에 다음 경고문을 포함하세요:
   "⚠️ 이 정보는 참고용이며, 실제 진단·처방은 반드시 수의사가 직접 판단해야 합니다."

[컨텍스트]
{context}

[질문]
{question}

위 규칙을 지켜서 한국어로 명확하고 구조적으로 답변하세요:

- 요약 답변
- 치료/의학적 설명(컨텍스트 기반)
- 주의사항 또는 금기
- 출처(어떤 문서/페이지에서 나온 정보인지)
"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True 
    )

    return qa_chain
