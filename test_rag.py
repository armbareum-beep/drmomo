from rag_system import load_and_process_documents, create_rag_chain
import sys

def test_system():
    print("Testing RAG System...")
    try:
        vectorstore = load_and_process_documents(file_paths=["veterinary_guide.pdf"])
        qa_chain = create_rag_chain(vectorstore)
        
        question = "강아지가 초콜릿을 먹었어. 어떻게 해야 해?"
        print(f"Question: {question}")
        
        result = qa_chain.invoke({"query": question})
        print("Answer:")
        print(result["result"])
        print("Test Complete.")
    except Exception as e:
        print(f"Test Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_system()
