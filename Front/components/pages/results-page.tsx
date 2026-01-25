"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"
import InvoiceForm from "../invoice-form"
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
  const [errors, setErrors] = useState<Record<string, string>>({})
  const { toast } = useToast()

  const handleConfirm = async () => {
    if (!clientData) return

    setIsLoading(true)
    setErrors({})

    try {
      await confirmInvoice(clientData)
      toast({ title: "Éxito", description: "Factura registrada correctamente" })
      onConfirm()
    } catch (err: any) {
      try {
        const parsed = JSON.parse(err.message)
        const fieldErrors: Record<string, string> = {}

        if (Array.isArray(parsed.detail)) {
          parsed.detail.forEach((e: any) => {
            const loc = e.loc
            const cleanMsg = e.msg.replace(/^Value error,\s*/i, "")

            // 🔹 Validación cruzada del total vs subtotales
            if (loc.length === 1 && loc[0] === "body" && cleanMsg.includes("no coincide con la suma de subtotales")) {
              fieldErrors["total"] = cleanMsg
              return
            }

            // 🔹 Errores de tabla_items
            if (loc[0] === "body" && loc[1] === "tabla_items") {
              const index = loc[2] // índice del item
              const field = loc[3] // descripcion, cantidad, subtotal
              fieldErrors[`tabla_items.${index}.${field}`] = cleanMsg
              return
            }

            // 🔹 Errores de campos normales (numero_factura, fecha, total, etc.)
            const field = loc[loc.length - 1]
            fieldErrors[field] = cleanMsg
          })

          setErrors(fieldErrors)
          return
        }

        // ✅ Error custom (ej: fecha inválida)
        if (parsed.detail?.message) {
          setErrors({ fecha: parsed.detail.message })
          return
        }

      } catch {
        console.error("Error no parseable:", err)
      }

      toast({
        title: "Error",
        description: "No se pudo registrar la factura",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  if (!clientData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg text-muted-foreground">
          Cargando datos de la factura...
        </p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 px-4 py-12">
      <div className="mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-6 w-6 text-primary" />
            <h1 className="text-3xl font-bold text-foreground">
              Datos de la Factura
            </h1>
          </div>
          <p className="text-muted-foreground">
            Revise y corrija los datos extraídos antes de confirmar el registro
          </p>
        </motion.div>

        <InvoiceForm
          data={clientData}
          onChange={setClientData}
          isEditable={true}
          errors={errors}
        />

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-8 flex flex-col sm:flex-row gap-4 justify-center"
        >
          <Button variant="outline" onClick={onCancel} disabled={isLoading}>
            Cancelar
          </Button>
          <Button onClick={handleConfirm} disabled={isLoading}>
            {isLoading ? "Confirmando..." : "Confirmar y Registrar"}
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
