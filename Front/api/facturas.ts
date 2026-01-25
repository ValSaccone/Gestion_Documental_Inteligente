const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface TablaItem {
  descripcion: string
  cantidad: number
  subtotal: number
}

export interface ProcessedData {
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}

export interface Invoice {
  id: number
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: TablaItem[]
  total: number
}

// =======================
// Subida de factura (OCR)
// =======================
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

  const data: ProcessedData = await response.json()

  if (!Array.isArray(data.tabla_items)) {
    data.tabla_items = []
  }

  return data
}

// =======================
// Confirmar factura (DB)
// =======================
export async function confirmInvoice(data: ProcessedData): Promise<void> {

  const payload = {
    tipo_factura: data.tipo_factura?.trim() || "",
    razon_social: data.razon_social?.trim() || "",
    cuit_emisor: data.cuit_emisor ? data.cuit_emisor.replace(/\D/g, "") : "",
    numero_factura: data.numero_factura?.trim() || "",
    fecha: data.fecha?.trim() || "",

    tabla_items: data.tabla_items.map(item => ({
      descripcion: item.descripcion?.trim() || "",
      cantidad: Number(item.cantidad),
      subtotal: Number(item.subtotal),
    })),

    total: Number(data.total),
  }

  console.log("Payload enviado:", payload)

  const response = await fetch(`${API_BASE_URL}/facturas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const err = await response.text()
    console.error("Error backend:", err)
    throw new Error(err)
  }
}

// =======================
// Obtener facturas
// =======================
export async function getInvoices(): Promise<Invoice[]> {
  const response = await fetch(`${API_BASE_URL}/facturas`)

  if (!response.ok) {
    throw new Error("Failed to fetch invoices")
  }

  return response.json()
}

export async function getInvoiceById(id: number): Promise<Invoice> {
  const response = await fetch(`${API_BASE_URL}/facturas/${id}`)

  if (!response.ok) {
    throw new Error("Failed to fetch invoice")
  }

  return response.json()
}

// =======================
// Exportar facturas
// =======================
export async function exportInvoices(format: "pdf" | "csv"): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/facturas/export?format=${format}`, {
    method: "GET",
  })

  if (!response.ok) {
    throw new Error(`Failed to export invoices as ${format.toUpperCase()}`)
  }

  return response.blob()
}
