"use client"

import { motion } from "framer-motion"
import { Search, Filter } from "lucide-react"

interface FiltersBarProps {
  searchTerm: string
  onSearchChange: (value: string) => void
  dateFilter: string
  onDateChange: (value: string) => void
  providerFilter: string
  onProviderChange: (value: string) => void
}

export default function FiltersBar({ searchTerm, onSearchChange, dateFilter, onDateChange, providerFilter, onProviderChange }: FiltersBarProps) {
  return (
    <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="rounded-lg border border-border bg-white p-4 space-y-4 shadow-sm">
      <div className="flex items-center gap-2 text-foreground font-medium">
        <Filter className="h-5 w-5" />
        <span>Filtros</span>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Número de factura</label>
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
            <input type="text" placeholder="Número de Factura..." value={searchTerm} onChange={(e) => onSearchChange(e.target.value)} className="w-full rounded-lg border border-border bg-background pl-10 pr-4 py-2 text-sm placeholder-muted-foreground" />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Fecha</label>
          <input type="date" value={dateFilter} onChange={(e) => onDateChange(e.target.value)} className="w-full rounded-lg border border-border bg-background px-4 py-2 text-sm" />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Proveedor</label>
          <input type="text" placeholder="Proveedor..." value={providerFilter} onChange={(e) => onProviderChange(e.target.value)} className="w-full rounded-lg border border-border bg-background px-4 py-2 text-sm placeholder-muted-foreground" />
        </div>
      </div>
    </motion.div>
  )
}
