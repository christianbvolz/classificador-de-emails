import type { APIResponse, Email } from './types';

const API_URL = import.meta.env.VITE_API_URL;

export async function processEmails(emails: Email[]): Promise<APIResponse[]> {
  const response = await fetch(`${API_URL}/process-email`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ emails }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Erro ao processar emails');
  }

  const data = await response.json();
  
  return data as APIResponse[];
}
