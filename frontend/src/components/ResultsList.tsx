import type { APIResponse } from '../types';
import { ResultCard } from './ResultCard';

interface ResultsListProps {
  results: APIResponse[];
}

export function ResultsList({ results }: ResultsListProps) {
  return (
    <div className="space-y-6">
      {results.map((result, index) => (
        <ResultCard key={index} result={result} index={index} />
      ))}
    </div>
  );
}
