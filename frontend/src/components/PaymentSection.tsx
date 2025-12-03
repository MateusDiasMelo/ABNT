import React, { useState } from 'react';
import { QrCode, Copy, Check } from 'lucide-react';

interface PaymentSectionProps {
  price: number;
  pages: number;
  onPaymentInitiate: (gateway: 'mercadopago', email?: string) => void;
  onGenerateNewQRCode?: () => void;
  paymentData?: {
    qr_code?: string;
    qr_code_base64?: string;
    ticket_url?: string;
    status?: string;
  };
  loading?: boolean;
}

const PaymentSection: React.FC<PaymentSectionProps> = ({
  price,
  pages,
  onPaymentInitiate,
  onGenerateNewQRCode,
  paymentData,
  loading
}) => {
  const [email, setEmail] = useState('');
  const [copiedCode, setCopiedCode] = useState(false);

  const handlePayment = () => {
    onPaymentInitiate('mercadopago', email || undefined);
  };

  const handleCopyCode = async () => {
    if (paymentData?.qr_code) {
      await navigator.clipboard.writeText(paymentData.qr_code);
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    }
  };

  return (
    <div className="card">
      <h2>💰 Valor do Serviço</h2>

      <div className="price-display">
        <p className="details">
          {pages} {pages === 1 ? 'página' : 'páginas'} × R$ 0,80
        </p>
        <div className="price">
          R$ {price.toFixed(2)}
        </div>
        <p className="details">Formatação ABNT completa</p>
      </div>

      {!paymentData && (
        <>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Forma de Pagamento
            </label>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.75rem',
              background: 'var(--primary-color)',
              color: 'white',
              borderRadius: '8px',
              fontWeight: '500'
            }}>
              <QrCode size={20} />
              PIX / Mercado Pago
            </div>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="email" style={{ display: 'block', marginBottom: '0.5rem' }}>
              Email (opcional)
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                fontSize: '1rem',
                fontFamily: 'inherit'
              }}
            />
            <p style={{
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
              marginTop: '0.5rem'
            }}>
              Se informado, o arquivo será enviado automaticamente após o pagamento
            </p>
          </div>

          <button
            className="button button-success"
            onClick={handlePayment}
            disabled={loading}
            style={{ width: '100%' }}
          >
            {loading ? 'Processando...' : 'Pagar e Baixar'}
          </button>
        </>
      )}

      {paymentData?.qr_code_base64 && (
        <div className="qr-code-container">
          <h3>Escaneie o QR Code para pagar com PIX</h3>
          <img
            src={`data:image/png;base64,${paymentData.qr_code_base64}`}
            alt="QR Code PIX"
            style={{ maxWidth: '300px', margin: '1rem auto', display: 'block' }}
          />

          {paymentData.qr_code && (
            <div style={{ marginTop: '1rem' }}>
              <p style={{
                marginBottom: '0.5rem',
                fontWeight: '500',
                color: 'var(--text-color)'
              }}>
                Ou copie o código PIX:
              </p>
              <div style={{
                display: 'flex',
                gap: '0.5rem',
                alignItems: 'stretch'
              }}>
                <input
                  type="text"
                  value={paymentData.qr_code}
                  readOnly
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid var(--border-color)',
                    fontSize: '0.85rem',
                    fontFamily: 'monospace',
                    background: '#f5f5f5'
                  }}
                />
                <button
                  onClick={handleCopyCode}
                  style={{
                    padding: '0.75rem 1rem',
                    borderRadius: '8px',
                    border: '1px solid var(--border-color)',
                    background: copiedCode ? '#22c55e' : 'white',
                    color: copiedCode ? 'white' : 'var(--text-color)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    fontWeight: '500',
                    transition: 'all 0.2s'
                  }}
                >
                  {copiedCode ? (
                    <>
                      <Check size={18} />
                      Copiado!
                    </>
                  ) : (
                    <>
                      <Copy size={18} />
                      Copiar
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
            Após o pagamento, o download será liberado automaticamente
          </p>
          {paymentData.status === 'pending' && (
            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#666' }}>
              Aguardando confirmação do pagamento...
            </p>
          )}

          {onGenerateNewQRCode && (
            <button
              className="button"
              onClick={onGenerateNewQRCode}
              disabled={loading}
              style={{
                width: '100%',
                marginTop: '1rem',
                background: 'var(--border-color)',
                color: 'var(--text-color)'
              }}
            >
              {loading ? 'Gerando...' : '🔄 Gerar Novo QR Code'}
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default PaymentSection;
