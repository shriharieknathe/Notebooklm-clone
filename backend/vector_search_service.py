import os
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from vector_store import VectorStore
from config import Config

class VectorSearchService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def search_and_summarize(self, question: str, k: int = 3) -> Dict[str, Any]:
        """
        Search vector database and return relevant content without using LLM
        """
        try:
            # Get relevant documents from vector store
            relevant_docs = self.vector_store.similarity_search(question, k=k)
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant information in the document for your question.",
                    "citations": [],
                    "source_documents": [],
                    "question": question,
                    "method": "vector_search"
                }
            
            # Extract and format the most relevant content
            answer = self._format_relevant_content(relevant_docs, question)
            
            # Process citations
            citations = self._process_citations(relevant_docs)
            
            return {
                "answer": answer,
                "citations": citations,
                "source_documents": relevant_docs,
                "question": question,
                "method": "vector_search"
            }
            
        except Exception as e:
            print(f"Error in vector search: {e}")
            return {
                "answer": f"I encountered an error while searching the document: {str(e)}",
                "citations": [],
                "source_documents": [],
                "question": question,
                "method": "vector_search"
            }
    
    def _format_relevant_content(self, documents: List[Document], question: str) -> str:
        """
        Format the most relevant content from documents into a coherent answer
        """
        if not documents:
            return "No relevant information found."
        
        # Extract content from documents with deduplication
        unique_contents = []
        seen_content = set()
        
        for doc in documents:
            content = doc.page_content.strip()
            if content and len(content) > 10:  # Only include meaningful content
                # Create a simplified version for deduplication
                simplified = ' '.join(content.split()[:20]).lower()  # First 20 words
                if simplified not in seen_content:
                    unique_contents.append(content)
                    seen_content.add(simplified)
        
        if not unique_contents:
            return "No relevant information found."
        
        # Take only the first 2 unique contents to avoid repetition
        combined_content = "\n\n".join(unique_contents[:2])
        
        # Create a structured response
        response_parts = []
        
        # Add a brief summary based on question type
        question_lower = question.lower()
        
        if "skill" in question_lower or "skills" in question_lower:
            response_parts.append("Based on the document, here are the skills mentioned:")
            # For skills, try to extract specific skill keywords
            combined_content = self._extract_skills_from_content(combined_content)
        elif "experience" in question_lower or "work" in question_lower:
            response_parts.append("Based on the document, here is the experience/work history:")
        elif "education" in question_lower or "degree" in question_lower:
            response_parts.append("Based on the document, here is the education background:")
        elif "contact" in question_lower or "email" in question_lower or "phone" in question_lower:
            response_parts.append("Based on the document, here is the contact information:")
        elif "summary" in question_lower or "overview" in question_lower or "key points" in question_lower:
            response_parts.append("Based on the document, here are the key points:")
        else:
            response_parts.append("Based on the document, here is the relevant information:")
        
        # Add the actual content with better formatting
        if combined_content:
            # Clean up the content - remove excessive whitespace and line breaks
            cleaned_content = ' '.join(combined_content.split())
            # Split into sentences for better readability
            sentences = cleaned_content.split('.')
            # Take only meaningful sentences
            meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            # Limit to 5 sentences maximum
            final_content = '. '.join(meaningful_sentences[:5]) + '.'
            response_parts.append(final_content)
        
        return "\n\n".join(response_parts)
    
    def _process_citations(self, source_documents: List[Document]) -> List[Dict[str, Any]]:
        """Process source documents to create citations"""
        citations = []
        
        # Create citations for each relevant document
        for i, doc in enumerate(source_documents[:3]):  # Limit to top 3
            page_number = doc.metadata.get("page", 1)
            filename = doc.metadata.get("filename", "Document")
            
            citation = {
                "page": page_number,
                "text": f"Page {page_number}",
                "filename": filename,
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "relevance_rank": i + 1
            }
            
            citations.append(citation)
        
        return citations
    
    def get_document_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all documents in the vector store
        """
        try:
            stats = self.vector_store.get_collection_stats()
            
            # Get a sample of documents for overview
            sample_docs = self.vector_store.similarity_search("", k=5)
            
            summary = {
                "total_documents": stats.get("count", 0),
                "total_chunks": len(sample_docs),
                "document_types": self._get_document_types(sample_docs),
                "method": "vector_search"
            }
            
            return summary
            
        except Exception as e:
            return {
                "error": f"Error getting document summary: {e}",
                "method": "vector_search"
            }
    
    def _get_document_types(self, documents: List[Document]) -> List[str]:
        """Extract document types from metadata"""
        doc_types = set()
        for doc in documents:
            filename = doc.metadata.get("filename", "").lower()
            if filename.endswith('.pdf'):
                doc_types.add("PDF")
            elif filename.endswith('.txt'):
                doc_types.add("Text")
            elif filename.endswith('.doc'):
                doc_types.add("Word")
            else:
                doc_types.add("Document")
        
        return list(doc_types)
    
    def _extract_skills_from_content(self, content: str) -> str:
        """Extract and format skills from content"""
        if not content:
            return content
        
        # Common skill keywords to look for (comprehensive list for any resume/document)
        skill_keywords = [
            # Programming Languages
            'javascript', 'typescript', 'python', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'html', 'css', 'scss', 'sass', 'sql', 'nosql', 'r', 'matlab', 'swift', 'kotlin', 'scala',
            
            # Frameworks & Libraries
            'react', 'reactjs', 'nextjs', 'angular', 'vue', 'vue.js', 'node.js', 'express', 'expressjs',
            'django', 'flask', 'fastapi', 'spring', 'laravel', 'symfony', 'jquery', 'bootstrap',
            'tailwind', 'material-ui', 'ant design', 'redux', 'mobx', 'zustand', 'svelte', 'ember',
            
            # Databases & Storage
            'mongodb', 'mysql', 'postgresql', 'sqlite', 'redis', 'elasticsearch', 'dynamodb',
            'firebase', 'supabase', 'cassandra', 'neo4j', 'oracle', 'sql server', 'mariadb',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
            'git', 'bitbucket', 'terraform', 'ansible', 'nginx', 'apache', 'vault', 'consul',
            
            # AI & ML
            'ai', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'langchain', 'genai', 'openai', 'chatgpt', 'nlp', 'computer vision', 'neural networks',
            
            # Tools & Platforms
            'jira', 'confluence', 'slack', 'trello', 'asana', 'figma', 'sketch', 'adobe',
            'socket.io', 'webpack', 'babel', 'eslint', 'prettier', 'jest', 'cypress', 'postman',
            
            # Concepts & Methodologies
            'rest api', 'graphql', 'microservices', 'serverless', 'agile', 'scrum', 'kanban',
            'tdd', 'bdd', 'ci/cd', 'devops', 'api', 'sdlc', 'responsive design', 'ux/ui',
            
            # Specific Technologies
            'canvas api', 'webgl', 'three.js', 'd3.js', 'chart.js', 'konva', 'fabric.js',
            'websockets', 'real-time', 'collaboration', 'drawing', 'erasing', 'undo', 'redo',
            'sticky notes', 'voice search', 'image upload', 'text manipulation',
            
            # Problem Solving
            'algorithms', 'data structures', 'leetcode', 'hackathon', 'competitive programming',
            'dsa', 'problem solving', 'optimization', 'performance', 'testing'
        ]
        
        # Find skills in the content
        found_skills = []
        content_lower = content.lower()
        
        for skill in skill_keywords:
            if skill in content_lower:
                # Handle special cases for better formatting
                if skill == 'reactjs':
                    found_skills.append('ReactJS')
                elif skill == 'nextjs':
                    found_skills.append('NextJS')
                elif skill == 'expressjs':
                    found_skills.append('ExpressJS')
                elif skill == 'c++':
                    found_skills.append('C++')
                elif skill == 'rest api':
                    found_skills.append('REST API')
                elif skill == 'socket.io':
                    found_skills.append('Socket.IO')
                elif skill == 'canvas api':
                    found_skills.append('Canvas API')
                elif skill == 'real-time':
                    found_skills.append('Real-time')
                elif skill == 'machine learning':
                    found_skills.append('Machine Learning')
                elif skill == 'data structures':
                    found_skills.append('Data Structures')
                elif skill == 'competitive programming':
                    found_skills.append('Competitive Programming')
                elif skill == 'responsive design':
                    found_skills.append('Responsive Design')
                elif skill == 'voice search':
                    found_skills.append('Voice Search')
                elif skill == 'image upload':
                    found_skills.append('Image Upload')
                elif skill == 'text manipulation':
                    found_skills.append('Text Manipulation')
                elif skill == 'sticky notes':
                    found_skills.append('Sticky Notes')
                elif skill == 'genai':
                    found_skills.append('GenAI')
                elif skill == 'langchain':
                    found_skills.append('LangChain')
                elif skill == 'sql server':
                    found_skills.append('SQL Server')
                elif skill == 'ux/ui':
                    found_skills.append('UX/UI')
                else:
                    found_skills.append(skill.title())
        
        # Remove duplicates and sort alphabetically
        unique_skills = sorted(list(set(found_skills)))
        
        if unique_skills:
            return f"Skills found: {', '.join(unique_skills)}"
        else:
            return content
    
    def search_by_keyword(self, keyword: str, k: int = 3) -> Dict[str, Any]:
        """
        Search for specific keywords in the document
        """
        try:
            # Use the keyword as the search query
            relevant_docs = self.vector_store.similarity_search(keyword, k=k)
            
            if not relevant_docs:
                return {
                    "answer": f"No content found containing the keyword '{keyword}'.",
                    "citations": [],
                    "source_documents": [],
                    "keyword": keyword,
                    "method": "keyword_search"
                }
            
            # Format the response
            answer = f"Found {len(relevant_docs)} relevant sections containing '{keyword}':\n\n"
            answer += self._format_relevant_content(relevant_docs, keyword)
            
            citations = self._process_citations(relevant_docs)
            
            return {
                "answer": answer,
                "citations": citations,
                "source_documents": relevant_docs,
                "keyword": keyword,
                "method": "keyword_search"
            }
            
        except Exception as e:
            return {
                "answer": f"Error searching for keyword '{keyword}': {str(e)}",
                "citations": [],
                "source_documents": [],
                "keyword": keyword,
                "method": "keyword_search"
            } 