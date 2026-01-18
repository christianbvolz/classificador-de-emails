import type { Email } from '../types';

export function parseEmailsFromFile(content: string): Email[] {
  const emails: Email[] = [];
  const lines = content.split('\n');
  let currentEmail: Partial<Email> | null = null;
  let bodyLines: string[] = [];

  for (let line of lines) {
    line = line.trim();

    if (line.toLowerCase().startsWith('subject:')) {
      // Save previous email if exists
      if (currentEmail) {
        currentEmail.body = bodyLines.join('\n').trim();
        if (currentEmail.subject && currentEmail.body) {
          emails.push(currentEmail as Email);
        }
      }

      // Start new email
      currentEmail = {
        subject: line.substring(8).trim(),
        body: '',
      };
      bodyLines = [];
    } else if (line.toLowerCase().startsWith('body:')) {
      bodyLines.push(line.substring(5).trim());
    } else if (line && currentEmail) {
      bodyLines.push(line);
    }
  }

  // Save last email
  if (currentEmail) {
    currentEmail.body = bodyLines.join('\n').trim();
    if (currentEmail.subject && currentEmail.body) {
      emails.push(currentEmail as Email);
    }
  }

  return emails.slice(0, 10); // Max 10 emails
}

export function readFileContent(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target?.result as string);
    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsText(file);
  });
}
