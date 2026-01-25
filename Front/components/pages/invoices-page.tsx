"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import FiltersBar from "@/components/filters-bar"
import InvoiceTable from "@/components/invoice-table"
import ExportButtons from "@/components/export-buttons"
import {getInvoices} from "@/api/facturas"
import {TablaItem} from "@/api/facturas"

interface Invoice {
  id: number
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}


interface InvoicesPageProps {
  onNavigate: (page: "upload" | "results" | "invoices") => void
}

export default function InvoicesPage({ onNavigate }: InvoicesPageProps) {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [filteredInvoices, setFilteredInvoices] = useState<Invoice[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [dateFilter, setDateFilter] = useState("")
  const [providerFilter, setProviderFilter] = useState("")

  useEffect(() => {
    loadInvoices()
  }, [])

  useEffect(() => {
    filterInvoices()
  }, [invoices, searchTerm, dateFilter, providerFilter])

  const loadInvoices = async () => {
    setIsLoading(true)
    try {
      const data = await getInvoices()
      setInvoices(data)
    } catch (err) {
      console.error("Failed to load invoices:", err)
      setInvoices([])
    } finally {
      setIsLoading(false)
    }
  }

  const filterInvoices = () => {
    let filtered = invoices

    if (searchTerm) {
      filtered = filtered.filter(
        (inv) =>
          inv.numero_factura.toLowerCase().includes(searchTerm.toLowerCase()) ||
          inv.razon_social.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (dateFilter) {
      filtered = filtered.filter((inv) => inv.fecha.startsWith(dateFilter))
    }

    if (providerFilter) {
      filtered = filtered.filter((inv) =>
        inv.razon_social.toLowerCase().includes(providerFilter.toLowerCase())
      )
    }

    setFilteredInvoices(filtered)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 px-4 py-12">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
        >
          <div>
            <h1 className="text-3xl font-bold text-foreground">Facturas Registradas</h1>
            <p className="text-muted-foreground">Gestione y exporte sus facturas digitalizadas.</p>
          </div>
          <Button onClick={() => onNavigate("upload")} className="bg-primary hover:bg-primary/90 gap-2">
            <Plus className="h-4 w-4" />
            Cargar Facturas
          </Button>
        </motion.div>

        {/* Filtros */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-6"
        >
          <FiltersBar
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            dateFilter={dateFilter}
            onDateChange={setDateFilter}
            providerFilter={providerFilter}
            onProviderChange={setProviderFilter}
          />
        </motion.div>

        {/* Export Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.15 }}
          className="mb-6"
        >
          <ExportButtons invoices={filteredInvoices} />
        </motion.div>

        {/* Table */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <InvoiceTable invoices={filteredInvoices} isLoading={isLoading} />
        </motion.div>
      </div>
    </div>
  )
}
