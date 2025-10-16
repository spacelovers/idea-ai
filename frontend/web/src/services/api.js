import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatAPI = {
  sendMessage: async (message, model = 'aria', conversationId = null) => {
    const response = await api.post('/chat/send', {
      message,
      model,
      conversation_id: conversationId
    });
    return response.data;
  },

  getHistory: async (conversationId) => {
    const response = await api.get(`/chat/history/${conversationId}`);
    return response.data;
  },

  deleteConversation: async (conversationId) => {
    const response = await api.delete(`/chat/conversation/${conversationId}`);
    return response.data;
  }
};

// Analysis API
export const analysisAPI = {
  analyzeText: async (text, analysisType = 'sentiment') => {
    const response = await api.post('/analyze/text', {
      text,
      analysis_type: analysisType
    });
    return response.data;
  }
};

// Voice API
export const voiceAPI = {
  speechToText: async (audioFile) => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);

    const response = await api.post('/voice/speech-to-text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  textToSpeech: async (text, voice = 'default') => {
    const response = await api.post('/voice/text-to-speech', {
      text,
      voice
    });
    return response.data;
  }
};

export default api;