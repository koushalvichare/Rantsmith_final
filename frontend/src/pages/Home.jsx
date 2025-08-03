import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../contexts/AuthContext'

const Home = () => {
  const { isAuthenticated } = useAuth()

  const features = [
    {
      icon: 'fas fa-brain',
      title: 'AI Emotion Analysis',
      description: 'Advanced AI analyzes your emotions and provides insights',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: 'fas fa-magic',
      title: 'Creative Transformation',
      description: 'Turn your rants into memes, songs, tweets, and more',
      color: 'from-pink-500 to-pink-600'
    },
    {
      icon: 'fas fa-lightbulb',
      title: 'Action Suggestions',
      description: 'Get personalized recommendations for emotional wellness',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: 'fas fa-robot',
      title: 'AI Companion',
      description: 'Chat with your personalized AI that understands you',
      color: 'from-green-500 to-green-600'
    }
  ]

  const stats = [
    { number: '10K+', label: 'Happy Users' },
    { number: '50K+', label: 'Rants Processed' },
    { number: '100K+', label: 'Content Generated' },
    { number: '24/7', label: 'AI Support' }
  ]

  return (
    <div className="min-h-screen flex flex-col bg-mesh relative overflow-x-hidden">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center overflow-hidden pt-32 pb-24 px-4 sm:px-8 lg:px-16 w-full">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-800/20 to-pink-800/20 z-0" />
        <div className="relative max-w-4xl w-full mx-auto text-center z-10 space-y-6">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-6xl md:text-7xl font-extrabold mb-8 leading-tight gradient-text"
          >
            Transform Your Rants<br />
            <span className="text-white">Into Creative Gold ✨</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-2xl md:text-3xl text-gray-300 mb-10 max-w-2xl mx-auto"
          >
            Your AI-powered emotional companion that turns frustration into creativity. Rant, create, and discover new perspectives with cutting-edge AI.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-6 justify-center items-center"
          >
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="btn-primary btn-large shadow-xl"
              >
                <i className="fas fa-chart-line mr-2"></i>
                Go to Dashboard
              </Link>
            ) : (
              <Link
                to="/auth"
                className="btn-primary btn-large shadow-xl"
              >
                <i className="fas fa-rocket mr-2"></i>
                Start Your Journey
              </Link>
            )}
            <button className="btn-secondary btn-large shadow-lg">
              <i className="fas fa-play mr-2"></i>
              Watch Demo
            </button>
          </motion.div>
        </div>
        {/* Floating Elements */}
        <div className="absolute top-20 left-10 animate-float z-0">
          <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full opacity-20"></div>
        </div>
        <div className="absolute top-40 right-20 animate-float z-0" style={{ animationDelay: '1s' }}>
          <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-20"></div>
        </div>
        <div className="absolute bottom-20 left-1/4 animate-float z-0" style={{ animationDelay: '2s' }}>
          <div className="w-28 h-28 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full opacity-10"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-black/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Why Choose <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">RantSmith AI?</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Experience the future of emotional expression with our cutting-edge AI technology
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                whileHover={{ y: -10, scale: 1.05 }}
                className="bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-4 mx-auto`}>
                  <i className={`${feature.icon} text-white text-2xl`}></i>
                </div>
                <h3 className="text-xl font-bold text-white mb-3 text-center">{feature.title}</h3>
                <p className="text-gray-300 text-center">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.5 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-300 text-lg">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-900/50 to-pink-900/50">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Emotions?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of users who are already turning their rants into creative masterpieces
            </p>
            {!isAuthenticated && (
              <Link
                to="/auth"
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-4 px-8 rounded-full text-lg transition-all duration-300 transform hover:scale-105 shadow-lg inline-block"
              >
                <i className="fas fa-user-plus mr-2"></i>
                Sign Up Now - It's Free!
              </Link>
            )}
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home
