/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          750: '#1f2937',
          800: '#1e293b',
          900: '#0f172a',
          950: '#030712',
        },
        neon: {
          pink: '#f472b6',
          blue: '#60a5fa',
          purple: '#a855f7',
          cyan: '#22d3ee',
          green: '#34d399',
          yellow: '#fbbf24',
          orange: '#f97316',
          emerald: '#10b981',
          amber: '#f59e0b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'monospace'],
        display: ['Space Grotesk', 'Inter', 'system-ui', 'sans-serif'],
        cyber: ['Orbitron', 'monospace'],
      },
      animation: {
        'gradient-shift': 'gradient-shift 4s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'bounce-slow': 'bounce 3s infinite',
        'bounce-gentle': 'bounce-gentle 2s infinite',
        'shimmer': 'shimmer 1.8s ease-in-out infinite',
        'slideIn': 'slideIn 0.3s ease-out',
        'slideUp': 'slideUp 0.3s ease-out',
        'fadeIn': 'fadeIn 0.3s ease-out',
        'spin-slow': 'rotate 3s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        'gradient-shift': {
          '0%, 100%': {
            'background-position': '0% 50%'
          },
          '50%': {
            'background-position': '100% 50%'
          },
        },
        float: {
          '0%, 100%': { 
            transform: 'translateY(0px) rotate(0deg)' 
          },
          '25%': { 
            transform: 'translateY(-10px) rotate(1deg)' 
          },
          '50%': { 
            transform: 'translateY(-20px) rotate(0deg)' 
          },
          '75%': { 
            transform: 'translateY(-10px) rotate(-1deg)' 
          },
        },
        shimmer: {
          '0%': { 
            'background-position': '-200% 0' 
          },
          '100%': { 
            'background-position': '200% 0' 
          },
        },
        slideIn: {
          'from': { 
            transform: 'translateX(100%)', 
            opacity: '0' 
          },
          'to': { 
            transform: 'translateX(0)', 
            opacity: '1' 
          },
        },
        slideUp: {
          'from': { 
            transform: 'translateY(20px)', 
            opacity: '0' 
          },
          'to': { 
            transform: 'translateY(0)', 
            opacity: '1' 
          },
        },
        fadeIn: {
          'from': { 
            opacity: '0', 
            transform: 'scale(0.95)' 
          },
          'to': { 
            opacity: '1', 
            transform: 'scale(1)' 
          },
        },
        'pulse-glow': {
          '0%, 100%': { 
            'box-shadow': '0 0 20px rgba(99, 102, 241, 0.3)' 
          },
          '50%': { 
            'box-shadow': '0 0 40px rgba(99, 102, 241, 0.6)' 
          },
        },
        'bounce-gentle': {
          '0%, 100%': { 
            transform: 'translateY(0)',
            'animation-timing-function': 'cubic-bezier(0.8, 0, 1, 1)'
          },
          '50%': { 
            transform: 'translateY(-5px)',
            'animation-timing-function': 'cubic-bezier(0, 0, 0.2, 1)'
          },
        },
        rotate: {
          'from': { 
            transform: 'rotate(0deg)' 
          },
          'to': { 
            transform: 'rotate(360deg)' 
          },
        },
        glow: {
          'from': { 
            'box-shadow': '0 0 20px #a855f7, 0 0 30px #a855f7, 0 0 40px #a855f7' 
          },
          'to': { 
            'box-shadow': '0 0 10px #f472b6, 0 0 20px #f472b6, 0 0 30px #f472b6' 
          },
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-cyber': 'linear-gradient(135deg, #6366f1 0%, #ec4899 50%, #06b6d4 100%)',
        'gradient-neon': 'linear-gradient(135deg, #a855f7 0%, #f472b6 50%, #22d3ee 100%)',
        'cyber-grid': 'linear-gradient(rgba(99,102,241,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.1) 1px, transparent 1px)',
        'noise': 'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.02) 1px, transparent 0)',
      },
      backgroundSize: {
        'cyber': '20px 20px',
        'noise': '20px 20px',
      },
      boxShadow: {
        'glass': '0 8px 32px rgba(0, 0, 0, 0.3)',
        'glass-strong': '0 16px 64px rgba(0, 0, 0, 0.4)',
        'neon': '0 0 20px rgba(168, 85, 247, 0.3)',
        'neon-strong': '0 0 40px rgba(168, 85, 247, 0.5)',
        'glow': '0 0 20px rgba(99, 102, 241, 0.3), 0 0 40px rgba(236, 72, 153, 0.2)',
        'glow-strong': '0 0 30px rgba(99, 102, 241, 0.5), 0 0 60px rgba(236, 72, 153, 0.3)',
      },
      backdropBlur: {
        'xs': '2px',
        'sm': '4px',
        'md': '8px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '32px',
        '3xl': '40px',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '112': '28rem',
        '128': '32rem',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '2rem',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
        'out-expo': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'in-out-circ': 'cubic-bezier(0.785, 0.135, 0.15, 0.86)',
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '3.5rem' }],
        '6xl': ['3.75rem', { lineHeight: '4rem' }],
        '7xl': ['4.5rem', { lineHeight: '5rem' }],
        '8xl': ['6rem', { lineHeight: '6.5rem' }],
        '9xl': ['8rem', { lineHeight: '8.5rem' }],
      },
    },
  },
  plugins: [],
}
