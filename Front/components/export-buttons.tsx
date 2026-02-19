"use client"

import { motion } from "framer-motion"
import { Download, FileJson } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import { Invoice } from "@/api/facturas"

interface ExportButtonsProps {
  invoices: Invoice[]
}

export default function ExportButtons({ invoices = [] }: ExportButtonsProps) {
  const { toast } = useToast()

  const exportToCSV = () => {
    if (!invoices || invoices.length === 0) {
      toast({ title: "No data", description: "No hay facturas para exportar", variant: "destructive" })
      return
    }

    const headers = ["Numero Factura","Tipo Factura", "Fecha", "Proveedor", "CUIT", "Total"]
    const rows = invoices?.map((inv) => [inv.numero_factura,inv.tipo_factura, inv.fecha, inv.razon_social, inv.cuit_emisor, inv.total])

    const csv = [headers.join(","), ...rows?.map((row) => row.join(","))].join("\n")

    const blob = new Blob([csv], { type: "text/csv" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `invoices-${new Date().toISOString().split("T")[0]}.csv`
    a.click()

    toast({ title: "Success", description: "Facturas exportadas en formato CSV" })
  }



  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-2">
      <Button variant="outline" onClick={exportToCSV} className="gap-2 bg-transparent">
        <FileJson className="h-4 w-4" />
        Exportar CSV
      </Button>

    </motion.div>
  )
}


