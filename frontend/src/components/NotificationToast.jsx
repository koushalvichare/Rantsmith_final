import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNotification } from '../contexts/NotificationContext'

const NotificationToast = () => {
  const { notifications, removeNotification } = useNotification()

  const getNotificationStyles = (type) => {
    const styles = {
      success: 'bg-green-500 border-green-400',
      error: 'bg-red-500 border-red-400',
      warning: 'bg-yellow-500 border-yellow-400',
      info: 'bg-blue-500 border-blue-400'
    }
    return styles[type] || styles.info
  }

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ opacity: 0, x: 300, scale: 0.3 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 300, scale: 0.3 }}
            className={`${getNotificationStyles(notification.type)} text-white p-4 rounded-lg shadow-lg border-l-4 max-w-sm`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <i className={notification.icon}></i>
                <div>
                  <h4 className="font-semibold text-sm">{notification.title}</h4>
                  <p className="text-xs opacity-90">{notification.message}</p>
                </div>
              </div>
              <button
                onClick={() => removeNotification(notification.id)}
                className="text-white hover:text-gray-200 ml-2"
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}

export default NotificationToast
