import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useRef } from "react"

interface EditorProps {
  text?: string
  onChange?: (text: string) => void
}

const HEADER_DESCRIPTION = "You can select the span of text to correct it."
// BUG: at the end of the text there will be always mutliple spaces. This is to have the selection to end because the issue with current one is if selected to end it will not display all the selected.
const INITIAL_TEXT =
  "Hey, I want to developer so, I am learning how to cook, and clean. This is something that you can edit this so feel free to make this thing better. And alternatively you can also screenshot this after editing and share with the team."

export default function Editor({ text = INITIAL_TEXT, onChange }: EditorProps) {
  const editorParagraphRef = useRef<HTMLParagraphElement>(null)

  function handleMouseUp() {
    const selection = window.getSelection()

    // if there is not selection then out
    if (!selection || selection.rangeCount === 0 || selection.isCollapsed)
      return null

    // first selected range
    const range = selection.getRangeAt(0)

    // editorParagraphRef should be used to see if the selection is inside the paragraph or not
    const p = editorParagraphRef.current
    if (!p) return

    // check if selection is inside and accept only if inside
    const isInside =
      p.contains(range.startContainer) && p.contains(range.endContainer)
    if (!isInside) return

    const preRange = range.cloneRange()
    preRange.selectNodeContents(p)
    preRange.setEnd(range.startContainer, range.startOffset)

    const start = preRange.toString().length
    const end = start + range.toString().length

    // trying to change the selection range and seeing if visually effects
    range.setStart(range.startContainer, start - 1)
    range.setEnd(range.endContainer, end + 1)

    selection.removeAllRanges()
    selection.addRange(range)

    const text = selection.toString()

    if (!text) return null

    const rect = range.getBoundingClientRect()

    const ret = {
      text,
      rect,
      start,
      end, // excluding
    }

    return ret
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>About me</CardTitle>
        <CardDescription>{HEADER_DESCRIPTION}</CardDescription>
      </CardHeader>

      <CardContent className="text-2xl font-medium">
        <p onMouseUp={handleMouseUp} ref={editorParagraphRef}>
          {text + "    "}
        </p>
      </CardContent>
    </Card>
  )
}
