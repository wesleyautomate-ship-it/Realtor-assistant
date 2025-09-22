import React, { useState } from 'react';
import BottomNav from './components/BottomNav';
import CommandCenter from './components/CommandCenter';
import DashboardView from './components/DashboardView';
import TasksView from './components/TasksView';
import ChatView from './components/ChatView';
import ProfileView from './components/ProfileView';
import FeatureView from './components/FeatureView';
import MarketingView from './components/MarketingView';
import SocialMediaView from './components/SocialMediaView';
import ContactManagementView from './components/ContactManagementView';
import PlaywrightTestView from './components/PlaywrightTestView';
import { View, ActionId, Task } from './types';
import { ACTION_ITEMS, MOCK_TASKS } from './constants';

const App: React.FC = () => {
    const [currentView, setCurrentView] = useState<View>('dashboard');
    const [isCommandCenterOpen, setCommandCenterOpen] = useState(false);
    const [selectedAction, setSelectedAction] = useState<ActionId | null>(null);
    const [tasks, setTasks] = useState<Task[]>(MOCK_TASKS);

    const handleActionClick = (id: ActionId) => {
        setSelectedAction(id);
    };

    const handleBackFromFeature = () => {
        setSelectedAction(null);
    };

    const renderView = () => {
        switch (currentView) {
            case 'dashboard':
                return <DashboardView onActionClick={handleActionClick} onRequestClick={() => {}} />;
            case 'tasks':
                return <TasksView tasks={tasks} setTasks={setTasks} />;
            case 'chat':
                return <ChatView />;
            case 'profile':
                return <ProfileView />;
            default:
                return <DashboardView onActionClick={handleActionClick} onRequestClick={() => {}} />;
        }
    };

    const selectedActionData = selectedAction ? ACTION_ITEMS.find(item => item.id === selectedAction) : null;

    const renderFeatureView = () => {
        if (!selectedAction) return null;

        switch (selectedAction) {
            case 'marketing':
                return <MarketingView onBack={handleBackFromFeature} />;
            case 'social':
                return <SocialMediaView onBack={handleBackFromFeature} />;
            case 'contacts':
                return <ContactManagementView onBack={handleBackFromFeature} />;
            case 'playwright':
                return <PlaywrightTestView onBack={handleBackFromFeature} />;
            default:
                if (selectedActionData) {
                    return <FeatureView title={selectedActionData.title} onBack={handleBackFromFeature} />;
                }
                return null;
        }
    };

    return (
        <div className="min-h-screen font-sans md:flex md:items-center md:justify-center md:p-4">
            <div className="w-full h-screen bg-white flex flex-col relative md:max-w-4xl md:h-[calc(100vh-2rem)] md:rounded-[48px] md:shadow-2xl overflow-hidden">
                {selectedAction ? (
                    renderFeatureView()
                ) : (
                    <>
                        <div className="flex-grow overflow-hidden">
                            {renderView()}
                        </div>
                        <BottomNav 
                            activeView={currentView} 
                            onNavigate={setCurrentView}
                            onOpenCommandCenter={() => setCommandCenterOpen(true)} 
                        />
                        {isCommandCenterOpen && <CommandCenter onClose={() => setCommandCenterOpen(false)} />}
                    </>
                )}
            </div>
        </div>
    );
};

export default App;