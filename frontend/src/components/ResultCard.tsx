import { useState } from 'react';
import { 
  CheckCircle, 
  XCircle, 
  Mail, 
  MessageSquare, 
  Copy, 
  Check,
  CreditCard,
  Wrench,
  HelpCircle,
  Smile,
  AlertTriangle,
  Trash2
} from 'lucide-react';
import type { APIResponse } from '../types';
import { CATEGORY_CONFIG } from '../types';

interface ResultCardProps {
  result: APIResponse;
  index: number;
}

export function ResultCard({ result, index }: ResultCardProps) {
  const [copiedSubject, setCopiedSubject] = useState(false);
  const [copiedBody, setCopiedBody] = useState(false);
  const [copiedAll, setCopiedAll] = useState(false);

  const config = CATEGORY_CONFIG[result.category] || {
    label: result.category,
    color: 'gray',
    icon: 'Mail',
    productive: false,
  };

  const isProductive = config.productive;
  const productiveClass = isProductive
    ? 'bg-green-50 text-green-700 border-green-200'
    : 'bg-gray-50 text-gray-700 border-gray-200';
  const productiveLabel = isProductive ? 'Produtivo' : 'Improdutivo';
  const ProductiveIcon = isProductive ? CheckCircle : XCircle;

  // Get icon component based on category
  const iconMap: Record<string, typeof Mail> = {
    'credit-card': CreditCard,
    'wrench': Wrench,
    'help-circle': HelpCircle,
    'smile': Smile,
    'alert-triangle': AlertTriangle,
    'trash-2': Trash2,
  };
  const CategoryIcon = iconMap[config.icon] || Mail;

  const handleCopySubject = async () => {
    try {
      await navigator.clipboard.writeText(result.suggestedSubject);
      setCopiedSubject(true);
      setTimeout(() => setCopiedSubject(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleCopyBody = async () => {
    try {
      await navigator.clipboard.writeText(result.suggestedBody);
      setCopiedBody(true);
      setTimeout(() => setCopiedBody(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleCopyAll = async () => {
    try {
      const fullEmail = `Assunto: ${result.suggestedSubject}\n\n${result.suggestedBody}`;
      await navigator.clipboard.writeText(fullEmail);
      setCopiedAll(true);
      setTimeout(() => setCopiedAll(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const colorClasses: Record<string, string> = {
    red: 'bg-red-100 text-red-700',
    orange: 'bg-orange-100 text-orange-700',
    blue: 'bg-blue-100 text-blue-700',
    green: 'bg-green-100 text-green-700',
    purple: 'bg-purple-100 text-purple-700',
    gray: 'bg-gray-100 text-gray-700',
  };

  const iconColorClasses: Record<string, string> = {
    red: 'text-red-600',
    orange: 'text-orange-600',
    blue: 'text-blue-600',
    green: 'text-green-600',
    purple: 'text-purple-600',
    gray: 'text-gray-600',
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 fade-in">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="text-sm font-semibold text-gray-500 dark:text-gray-400">Email {index + 1}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${productiveClass} border flex items-center`}>
            <ProductiveIcon className="w-3 h-3 mr-1" />
            {productiveLabel}
          </span>
        </div>
      </div>

      <div className="mb-4">
        <h3 className="font-bold text-gray-800 dark:text-gray-100 mb-2 flex items-center">
          <Mail className="w-4 h-4 mr-2 text-gray-600 dark:text-gray-400" />
          {result.originalEmail.subject}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3">{result.originalEmail.body}</p>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mb-4">
        <div className="flex items-center space-x-2 mb-3">
          <CategoryIcon className={`w-5 h-5 ${iconColorClasses[config.color]}`} />
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${colorClasses[config.color]}`}>
            {config.label}
          </span>
        </div>
      </div>

      <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold text-gray-800 dark:text-gray-100 flex items-center">
            <MessageSquare className="w-4 h-4 mr-2 text-indigo-600 dark:text-indigo-400" />
            Resposta Sugerida
          </h4>
          <button
            onClick={handleCopyAll}
            className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition flex items-center text-sm font-medium"
          >
            {copiedAll ? (
              <>
                <Check className="w-4 h-4 mr-1" />
                Copiado!
              </>
            ) : (
              <>
                <Copy className="w-4 h-4 mr-1" />
                Copiar Tudo
              </>
            )}
          </button>
        </div>

        <div className="mb-3 bg-white dark:bg-gray-700 rounded-lg p-3 border border-indigo-200 dark:border-indigo-800">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 uppercase">Assunto</span>
            <button
              onClick={handleCopySubject}
              className="text-indigo-500 dark:text-indigo-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition flex items-center text-xs"
            >
              {copiedSubject ? (
                <>
                  <Check className="w-3 h-3 mr-1" />
                  Copiado
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3 mr-1" />
                  Copiar
                </>
              )}
            </button>
          </div>
          <p className="text-gray-800 dark:text-gray-100 text-sm font-medium">{result.suggestedSubject}</p>
        </div>

        <div className="bg-white dark:bg-gray-700 rounded-lg p-3 border border-indigo-200 dark:border-indigo-800">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 uppercase">Corpo</span>
            <button
              onClick={handleCopyBody}
              className="text-indigo-500 dark:text-indigo-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition flex items-center text-xs"
            >
              {copiedBody ? (
                <>
                  <Check className="w-3 h-3 mr-1" />
                  Copiado
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3 mr-1" />
                  Copiar
                </>
              )}
            </button>
          </div>
          <p className="text-gray-700 dark:text-gray-300 text-sm whitespace-pre-line">{result.suggestedBody}</p>
        </div>
      </div>
    </div>
  );
}
