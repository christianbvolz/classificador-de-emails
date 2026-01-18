import { Info } from 'lucide-react';

export function InfoCard() {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex items-start space-x-3">
      <Info className="w-5 h-5 text-blue-600 mt-0.5" />
      <div className="text-sm text-blue-800">
        <p className="font-semibold mb-1">Como funciona?</p>
        <p>
          Cole o texto do email ou faça upload de um arquivo .txt ou .json. A IA irá classificar como{' '}
          <strong>Produtivo</strong> ou <strong>Improdutivo</strong> e sugerir uma resposta automática. Máximo de 10 emails por análise.
        </p>
      </div>
    </div>
  );
}
