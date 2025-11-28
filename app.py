from flask import Flask, render_template, request, jsonify, session
import os
from rag_system import load_and_process_documents, create_rag_chain
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global variable to store the QA chain
qa_chain = None

def initialize_rag_system():
    """Initialize the RAG system with Pinecone"""
    global qa_chain
    
    documents_folder = "documents"
    
    # Create documents folder if it doesn't exist
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        from create_dummy_pdf import create_dummy_pdf
        pdf_file = os.path.join(documents_folder, "veterinary_guide.pdf")
        create_dummy_pdf(pdf_file)
    
    print("="*70)
    print("🔄 Initializing Pinecone RAG System...")
    print("="*70)
    
    try:
        # Process documents and upload to Pinecone
        print("\n📂 Processing documents and connecting to Pinecone...")
        vectorstore = load_and_process_documents(folder_path=documents_folder)
        
        qa_chain = create_rag_chain(vectorstore)
        print("\n" + "="*70)
        print("✅ RAG system initialized successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        raise

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    """API endpoint for asking questions"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': '질문을 입력해주세요.'}), 400
        
        if qa_chain is None:
            return jsonify({'error': 'RAG 시스템이 초기화되지 않았습니다.'}), 500
        
        # Get answer from RAG system
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        
        return jsonify({
            'answer': answer,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'오류가 발생했습니다: {str(e)}',
            'success': False
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'rag_initialized': qa_chain is not None
    })

if __name__ == '__main__':
    print("=== Veterinary RAG Web Interface ===")
    initialize_rag_system()
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
