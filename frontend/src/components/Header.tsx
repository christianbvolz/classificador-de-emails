import { Mail, BookOpen, Moon, Sun } from 'lucide-react';

interface HeaderProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
}

export function Header({ darkMode, toggleDarkMode }: HeaderProps) {
  const API_URL = import.meta.env.VITE_API_URL;

  return (
    <header className="gradient-bg text-white shadow-lg dark:from-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Mail className="w-8 h-8" />
            <div>
              <h1 className="text-2xl font-bold">Classificador de Email</h1>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={toggleDarkMode}
              className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition"
              aria-label="Toggle dark mode"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
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
      </div>
    </header>
  );
}
