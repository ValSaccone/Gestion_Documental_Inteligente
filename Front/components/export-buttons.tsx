"use client"

import { motion } from "framer-motion"
import { Download, FileJson } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"

interface Invoice {
  id: string
  invoiceNumber: string
  date: string
  total: string
  provider: string
  user: string
}

interface ExportButtonsProps {
  invoices: Invoice[]
}

export default function ExportButtons({ invoices }: ExportButtonsProps) {
  const { toast } = useToast()

  const exportToCSV = () => {
    if (invoices.length === 0) {
      toast({
        title: "No data",
        description: "There are no invoices to export",
        variant: "destructive",
      })
      return
    }

    const headers = ["Invoice Number", "Date", "Provider", "User", "Total"]
    const rows = invoices.map((inv) => [inv.invoiceNumber, inv.date, inv.provider, inv.user, inv.total])

    const csv = [headers.join(","), ...rows.map((row) => row.join(","))].join("\n")

    const blob = new Blob([csv], { type: "text/csv" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `invoices-${new Date().toISOString().split("T")[0]}.csv`
    a.click()

    toast({
      title: "Success",
      description: "Invoices exported to CSV",
    })
  }

  const exportToPDF = async () => {
    if (invoices.length === 0) {
      toast({
        title: "No data",
        description: "There are no invoices to export",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Processing",
      description: "PDF generation not yet implemented. Contact backend API.",
    })
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-2">
      <Button variant="outline" onClick={exportToCSV} className="gap-2 bg-transparent">
        <FileJson className="h-4 w-4" />
        Exportar CSV
      </Button>
      <Button variant="outline" onClick={exportToPDF} className="gap-2 bg-transparent">
        <Download className="h-4 w-4" />
        Exportar PDF
      </Button>
    </motion.div>
  )
}
