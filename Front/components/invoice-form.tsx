"use client"

import { motion } from "framer-motion"
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
  // Aseguramos que tabla_items nunca sea undefined
  const tablaItems = data.tabla_items || []

  const handleChange = (field: keyof BackendProcessedData, value: any) => {
    onChange({ ...data, [field]: value })
  }

  const handleItemChange = (index: number, field: keyof TablaItem, value: string | number) => {
    const newItems = [...tablaItems]
    newItems[index] = { ...newItems[index], [field]: value }
    onChange({ ...data, tabla_items: newItems })
  }

  const InputField = ({
    label,
    value,
    onChange,
  }: {
    label: string
    value: string | number
    onChange: (val: string) => void
  }) => (
    <div className="space-y-1">
      <label className="text-sm font-medium text-foreground">{label}</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={!isEditable}
        className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm disabled:bg-muted"
      />
    </div>
  )

  const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.1 } } }
  const itemVariants = { hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0, transition: { duration: 0.3 } } }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-8 rounded-lg border border-border bg-white p-6 shadow-sm"
    >
      {/* Invoice Header */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Detalles de la Factura</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <InputField
            label="Número de Factura"
            value={data.numero_factura}
            onChange={(val) => handleChange("numero_factura", val)}
          />
          <InputField label="Fecha" value={data.fecha} onChange={(val) => handleChange("fecha", val)} />
        </div>
      </motion.section>

      {/* Amount */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Montos</h2>
        <InputField label="Total" value={data.total} onChange={(val) => handleChange("total", val)} />
      </motion.section>

      {/* Provider */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Proveedor</h2>
        <InputField label="Razón Social" value={data.razon_social} onChange={(val) => handleChange("razon_social", val)} />
        <InputField label="CUIT" value={data.cuit_emisor} onChange={(val) => handleChange("cuit_emisor", val)} />
      </motion.section>


      {/* Items */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Items</h2>
        {(data.tabla_items || [])?.map((item, idx) => (
          <motion.div key={idx} variants={itemVariants} className="rounded-lg border border-border p-4 space-y-3">
            <InputField
              label="Descripción"
              value={item.descripcion}
              onChange={(val) => handleItemChange(idx, "descripcion", val)}
            />
            <div className="grid gap-4 sm:grid-cols-2">
              <InputField label="Cantidad" value={item.cantidad} onChange={(val) => handleItemChange(idx, "cantidad", val)} />
              <InputField label="Subtotal" value={item.subtotal} onChange={(val) => handleItemChange(idx, "subtotal", val)} />
            </div>
          </motion.div>
        ))}
      </motion.section>
    </motion.div>
  )
}



