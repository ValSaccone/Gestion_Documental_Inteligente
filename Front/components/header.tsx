"use client"

import { useState } from "react"
import Link from "next/link"
import { Menu, X, FileText } from "lucide-react"
import { motion } from "framer-motion"
import { useNavigation } from "@/lib/navigation-context"

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const { navigateTo } = useNavigation()

  const navItems = [
    { label: "Cargar Factura", action: "upload" as const },
    { label: "Facturas", action: "invoices" as const },
  ]

  const handleNavigate = (action: "upload" | "invoices") => {
    navigateTo(action)
    setIsOpen(false)
  }

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <motion.div whileHover={{ scale: 1.05 }} className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold text-foreground">Procesar Facturas</span>
            </motion.div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            {navItems?.map((item) => (
              <button
                key={item.label}
                onClick={() => handleNavigate(item.action)}
                className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors cursor-pointer"
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Mobile Menu Button */}
          <motion.button whileHover={{ scale: 1.05 }} className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </motion.button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <motion.nav
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:hidden pb-4 space-y-2"
          >
            {navItems?.map((item) => (
              <button
                key={item.label}
                onClick={() => handleNavigate(item.action)}
                className="block w-full text-left px-4 py-2 text-sm font-medium text-muted-foreground hover:text-primary hover:bg-muted rounded transition-colors cursor-pointer"
              >
                {item.label}
              </button>
            ))}
          </motion.nav>
        )}
      </div>
    </header>
  )
}
