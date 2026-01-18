export interface Email {
  subject: string;
  body: string;
}

export interface EmailResult extends Email {
  category: EmailCategory;
  response: string;
}

export interface APIResponse {
  isProductive: boolean;
  category: EmailCategory;
  suggestedSubject: string;
  suggestedBody: string;
  detectedLanguage?: string;
  originalEmail: {
    subject: string;
    body: string;
  };
}

export type EmailCategory =
  | 'payment_issue'
  | 'technical_support'
  | 'information_request'
  | 'greeting'
  | 'complaint'
  | 'spam';

export interface CategoryConfig {
  label: string;
  color: string;
  icon: string;
  productive: boolean;
}

export const CATEGORY_CONFIG: Record<EmailCategory, CategoryConfig> = {
  payment_issue: {
    label: 'Problema de Pagamento',
    color: 'red',
    icon: 'credit-card',
    productive: true,
  },
  technical_support: {
    label: 'Suporte Técnico',
    color: 'orange',
    icon: 'wrench',
    productive: true,
  },
  information_request: {
    label: 'Pedido de Informação',
    color: 'blue',
    icon: 'help-circle',
    productive: true,
  },
  greeting: {
    label: 'Saudação',
    color: 'green',
    icon: 'smile',
    productive: false,
  },
  complaint: {
    label: 'Reclamação',
    color: 'purple',
    icon: 'alert-triangle',
    productive: true,
  },
  spam: {
    label: 'Spam',
    color: 'gray',
    icon: 'trash-2',
    productive: false,
  },
};
