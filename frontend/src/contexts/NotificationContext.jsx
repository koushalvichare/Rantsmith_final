import React, { createContext, useContext, useState } from 'react'

const NotificationContext = createContext()

export const useNotification = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider')
  }
  return context
}

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([])

  const addNotification = (notification) => {
    const id = Date.now().toString()
    const newNotification = {
      id,
      type: 'info',
      duration: 5000,
      ...notification
    }
    
    setNotifications(prev => [...prev, newNotification])
    
    // Auto remove after duration
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id))
  }

  const showSuccess = (message) => {
    addNotification({
      type: 'success',
      title: 'Success',
      message,
      icon: 'fas fa-check-circle'
    })
  }

  const showError = (message) => {
    addNotification({
      type: 'error',
      title: 'Error',
      message,
      icon: 'fas fa-exclamation-circle',
      duration: 7000
    })
  }

  const showInfo = (message) => {
    addNotification({
      type: 'info',
      title: 'Info',
      message,
      icon: 'fas fa-info-circle'
    })
  }

  const showWarning = (message) => {
    addNotification({
      type: 'warning',
      title: 'Warning',
      message,
      icon: 'fas fa-exclamation-triangle'
    })
  }

  const value = {
    notifications,
    addNotification,
    removeNotification,
    showSuccess,
    showError,
    showInfo,
    showWarning
  }

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  )
}
