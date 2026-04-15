import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  const [strategy, setStrategy] = useState('v1');
  const [sessionId, setSessionId] = useState(null);
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [message, setMessage] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadInfo, setUploadInfo] = useState(null);
  const API_URL = 'http://localhost:8000';

  const handleUpload = async () => {
    if (!file) {
      alert('Selecione um arquivo primeiro');
      return;
    }

    setLoading(true);
    setUploadInfo(null);
    setMessage([])
    setSessionId(null)

    const formData = new FormData();
    formData.append('file', file);
    formData.append('strategy', strategy)

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        alert('Erro:' + error.detail);
        setLoading(false);
        return;
      }

      const data = await  response.json();

      setSessionId(data.session_id)
      setUploadInfo(data)

    } catch (err) {
      alert('Erro de conexão')
    }

    setLoading(false)

  };

  const handleSend = async () => {
    if (!question.trim()) return;
    if (!sessionId) {
      alert('Faça um upload');
      return;
    }
    //add pergunta do user na lista de msg
    const userMessage = { role: 'user', text: question};
    setMessage((prev) => [...prev, userMessage]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          session_id: sessionId,
          question: question,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        const errorMessage = {role: 'bot', text: 'erro: ' + error.detail};
        setMessage((prev) => [...prev, errorMessage]);
        setLoading(false);
        return; 
      }

      const data = await response.json();


      //add reposta do bot na lista de msg
      const botMessage = {role: 'bot', text: data.answer};
      setMessage ((prev) => [...prev, botMessage]);
    }
    catch(err) {
      const errorMessage = {role: 'bot', text: 'Erro de conexão'}
    }

    setLoading(false);

  };



  //Enviar com enter
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !loading) {
      handleSend();
    }
  };


  //RENDERIZAÇÃO DA TELA


  return (
    <div className='app'>
      <h1>Missão RAG</h1>

      <div className='config-section'>

        <div className='strategy-selector'>
          <label>Estratégia:</label>
          <select
            value={strategy}
            onChange={(e) => setStrategy(e.target.value)}
            disabled={loading}
          >
            <option value='v1'>v1 - Default</option>
            <option value='v2'>v2 - Hybrid - Semantic + BM25 + CoT</option>
          </select>
        </div>
        <div className='upload-section'>
          <input
            type='file'
            accept='.pdf'
            onChange={(e) => setFile(e.target.files[0])}
            disabled={loading}
          />
          <button onClick={handleUpload} disabled={loading || !file}>
            {loading && !sessionId ? 'Processando' : 'Enviar PDF'}
          </button>
        </div>

        {uploadInfo && (
          <div className='upload-info'>
            <p>Feito! {uploadInfo.filename} enviado.</p>
            <p>Estratégia: {uploadInfo.strategy}</p>
            <p>Chunks gerados: {uploadInfo.chunks}</p>
          </div>
        )}
      </div>
      <div className='chat-section'>
        <div className='messages'>
          {message.length === 0 && sessionId && (
            <p className='empty-chat'>PDF carregado</p>
          )}
          {message.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong> {msg.role === 'user' ? 'Você' : 'Greg'}</strong>
            <p>{msg.text}</p>
          </div>
          ))}
          {loading && sessionId && (
            <div className='message-bot'>
              <strong>Greg:</strong>
              <p>Pensando...</p>
            </div>
          )}
        </div>
        
        <div className='input-section'>
          <input
            type='text'
            placeholder={sessionId ? 'Digite sua pergunta' : "Envie um PDF primeiro"}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyPress}
            disabled={!sessionId || loading}
          />
          <button onClick={handleSend} disabled={!sessionId || loading || !question.trim()}>
            Enviar
          </button>
        </div>
      </div>        
    </div>
  );
}
  
export default App;