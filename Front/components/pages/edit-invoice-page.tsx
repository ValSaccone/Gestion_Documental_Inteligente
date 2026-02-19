"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast"
import { updateInvoice, deleteInvoice, TablaItem, Invoice } from "@/api/facturas"

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

interface EditInvoicePageProps {
  invoice: Invoice
  onCancel: () => void
  onUpdated: () => void
}

export default function EditInvoicePage({ invoice, onCancel, onUpdated }: EditInvoicePageProps) {
  const [clientData, setClientData] = useState<Invoice>(invoice)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const { toast } = useToast()

  const handleChange = (field: keyof Invoice, value: any) => {
    setClientData((prev) => ({ ...prev, [field]: value }))
  }

  const handleItemChange = (index: number, field: keyof TablaItem, value: string | number) => {
    setClientData((prev) => {
      const newItems = [...prev.tabla_items]
      newItems[index] = { ...newItems[index], [field]: value }
      return { ...prev, tabla_items: newItems }
    })
  }

  const handleUpdate = async () => {
    setIsLoading(true)
    setErrors({}) // Limpiar errores previos

    try {
      await updateInvoice(clientData.id, clientData)
      toast({ title: "Éxito", description: "Factura actualizada correctamente" })
      onUpdated()
    } catch (err: any) {
      console.error(err)

      try {
        const parsed = JSON.parse(err.message)
        const fieldErrors: Record<string, string> = {}

        // 🔹 Si detail es un array de errores tipo Pydantic/FastAPI
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

            // 🔹 Errores de campos normales (numero_factura, fecha, total, razon_social, cuit_emisor, etc.)
            const field = loc[loc.length - 1]
            fieldErrors[field] = cleanMsg
          })

          setErrors(fieldErrors)
          return
        }

        // 🔹 Error custom (como ServiceError de CUIT duplicado)
        if (parsed.detail?.message) {
          // 🔹 Ahora CUIT duplicado aparece SOLO en el input de CUIT
          if (parsed.detail.message.includes("CUIT")) {
            fieldErrors.cuit_emisor = "El CUIT ingresado ya pertenece a un proveedor"
          } else {
            fieldErrors.razon_social = parsed.detail.message
          }
          setErrors(fieldErrors)
          return
        }

      } catch {
        // Si no se puede parsear, mostramos toast
        toast({
          title: "Error",
          description: "No se pudo actualizar la factura",
          variant: "destructive",
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm("¿Está seguro que desea eliminar esta factura?")) return
    setIsLoading(true)
    try {
      await deleteInvoice(clientData.id)
      toast({ title: "Éxito", description: "Factura eliminada correctamente" })
      onUpdated()
    } catch (err: any) {
      console.error(err)
      toast({
        title: "Error",
        description: "No se pudo eliminar la factura",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 px-4 py-12">
      <div className="mx-auto max-w-4xl">
        <motion.div className="mb-8 flex items-center gap-2">
          <CheckCircle className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold text-foreground">Editar Factura</h1>
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
            error={errors.cuit_emisor} // 🔹 CUIT duplicado ahora solo se muestra aquí
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
        </motion.div>

        <motion.div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Button variant="outline" onClick={onCancel} disabled={isLoading}>
            Cancelar
          </Button>
          <Button onClick={handleUpdate} disabled={isLoading}>
            {isLoading ? "Actualizando..." : "Guardar Cambios"}
          </Button>
          <Button variant="destructive" onClick={handleDelete} disabled={isLoading}>
            Eliminar
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
