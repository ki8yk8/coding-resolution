import { describe, it, expect } from "vitest"
import { expandSelectionToWords } from "./src/features/editor/utils.ts"

describe("Expand annotation span toward words", () => {
  const paragraph = "This is a dummy paragraph"

  it("should expand the span whenever the current span is in middle of words", () => {
    const [newStart, newEnd] = expandSelectionToWords(paragraph, 6, 11)
    const newParagraph = paragraph.slice(newStart, newEnd)

    expect(newParagraph).toBe("is a dummy")
  })

  it("should handle the edge cases whenever the current span is near boundary", () => {
    const [newStart, newEnd] = expandSelectionToWords(
      paragraph,
      2,
      paragraph.length - 4
    )
    const newParagraph = paragraph.slice(newStart, newEnd)

    expect(newParagraph).toBe(paragraph)
  })
})
