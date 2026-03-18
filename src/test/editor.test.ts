import { describe, it, expect } from "vitest"
import type { Segment } from "@/features/editor/types"
import { cleanSegments, expandSelectionToWords } from "../features/editor/utils"

describe("Expand annotation span toward words", () => {
  const paragraph = "This is a dummy paragraph"

  it("should expand the span whenever the current span is in middle of words", () => {
    const [newStart, newEnd] = expandSelectionToWords(paragraph, 6, 11)
    const newParagraph = paragraph.slice(newStart, newEnd)

    expect(newParagraph).toBe("is a dummy")
  })

  it("should not expand whenever the current span encloses words exactly", () => {
    const [newStart, newEnd] = expandSelectionToWords(paragraph, 5, 15)
    const newParagraph = paragraph.slice(newStart, newEnd)

    expect(newParagraph).toBe("is a dummy")
  })

  it("should handle when all the spans are selected", () => {
    const [newStart, newEnd] = expandSelectionToWords(
      paragraph,
      0,
      paragraph.length
    )
    const newParagraph = paragraph.slice(newStart, newEnd)

    expect(newParagraph).toBe(paragraph)
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

describe("clean merging should work", () => {
  it("should be same if there are no consecutive segments with same type", () => {
    const segments: Array<Segment> = [
      { type: "text", content: "a" },
      { type: "edit", content: "b", replacement: "B" },
      { type: "text", content: "c" },
      { type: "edit", content: "d", replacement: "D" },
      { type: "text", content: "e" },
    ]

    expect(cleanSegments(segments)).toEqual(segments)
  })

  it("should merge if two contents have same type", () => {
    const segments: Array<Segment> = [
      { type: "text", content: "a" },
      { type: "edit", content: "b", replacement: "B" },
      { type: "edit", content: "d", replacement: "D" },
      { type: "text", content: "c" },
      { type: "text", content: "e" },
      { type: "edit", content: "d", replacement: "D" },
    ]

    expect(cleanSegments(segments)).toEqual([
      { type: "text", content: "a" },
      { type: "edit", content: "bd", replacement: "BD" },
      { type: "text", content: "ce" },
      { type: "edit", content: "d", replacement: "D" },
    ])
  })

  it("should handle edge cases", () => {
    const segments: Array<Segment> = [
      { type: "text", content: "a" },
      { type: "text", content: "b" },
      { type: "text", content: "c" },
      { type: "edit", content: "d", replacement: "D" },
      { type: "edit", content: "e", replacement: "E" },
    ]

    expect(cleanSegments(segments)).toEqual([
      { type: "text", content: "abc" },
      { type: "edit", content: "de", replacement: "DE" },
    ])
  })
})
