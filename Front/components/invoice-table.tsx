"use client"

import { motion } from "framer-motion"
import { Loader2 } from "lucide-react"
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
}

export default function InvoiceTable({ invoices = [], isLoading }: InvoiceTableProps) {
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
        <p className="text-muted-foreground">No invoices found</p>
      </motion.div>
    )
  }

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-lg border border-border bg-white shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border bg-muted/50">
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">Invoice</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">Date</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">Provider</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-foreground">User</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-foreground">Total</th>
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
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  )
}
