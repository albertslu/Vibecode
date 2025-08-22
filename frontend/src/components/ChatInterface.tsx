'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Download, Copy } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'bot' | 'system';
  content: string;
  timestamp: Date;
  interviewData?: any;
}

interface InterviewRequest {
  topic: string;
  difficulty: string;
  duration_minutes: number;
  company_type: string;
  focus_areas: string[];
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: "Hi! I'm your AI interview generator. Tell me what kind of interview you'd like me to create. For example:\n\n• \"Generate a Software Engineering interview for a mid-level candidate\"\n• \"Create a Frontend Engineering interview for a junior developer\"\n• \"Make a Product Management interview for a senior role\"",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const parseUserInput = (input: string): InterviewRequest | null => {
    const lowerInput = input.toLowerCase();
    
    // Extract topic
    let topic = 'Software Engineering';
    if (lowerInput.includes('frontend') || lowerInput.includes('front-end')) {
      topic = 'Frontend Engineering';
    } else if (lowerInput.includes('backend') || lowerInput.includes('back-end')) {
      topic = 'Backend Engineering';
    } else if (lowerInput.includes('product') || lowerInput.includes('pm')) {
      topic = 'Product Management';
    } else if (lowerInput.includes('data science') || lowerInput.includes('data scientist')) {
      topic = 'Data Science';
    } else if (lowerInput.includes('devops')) {
      topic = 'DevOps Engineering';
    } else if (lowerInput.includes('mobile')) {
      topic = 'Mobile Development';
    }

    // Extract difficulty
    let difficulty = 'mid-level';
    if (lowerInput.includes('junior') || lowerInput.includes('entry')) {
      difficulty = 'junior';
    } else if (lowerInput.includes('senior')) {
      difficulty = 'senior';
    } else if (lowerInput.includes('staff') || lowerInput.includes('principal')) {
      difficulty = 'staff';
    }

    // Extract duration (default to 30 minutes)
    let duration = 30;
    const durationMatch = lowerInput.match(/(\d+)\s*(?:minute|min)/);
    if (durationMatch) {
      duration = parseInt(durationMatch[1]);
    }

    // Extract company type
    let companyType = 'startup';
    if (lowerInput.includes('big tech') || lowerInput.includes('faang')) {
      companyType = 'big-tech';
    } else if (lowerInput.includes('enterprise')) {
      companyType = 'enterprise';
    } else if (lowerInput.includes('consulting')) {
      companyType = 'consulting';
    }

    return {
      topic,
      difficulty,
      duration_minutes: duration,
      company_type: companyType,
      focus_areas: ['technical', 'behavioral']
    };
  };

  const generateInterview = async (request: InterviewRequest) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/generate-interview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error('Failed to generate interview');
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error generating interview:', error);
      throw error;
    }
  };

  const checkInterviewStatus = async (interviewId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/interviews/${interviewId}`);
      if (!response.ok) {
        throw new Error('Failed to check interview status');
      }
      return await response.json();
    } catch (error) {
      console.error('Error checking interview status:', error);
      throw error;
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Parse user input
      const request = parseUserInput(input);
      
      if (!request) {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'bot',
          content: "I couldn't understand your request. Please try something like:\n\n• \"Generate a Software Engineering interview for a mid-level candidate\"\n• \"Create a 45-minute Frontend interview for a senior developer\"",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
        setIsLoading(false);
        return;
      }

      // Show processing message
      const processingMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: `🎯 Generating a ${request.difficulty} ${request.topic} interview (${request.duration_minutes} minutes)...\n\nThis may take 10-30 seconds.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, processingMessage]);

      // Generate interview
      const result = await generateInterview(request);
      
      // Poll for completion
      let attempts = 0;
      const maxAttempts = 30; // 30 seconds max
      
      while (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
        const status = await checkInterviewStatus(result.interview_id);
        
        if (status.status === 'completed') {
          const successMessage: Message = {
            id: (Date.now() + 2).toString(),
            type: 'bot',
            content: `✅ Interview generated successfully!\n\n**${status.interview.topic}** - ${status.interview.difficulty} level\n**Duration:** ${status.interview.total_duration_minutes} minutes\n**Participants:** ${status.interview.participants.interviewer.name} & ${status.interview.participants.interviewee.name}\n\nClick "View Transcript" below to see the full interview.`,
            timestamp: new Date(),
            interviewData: status.interview
          };
          setMessages(prev => [...prev, successMessage]);
          break;
        } else if (status.status === 'failed') {
          const errorMessage: Message = {
            id: (Date.now() + 2).toString(),
            type: 'bot',
            content: `❌ Failed to generate interview: ${status.error_message || 'Unknown error'}`,
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
          break;
        }
        
        attempts++;
      }
      
      if (attempts >= maxAttempts) {
        const timeoutMessage: Message = {
          id: (Date.now() + 2).toString(),
          type: 'bot',
          content: "⏱️ Interview generation is taking longer than expected. Please try again.",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, timeoutMessage]);
      }

    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: `❌ Error: ${error instanceof Error ? error.message : 'Something went wrong'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const downloadTranscript = (interview: any) => {
    const transcript = JSON.stringify(interview, null, 2);
    const blob = new Blob([transcript], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `interview-${interview.topic.replace(/\s+/g, '-').toLowerCase()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Chat Messages */}
      <div className="h-96 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex max-w-xs lg:max-w-md xl:max-w-lg ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              <div
                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.type === 'user'
                    ? 'bg-blue-500 ml-2'
                    : message.type === 'system'
                    ? 'bg-yellow-500 mr-2'
                    : 'bg-gray-500 mr-2'
                }`}
              >
                {message.type === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-white" />
                )}
              </div>
              <div
                className={`px-4 py-2 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-blue-500 text-white'
                    : message.type === 'system'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                {message.interviewData && (
                  <div className="mt-3 space-y-2">
                    <button
                      onClick={() => copyToClipboard(JSON.stringify(message.interviewData, null, 2))}
                      className="inline-flex items-center px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 mr-2"
                    >
                      <Copy className="w-3 h-3 mr-1" />
                      Copy JSON
                    </button>
                    <button
                      onClick={() => downloadTranscript(message.interviewData)}
                      className="inline-flex items-center px-3 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600"
                    >
                      <Download className="w-3 h-3 mr-1" />
                      Download
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex flex-row">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-500 mr-2 flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="px-4 py-2 rounded-lg bg-gray-100 text-gray-800">
                <Loader2 className="w-4 h-4 animate-spin" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your interview request... (e.g., 'Generate a Software Engineering interview for a mid-level candidate')"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Try: "Generate a Frontend Engineering interview for a senior developer" or "Create a 20-minute Product Management interview"
        </div>
      </div>
    </div>
  );
}
