import os
import sys
from rag_system import load_and_process_documents, create_rag_chain
from create_dummy_pdf import create_dummy_pdf

def main():
    print("=== Veterinary RAG System Initialization ===")
    
    # Define documents folder
    documents_folder = "documents"
    
    # 1. Check/Create Dummy PDF if documents folder is empty
    pdf_file = os.path.join(documents_folder, "veterinary_guide.pdf")
    if not os.path.exists(documents_folder) or len(os.listdir(documents_folder)) == 0:
        print(f"Documents folder is empty. Creating dummy PDF: {pdf_file}...")
        os.makedirs(documents_folder, exist_ok=True)
        create_dummy_pdf(pdf_file)
    
    # 2. Process all documents in the folder
    print(f"\n📂 Loading documents from '{documents_folder}' folder...")
    print("Supported formats: PDF, DOCX, DOC, TXT, MD, CSV, XLSX, XLS, HTML\n")
    try:
        vectorstore = load_and_process_documents(folder_path=documents_folder)
        print("\n✅ Indexing complete.")
    except Exception as e:
        print(f"❌ Error processing documents: {e}")
        return

    # 3. Create Chain
    qa_chain = create_rag_chain(vectorstore)

    # 4. Interaction Loop
    print("\n=== Veterinary AI Assistant Ready ===")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        question = input("\n질문을 입력하세요 (Enter Question): ")
        if question.lower() in ["exit", "quit", "종료"]:
            break
        
        if not question.strip():
            continue

        print("\nThinking...")
        try:
            result = qa_chain.invoke({"query": question})
            answer = result["result"]
            source_docs = result["source_documents"]
            
            print("\n" + "="*50)
            print(answer)
            print("="*50)
            
            # Optional: Print raw source metadata for debugging
            # print("\n[Reference Documents]")
            # for doc in source_docs:
            #     print(f"- Page {doc.metadata.get('page', '?')}")

        except Exception as e:
            print(f"Error generating answer: {e}")

if __name__ == "__main__":
    main()
