import React from 'react';
import { View } from '../types';

interface BottomNavProps {
    activeView: View;
    onNavigate: (view: View) => void;
    onOpenCommandCenter: () => void;
}

const NavItem: React.FC<{
    isActive: boolean;
    onClick: () => void;
    label: string;
    children: React.ReactNode;
}> = ({ isActive, onClick, label, children }) => (
    <button onClick={onClick} className={`flex flex-col items-center justify-center w-16 transition-colors ${isActive ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'}`}>
        {children}
        <span className="text-xs font-medium mt-1">{label}</span>
    </button>
);

const BottomNav: React.FC<BottomNavProps> = ({ activeView, onNavigate, onOpenCommandCenter }) => {
    return (
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-white/80 backdrop-blur-lg border-t border-gray-200">
            <div className="flex items-center justify-around h-full px-4">
                <NavItem isActive={activeView === 'dashboard'} onClick={() => onNavigate('dashboard')} label="Home">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
                </NavItem>
                <NavItem isActive={activeView === 'tasks'} onClick={() => onNavigate('tasks')} label="Tasks">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </NavItem>

                <div className="w-16 h-16">
                    <button 
                        onClick={onOpenCommandCenter}
                        className="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center -translate-y-6 shadow-lg shadow-blue-500/50 hover:bg-blue-700 transition"
                        aria-label="Open Command Center"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                        </svg>
                    </button>
                </div>

                <NavItem isActive={activeView === 'chat'} onClick={() => onNavigate('chat')} label="Chat">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
                </NavItem>
                <NavItem isActive={activeView === 'profile'} onClick={() => onNavigate('profile')} label="Profile">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                </NavItem>
            </div>
        </div>
    );
};

export default BottomNav;
