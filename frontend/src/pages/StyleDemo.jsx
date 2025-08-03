import React, { useState } from 'react';

const StyleDemo = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  const showNotification = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleLoading = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div className="min-h-screen flex flex-col bg-mesh relative overflow-x-hidden items-center justify-center">
      {/* Particle Background */}
      <div className="particle-bg absolute inset-0 z-0 pointer-events-none" />
      {/* Header */}
      <header className="glass-strong border-b border-white/10 py-16 px-4 sm:px-12 lg:px-24 mb-20 flex flex-col items-center justify-center w-full min-h-[320px]">
        <div className="w-full flex flex-col items-center justify-center">
          <h1 className="text-6xl sm:text-7xl lg:text-8xl font-extrabold gradient-text mb-6 leading-tight text-center">RantSmith AI Style Demo</h1>
          <p className="text-gray-300 text-2xl sm:text-3xl lg:text-4xl max-w-3xl mx-auto text-center mb-8">Showcasing enhanced CSS components, effects, and responsive design system</p>
          <div className="mt-8 flex flex-wrap justify-center items-center gap-8 w-full max-w-xl mx-auto">
            <div className="flex items-center space-x-2 text-lg text-gray-400">
              <div className="status-dot online"></div>
              <span>Live Demo Active</span>
            </div>
            <div className="flex items-center space-x-2 text-lg text-gray-400">
              <i className="fas fa-mobile-alt"></i>
              <span>Fully Responsive</span>
            </div>
            <div className="flex items-center space-x-2 text-lg text-gray-400">
              <i className="fas fa-palette"></i>
              <span>Modern Design</span>
            </div>
          </div>
        </div>
      </header>
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-8 lg:px-16 py-12 space-y-24 flex flex-col items-center justify-center">
        {/* Notification */}
        {notification && (
          <div className={`notification ${notification.type} fixed top-24 right-8 z-50 max-w-sm`}> {/* moved down for less overlap */}
            <div className="flex items-center space-x-3">
              <div className={`status-dot ${notification.type === 'success' ? 'online' : notification.type === 'error' ? 'offline' : 'busy'}`}></div>
              <p className="text-white font-medium">{notification.message}</p>
            </div>
          </div>
        )}

        {/* Typography Section */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Typography & Text Effects</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-white mb-3">Gradient Text</h3>
                <p className="gradient-text text-4xl lg:text-5xl font-bold">Amazing Gradient</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-3">Cyber Text</h3>
                <p className="text-cyber text-2xl lg:text-3xl neon-text">CYBER STYLE</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-3">Display Text</h3>
                <p className="text-display text-3xl lg:text-4xl font-bold text-white">Modern Display</p>
              </div>
            </div>
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-white mb-3">Glitch Effect</h3>
                <p className="glitch text-2xl lg:text-3xl font-bold" data-text="GLITCH EFFECT">GLITCH EFFECT</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-3">Monospace Text</h3>
                <p className="text-mono text-lg lg:text-xl text-gray-300">const code = 'amazing';</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-3">Neon Glow</h3>
                <p className="neon-text text-2xl lg:text-3xl font-bold">NEON GLOW</p>
              </div>
            </div>
          </div>
        </section>

        {/* Button Section */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Button Styles & Sizes</h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Standard Buttons</h3>
              <div className="flex flex-wrap gap-4">
                <button 
                  className="btn-primary"
                  onClick={() => showNotification('success', 'Primary button clicked!')}
                >
                  Primary Button
                </button>
                <button 
                  className="btn-secondary"
                  onClick={() => showNotification('info', 'Secondary button clicked!')}
                >
                  Secondary Button
                </button>
                <button 
                  className="btn-ghost"
                  onClick={() => showNotification('warning', 'Ghost button clicked!')}
                >
                  Ghost Button
                </button>
                <button 
                  className="btn-neon"
                  onClick={() => showNotification('error', 'Neon button clicked!')}
                >
                  Neon Button
                </button>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Button Sizes</h3>
              <div className="flex flex-wrap items-center gap-4">
                <button className="btn-primary btn-small">Small</button>
                <button className="btn-secondary">Default</button>
                <button className="btn-ghost btn-large">Large</button>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Full Width & States</h3>
              <div className="space-y-4">
                <button className="btn-primary btn-full">Full Width Primary</button>
                <div className="flex gap-4">
                  <button 
                    className="btn-primary animate-pulse-glow"
                    onClick={handleLoading}
                  >
                    {isLoading ? 'Loading...' : 'Animated Button'}
                  </button>
                  <button className="btn-secondary" disabled>
                    Disabled Button
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Input Section */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Input Components & Sizes</h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Input Sizes</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-white font-medium mb-2">Small Input</label>
                  <input
                    type="text"
                    className="input-small max-w-sm"
                    placeholder="Small input field..."
                  />
                </div>
                <div>
                  <label className="block text-white font-medium mb-2">Standard Input</label>
                  <input
                    type="text"
                    className="input max-w-md"
                    placeholder="Standard input field..."
                  />
                </div>
                <div>
                  <label className="block text-white font-medium mb-2">Large Input</label>
                  <input
                    type="email"
                    className="input-large max-w-lg"
                    placeholder="Large input field..."
                  />
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Textarea Sizes</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label className="block text-white font-medium mb-2">Small Textarea</label>
                  <textarea
                    className="textarea-small w-full"
                    placeholder="Small textarea for brief messages..."
                  />
                </div>
                <div>
                  <label className="block text-white font-medium mb-2">Standard Textarea</label>
                  <textarea
                    className="textarea w-full"
                    placeholder="Standard textarea for longer content..."
                  />
                </div>
              </div>
              <div className="mt-6">
                <label className="block text-white font-medium mb-2">Large Textarea</label>
                <textarea
                  className="textarea-large w-full"
                  placeholder="Large textarea for detailed content and longer messages..."
                />
              </div>
            </div>
          </div>
        </section>

        {/* Card Section */}
        <section className="space-y-8">
          <h2 className="text-3xl font-bold gradient-text-alt">Card Styles & Sizes</h2>
          
          <div>
            <h3 className="text-xl font-semibold text-white mb-4">Card Sizes</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="card-small">
                <h4 className="text-lg font-semibold text-white mb-2">Small Card</h4>
                <p className="text-gray-300 text-sm">Compact card for brief content and minimal information.</p>
              </div>
              <div className="card">
                <h4 className="text-lg font-semibold text-white mb-2">Standard Card</h4>
                <p className="text-gray-300">Standard card with balanced proportions for regular content.</p>
              </div>
              <div className="card-large">
                <h4 className="text-lg font-semibold text-white mb-2">Large Card</h4>
                <p className="text-gray-300">Large card with generous spacing for detailed content and enhanced visual impact.</p>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold text-white mb-4">Interactive Cards</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card-interactive">
                <h4 className="text-lg font-semibold text-white mb-2">Interactive Card</h4>
                <p className="text-gray-300">This card has enhanced hover effects with scale and lift animations.</p>
              </div>
              <div className="card-neon">
                <h4 className="text-lg font-semibold text-white mb-2">Neon Card</h4>
                <p className="text-gray-300">This card features a glowing neon border effect.</p>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold text-white mb-4">Compact Cards</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="card-compact">
                <h4 className="text-base font-semibold text-white mb-1">Compact 1</h4>
                <p className="text-gray-300 text-sm">Minimal card design</p>
              </div>
              <div className="card-compact">
                <h4 className="text-base font-semibold text-white mb-1">Compact 2</h4>
                <p className="text-gray-300 text-sm">Space-efficient layout</p>
              </div>
              <div className="card-compact">
                <h4 className="text-base font-semibold text-white mb-1">Compact 3</h4>
                <p className="text-gray-300 text-sm">Perfect for dashboards</p>
              </div>
              <div className="card-compact">
                <h4 className="text-base font-semibold text-white mb-1">Compact 4</h4>
                <p className="text-gray-300 text-sm">Clean and focused</p>
              </div>
            </div>
          </div>
        </section>

        {/* Loading Section */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Loading Animations & Sizes</h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Loading Dots</h3>
              <div className="flex flex-wrap items-center gap-8">
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Small</p>
                  <div className="loading-dots-small">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Standard</p>
                  <div className="loading-dots">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Large</p>
                  <div className="loading-dots-large">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Loading Spinners</h3>
              <div className="flex flex-wrap items-center gap-8">
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Small</p>
                  <div className="loading-spinner-small"></div>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Standard</p>
                  <div className="loading-spinner"></div>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Large</p>
                  <div className="loading-spinner-large"></div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Loading Waves</h3>
              <div className="flex flex-wrap items-center gap-8">
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Small</p>
                  <div className="loading-wave-small">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Standard</p>
                  <div className="loading-wave">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium mb-3">Large</p>
                  <div className="loading-wave-large">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Skeleton Loading */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Skeleton Loading States</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Content Skeletons</h3>
              <div className="space-y-4">
                <div className="loading-skeleton h-8 w-3/4"></div>
                <div className="loading-skeleton h-6 w-full"></div>
                <div className="loading-skeleton h-6 w-5/6"></div>
                <div className="loading-skeleton h-4 w-1/2"></div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Card Skeleton</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="card">
                  <div className="loading-skeleton h-6 w-3/4 mb-4"></div>
                  <div className="loading-skeleton h-4 w-full mb-2"></div>
                  <div className="loading-skeleton h-4 w-5/6 mb-2"></div>
                  <div className="loading-skeleton h-4 w-2/3"></div>
                </div>
                <div className="card">
                  <div className="loading-skeleton h-8 w-1/2 mb-4"></div>
                  <div className="loading-skeleton h-16 w-full mb-4"></div>
                  <div className="loading-skeleton h-4 w-1/3"></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Effects Section */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Special Effects & Borders</h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Cyber & Neon Effects</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="cyber-border p-8 rounded-xl">
                  <h4 className="text-xl font-semibold text-white mb-3">Cyber Border</h4>
                  <p className="text-gray-300">This element features an animated cyber border effect with gradient colors.</p>
                </div>
                <div className="glass-strong p-8 rounded-xl neon-glow">
                  <h4 className="text-xl font-semibold text-white mb-3">Neon Glow</h4>
                  <p className="text-gray-300">This element has a beautiful neon glow shadow effect.</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Glass Effects</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="glass p-6 rounded-xl">
                  <h4 className="text-lg font-semibold text-white mb-2">Glass</h4>
                  <p className="text-gray-300 text-sm">Standard glass morphism with subtle transparency.</p>
                </div>
                <div className="glass-strong p-6 rounded-xl">
                  <h4 className="text-lg font-semibold text-white mb-2">Glass Strong</h4>
                  <p className="text-gray-300 text-sm">Enhanced glass effect with stronger blur.</p>
                </div>
                <div className="glass backdrop-blur-glass p-6 rounded-xl">
                  <h4 className="text-lg font-semibold text-white mb-2">Glass Blur</h4>
                  <p className="text-gray-300 text-sm">Maximum blur effect for premium feel.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Interactive Elements */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Interactive Elements</h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Hover Effects</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="interactive-lift glass p-6 rounded-xl">
                  <h4 className="text-lg font-semibold text-white mb-2">Lift Effect</h4>
                  <p className="text-gray-300">Hover to see smooth lift animation with shadow.</p>
                </div>
                <div className="interactive glass p-6 rounded-xl">
                  <h4 className="text-lg font-semibold text-white mb-2">Scale Effect</h4>
                  <p className="text-gray-300">Hover to see subtle scale transformation.</p>
                </div>
                <div className="glass p-6 rounded-xl cursor-pointer hover:bg-white/10 transition-all duration-300">
                  <h4 className="text-lg font-semibold text-white mb-2">Custom Hover</h4>
                  <p className="text-gray-300">Custom hover effect with background change.</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Status Indicators</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass p-6 rounded-xl">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="status-dot online"></div>
                    <h4 className="text-lg font-semibold text-white">Online Status</h4>
                  </div>
                  <p className="text-gray-300">Active and connected status indicator.</p>
                </div>
                <div className="glass p-6 rounded-xl">
                  <div className="flex flex-wrap items-center gap-4 mb-4">
                    <div className="flex items-center space-x-2">
                      <div className="status-dot online"></div>
                      <span className="text-sm text-white">Online</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="status-dot busy"></div>
                      <span className="text-sm text-white">Busy</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="status-dot away"></div>
                      <span className="text-sm text-white">Away</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="status-dot offline"></div>
                      <span className="text-sm text-white">Offline</span>
                    </div>
                  </div>
                  <p className="text-gray-300">Various status indicators with animations.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Navigation Demo */}
        <section className="card-large">
          <h2 className="text-3xl font-bold gradient-text-alt mb-8">Navigation & Links</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Navigation Links</h3>
              <nav className="flex flex-wrap gap-8">
                <a href="#" className="nav-link text-lg">Home</a>
                <a href="#" className="nav-link active text-lg">Demo</a>
                <a href="#" className="nav-link text-lg">Features</a>
                <a href="#" className="nav-link text-lg">About</a>
                <a href="#" className="nav-link text-lg">Contact</a>
              </nav>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Link Variations</h3>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-4">
                  <a href="#" className="text-white hover:text-purple-400 transition-colors duration-200">Standard Link</a>
                  <a href="#" className="text-purple-400 hover:text-purple-300 transition-colors duration-200">Colored Link</a>
                  <a href="#" className="text-white hover:text-white/70 underline transition-colors duration-200">Underlined Link</a>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default StyleDemo;
