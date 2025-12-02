import { useState } from 'react';
import { FileText, Download, CheckCircle, AlertCircle } from 'lucide-react';
import './styles/App.css';

import UploadZone from './components/UploadZone';
import ProgressSteps from './components/ProgressSteps';
import PaymentSection from './components/PaymentSection';

import {
  uploadDocument,
  processDocument,
  createPayment,
  verifyPayment,
  getDownloadUrl,
  DocumentResponse,
  ProcessingResponse,
  PaymentResponse
} from './services/api';

type Step = 1 | 2 | 3 | 4;

interface AppState {
  step: Step;
  selectedFile: File | null;
  documentData: DocumentResponse | null;
  processingData: ProcessingResponse | null;
  paymentData: PaymentResponse | null;
  loading: boolean;
  error: string | null;
  paymentVerificationInterval: NodeJS.Timeout | null;
}

function App() {
  const [state, setState] = useState<AppState>({
    step: 1,
    selectedFile: null,
    documentData: null,
    processingData: null,
    paymentData: null,
    loading: false,
    error: null,
    paymentVerificationInterval: null
  });

  const handleFileSelect = async (file: File) => {
    setState(prev => ({ ...prev, selectedFile: file, loading: true, error: null }));

    try {
      // Upload
      const uploadResult = await uploadDocument(file);
      setState(prev => ({
        ...prev,
        documentData: uploadResult,
        step: 2,
        loading: true
      }));

      // Processamento automático
      const processResult = await processDocument(uploadResult.file_id);
      setState(prev => ({
        ...prev,
        processingData: processResult,
        step: 3,
        loading: false
      }));
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.response?.data?.detail || 'Erro ao processar arquivo'
      }));
    }
  };

  const handlePaymentInitiate = async (gateway: 'mercadopago', email?: string) => {
    if (!state.documentData) return;

    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const paymentResult = await createPayment(
        state.documentData.file_id,
        gateway,
        email
      );

      if (paymentResult.success) {
        setState(prev => ({
          ...prev,
          paymentData: paymentResult,
          loading: false
        }));

        // Verifica pagamento periodicamente
        startPaymentVerification(state.documentData.file_id, paymentResult.payment_id!, gateway);
      } else {
        throw new Error(paymentResult.error || 'Erro ao criar pagamento');
      }
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.response?.data?.detail || error.message || 'Erro ao criar pagamento'
      }));
    }
  };

  const handleGenerateNewQRCode = async () => {
    if (!state.documentData) return;

    // Limpa o interval de verificação anterior se existir
    if (state.paymentVerificationInterval) {
      clearInterval(state.paymentVerificationInterval);
    }

    // Limpa o pagamento anterior
    setState(prev => ({ ...prev, paymentData: null, loading: true, error: null, paymentVerificationInterval: null }));

    // Cria um novo pagamento
    try {
      const paymentResult = await createPayment(
        state.documentData.file_id,
        'mercadopago'
      );

      if (paymentResult.success) {
        setState(prev => ({
          ...prev,
          paymentData: paymentResult,
          loading: false
        }));

        // Verifica pagamento periodicamente
        startPaymentVerification(state.documentData.file_id, paymentResult.payment_id!, 'mercadopago');
      } else {
        throw new Error(paymentResult.error || 'Erro ao gerar novo QR Code');
      }
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.response?.data?.detail || error.message || 'Erro ao gerar novo QR Code'
      }));
    }
  };

  const startPaymentVerification = (fileId: string, paymentId: string, gateway: 'mercadopago') => {
    // Limpa o interval anterior se existir
    if (state.paymentVerificationInterval) {
      clearInterval(state.paymentVerificationInterval);
    }

    const interval = setInterval(async () => {
      try {
        const result = await verifyPayment(fileId, paymentId, gateway);

        if (result.approved) {
          clearInterval(interval);
          setState(prev => ({ ...prev, step: 4, paymentVerificationInterval: null }));
        }
      } catch (error) {
        console.error('Erro ao verificar pagamento:', error);
      }
    }, 3000); // Verifica a cada 3 segundos

    // Armazena a referência do interval no estado
    setState(prev => ({ ...prev, paymentVerificationInterval: interval }));

    // Para após 10 minutos
    setTimeout(() => {
      clearInterval(interval);
      setState(prev => ({ ...prev, paymentVerificationInterval: null }));
    }, 600000);
  };

  const handleDownload = () => {
    if (state.documentData) {
      window.open(getDownloadUrl(state.documentData.file_id), '_blank');
    }
  };

  const handleReset = () => {
    // Limpa o interval de verificação se existir
    if (state.paymentVerificationInterval) {
      clearInterval(state.paymentVerificationInterval);
    }

    setState({
      step: 1,
      selectedFile: null,
      documentData: null,
      processingData: null,
      paymentData: null,
      loading: false,
      error: null,
      paymentVerificationInterval: null
    });
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>📚 ABNT Formatador</h1>
          <p>Formatação automática de trabalhos acadêmicos seguindo normas ABNT</p>
        </div>
      </header>

      <main className="container">
        <ProgressSteps currentStep={state.step} />

        {state.error && (
          <div className="info-box info-box-warning">
            <AlertCircle size={20} style={{ display: 'inline', marginRight: '0.5rem' }} />
            <strong>Erro:</strong> {state.error}
          </div>
        )}

        {/* Step 1: Upload */}
        {state.step === 1 && (
          <div className="card">
            <h2>1️⃣ Faça o Upload do seu Trabalho</h2>
            <UploadZone
              onFileSelect={handleFileSelect}
              disabled={state.loading}
            />

            {state.loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Enviando arquivo...</p>
              </div>
            )}

            <div className="info-box" style={{ marginTop: '2rem' }}>
              <h4>✅ O que será formatado:</h4>
              <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
                <li>Margens ABNT (3cm superior/esquerda, 2cm inferior/direita)</li>
                <li>Fonte Times New Roman, tamanho 12</li>
                <li>Espaçamento 1,5 no texto</li>
                <li>Numeração de páginas correta</li>
                <li>Formatação de citações e referências (NBR 6023)</li>
                <li>Estrutura completa do trabalho acadêmico</li>
              </ul>
            </div>
          </div>
        )}

        {/* Step 2: Processing */}
        {state.step === 2 && (
          <div className="card">
            <div className="loading">
              <div className="spinner"></div>
              <h2>🔄 Processando e Formatando</h2>
              <p>Aplicando normas ABNT ao seu documento...</p>
              <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                Arquivo: {state.selectedFile?.name}
              </p>
            </div>
          </div>
        )}

        {/* Step 3: Payment */}
        {state.step === 3 && state.processingData && (
          <>
            <div className="info-box info-box-success">
              <CheckCircle size={20} style={{ display: 'inline', marginRight: '0.5rem' }} />
              <strong>Documento formatado com sucesso!</strong>
              <p style={{ marginTop: '0.5rem' }}>
                <FileText size={16} style={{ display: 'inline', marginRight: '0.25rem' }} />
                {state.processingData.formatted_pages} {state.processingData.formatted_pages === 1 ? 'página' : 'páginas'} formatadas
              </p>
            </div>

            <PaymentSection
              price={state.processingData.price}
              pages={state.processingData.formatted_pages}
              onPaymentInitiate={handlePaymentInitiate}
              onGenerateNewQRCode={handleGenerateNewQRCode}
              paymentData={state.paymentData || undefined}
              loading={state.loading}
            />
          </>
        )}

        {/* Step 4: Download */}
        {state.step === 4 && (
          <div className="card" style={{ textAlign: 'center' }}>
            <CheckCircle size={80} color="var(--success-color)" style={{ margin: '0 auto 1rem' }} />
            <h2>✅ Pagamento Confirmado!</h2>
            <p style={{ marginBottom: '2rem', color: 'var(--text-secondary)' }}>
              Seu documento está pronto para download
            </p>

            <button
              className="button button-success"
              onClick={handleDownload}
              style={{ fontSize: '1.1rem', padding: '1rem 2rem' }}
            >
              <Download size={24} />
              Baixar Documento Formatado
            </button>

            <button
              className="button"
              onClick={handleReset}
              style={{ marginTop: '1rem', background: '#e2e8f0' }}
            >
              Formatar Outro Documento
            </button>

            <div className="info-box" style={{ marginTop: '2rem', textAlign: 'left' }}>
              <h4>📝 Seu documento foi formatado com:</h4>
              <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
                <li>Normas ABNT NBR 14724 (trabalhos acadêmicos)</li>
                <li>Normas ABNT NBR 6023 (referências)</li>
                <li>Margens, fontes e espaçamentos corretos</li>
                <li>Numeração de páginas adequada</li>
              </ul>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>ABNT Formatador © 2024 - Formatação automática de trabalhos acadêmicos</p>
        <p style={{ marginTop: '0.5rem' }}>
          NBR 14724 | NBR 6023 | R$ 0,80 por página
        </p>
      </footer>
    </div>
  );
}

export default App;
