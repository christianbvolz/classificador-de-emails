export function LoadingState() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-6 text-center fade-in">
      <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-4" />
      <p className="text-gray-600 dark:text-gray-300">Analisando email com IA...</p>
      <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Isso pode levar alguns segundos</p>
    </div>
  );
}
