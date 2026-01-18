export function Footer() {
  return (
    <footer className="bg-gray-800 dark:bg-gray-950 text-gray-300 dark:text-gray-400 py-6 mt-12 border-t border-gray-700 dark:border-gray-800">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm flex items-center justify-center">
          Desenvolvido por Christian Volz
        </p>
        <p className="text-xs text-gray-500 dark:text-gray-600 mt-2">
          <a
            href="https://github.com/christianbvolz/classificador-de-emails"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-white dark:hover:text-gray-300 transition"
          >
            GitHub Repository
          </a>
        </p>
      </div>
    </footer>
  );
}
