"use client"

import type React from "react"

import { createContext, useContext, useState } from "react"

type PageType = "upload" | "results" | "invoices"

interface NavigationContextType {
  currentPage: PageType
  navigateTo: (page: PageType) => void
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined)

export function NavigationProvider({ children }: { children: React.ReactNode }) {
  const [currentPage, setCurrentPage] = useState<PageType>("upload")

  const navigateTo = (page: PageType) => {
    setCurrentPage(page)
  }

  return <NavigationContext.Provider value={{ currentPage, navigateTo }}>{children}</NavigationContext.Provider>
}

export function useNavigation() {
  const context = useContext(NavigationContext)
  if (!context) {
    throw new Error("useNavigation must be used within NavigationProvider")
  }
  return context
}
