const API_BASE_URL = 'http://localhost:8000';

class ApiService {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    async uploadPDF(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.baseURL}/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to upload PDF');
        }

        return response.json();
    }

    async chatWithAI(question, sessionId = null) {
        const response = await fetch(`${this.baseURL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                session_id: sessionId
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get AI response');
        }

        return response.json();
    }

    async clearMemory(sessionId = null) {
        const response = await fetch(`${this.baseURL}/clear-memory`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to clear memory');
        }

        return response.json();
    }

    async getStats() {
        const response = await fetch(`${this.baseURL}/stats`);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get stats');
        }

        return response.json();
    }

    async healthCheck() {
        const response = await fetch(`${this.baseURL}/health`);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Backend health check failed');
        }

        return response.json();
    }

    async clearDocuments() {
        const response = await fetch(`${this.baseURL}/clear-documents`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to clear documents');
        }

        return response.json();
    }
}

const apiService = new ApiService();
export default apiService; 