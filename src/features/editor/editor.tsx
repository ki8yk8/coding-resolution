import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useRef } from "react"
import type { EditorProps } from "./types"
import { getSelection } from "./utils"

const HEADER_DESCRIPTION = "You can select the span of text to correct it."
// BUG: at the end of the text there will be always mutliple spaces. This is to have the selection to end because the issue with current one is if selected to end it will not display all the selected.
const INITIAL_TEXT =
  "Hey, I want to developer so, I am learning how to cook, and clean. This is something that you can edit this so feel free to make this thing better. And alternatively you can also screenshot this after editing and share with the team."

export default function Editor({ text = INITIAL_TEXT, onChange }: EditorProps) {
  const editorParagraphRef = useRef<HTMLParagraphElement>(null)

  function handleMouseUp() {
		if (!editorParagraphRef.current) return;

    const sel = getSelection(editorParagraphRef.current);
		if (!sel) return;
		const {range, selection, text, rect, start, end} = sel

    // trying to change the selection range and seeing if visually effects
    range.setStart(range.startContainer, start - 1)
    range.setEnd(range.endContainer, end + 1)

    selection.removeAllRanges()
    selection.addRange(range)
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
