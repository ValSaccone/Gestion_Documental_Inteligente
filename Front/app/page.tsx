"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { useNavigation } from "@/lib/navigation-context"
import UploadPage from "@/components/pages/upload-page"
import ResultsPage from "@/components/pages/results-page"
import InvoicesPage from "@/components/pages/invoices-page"

type PageType = "upload" | "results" | "invoices"

interface ProcessedData {
  tipo_factura: string
  razon_social: string
  cuit_emisor: string
  numero_factura: string
  fecha: string
  tabla_items: Array<{
    descripcion: string
    cantidad: number
    subtotal: number
  }>
    total: number
}

export default function Home() {
  const { currentPage, navigateTo } = useNavigation()
  const [processedData, setProcessedData] = useState<ProcessedData | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleFileUpload = (file: File, data: ProcessedData) => {
    setUploadedFile(file)
    setProcessedData(data)
    navigateTo("results")
  }

  const handleConfirm = () => {
    navigateTo("invoices")
    setProcessedData(null)
    setUploadedFile(null)
  }

  const handleCancel = () => {
    navigateTo("upload")
    setProcessedData(null)
    setUploadedFile(null)
  }

  const handleNavigate = (page: PageType) => {
    navigateTo(page)
    if (page === "upload") {
      setProcessedData(null)
      setUploadedFile(null)
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }}>
      {currentPage === "upload" && (
        <UploadPage onFileUpload={handleFileUpload} onNavigate={handleNavigate} />
      )}

      {/* Render condicional*/}
      {currentPage === "results" && processedData && (
        <ResultsPage
          data={processedData}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}

      {currentPage === "invoices" && <InvoicesPage onNavigate={handleNavigate} />}
    </motion.div>
  )
}
