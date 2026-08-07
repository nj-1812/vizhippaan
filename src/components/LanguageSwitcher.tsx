"use client"

import { Languages } from "lucide-react"

import { INDIAN_LANGUAGES } from "@/lib/languages"
import { useLanguage } from "@/context/LanguageContext"

export default function LanguageSwitcher() {
  const { language, changeLanguage } = useLanguage()

  return (
    <div className="relative flex items-center gap-2">
      <Languages className="h-4 w-4 text-slate-500" />

      <select
        value={language}
        onChange={(e) => changeLanguage(e.target.value)}
        className="
          h-9
          min-w-[145px]
          rounded-lg
          border
          border-slate-200
          bg-white
          px-3
          text-sm
          font-medium
          text-slate-700
          outline-none
          transition
          hover:border-slate-300
          focus:ring-2
          focus:ring-emerald-500/20
        "
      >
        {INDIAN_LANGUAGES.map((item) => (
          <option
            key={item.code}
            value={item.code}
          >
            {item.nativeName}
          </option>
        ))}
      </select>
    </div>
  )
}
