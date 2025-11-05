const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"

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

interface Invoice {
  id: string
  invoiceNumber: string
  date: string
  total: string
  provider: string
  user: string
}

export async function uploadAndProcessInvoice(file: File): Promise<ProcessedData> {
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(`${API_BASE_URL}/facturas/upload`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error("Failed to upload and process invoice")
  }

  return response.json()
}

export async function confirmInvoice(data: ProcessedData, file: File): Promise<void> {
  const payload = {
    ...data,
    fileName: file.name,
    fileSize: file.size,
  }

  const response = await fetch(`${API_BASE_URL}/facturas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error("Failed to confirm invoice")
  }
}

export async function getInvoices(): Promise<Invoice[]> {
  const response = await fetch(`${API_BASE_URL}/facturas`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })

  if (!response.ok) {
    throw new Error("Failed to fetch invoices")
  }

  return response.json()
}

export async function getInvoiceById(id: string): Promise<ProcessedData> {
  const response = await fetch(`${API_BASE_URL}/facturas/${id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })

  if (!response.ok) {
    throw new Error("Failed to fetch invoice")
  }

  return response.json()
}

export async function exportInvoices(format: "pdf" | "csv"): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/facturas/export?format=${format}`, {
    method: "GET",
  })

  if (!response.ok) {
    throw new Error(`Failed to export invoices as ${format.toUpperCase()}`)
  }

  return response.blob()
}
