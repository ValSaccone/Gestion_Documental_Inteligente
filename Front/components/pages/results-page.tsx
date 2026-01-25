"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import InvoiceForm from "@/components/invoice-form"
import { confirmInvoice, TablaItem } from "@/api/facturas"

export interface BackendProcessedData {
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}

interface ResultsPageProps {
  data: BackendProcessedData | null
  onConfirm: () => void
  onCancel: () => void
}

export default function ResultsPage({ data, onConfirm, onCancel }: ResultsPageProps) {
  const [clientData, setClientData] = useState<BackendProcessedData | null>(data)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleConfirm = async () => {
    if (!clientData) return
    setIsLoading(true)
    try {
      await confirmInvoice(clientData)
      toast({ title: "Éxito", description: "Factura registrada correctamente" })
      onConfirm()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "No se pudo registrar la factura"
      toast({ title: "Error", description: errorMessage, variant: "destructive" })
    } finally {
      setIsLoading(false)
    }
  }

  if (!clientData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg text-muted-foreground">Cargando datos de la factura...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 px-4 py-12">
      <div className="mx-auto max-w-4xl">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="mb-8">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-6 w-6 text-primary" />
            <h1 className="text-3xl font-bold text-foreground">Datos de la Factura</h1>
          </div>
          <p className="text-muted-foreground">Revise y corrija los datos extraídos antes de confirmar el registro</p>
        </motion.div>

        {/* 🔹 InvoiceForm ahora maneja localData internamente sin reset */}
        <InvoiceForm data={clientData} onChange={setClientData} isEditable={true} />

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Button variant="outline" onClick={onCancel} disabled={isLoading} className="sm:w-40 bg-transparent">
            Cancelar
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading} className="sm:w-40 bg-primary hover:bg-primary/90">
            {isLoading ? "Confirmando..." : "Confirmar y Registrar"}
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
