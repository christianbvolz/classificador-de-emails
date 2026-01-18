export function Footer() {
  return (
    <footer className="gradient-bg text-white py-6 mt-12 border-t border-white/10">
      <div className="container mx-auto px-4 text-center">
        <p className="text-base font-medium flex items-center justify-center">
          Desenvolvido por Christian Volz
        </p>
        <p className="text-sm text-white/90 mt-2">
          <a
            href="https://github.com/christianbvolz/classificador-de-emails"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-white hover:underline transition"
          >
            GitHub Repository
          </a>
        </p>
      </div>
    </footer>
  );
}
