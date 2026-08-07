"use client"

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react"

import { INDIAN_LANGUAGES } from "@/lib/languages"

type LanguageContextType = {
  language: string
  changeLanguage: (code: string) => void
  t: (key: string) => string
}

const LanguageContext = createContext<LanguageContextType | undefined>(
  undefined
)

export function LanguageProvider({
  children,
}: {
  children: ReactNode
}) {
  const [language, setLanguage] = useState("en")
  const [translations, setTranslations] = useState<Record<string, string>>({})

  useEffect(() => {
    const savedLanguage =
      localStorage.getItem("vizhippaan-language") || "en"

    setLanguage(savedLanguage)
  }, [])

  useEffect(() => {
    async function loadTranslations() {
      try {
        const response = await fetch(
          `/locales/${language}.json`
        )

        if (!response.ok) {
          throw new Error("Translation file not found")
        }

        const data = await response.json()

        setTranslations(data)

        const selectedLanguage = INDIAN_LANGUAGES.find(
          (item) => item.code === language
        )

        document.documentElement.lang = language

        document.documentElement.dir =
          selectedLanguage?.direction || "ltr"
      } catch (error) {
        console.error(error)

        if (language !== "en") {
          setLanguage("en")
        }
      }
    }

    loadTranslations()
  }, [language])

  const changeLanguage = (code: string) => {
    setLanguage(code)

    localStorage.setItem(
      "vizhippaan-language",
      code
    )
  }

  const t = (key: string) => {
    return translations[key] || key
  }

  return (
    <LanguageContext.Provider
      value={{
        language,
        changeLanguage,
        t,
      }}
    >
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)

  if (!context) {
    throw new Error(
      "useLanguage must be used inside LanguageProvider"
    )
  }

  return context
}
