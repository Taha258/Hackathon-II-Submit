"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "./theme-provider"
import { motion } from "framer-motion"

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      onClick={toggleTheme}
      className="relative p-3 rounded-full glass hover:bg-white/10 transition-all duration-300"
      aria-label="Toggle theme"
    >
      {theme === "light" ? (
        <motion.div
          initial={{ rotate: 0, scale: 0 }}
          animate={{ rotate: 0, scale: 1 }}
          exit={{ rotate: 180, scale: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Sun className="h-5 w-5 text-yellow-400" />
        </motion.div>
      ) : (
        <motion.div
          initial={{ rotate: -180, scale: 0 }}
          animate={{ rotate: 0, scale: 1 }}
          exit={{ rotate: 180, scale: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Moon className="h-5 w-5 text-blue-400" />
        </motion.div>
      )}
    </motion.button>
  )
}