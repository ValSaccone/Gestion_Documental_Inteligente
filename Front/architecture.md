# FacturaVision - Frontend Architecture

## Overview
FacturaVision is a modern React-based invoice digitization application that leverages OCR technology to automate invoice data extraction and management.

## Project Structure

\`\`\`
src/
├── app/
│   ├── layout.tsx          # Root layout with header and Toaster
│   ├── page.tsx            # Main page with routing logic
│   └── globals.css         # Global styles and theme tokens
├── components/
│   ├── header.tsx          # Main navigation header
│   ├── pages/
│   │   ├── upload-page.tsx      # File upload page
│   │   ├── results-page.tsx     # Data confirmation page
│   │   └── invoices-page.tsx    # Invoice management page
│   ├── file-upload.tsx     # File upload with drag & drop
│   ├── invoice-form.tsx    # Editable invoice form
│   ├── invoice-table.tsx   # Invoice list table
│   ├── filters-bar.tsx     # Search and filter controls
│   ├── export-buttons.tsx  # PDF/CSV export buttons
│   └── ui/                 # shadcn/ui components
└── api/
    └── facturas.ts         # Backend API client
\`\`\`

## Data Flow

### 1. Upload Flow
1. User accesses `/` (Upload Page)
2. User selects/drags invoice file
3. `FileUpload` component calls `uploadAndProcessInvoice()` API
4. Backend processes image with OCR
5. Results page displays extracted data
6. User can edit and confirm

### 2. Confirmation Flow
1. User reviews extracted data on Results Page
2. User can edit any field (all fields are editable)
3. User clicks "Confirm & Register"
4. `confirmInvoice()` sends data to backend
5. Upon success, user is redirected to Invoices Page

### 3. Management Flow
1. User accesses Invoices Page
2. `getInvoices()` fetches all registered invoices
3. User can search, filter by date/provider
4. User can export to CSV or PDF

## Frontend-Backend Communication

### API Endpoints

The frontend communicates with FastAPI backend at `${API_BASE_URL}` (default: `http://localhost:8000/api`):

- **POST** `/facturas/upload` - Upload and process invoice image
  - Request: FormData with file
  - Response: ProcessedData object with extracted information

- **POST** `/facturas` - Confirm and register invoice
  - Request: JSON with invoice details
  - Response: Success confirmation

- **GET** `/facturas` - List all invoices
  - Response: Array of Invoice objects

- **GET** `/facturas/{id}` - Get specific invoice details
  - Response: ProcessedData object

- **GET** `/facturas/export` - Export invoices
  - Query params: `format=pdf|csv`
  - Response: Blob (PDF or CSV file)

## Technology Stack

- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS v4 with design tokens
- **Components**: shadcn/ui
- **Animations**: Framer Motion
- **Icons**: lucide-react
- **Notifications**: Toast notifications (shadcn/ui)
- **HTTP Client**: Native Fetch API

## Design System

### Color Scheme
- Primary: #2563eb (Blue)
- Secondary: #0ea5e9 (Sky)
- Accent: #06b6d4 (Cyan)
- Backgrounds: White & Light Blue gradients

### Typography
- Font: Inter (system font family)
- Headings: Bold, responsive sizing
- Body: Regular weight, readable line-height

### Layout
- Mobile-first responsive design
- Flexbox-based layouts
- Maximum width constraint (max-w-7xl)

## Key Components

### File Upload
- Drag & drop support
- File preview
- Size validation
- Loading states

### Invoice Form
- Editable fields
- Line items management
- Provider information
- Amount fields

### Invoice Table
- Responsive table design
- Row animations
- Empty state handling
- Loading indicator

### Filters Bar
- Search by invoice number/provider
- Date filtering
- Provider filtering

## Environment Variables

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000/api  # Backend API base URL
\`\`\`

## Installation & Setup

1. Clone the repository
2. Install dependencies: `npm install`
3. Set environment variables in `.env.local`
4. Run development server: `npm run dev`
5. Open http://localhost:3000

## Notes

- All API calls are error-handled with user-friendly toast notifications
- Animations use Framer Motion for smooth transitions
- Responsive design works on mobile, tablet, and desktop
- State management uses React hooks (useState, useEffect)
- No external state management library needed for current scope
