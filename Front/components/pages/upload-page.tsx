"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import FileUpload from "@/components/file-upload"
import { uploadAndProcessInvoice, TablaItem } from "@/api/facturas"

export interface BackendProcessedData {
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}


interface UploadPageProps {
  onFileUpload: (file: File, data: BackendProcessedData) => void
  onNavigate: (page: "upload" | "results" | "invoices") => void
}

export default function UploadPage({ onFileUpload, onNavigate }: UploadPageProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [tablaItems, setTablaItems] = useState<TablaItem[]>([]) // ✅ inicializamos array vacío
  const { toast } = useToast()

  const handleFileSelect = async (file: File) => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await uploadAndProcessInvoice(file)

      console.log("Factura procesada desde el backend:", data)
      console.log("tabla_items recibidos:", data.tabla_items)

      // Actualizamos el estado interno para que el render de la tabla de items nunca rompa
      setTablaItems(data.tabla_items || [])

      toast({
        title: "Éxito",
        description: "Factura procesada correctamente",
      })
      onFileUpload(file, data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "No se pudo procesar la factura"
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
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center"
        >
          <h1 className="text-4xl font-bold text-foreground mb-2">Cargue una Factura</h1>
          <p className="text-lg text-muted-foreground">
            Cargue una factura en formato JPG, PNG o PDF para extraer automáticamente sus datos
          </p>
        </motion.div>

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

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />
        </motion.div>

        {/* Ejemplo de render seguro de items */}
        {tablaItems.length > 0 && (
          <motion.section className="mt-6">
            <h2 className="text-xl font-bold mb-2">Items extraídos</h2>
            {tablaItems?.map((item, idx) => (
              <div key={idx} className="p-2 border rounded mb-2">
                <p>Descripción: {item.descripcion}</p>
                <p>Cantidad: {item.cantidad}</p>
                <p>Subtotal: {item.subtotal}</p>
              </div>
            ))}
          </motion.section>
        )}

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

