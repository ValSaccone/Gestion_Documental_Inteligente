"use client"

import type React from "react"

import { useRef, useState } from "react"
import { motion } from "framer-motion"
import { Upload, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"

interface FileUploadProps {
  onFileSelect: (file: File) => void
  isLoading: boolean
}

export default function FileUpload({ onFileSelect, isLoading }: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileChange(files[0])
    }
  }

  const handleFileChange = (file: File) => {
    const validTypes = ["image/jpeg", "image/png", "application/pdf"]
    if (validTypes.includes(file.type)) {
      setSelectedFile(file)
    } else {
      alert("Cargue un archivo en formato JPG, PNG, o PDF")
    }
  }

  const handleButtonClick = () => {
    fileInputRef.current?.click()
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      handleFileChange(files[0])
    }
  }

  const handleProcess = () => {
    if (selectedFile) {
      onFileSelect(selectedFile)
    }
  }

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <motion.div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        animate={{
          backgroundColor: isDragging ? "#eff6ff" : "#f8fafc",
          borderColor: isDragging ? "#2563eb" : "#e2e8f0",
        }}
        className="relative rounded-lg border-2 border-dashed border-border bg-muted/30 p-12 transition-colors cursor-pointer"
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleInputChange}
          className="hidden"
          accept=".jpg,.jpeg,.png,.pdf"
          disabled={isLoading}
        />

        {!selectedFile ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ repeat: Number.POSITIVE_INFINITY, duration: 2 }}
              className="mb-4 flex justify-center"
            >
              <Upload className="h-12 w-12 text-primary" />
            </motion.div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Arrastre y suelte la factura</h3>
            <p className="text-sm text-muted-foreground mb-4">O haga clic para buscar (JPG, PNG, PDF)</p>
            <Button onClick={handleButtonClick} disabled={isLoading} className="bg-primary hover:bg-primary/90">
              {isLoading ? "Procesando..." : "Seleccione el Archivo"}
            </Button>
          </motion.div>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
            <FileText className="h-12 w-12 text-primary mx-auto mb-4" />
            <p className="font-semibold text-foreground mb-2">{selectedFile.name}</p>
            <p className="text-sm text-muted-foreground mb-4">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            <Button onClick={handleButtonClick} variant="outline" disabled={isLoading} className="mr-2 bg-transparent">
              Cambiar archivo
            </Button>
            <Button onClick={handleProcess} disabled={isLoading} className="bg-primary hover:bg-primary/90">
              {isLoading ? "Cargando..." : "Cargar Factura"}
            </Button>
          </motion.div>
        )}
      </motion.div>

      {/* Supported Formats
      <div className="rounded-lg bg-muted/50 p-4">
        <p className="text-sm font-medium text-foreground mb-2">Formatos soportados:</p>
        <ul className="text-sm text-muted-foreground space-y-1">
          <li>• JPG/JPEG (max 10 MB)</li>
          <li>• PNG (max 10 MB)</li>
          <li>• PDF (max 10 MB)</li>
        </ul>
      </div>*/}
    </div>
  )
}
