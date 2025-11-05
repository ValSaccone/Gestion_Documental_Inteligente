"use client"

import { motion } from "framer-motion"

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

interface InvoiceFormProps {
  data: ProcessedData
  onChange: (data: ProcessedData) => void
  isEditable: boolean
}

export default function InvoiceForm({ data, onChange, isEditable }: InvoiceFormProps) {
  const handleChange = (field: keyof ProcessedData, value: any) => {
    onChange({ ...data, [field]: value })
  }

  const handleItemChange = (index: number, field: string, value: string) => {
    const newItems = [...data.items]
    newItems[index] = { ...newItems[index], [field]: value }
    onChange({ ...data, items: newItems })
  }

  const InputField = ({
    label,
    value,
    onChange: onChangeField,
  }: {
    label: string
    value: string
    onChange: (value: string) => void
  }) => (
    <div className="space-y-1">
      <label className="text-sm font-medium text-foreground">{label}</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChangeField(e.target.value)}
        disabled={!isEditable}
        className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm disabled:bg-muted"
      />
    </div>
  )

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.3 },
    },
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-8 rounded-lg border border-border bg-white p-6 shadow-sm"
    >
      {/* Invoice Header */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Invoice Details</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <InputField
            label="Invoice Number"
            value={data.invoiceNumber}
            onChange={(val) => handleChange("invoiceNumber", val)}
          />
          <InputField label="Date" value={data.date} onChange={(val) => handleChange("date", val)} />
        </div>
      </motion.section>

      {/* Amounts */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Amounts</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <InputField label="Total" value={data.total} onChange={(val) => handleChange("total", val)} />
          <InputField label="Tax" value={data.tax} onChange={(val) => handleChange("tax", val)} />
        </div>
      </motion.section>

      {/* Provider */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Provider</h2>
        <div className="space-y-4">
          <InputField label="Provider Name" value={data.provider} onChange={(val) => handleChange("provider", val)} />
          <InputField label="CUIT" value={data.providerCuit} onChange={(val) => handleChange("providerCuit", val)} />
          <InputField
            label="Address"
            value={data.providerAddress}
            onChange={(val) => handleChange("providerAddress", val)}
          />
        </div>
      </motion.section>

      {/* Items */}
      <motion.section variants={itemVariants} className="space-y-4">
        <h2 className="text-xl font-bold text-foreground">Line Items</h2>
        <div className="space-y-4">
          {data.items.map((item, index) => (
            <motion.div key={index} variants={itemVariants} className="rounded-lg border border-border p-4 space-y-3">
              <p className="text-sm font-medium text-muted-foreground">Item {index + 1}</p>
              <InputField
                label="Description"
                value={item.description}
                onChange={(val) => handleItemChange(index, "description", val)}
              />
              <div className="grid gap-4 sm:grid-cols-2">
                <InputField
                  label="Quantity"
                  value={item.quantity}
                  onChange={(val) => handleItemChange(index, "quantity", val)}
                />
                <InputField
                  label="Unit Price"
                  value={item.unitPrice}
                  onChange={(val) => handleItemChange(index, "unitPrice", val)}
                />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>
    </motion.div>
  )
}
