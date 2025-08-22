'use client';

import { useState } from 'react';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Vibecode AI Interview Generator
          </h1>
          <p className="text-lg text-gray-600">
            Generate realistic interview transcripts with AI
          </p>
        </div>
        
        <ChatInterface />
      </div>
    </main>
  );
}