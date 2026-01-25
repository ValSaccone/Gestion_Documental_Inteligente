"use client"

import { motion } from "framer-motion"
import { useState } from "react"
import { TablaItem } from "@/api/facturas"

export interface BackendProcessedData {
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}

interface InvoiceFormProps {
  data: BackendProcessedData
  onChange: (data: BackendProcessedData) => void
  isEditable: boolean
  errors: Record<string, string>
}

// InputField defined OUTSIDE InvoiceForm to prevent re-creation on each render
interface InputFieldProps {
  label: string
  value: string | number
  onChange: (val: string) => void
  type?: string
  error?: string
  disabled?: boolean
}

function InputField({
  label,
  value,
  onChange,
  type = "text",
  error,
  disabled = false,
}: InputFieldProps) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className={`w-full rounded-lg px-3 py-2 text-sm border 
          ${error ? "border-red-500 bg-red-50" : "border-border"}
        `}
      />
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  )
}

export default function InvoiceForm({ data, onChange, isEditable, errors }: InvoiceFormProps) {
  const [localData, setLocalData] = useState<BackendProcessedData>(data)

  const handleChange = (field: keyof BackendProcessedData, value: any) => {
    setLocalData(prev => {
      const newData = { ...prev, [field]: value }
      onChange(newData)
      return newData
    })
  }

  const handleItemChange = (index: number, field: keyof TablaItem, value: string | number) => {
    setLocalData(prev => {
      const newItems = [...prev.tabla_items]
      newItems[index] = { ...newItems[index], [field]: value }
      const newData = { ...prev, tabla_items: newItems }
      onChange(newData)
      return newData
    })
  }

  return (
    <motion.div className="space-y-8 rounded-lg border p-6 bg-white shadow-sm">
      <div className="grid gap-4 sm:grid-cols-2">
        <InputField
          label="Número de Factura"
          value={localData.numero_factura}
          onChange={(val) => handleChange("numero_factura", val)}
          error={errors.numero_factura}
          disabled={!isEditable}
        />
        <InputField
          label="Fecha"
          value={localData.fecha}
          onChange={(val) => handleChange("fecha", val)}
          error={errors.fecha}
          disabled={!isEditable}
        />
      </div>

      <InputField
        label="Total"
        type="number"
        value={String(localData.total)}
        onChange={(val) => handleChange("total", Number(val))}
        error={errors.total}
        disabled={!isEditable}
      />

      <InputField
        label="Razón Social"
        value={localData.razon_social}
        onChange={(val) => handleChange("razon_social", val)}
        error={errors.razon_social}
        disabled={!isEditable}
      />

      <InputField
        label="CUIT"
        value={localData.cuit_emisor}
        onChange={(val) => handleChange("cuit_emisor", val)}
        error={errors.cuit_emisor}
        disabled={!isEditable}
      />

      {localData.tabla_items.map((item, idx) => (
        <div key={idx} className="border p-4 rounded space-y-2">
          <InputField
            label="Descripción"
            value={item.descripcion}
            onChange={(val) => handleItemChange(idx, "descripcion", val)}
            error={errors[`tabla_items.${idx}.descripcion`]}
            disabled={!isEditable}
          />
          <InputField
            label="Cantidad"
            type="number"
            value={String(item.cantidad)}
            onChange={(val) => handleItemChange(idx, "cantidad", Number(val))}
            error={errors[`tabla_items.${idx}.cantidad`]}
            disabled={!isEditable}
          />
          <InputField
            label="Subtotal"
            type="number"
            value={String(item.subtotal)}
            onChange={(val) => handleItemChange(idx, "subtotal", Number(val))}
            error={errors[`tabla_items.${idx}.subtotal`]}
            disabled={!isEditable}
          />
        </div>
      ))}
    </motion.div>
  )
}
