import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useRef, useState } from "react"
import type { EditorProps } from "./types"
import { expandSelectionToWords, getSelection } from "./utils"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

const HEADER_DESCRIPTION = "You can select the span of text to correct it."
// BUG: at the end of the text there will be always mutliple spaces. This is to have the selection to end because the issue with current one is if selected to end it will not display all the selected.
const INITIAL_TEXT =
  "Hey, I want to developer so, I am learning how to cook, and clean. This is something that you can edit this so feel free to make this thing better. And alternatively you can also screenshot this after editing and share with the team."

export default function Editor({ text = INITIAL_TEXT, onChange }: EditorProps) {
  const editorParagraphRef = useRef<HTMLParagraphElement>(null)
  const [popOpen, setPopOpen] = useState<boolean>(false)
  const [popPosition, setPopPosition] = useState<[number, number]>([0, 0])

  function handleMouseUp() {
    if (!editorParagraphRef.current) return

    const sel = getSelection(editorParagraphRef.current)
    if (!sel) return
    const { range, selection, text: selectedText, rect, start, end } = sel

    // change the selection to be bounded on words
    const [newStart, newEnd] = expandSelectionToWords(text, start, end)
    range.setStart(range.startContainer, newStart)
    range.setEnd(range.endContainer, newEnd)

    selection.removeAllRanges()
    selection.addRange(range)

    setPopOpen(true)
    setPopPosition([rect.left, rect.bottom + 2])
  }

  return (
    <div>
      <Popover open={popOpen}>
        <PopoverTrigger asChild className="hidden">
          <span />
        </PopoverTrigger>
        <PopoverContent
          className="fixed"
          style={{ left: popPosition[0], top: popPosition[1] }}
        >
          <div>
            <Field>
              <FieldLabel htmlFor="popover-edit-content">Correction</FieldLabel>
              <Textarea
                id="popover-edit-content"
                placeholder="Corrected Text"
              />
              <FieldDescription>
                Edits only the content you have selected. If you want to exapnd
                the correction you need to reselect.
              </FieldDescription>
            </Field>

            <div className="float-right">
              <Button>Done</Button>
            </div>
          </div>
        </PopoverContent>
      </Popover>

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
    </div>
  )
}
