import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import DiagnosticPanel from '../components/DiagnosticPanel';
import { motion } from 'framer-motion';

const TestPage = () => {
  const { user } = useAuth();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 py-8"
    >
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">🔧 System Test Page</h1>
            <p className="text-gray-300">Comprehensive testing for all RantAi features</p>
          </div>

          <DiagnosticPanel />

          <div className="mt-8 text-center">
            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-lg p-6">
              <h2 className="text-xl font-bold text-white mb-4">Current Status</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-blue-900/20 border border-blue-500/50 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-400">Authentication</h3>
                  <p className="text-sm text-blue-300">
                    {user ? `Logged in as ${user.email}` : 'Not logged in'}
                  </p>
                </div>
                <div className="bg-green-900/20 border border-green-500/50 rounded-lg p-4">
                  <h3 className="font-semibold text-green-400">Backend</h3>
                  <p className="text-sm text-green-300">Running on port 5000</p>
                </div>
                <div className="bg-purple-900/20 border border-purple-500/50 rounded-lg p-4">
                  <h3 className="font-semibold text-purple-400">Frontend</h3>
                  <p className="text-sm text-purple-300">Running on port 3004</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default TestPage;
