import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Input } from '../components/ui/input'
import { Button } from '../components/ui/button'
import { Search } from 'lucide-react'


interface SearchPageProps {
  minimal?: boolean
}

export default function SearchPage({ minimal = false }: SearchPageProps) {
  const [search, setSearch] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (search.trim()) {
      navigate(`/fund/${search.toLowerCase()}`)
    }
  }

  if (minimal) {
    return (
      <form onSubmit={handleSearch} className="w-full max-w-2xl mx-auto">
        <div className="flex gap-2">
          <Input
            type="text"
            placeholder="Search by fund name or CIK..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="text-base py-2"
          />
          <Button type="submit" size="default">
            <Search className="h-4 w-4" />
          </Button>
        </div>
      </form>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <h1 className="text-4xl font-bold mb-8">13F Holdings Explorer</h1>
      <form onSubmit={handleSearch} className="w-full max-w-2xl">
        <div className="flex gap-2">
          <Input
            type="text"
            placeholder="Search by fund name or CIK..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="text-lg py-6"
          />
          <Button type="submit" size="lg">
            <Search className="mr-2" />
            Search
          </Button>
        </div>
      </form>
    </div>
  )
} 