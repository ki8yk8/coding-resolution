import type { SelectionInfo } from "./types"

export function getSelection(
  p: HTMLParagraphElement
): SelectionInfo | null {
  const selection = window.getSelection()

  // if there is not selection then out
  if (!selection || selection.rangeCount === 0 || selection.isCollapsed)
    return null

  // first selected range
  const range = selection.getRangeAt(0)

  // check if selection is inside and accept only if inside
  const isInside =
    p.contains(range.startContainer) && p.contains(range.endContainer)
  if (!isInside) return null

  const preRange = range.cloneRange()
  preRange.selectNodeContents(p)
  preRange.setEnd(range.startContainer, range.startOffset)

  const start = preRange.toString().length
  const end = start + range.toString().length

  const text = selection.toString()

  if (!text) return null

  const rect = range.getBoundingClientRect()

  // format of start and end = [start, end)
  return {
    range,
    selection,
    text,
    rect,
    start,
    end,
  }
}
