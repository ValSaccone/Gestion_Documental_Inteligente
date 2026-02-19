"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast"
import { confirmInvoice, TablaItem } from "@/api/facturas"

interface InputFieldProps {
  label: string
  value: string
  onChange: (value: string) => void
  error?: string
  type?: string
}

function InputField({ label, value, onChange, error, type = "text" }: InputFieldProps) {
  return (
    <div className="space-y-1">
      <Label>{label}</Label>
      <Input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={error ? "border-red-500" : ""}
      />
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  )
}

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
  const [globalError, setGlobalError] = useState<string>("")
  const { toast } = useToast()

  const handleChange = (field: keyof BackendProcessedData, value: any) => {
      setClientData((prev) => prev ? { ...prev, [field]: value } : null);
  }

  const handleItemChange = (index: number, field: keyof TablaItem, value: string | number) => {
      setClientData((prev) => {
        if (!prev) return null;
        const newItems = [...prev.tabla_items];
        newItems[index] = { ...newItems[index], [field]: value };
        return { ...prev, tabla_items: newItems };
      });
  }

  const handleConfirm = async () => {
    if (!clientData) return

    setIsLoading(true)
    setErrors({})
    setGlobalError("")

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

            // Validación cruzada del total vs subtotales
            if (loc.length === 1 && loc[0] === "body" && cleanMsg.includes("no coincide con la suma de subtotales")) {
              fieldErrors["total"] = cleanMsg
              return
            }

            // Errores de tabla_items
            if (loc[0] === "body" && loc[1] === "tabla_items") {
              const index = loc[2]
              const field = loc[3]
              fieldErrors[`tabla_items.${index}.${field}`] = cleanMsg
              return
            }

            // Errores de campos normales
            const field = loc[loc.length - 1]
            fieldErrors[field] = cleanMsg
          })

          setErrors(fieldErrors)
          return
        }

        // Error custom del backend (ej: CUIT duplicado)
        if (parsed.detail?.message) {
          const msg = parsed.detail.message

          // 🔹 Si es CUIT duplicado, asignarlo al campo cuit_emisor
          if (msg.includes("CUIT")) {
            setErrors({ cuit_emisor: "El CUIT ingresado ya pertenece a un proveedor" })
          } else {
            setGlobalError(msg) // otros errores
          }

          return
        }

      } catch {
        console.error("Error no parseable:", err)
        setGlobalError("No se pudo registrar la factura")
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

        <motion.div className="space-y-8 rounded-lg border p-6 bg-white shadow-sm">
          <div className="grid gap-4 sm:grid-cols-2">
            <InputField
              label="Número de Factura"
              value={clientData.numero_factura}
              onChange={(val) => handleChange("numero_factura", val)}
              error={errors.numero_factura}
            />

            <InputField
              label="Tipo de Factura"
              value={clientData.tipo_factura}
              onChange={(val) => handleChange("tipo_factura", val)}
              error={errors.tipo_factura}
            />

            <InputField
              label="Fecha"
              value={clientData.fecha}
              onChange={(val) => handleChange("fecha", val)}
              error={errors.fecha}
            />
          </div>

          <InputField
            label="Total"
            type="number"
            value={String(clientData.total)}
            onChange={(val) => handleChange("total", Number(val))}
            error={errors.total}
          />

          <InputField
            label="Razón Social"
            value={clientData.razon_social}
            onChange={(val) => handleChange("razon_social", val)}
            error={errors.razon_social}
          />

          <InputField
            label="CUIT"
            value={clientData.cuit_emisor}
            onChange={(val) => handleChange("cuit_emisor", val)}
            error={errors.cuit_emisor} // 🔹 ahora el error aparece aquí en rojo
          />

          {clientData.tabla_items.map((item, idx) => (
            <div key={idx} className="border p-4 rounded space-y-2">
              <InputField
                label="Descripción"
                value={item.descripcion}
                onChange={(val) => handleItemChange(idx, "descripcion", val)}
                error={errors[`tabla_items.${idx}.descripcion`]}
              />
              <InputField
                label="Cantidad"
                type="number"
                value={String(item.cantidad)}
                onChange={(val) => handleItemChange(idx, "cantidad", Number(val))}
                error={errors[`tabla_items.${idx}.cantidad`]}
              />
              <InputField
                label="Subtotal"
                type="number"
                value={String(item.subtotal)}
                onChange={(val) => handleItemChange(idx, "subtotal", Number(val))}
                error={errors[`tabla_items.${idx}.subtotal`]}
              />
            </div>
          ))}


          {globalError && (
            <p className="text-center text-red-600 font-medium mt-2">{globalError}</p>
          )}
        </motion.div>

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
