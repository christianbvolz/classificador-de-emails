export function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6 mt-12">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm flex items-center justify-center">
          Desenvolvido por Christian Volz
        </p>
        <p className="text-xs text-gray-500 mt-2">
          <a
            href="https://github.com/christianbvolz/classificador-de-emails"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-white transition"
          >
            GitHub Repository
          </a>
        </p>
      </div>
    </footer>
  );
}
