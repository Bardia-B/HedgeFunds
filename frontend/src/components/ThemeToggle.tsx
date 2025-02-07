import { Moon, Sun } from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      className="w-8 h-8 rounded-full border border-border flex items-center justify-center bg-background hover:bg-muted transition-colors"
    >
      {theme === 'dark' ? (
        <Sun className="h-4 w-4 text-foreground hover:text-yellow-400 transition-colors" />
      ) : (
        <Moon className="h-4 w-4 text-foreground hover:text-blue-400 transition-colors" />
      )}
    </button>
  )
} 