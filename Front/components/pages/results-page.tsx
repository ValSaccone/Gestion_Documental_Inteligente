"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import InvoiceForm from "@/components/invoice-form"
import { confirmInvoice } from "@/api/facturas"

interface ProcessedData {
  invoiceNumber: string
  date: string
  total: string
  tax: string
  provider: string
  providerCuit: string
  providerAddress: string
  items: Array<{ description: string; quantity: string; unitPrice: string }>
}

interface ResultsPageProps {
  data: ProcessedData
  file: File
  onConfirm: () => void
  onCancel: () => void
}

export default function ResultsPage({ data, file, onConfirm, onCancel }: ResultsPageProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [editedData, setEditedData] = useState(data)
  const { toast } = useToast()

  const handleConfirm = async () => {
    setIsLoading(true)
    try {
      await confirmInvoice(editedData, file)
      toast({
        title: "Success",
        description: "Invoice registered successfully",
      })
      onConfirm()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to confirm invoice"
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 px-4 py-12">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-6 w-6 text-primary" />
            <h1 className="text-3xl font-bold text-foreground">Invoice Data Extracted</h1>
          </div>
          <p className="text-muted-foreground">Review and correct the extracted data before confirming registration</p>
        </motion.div>

        {/* Form */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <InvoiceForm data={editedData} onChange={setEditedData} isEditable={true} />
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-8 flex flex-col sm:flex-row gap-4 justify-center"
        >
          <Button variant="outline" onClick={onCancel} disabled={isLoading} className="sm:w-40 bg-transparent">
            Cancel
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading} className="sm:w-40 bg-primary hover:bg-primary/90">
            {isLoading ? "Confirming..." : "Confirm & Register"}
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
