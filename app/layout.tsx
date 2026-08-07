import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'VIZHIPPAAN | Child Education Risk Intelligence',
  description: 'AI-powered child education risk intelligence and intervention dashboard.',
  generator: 'VIZHIPPAAN',
  icons: {
    icon: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/VIZHIPPAAN%20LOGO-6iZUsWvm0v2UTOuQwqCoD2cR1K6HIV.jpg',
    shortcut: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/VIZHIPPAAN%20LOGO-6iZUsWvm0v2UTOuQwqCoD2cR1K6HIV.jpg',
    apple: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/VIZHIPPAAN%20LOGO-6iZUsWvm0v2UTOuQwqCoD2cR1K6HIV.jpg',
  },
  openGraph: {
    title: 'VIZHIPPAAN | Child Education Risk Intelligence',
    description: 'AI-powered child education risk intelligence and intervention dashboard.',
    images: ['https://hebbkx1anhila5yf.public.blob.vercel-storage.com/VIZHIPPAAN%20LOGO-6iZUsWvm0v2UTOuQwqCoD2cR1K6HIV.jpg'],
  },
}

export const viewport: Viewport = {
  colorScheme: 'light',
  themeColor: '#f7f9fc',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
