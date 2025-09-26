import React from 'react';
import { TransactionMilestone } from '@/types';

type Props = {
  milestones: TransactionMilestone[];
  onMilestoneClick?: (m: TransactionMilestone) => void;
};

const iconFor = (type: TransactionMilestone['type']) => {
  switch (type) {
    case 'offer_submitted':
    case 'closing':
      return '📝';
    case 'offer_accepted':
      return '👍';
    case 'contract_signed':
      return '🖊️';
    case 'inspection':
      return '🔍';
    case 'appraisal':
      return '📊';
    case 'financing_approved':
      return '🏦';
    case 'possession':
      return '🔑';
    default:
      return '⏺️';
  }
};

const TransactionTimeline: React.FC<Props> = ({ milestones, onMilestoneClick }) => {
  const sorted = [...milestones].sort((a,b) => a.dueDate.localeCompare(b.dueDate));

  return (
    <ol className="relative border-s border-gray-200">
      {sorted.map((m, idx) => (
        <li key={m.id} className="mb-6 ms-6">
          <span className={`absolute -start-3 flex h-6 w-6 items-center justify-center rounded-full ring-4 ring-white ${m.completed ? 'bg-orange-600 text-white' : 'bg-white border border-gray-300'}`}>
            <span className="text-xs" aria-hidden>{iconFor(m.type)}</span>
          </span>
          <div className="flex items-center justify-between">
            <h3 className="font-medium text-gray-900">{m.title}</h3>
            <span className="text-xs text-gray-500">{new Date(m.dueDate).toLocaleDateString()}</span>
          </div>
          <p className="text-sm text-gray-600 mt-1">{m.description}</p>
          {m.completed && m.completedAt && (
            <div className="mt-1 text-xs text-emerald-700">Completed on {new Date(m.completedAt).toLocaleDateString()}</div>
          )}
          {!!m.documents?.length && (
            <div className="mt-2 text-xs text-gray-500">{m.documents.length} document{m.documents.length>1?'s':''} attached</div>
          )}
          {onMilestoneClick && (
            <button className="mt-2 text-sm text-orange-700 hover:underline" onClick={() => onMilestoneClick(m)}>View actions</button>
          )}
        </li>
      ))}
    </ol>
  );
};

export default TransactionTimeline;
