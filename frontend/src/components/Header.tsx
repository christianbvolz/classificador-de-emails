import { Mail, BookOpen } from 'lucide-react';

export function Header() {
  const API_URL = import.meta.env.VITE_API_URL;

  return (
    <header className="gradient-bg text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Mail className="w-8 h-8" />
            <div>
              <h1 className="text-2xl font-bold">Classificador de Email</h1>
            </div>
          </div>
          <a
            href={`${API_URL}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition"
          >
            <BookOpen className="w-4 h-4" />
            <span className="hidden sm:inline">API Docs</span>
          </a>
        </div>
      </div>
    </header>
  );
}
