import React, { useState, useEffect, useRef } from 'react';
import { voiceService, VoiceProcessingResponse } from '../services/voiceService';
import { userService } from '../services/userService';
import { audioService, AudioRecordingResult } from '../services/audioService';

interface CommandCenterProps {
    onClose: () => void;
}

const CommandCenter: React.FC<CommandCenterProps> = ({ onClose }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [elapsedTime, setElapsedTime] = useState(0);
    const [isProcessing, setIsProcessing] = useState(false);
    const [processingStatus, setProcessingStatus] = useState<string>('');
    const [voiceResponse, setVoiceResponse] = useState<VoiceProcessingResponse | null>(null);
    const [hasPermission, setHasPermission] = useState<boolean | null>(null);
    const [error, setError] = useState<string>('');
    
    // User service is automatically initialized

    // Timer effect
    useEffect(() => {
        let interval: NodeJS.Timeout | null = null;
        if (isRecording) {
            interval = setInterval(() => {
                setElapsedTime(time => time + 1);
            }, 1000);
        } else if (interval) {
            clearInterval(interval);
        }
        return () => {
            if (interval) clearInterval(interval);
        };
    }, [isRecording]);

    // Format time as MM:SS
    const formatTime = (time: number) => {
        const minutes = Math.floor(time / 60).toString().padStart(2, '0');
        const seconds = (time % 60).toString().padStart(2, '0');
        return `${minutes}:${seconds}`;
    };

    // Simulate waveform data for visual effect. Let's make it dynamic based on recording state.
    const waveformHeights = Array.from({ length: 50 }, () => 
        isRecording ? Math.floor(Math.random() * 60) + 4 : 4
    );

    // Check microphone permission on component mount
    useEffect(() => {
        const checkPermission = async () => {
            try {
                const hasPermission = await audioService.requestMicrophonePermission();
                setHasPermission(hasPermission);
                if (!hasPermission) {
                    setError('Microphone permission is required for voice commands');
                }
            } catch (error) {
                console.error('Error checking microphone permission:', error);
                setHasPermission(false);
                setError('Could not access microphone');
            }
        };
        
        checkPermission();
    }, []);

    // Start recording
    const startRecording = async () => {
        try {
            setError('');
            
            if (!audioService.isMediaRecorderSupported()) {
                throw new Error('Voice recording is not supported in this browser');
            }

            if (!audioService.isGetUserMediaSupported()) {
                throw new Error('Microphone access is not supported in this browser');
            }

            await audioService.startRecording({
                audioBitsPerSecond: 128000,
                mimeType: 'audio/webm;codecs=opus'
            });
            
            setIsRecording(true);
            setElapsedTime(0);
        } catch (error) {
            console.error('Error starting recording:', error);
            setError(`Error: ${error instanceof Error ? error.message : 'Could not start recording'}`);
            setProcessingStatus('Error: Could not start recording');
        }
    };

    // Stop recording
    const stopRecording = async () => {
        try {
            if (isRecording) {
                const result: AudioRecordingResult = await audioService.stopRecording();
                setIsRecording(false);
                await processVoiceRequest(result.audioBlob);
            }
        } catch (error) {
            console.error('Error stopping recording:', error);
            setError(`Error: ${error instanceof Error ? error.message : 'Could not stop recording'}`);
            setIsRecording(false);
        }
    };

    // Process voice request
    const processVoiceRequest = async (audioBlob: Blob) => {
        try {
            setIsProcessing(true);
            setProcessingStatus('Processing voice request...');
            
            // Get user and session info
            const userId = userService.getUserId();
            const sessionId = userService.getSessionId();
            
            // Convert blob to file
            const audioFile = audioService.audioBlobToFile(audioBlob, 'voice-command.webm');
            
            const response = await voiceService.processVoiceRequest(
                audioFile,
                userId,
                sessionId
            );
            
            setVoiceResponse(response);
            
            if (response.processing_type === 'realtime') {
                setProcessingStatus('Completed!');
                setTimeout(() => {
                    onClose();
                }, 2000);
            } else {
                setProcessingStatus(`Queued for batch processing. ETA: ${response.eta}`);
                // Poll for status updates
                pollRequestStatus(response.request_id);
            }
            
        } catch (error) {
            console.error('Error processing voice request:', error);
            setProcessingStatus('Error processing voice request');
        } finally {
            setIsProcessing(false);
        }
    };

    // Poll for request status
    const pollRequestStatus = async (requestId: string) => {
        try {
            const status = await voiceService.getVoiceRequestStatus(requestId);
            
            if (status.status === 'completed') {
                setProcessingStatus('Completed!');
                setVoiceResponse({
                    request_id: status.request_id,
                    transcript: status.transcript,
                    intent: status.intent,
                    entities: {},
                    processing_type: status.processing_type,
                    status: status.status,
                    response: status.result_data
                });
                setTimeout(() => {
                    onClose();
                }, 2000);
            } else if (status.status === 'failed') {
                setProcessingStatus('Processing failed');
            } else {
                // Continue polling
                setTimeout(() => pollRequestStatus(requestId), 3000);
            }
        } catch (error) {
            console.error('Error polling request status:', error);
            setProcessingStatus('Error checking status');
        }
    };

    const handleSend = () => {
        if (elapsedTime > 0) {
            stopRecording();
        }
    };

    const handleRestart = () => {
        setElapsedTime(0);
        setIsRecording(false);
        setIsProcessing(false);
        setProcessingStatus('');
        setVoiceResponse(null);
        startRecording();
    };

    return (
        <div 
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-end justify-center"
            onClick={onClose}
            aria-modal="true"
            role="dialog"
        >
            <div 
                className="w-full bg-white rounded-t-[28px] md:max-w-4xl md:rounded-[28px] md:mb-4 shadow-2xl animate-slide-up-fast"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="p-6 md:p-8 flex flex-col items-center">
                    {/* Header */}
                    <div className="w-full flex justify-between items-center mb-6">
                        <h2 className="text-lg font-bold text-gray-900">I'm listening...</h2>
                        <button onClick={onClose} className="p-2 rounded-full hover:bg-gray-100 text-gray-500" aria-label="Close command center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Timer and Waveform */}
                    <div className="w-full flex flex-col items-center mb-6">
                        <p className="text-5xl font-light text-gray-800 tracking-wider mb-6">{formatTime(elapsedTime)}</p>
                        <div className="w-full h-16 flex items-center justify-center space-x-1">
                            {waveformHeights.map((height, index) => (
                                <div 
                                    key={index}
                                    className="w-1 rounded-full bg-blue-500 transition-all duration-300"
                                    style={{ height: `${height}px` }}
                                ></div>
                            ))}
                        </div>
                    </div>

                    {/* Processing Status */}
                    {isProcessing && (
                        <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                            <p className="text-sm text-blue-700 text-center">{processingStatus}</p>
                        </div>
                    )}

                    {/* Voice Response */}
                    {voiceResponse && (
                        <div className="mb-4 p-3 bg-green-50 rounded-lg">
                            <p className="text-sm text-green-700 text-center">
                                Intent: {voiceResponse.intent} | Type: {voiceResponse.processing_type}
                            </p>
                        </div>
                    )}

                    {/* Controls */}
                    <div className="flex items-center justify-center w-full max-w-xs mb-8">
                        <button 
                            onClick={handleRestart} 
                            disabled={isRecording || isProcessing}
                            className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            Restart
                        </button>
                        
                        <div className="mx-6">
                            {!isRecording && !isProcessing ? (
                                <button 
                                    onClick={startRecording}
                                    className="w-20 h-20 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-lg shadow-blue-500/50 hover:bg-blue-700 transition-all transform hover:scale-105"
                                    aria-label="Start recording"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93V17a1 1 0 102 0v-2.07A5.986 5.986 0 0113 11v-1a1 1 0 10-2 0v1a3.987 3.987 0 00-1.03.177A1 1 0 008 11v1a5.986 5.986 0 013 3.93z" clipRule="evenodd" />
                                    </svg>
                                </button>
                            ) : isRecording ? (
                                <button 
                                    onClick={stopRecording}
                                    className="w-20 h-20 rounded-full bg-red-500 text-white flex items-center justify-center shadow-lg shadow-red-500/50 hover:bg-red-600 transition-all transform hover:scale-105"
                                    aria-label="Stop recording"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1zm4 0a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                                    </svg>
                                </button>
                            ) : (
                                <div className="w-20 h-20 rounded-full bg-gray-400 text-white flex items-center justify-center">
                                    <svg className="animate-spin h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                </div>
                            )}
                        </div>
                        
                        <button 
                            onClick={handleSend}
                            disabled={elapsedTime === 0 || isProcessing}
                            className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
                        >
                            Send
                        </button>
                    </div>

                    {/* Error Display */}
                    {error && (
                        <div className="mb-4 p-3 bg-red-50 rounded-lg">
                            <p className="text-sm text-red-700 text-center">{error}</p>
                        </div>
                    )}

                    {/* Permission Status */}
                    {hasPermission === false && (
                        <div className="mb-4 p-3 bg-yellow-50 rounded-lg">
                            <p className="text-sm text-yellow-700 text-center">
                                Microphone permission required. Please allow microphone access to use voice commands.
                            </p>
                        </div>
                    )}

                    {/* Instructions */}
                    <div className="text-center text-sm text-gray-600">
                        {hasPermission === null ? (
                            <p>Checking microphone permissions...</p>
                        ) : hasPermission ? (
                            <>
                                <p>Tap the microphone to start recording your request</p>
                                <p className="mt-1">PropertyPro AI will help you with properties, clients, and more</p>
                            </>
                        ) : (
                            <p>Please allow microphone access to use voice commands</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CommandCenter;