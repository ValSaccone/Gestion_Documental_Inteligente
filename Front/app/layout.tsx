import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import Header from "@/components/header"
import { NavigationProvider } from "@/lib/navigation-context"
import { Toaster } from "@/components/ui/toaster"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "FacturaVision - Invoice Digitization",
  description: "Modern OCR-based invoice processing and management system",
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-background text-foreground`}>
        <NavigationProvider>
          <Header />
          <main className="min-h-screen bg-background">{children}</main>
        </NavigationProvider>
        <Toaster />
      </body>
    </html>
  )
}
