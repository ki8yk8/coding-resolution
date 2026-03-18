import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useRef, useState } from "react"
import type { EditorProps, Segment } from "./types"
import { expandSelectionToWords, getSelection } from "./utils"
import Segments from "./components/segment-render"
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
  const [segments, setSegments] = useState<Array<Segment>>([
    { type: "text", content: text, selected: false },
  ])
  const segmentRefs = useRef<(HTMLSpanElement | null)[]>([])
  const [popup, setPopup] = useState<{
    display: boolean
    position: [number, number]
  }>({
    display: false,
    position: [0, 0],
  })

  /* 
	1. onMouseUp see if there are multiple segment or single segment; if multiple then toast
	2. find out the selectionoffsets with the span
	3. extend the selection offset to word boundaries
	4. based on the segment position show the popover
	5. the popover disappers if and only if pressed done or cancelled else not
	6. create new segment array based on the condition
	*/
  function handleMouseUp(index: number) {
    // if the segment ref is not assigned or segment is already edited or if popup is already open
    if (
      !segmentRefs.current[index] ||
      segments[index].type === "edit" ||
      popup.display
    )
      return

    // get the selection info
    const sel = getSelection(segmentRefs.current[index])
    if (!sel) return
    const { range, selection, text: selectedText, rect, start, end } = sel

    // change the selection to be bounded on words
    const [newStart, newEnd] = expandSelectionToWords(text, start, end)
    // isolating the current segment
    const [preSegments, thisSegment, postSegments] = [
      segments.slice(0, index),
      segments[index],
      segments.slice(index + 1, segments.length),
    ]

    // isolating the selected part only
    const beforeSelectedSegment: Array<Segment> =
      newStart === 0
        ? []
        : [
            {
              type: "text" as const,
              content: thisSegment.content.slice(0, newStart),
            },
          ]
    const selectedSegment: Segment = {
      type: "text" as const,
      content: thisSegment.content.slice(newStart, newEnd),
      selected: true,
    }
    const afterSelectedSegment =
      newEnd === thisSegment.content.length
        ? []
        : [
            {
              type: "text" as const,
              content: thisSegment.content.slice(newEnd),
            },
          ]

    // joining all the segment
    const updatedSegment = [
      ...preSegments,
      ...beforeSelectedSegment,
      selectedSegment,
      ...afterSelectedSegment,
      ...postSegments,
    ]
    setSegments(updatedSegment)

    setPopup({
      display: true,
      position: [rect.left, rect.bottom + 2],
    })
  }

  return (
    <div>
      <Popover open={popup.display}>
        <PopoverTrigger asChild className="hidden">
          <span />
        </PopoverTrigger>
        <PopoverContent
          className="fixed"
          style={{ left: popup.position[0], top: popup.position[1] }}
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
          <Segments
            segments={segments}
            refs={segmentRefs}
            onMouseUp={handleMouseUp}
          />
        </CardContent>
      </Card>
    </div>
  )
}
