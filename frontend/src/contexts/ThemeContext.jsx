import React, { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext()

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

export const ThemeProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(true)
  const [accentColor, setAccentColor] = useState('purple')

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    const savedAccent = localStorage.getItem('accentColor')
    
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark')
    }
    
    if (savedAccent) {
      setAccentColor(savedAccent)
    }
  }, [])

  const toggleTheme = () => {
    const newTheme = !isDarkMode
    setIsDarkMode(newTheme)
    localStorage.setItem('theme', newTheme ? 'dark' : 'light')
  }

  const changeAccentColor = (color) => {
    setAccentColor(color)
    localStorage.setItem('accentColor', color)
  }

  const value = {
    isDarkMode,
    accentColor,
    toggleTheme,
    changeAccentColor,
    theme: isDarkMode ? 'dark' : 'light'
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}
