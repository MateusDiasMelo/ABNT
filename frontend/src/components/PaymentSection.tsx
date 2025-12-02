import React from 'react';
import { QrCode } from 'lucide-react';

interface PaymentSectionProps {
  price: number;
  pages: number;
  onPaymentInitiate: (gateway: 'mercadopago', email?: string) => void;
  onGenerateNewQRCode?: () => void;
  paymentData?: {
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
  const handlePayment = () => {
    onPaymentInitiate('mercadopago');
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
