import { useState } from 'react';
import { Pencil, Type, Upload, UploadCloud, FileText, Sparkles } from 'lucide-react';
import type { Email } from '../types';
import { readFileContent, parseEmailsFromFile } from '../utils/emailParser';

interface InputSectionProps {
  onAnalyze: (emails: Email[]) => void;
  isLoading: boolean;
}

type InputMode = 'text' | 'file';

export function InputSection({ onAnalyze, isLoading }: InputSectionProps) {
  const [mode, setMode] = useState<InputMode>('text');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState('');

  const handleFileSelect = async (file: File | null) => {
    if (!file) return;

    if (!(file.name.endsWith('.txt') || file.name.endsWith('.json'))) {
      setError('Por favor, selecione um arquivo .txt ou .json');
      return;
    }

    if (file.size > 1024 * 1024) {
      setError('Arquivo muito grande. Tamanho máximo: 1MB');
      return;
    }

    setUploadedFile(file);
    setError('');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && (file.name.endsWith('.txt') || file.name.endsWith('.json'))) {
      handleFileSelect(file);
    } else {
      setError('Por favor, envie apenas arquivos .txt ou .json');
    }
  };

  const handleAnalyze = async () => {
    setError('');

    if (mode === 'text') {
      if (!subject.trim() || !body.trim()) {
        setError('Por favor, preencha o assunto e o corpo do email');
        return;
      }

      onAnalyze([{ subject: subject.trim(), body: body.trim() }]);
    } else {
      if (!uploadedFile) {
        setError('Por favor, selecione um arquivo .txt ou .json');
        return;
      }

      try {
        const content = await readFileContent(uploadedFile);
        const emails = parseEmailsFromFile(content);

        if (emails.length === 0) {
          setError('Nenhum email encontrado no arquivo. Formato esperado: "Subject: ... Body: ..."');
          return;
        }

        onAnalyze(emails);
      } catch (err) {
        setError('Erro ao ler o arquivo: ' + (err as Error).message);
      }
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
        <Pencil className="w-5 h-5 mr-2 text-primary" />
        Inserir Email
      </h2>

      {/* Tab Selector */}
      <div className="flex space-x-2 mb-4 border-b border-gray-200">
        <button
          onClick={() => setMode('text')}
          className={`px-4 py-2 font-medium transition flex items-center ${
            mode === 'text'
              ? 'text-primary border-b-2 border-primary'
              : 'text-gray-500 hover:text-primary'
          }`}
        >
          <Type className="w-4 h-4 mr-1" />
          Colar Texto
        </button>
        <button
          onClick={() => setMode('file')}
          className={`px-4 py-2 font-medium transition flex items-center ${
            mode === 'file'
              ? 'text-primary border-b-2 border-primary'
              : 'text-gray-500 hover:text-primary'
          }`}
        >
          <Upload className="w-4 h-4 mr-1" />
          Upload Arquivo
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 text-sm text-red-600">
          {error}
        </div>
      )}

      {/* Text Input Panel */}
      {mode === 'text' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Assunto</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="Ex: Problema com pagamento"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Corpo do Email</label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="Cole o conteúdo do email aqui..."
            />
          </div>
        </div>
      )}

      {/* File Upload Panel */}
      {mode === 'file' && (
        <div
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition cursor-pointer"
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <UploadCloud className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600 mb-2">
            <label htmlFor="file-input" className="text-primary font-semibold cursor-pointer hover:underline">
              Clique para selecionar
            </label>{' '}
            ou arraste um arquivo .txt ou .json
          </p>
          <p className="text-sm text-gray-500">Tamanho máximo: 1MB</p>
          <input
            id="file-input"
            type="file"
            accept=".txt,.json"
            className="hidden"
            onChange={(e) => handleFileSelect(e.target.files?.[0] || null)}
          />
          {uploadedFile && (
            <div className="mt-4">
              <div className="inline-flex items-center bg-green-50 text-green-700 px-4 py-2 rounded-lg">
                <FileText className="w-4 h-4 mr-2" />
                <span>{uploadedFile.name}</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Action Button */}
      <button
        onClick={handleAnalyze}
        disabled={isLoading}
        className={`w-full mt-6 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg transition transform hover:scale-[1.02] flex items-center justify-center space-x-2 ${
          isLoading ? 'opacity-50 cursor-not-allowed' : ''
        }`}
      >
        <Sparkles className="w-5 h-5" />
        <span>Analisar Email</span>
      </button>
    </div>
  );
}
