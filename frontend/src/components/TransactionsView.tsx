import React, { useMemo, useState } from 'react';
import { MOCK_TRANSACTIONS } from '@/constants.tsx';
import { Transaction } from '@/types';
import TransactionTimeline from './TransactionTimeline';
import DocumentManager from './DocumentManager';

type Props = {
  onBack: () => void;
};

const statusColor: Record<Transaction['status'], string> = {
  draft: 'bg-gray-200 text-gray-700',
  in_progress: 'bg-orange-100 text-orange-800',
  pending_approval: 'bg-amber-100 text-amber-800',
  completed: 'bg-emerald-100 text-emerald-800',
  cancelled: 'bg-rose-100 text-rose-800',
};

const TransactionsView: React.FC<Props> = ({ onBack }) => {
  const [txs, setTxs] = useState<Transaction[]>(MOCK_TRANSACTIONS as unknown as Transaction[]);
  const [selectedTx, setSelectedTx] = useState<Transaction | null>(txs[0] || null);

  const progress = useMemo(() => {
    if (!selectedTx) return 0;
    const done = selectedTx.milestones.filter(m => m.completed).length;
    return Math.round((done / selectedTx.milestones.length) * 100);
  }, [selectedTx]);

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-4 border-b">
        <button onClick={onBack} className="text-gray-600 hover:text-gray-900">← Back</button>
        <h1 className="text-lg font-semibold">Transactions</h1>
        <div />
      </div>

      <div className="flex flex-1 overflow-hidden">
        <aside className="w-72 border-r overflow-y-auto">
          <div className="p-3 border-b flex items-center justify-between">
            <span className="font-medium">All Transactions</span>
            <button className="px-3 py-1 rounded bg-orange-600 text-white text-sm">New</button>
          </div>
          <ul>
            {txs.map(tx => {
              const pct = Math.round((tx.milestones.filter(m=>m.completed).length/tx.milestones.length)*100);
              return (
                <li key={tx.id}>
                  <button
                    className={`w-full text-left p-3 hover:bg-gray-50 ${selectedTx?.id===tx.id?'bg-gray-50':''}`}
                    onClick={() => setSelectedTx(tx)}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="text-sm font-medium">{tx.id}</div>
                      <span className={`text-xs px-2 py-0.5 rounded ${statusColor[tx.status]}`}>{tx.status.replace('_',' ')}</span>
                    </div>
                    <div className="text-xs text-gray-500">Closing: {new Date(tx.expectedClosingDate).toLocaleDateString()}</div>
                    <div className="h-1 bg-gray-200 rounded mt-2">
                      <div className="h-1 rounded bg-orange-600" style={{width: `${pct}%`}} />
                    </div>
                  </button>
                </li>
              );
            })}
          </ul>
        </aside>

        <main className="flex-1 overflow-y-auto">
          {!selectedTx ? (
            <div className="p-8 text-gray-500">Select a transaction</div>
          ) : (
            <div className="p-4 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-xl font-semibold">Transaction {selectedTx.id}</div>
                  <div className="text-sm text-gray-500">Expected closing {new Date(selectedTx.expectedClosingDate).toLocaleDateString()}</div>
                </div>
                <div className="w-48">
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span>Progress</span>
                    <span>{progress}%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded">
                    <div className="h-2 rounded bg-orange-600" style={{width: `${progress}%`}} />
                  </div>
                </div>
              </div>

              <section className="bg-white rounded-xl border p-4">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="font-medium">Milestone Timeline</h2>
                  <button className="text-sm text-orange-700 hover:underline">Send update</button>
                </div>
                <TransactionTimeline milestones={selectedTx.milestones} />
              </section>

              <section className="bg-white rounded-xl border p-4">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="font-medium">Documents</h2>
                  <span className="text-sm text-gray-500">{selectedTx.documents?.length || 0} files</span>
                </div>
                <DocumentManager
                  documents={selectedTx.documents}
                  onDocumentsChange={(docs)=>{
                    setSelectedTx({...selectedTx, documents: docs, updatedAt: new Date().toISOString()});
                    setTxs(prev => prev.map(t => t.id===selectedTx.id?{...t, documents: docs, updatedAt: new Date().toISOString()}:t));
                  }}
                />
              </section>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default TransactionsView;
