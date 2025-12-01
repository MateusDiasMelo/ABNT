import React, { useState } from 'react';
import { CreditCard, QrCode } from 'lucide-react';

interface PaymentSectionProps {
  price: number;
  pages: number;
  onPaymentInitiate: (gateway: 'mercadopago' | 'stripe', email?: string) => void;
  paymentData?: {
    qr_code_base64?: string;
    ticket_url?: string;
    client_secret?: string;
  };
  loading?: boolean;
}

const PaymentSection: React.FC<PaymentSectionProps> = ({
  price,
  pages,
  onPaymentInitiate,
  paymentData,
  loading
}) => {
  const [email, setEmail] = useState('');
  const [selectedGateway, setSelectedGateway] = useState<'mercadopago' | 'stripe'>('mercadopago');

  const handlePayment = () => {
    onPaymentInitiate(selectedGateway, email || undefined);
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
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                fontSize: '1rem'
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Forma de Pagamento
            </label>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button
                className={`button ${selectedGateway === 'mercadopago' ? 'button-primary' : ''}`}
                onClick={() => setSelectedGateway('mercadopago')}
                style={{
                  flex: 1,
                  background: selectedGateway === 'mercadopago' ? undefined : '#e2e8f0'
                }}
              >
                <QrCode size={20} />
                PIX / Mercado Pago
              </button>
              <button
                className={`button ${selectedGateway === 'stripe' ? 'button-primary' : ''}`}
                onClick={() => setSelectedGateway('stripe')}
                style={{
                  flex: 1,
                  background: selectedGateway === 'stripe' ? undefined : '#e2e8f0'
                }}
              >
                <CreditCard size={20} />
                Cartão / Stripe
              </button>
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
          />
          <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
            Após o pagamento, o download será liberado automaticamente
          </p>
        </div>
      )}

      {paymentData?.client_secret && (
        <div className="info-box">
          <h4>Pagamento via Stripe</h4>
          <p>Complete o pagamento para liberar o download</p>
          {/* Aqui seria integrado o Stripe Elements */}
        </div>
      )}
    </div>
  );
};

export default PaymentSection;
