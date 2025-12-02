/**
 * API Service
 * Cliente para comunicação com backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface DocumentResponse {
  file_id: string;
  original_filename: string;
  original_extension: string;
  status: string;
  message: string;
}

export interface ProcessingResponse {
  file_id: string;
  status: string;
  formatted_pages: number;
  price: number;
  currency: string;
  message: string;
}

export interface PaymentResponse {
  success: boolean;
  payment_id?: string;
  status?: string;
  qr_code?: string;
  qr_code_base64?: string;
  ticket_url?: string;
  error?: string;
}

export interface DocumentStatus {
  file_id: string;
  original_filename: string;
  status: string;
  formatted_pages?: number;
  price?: number;
  payment_status: string;
  uploaded_at: string;
  expires_at: string;
}

/**
 * Upload de documento
 */
export const uploadDocument = async (file: File): Promise<DocumentResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<DocumentResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Processa documento
 */
export const processDocument = async (fileId: string): Promise<ProcessingResponse> => {
  const response = await api.post<ProcessingResponse>(`/process/${fileId}`);
  return response.data;
};

/**
 * Cria pagamento
 */
export const createPayment = async (
  fileId: string,
  gateway: 'mercadopago',
  payerEmail?: string
): Promise<PaymentResponse> => {
  const response = await api.post<PaymentResponse>('/payment/create', {
    file_id: fileId,
    gateway,
    payer_email: payerEmail,
  });

  return response.data;
};

/**
 * Verifica pagamento
 */
export const verifyPayment = async (
  fileId: string,
  paymentId: string,
  gateway: 'mercadopago'
): Promise<any> => {
  const response = await api.post('/payment/verify', {
    file_id: fileId,
    payment_id: paymentId,
    gateway,
  });

  return response.data;
};

/**
 * Obtém status do documento
 */
export const getDocumentStatus = async (fileId: string): Promise<DocumentStatus> => {
  const response = await api.get<DocumentStatus>(`/status/${fileId}`);
  return response.data;
};

/**
 * Gera URL de download
 */
export const getDownloadUrl = (fileId: string): string => {
  return `${API_BASE_URL}/download/${fileId}`;
};

export default api;
