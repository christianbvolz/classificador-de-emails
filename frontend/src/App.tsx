import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { InfoCard } from './components/InfoCard';
import { InputSection } from './components/InputSection';
import { LoadingState } from './components/LoadingState';
import { ErrorState } from './components/ErrorState';
import { ResultsList } from './components/ResultsList';
import { Footer } from './components/Footer';
import type { Email, APIResponse } from './types';
import { processEmails } from './api';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<APIResponse[]>([]);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : true;
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  const handleAnalyze = async (emails: Email[]) => {
    setLoading(true);
    setError('');
    setResults([]);

    try {
      const response = await processEmails(emails);
      setResults(response);
    } catch (err) {
      setError((err as Error).message || 'Error to process emails');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors">
      <Header darkMode={darkMode} toggleDarkMode={() => setDarkMode(!darkMode)} />

      <main className="container mx-auto px-4 py-8 max-w-4xl flex-grow">
        <InfoCard />
        <InputSection onAnalyze={handleAnalyze} isLoading={loading} />

        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}
        {results.length > 0 && <ResultsList results={results} />}
      </main>

      <Footer />
    </div>
  );
}

export default App;
