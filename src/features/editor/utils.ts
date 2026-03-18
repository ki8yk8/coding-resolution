import type { Segment, SelectionInfo } from "./types"

export function getSelection(p: HTMLSpanElement): SelectionInfo | null {
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

export function expandSelectionToWords(
  text: string,
  start: number,
  end: number
): [number, number] {
  // move from start to left for the start position
  for (let i = start - 1; i >= 0; i--) {
    if (text[i] === " ") {
      start = i + 1
      break
    }

    // handle edge case
    if (i === 0) {
      start = 0
    }
  }

  // move from end to right for the end position
  for (let i = end; i <= text.length; i++) {
    if (text[i] === " ") {
      end = i
      break
    }

    // handle the edge case
    if (i === text.length) {
      end = i
    }
  }

  return [start, end]
}

export function cleanSegments(segments: Array<Segment>):Array<Segment> {
	const cleanedSegments = [];

	// merging logic if the two consecutive elements have same type then merge them
	let [ptr_a, ptr_b] = [0, 1];
	while (ptr_b>ptr_a) {
		const [segment_a, segment_b] = [segments[ptr_a], segments[ptr_b]]
	}

}