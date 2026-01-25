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
}

export default function InvoiceForm({ data, onChange, isEditable }: InvoiceFormProps) {

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

  const InputField = ({
    label,
    value,
    onChange,
    type = "text",
  }: {
    label: string
    value: string | number
    onChange: (val: string) => void
    type?: string
  }) => (
    <div className="space-y-1">
      <label className="text-sm font-medium text-foreground">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={!isEditable}
        className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm disabled:bg-muted"
      />
    </div>
  )

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }} className="space-y-8 rounded-lg border border-border bg-white p-6 shadow-sm">
      {/* Factura Header */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Detalles de la Factura</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <InputField
            label="Número de Factura"
            value={localData.numero_factura}
            onChange={(val) => handleChange("numero_factura", val)}
          />
          <InputField
            label="Fecha"
            value={localData.fecha}
            onChange={(val) => handleChange("fecha", val)}
          />
        </div>
      </div>

      {/* Monto */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Monto Total</h2>
        <InputField
          label="Total"
          type="number"
          value={String(localData.total)}
          onChange={(val) => handleChange("total", Number(val))}
        />
      </div>

      {/* Proveedor */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Proveedor</h2>
        <InputField
          label="Razón Social"
          value={localData.razon_social}
          onChange={(val) => handleChange("razon_social", val)}
        />
        <InputField
          label="CUIT"
          value={localData.cuit_emisor}
          onChange={(val) => handleChange("cuit_emisor", val)}
        />
      </div>

      {/* Tabla items (detalle factura) */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Detalle</h2>
        {localData.tabla_items.map((item, idx) => (
          <div key={item.descripcion + idx} className="rounded-lg border border-border p-4 space-y-3">
            <InputField
              label="Descripción"
              value={item.descripcion}
              onChange={(val) => handleItemChange(idx, "descripcion", val)}
            />
            <div className="grid gap-4 sm:grid-cols-2">
              <InputField
                label="Cantidad"
                type="number"
                value={String(item.cantidad)}
                onChange={(val) => handleItemChange(idx, "cantidad", Number(val))}
              />
              <InputField
                label="Subtotal"
                type="number"
                value={String(item.subtotal)}
                onChange={(val) => handleItemChange(idx, "subtotal", Number(val))}
              />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
