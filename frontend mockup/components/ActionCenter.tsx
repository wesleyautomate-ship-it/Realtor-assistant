import React from 'react';
import ActionButton from './ActionButton';
import { ACTION_ITEMS } from '../constants';

interface ActionCenterProps {
    // FIX: Aligned the 'id' parameter's type with the id types defined in ACTION_ITEMS to resolve the type mismatch.
    onActionClick: (id: 'marketing' | 'analytics' | 'social' | 'strategy' | 'packages' | 'transactions') => void;
}

const ActionCenter: React.FC<ActionCenterProps> = ({ onActionClick }) => {
    return (
        <div>
            <h2 className="text-base font-bold text-gray-900 mb-4">What can Laura do for you?</h2>
            <div className="grid grid-cols-3 gap-x-4 gap-y-6">
                {ACTION_ITEMS.map(item => (
                    <ActionButton key={item.id} item={item} onClick={() => onActionClick(item.id)} />
                ))}
            </div>
        </div>
    );
};

export default ActionCenter;