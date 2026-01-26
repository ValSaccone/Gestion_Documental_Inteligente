"use client"

import { motion } from "framer-motion"
import { Loader2, Edit, Trash2 } from "lucide-react"
import { TablaItem } from "@/api/facturas"

export interface Invoice {
  id: number
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}

interface InvoiceTableProps {
  invoices: Invoice[]
  isLoading: boolean
  onEdit?: (invoice: Invoice) => void
  onDelete?: (invoiceId: number) => void
  deletingId?: number | null
}

export default function InvoiceTable({ invoices = [], isLoading, onEdit, onDelete, deletingId }: InvoiceTableProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }}>
          <Loader2 className="h-8 w-8 text-primary" />
        </motion.div>
      </div>
    )
  }

  if ((invoices || []).length === 0) {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="rounded-lg border border-border bg-white p-8 text-center">
        <p className="text-muted-foreground">No se encontraron facturas</p>
      </motion.div>
    )
  }

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-lg border border-border bg-white shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border bg-muted/50">
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">Número de Factura</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">Fecha</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">Proveedor</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">CUIT de Proveedor</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-foreground">Total</th>
              <th className="px-6 py-3 text-center text-sm font-semibold text-foreground">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {(invoices || [])?.map((invoice, index) => (
              <motion.tr
                key={invoice.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="border-b border-border hover:bg-muted/50 transition-colors"
              >
                <td className="px-6 py-4 text-sm font-medium text-foreground">{invoice.numero_factura}</td>
                <td className="px-6 py-4 text-sm text-muted-foreground">{invoice.fecha}</td>
                <td className="px-6 py-4 text-sm text-muted-foreground">{invoice.razon_social}</td>
                <td className="px-6 py-4 text-sm text-muted-foreground">{invoice.cuit_emisor}</td>
                <td className="px-6 py-4 text-right text-sm font-semibold text-foreground">${Number(invoice.total).toFixed(2)}</td>
                <td className="px-6 py-4 text-center space-x-2">
                  {onEdit && (
                    <button onClick={() => onEdit(invoice)} className="text-blue-600 hover:text-blue-800">
                      <Edit className="inline-block h-4 w-4" />
                    </button>
                  )}
                  {onDelete && (
                    <button
                      onClick={() => onDelete(invoice.id)}
                      disabled={deletingId === invoice.id}
                      className="text-red-600 hover:text-red-800"
                    >
                      {deletingId === invoice.id ? (
                        <Loader2 className="inline-block h-4 w-4 animate-spin" />
                      ) : (
                        <Trash2 className="inline-block h-4 w-4" />
                      )}
                    </button>
                  )}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  )
}
