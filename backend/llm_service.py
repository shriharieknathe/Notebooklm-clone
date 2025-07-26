import os
from typing import List, Dict, Any, Optional
from langchain_community.llms import HuggingFacePipeline
from langchain.schema import Document, HumanMessage, SystemMessage
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

from config import Config
from vector_store import VectorStore

class LLMService:
    def _initialize_huggingface_model(self):
        """Initialize HuggingFace model locally with API token for downloads"""
        try:
            # Load tokenizer and model with API token for access
            tokenizer = AutoTokenizer.from_pretrained(
                Config.MODEL_NAME, 
                token=Config.HUGGINGFACE_API_TOKEN
            )
            model = AutoModelForSeq2SeqLM.from_pretrained(
                Config.MODEL_NAME,
                token=Config.HUGGINGFACE_API_TOKEN
            )
            
            # Create pipeline for text generation
            text_generation_pipeline = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=Config.MAX_LENGTH,
                temperature=Config.TEMPERATURE,
                do_sample=True
            )
            
            # Create LangChain wrapper
            llm = HuggingFacePipeline(
                pipeline=text_generation_pipeline,
                model_kwargs={"temperature": Config.TEMPERATURE, "max_length": Config.MAX_LENGTH}
            )
            
            return llm
            
        except Exception as e:
            print(f"Error loading HuggingFace model: {e}")
            raise
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
        # Initialize HuggingFace LLM
        print("Loading HuggingFace model...")
        self.llm = self._initialize_huggingface_model()
        print("HuggingFace model loaded successfully!")
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        
        # Create conversational chain
        try:
            self.qa_chain = self._create_qa_chain()
            print("QA chain created successfully!")
        except Exception as e:
            print(f"Error creating QA chain: {e}")
            self.qa_chain = None
    
    def _create_qa_chain(self):
        """Create conversational retrieval chain"""
        # Custom prompt template for T5 model
        template = """Answer the following question based on the provided context. If you don't know the answer, say "I don't know."

Context: {context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create conversational retrieval chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.vector_store.as_retriever(
                search_kwargs={"k": 3}  # Reduced for T5 model
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True,
            verbose=False,
            return_generated_question=False
        )
        
        return qa_chain
    
    def get_response(self, question: str) -> Dict[str, Any]:
        """Get response for a question using RAG"""
        try:
            # Use the simple RAG approach directly for better reliability
            return self._get_simple_rag_response(question)
            
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            # Final fallback
            return {
                "answer": f"I apologize, but I encountered an error while processing your question: {str(e)}",
                "citations": [],
                "source_documents": [],
                "question": question
            }
    
    def _get_simple_rag_response(self, question: str) -> Dict[str, Any]:
        """Simple RAG response without conversation memory"""
        try:
            # Get relevant documents
            relevant_docs = self.vector_store.similarity_search(question, k=3)
            
            # Debug: Print what documents were found
            print(f"Found {len(relevant_docs)} relevant documents for question: {question}")
            for i, doc in enumerate(relevant_docs):
                print(f"Doc {i+1}: {doc.page_content[:200]}...")
            
            # Combine context
            context = "\n".join([doc.page_content for doc in relevant_docs])
            
            # Create a better prompt for T5 model
            prompt = f"""Question: {question}

Context: {context}

Provide a concise answer in 2-3 sentences based on the context above. Do not repeat information:"""
            
            # Get response from LLM
            answer = self.llm(prompt)
            
            # Clean up the response - remove repetitions and take only unique content
            answer = answer.strip()
            
            # Remove repetitions by finding unique sentences
            sentences = answer.split('.')
            unique_sentences = []
            seen_sentences = set()
            
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and len(sentence) > 10:  # Only consider meaningful sentences
                    # Create a simplified version for comparison
                    simplified = ' '.join(sentence.split()[:10]).lower()
                    if simplified not in seen_sentences:
                        unique_sentences.append(sentence)
                        seen_sentences.add(simplified)
            
            # Reconstruct answer with only unique content
            if unique_sentences:
                answer = '. '.join(unique_sentences[:5]) + '.'  # Limit to 5 sentences max
            else:
                # Fallback if no unique sentences found
                answer = answer[:500]  # Limit to 500 characters
            
            # If answer is too short, try a different approach
            if len(answer) < 50:
                # Try a more specific prompt
                prompt2 = f"""Based on this information: {context}

Answer this question: {question}

Provide a concise answer in 2-3 sentences:"""
                answer = self.llm(prompt2).strip()
                # Apply same deduplication
                sentences = answer.split('.')
                unique_sentences = []
                seen_sentences = set()
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) > 10:
                        simplified = ' '.join(sentence.split()[:10]).lower()
                        if simplified not in seen_sentences:
                            unique_sentences.append(sentence)
                            seen_sentences.add(simplified)
                if unique_sentences:
                    answer = '. '.join(unique_sentences[:3]) + '.'
            
            # Process citations
            citations = self._process_citations(relevant_docs)
            
            return {
                "answer": answer,
                "citations": citations,
                "source_documents": relevant_docs,
                "question": question
            }
            
        except Exception as e:
            print(f"Error in simple RAG response: {e}")
            raise
    
    def _process_citations(self, source_documents: List[Document]) -> List[Dict[str, Any]]:
        """Process source documents to create citations"""
        citations = []
        
        # Only show one citation to avoid clutter
        if source_documents:
            doc = source_documents[0]  # Take the first/most relevant document
            page_number = doc.metadata.get("page", 1)
            filename = doc.metadata.get("filename", "Document")
            
            # Create single citation
            citation = {
                "page": page_number,
                "text": f"Page {page_number}",
                "filename": filename,
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            }
            
            citations.append(citation)
        
        return citations
    
    def get_simple_response(self, question: str) -> str:
        """Get a simple response without RAG (fallback)"""
        try:
            # Simple prompt for HuggingFace API
            prompt = f"Question: {question}\nAnswer:"
            response = self.llm(prompt)
            return response.strip()
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def _get_fallback_response(self, question: str, context: str) -> str:
        """Fallback response when main LLM fails"""
        try:
            # Try a very simple approach
            simple_prompt = f"Answer this question: {question}"
            return self.llm(simple_prompt).strip()
        except:
            # Final fallback
            return f"Based on the available information, I can see relevant content in the document. Please try rephrasing your question about: {question}"
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        print("Conversation memory cleared")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of conversation memory"""
        try:
            chat_history = self.memory.chat_memory.messages
            return {
                "total_messages": len(chat_history),
                "memory_type": "ConversationBufferMemory"
            }
        except Exception as e:
            return {"error": f"Error getting memory summary: {e}"} 