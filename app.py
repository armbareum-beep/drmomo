from flask import Flask, render_template, request, jsonify, session
import os
from rag_system import load_and_process_documents, create_rag_chain, get_pinecone_vectorstore
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global variable to store the QA chain
qa_chain = None

def initialize_rag_system():
    """Initialize the RAG system with Pinecone"""
    global qa_chain
    
    print("="*70)
    print("🔄 Initializing Pinecone RAG System...")
    print("="*70)
    
    try:
        # Connect to existing Pinecone index
        print("\n🔌 Connecting to Pinecone index...")
        vectorstore = get_pinecone_vectorstore()
        
        qa_chain = create_rag_chain(vectorstore)
        print("\n" + "="*70)
        print("✅ RAG system initialized successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        # Don't raise here, let the app start even if RAG fails (though it won't work)
        # In production logs this will be visible

# Initialize on module load for Gunicorn
initialize_rag_system()

if __name__ == '__main__':
    print("=== Veterinary RAG Web Interface ===")
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
