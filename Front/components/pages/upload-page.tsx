"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import FileUpload from "@/components/file-upload"
import { uploadAndProcessInvoice } from "@/api/facturas"

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

interface UploadPageProps {
  onFileUpload: (file: File, data: ProcessedData) => void
  onNavigate: (page: "upload" | "results" | "invoices") => void
}

export default function UploadPage({ onFileUpload, onNavigate }: UploadPageProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  const handleFileSelect = async (file: File) => {
    setIsLoading(true)
    setError(null)

    try {
      // Call API to process invoice
      const data = await uploadAndProcessInvoice(file)
      toast({
        title: "Success",
        description: "Invoice processed successfully",
      })
      onFileUpload(file, data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to process invoice"
      setError(errorMessage)
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
      <div className="mx-auto max-w-2xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center"
        >
          <h1 className="text-4xl font-bold text-foreground mb-2">Cargue una Factura</h1>
          <p className="text-lg text-muted-foreground">Cargue una Factura en formato JPG, PNG, or PDF para extraer automáticamente sus datos</p>
        </motion.div>

        {/* Error Alert */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 flex items-center gap-3 rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-3"
          >
            <AlertCircle className="h-5 w-5 text-destructive" />
            <p className="text-sm text-destructive">{error}</p>
          </motion.div>
        )}

        {/* Upload Component */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />
        </motion.div>

        {/* View Invoices Link */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-8 flex justify-center"
        >
          <Button
            variant="outline"
            onClick={() => onNavigate("invoices")}
            className="text-primary hover:text-primary hover:bg-primary/10"
          >
            Facturas Registradas
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
