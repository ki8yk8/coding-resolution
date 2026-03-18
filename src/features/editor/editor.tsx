import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useRef, useState } from "react"
import type { EditorProps, Segment } from "./types"
import { cleanSegments, expandSelectionToWords, getSelection } from "./utils"
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
  const textareaRef = useRef<HTMLTextAreaElement>(null)
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
    const { rect, start, end } = sel

    // change the selection to be bounded on words
    const [newStart, newEnd] = expandSelectionToWords(segments[index]["content"], start, end)
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

  function handlePopupCancel() {
    // turning off the selected segment
    const updatedSegments = segments.map((item) =>
      item.type === "text" && item.selected
        ? { ...item, selected: false }
        : item
    )

    // merging the consecutive segments
    setSegments(cleanSegments(updatedSegments))

    // removing the popup
    setPopup((prev) => ({ ...prev, display: false }))
  }

  function handlePopupSubmit() {
    const editedText = textareaRef.current?.value.trim()

    // if submitted empty then it is equivalent to cancel
    if (!editedText) {
      handlePopupCancel()
      return
    }

    setSegments((prev) => {
      const oldSegments = [...prev]
      // find the edited segment and add the replacement
      const editSegmentIndex = oldSegments.findIndex(
        (item) => item.type === "text" && item.selected
      )
      oldSegments[editSegmentIndex] = {
        type: "edit",
        content: segments[editSegmentIndex]["content"],
        replacement: editedText,
      }

      return oldSegments
    })

    // removing the popup
    setPopup((prev) => ({ ...prev, display: false }))
  }

	console.log(segments);

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
                ref={textareaRef}
              />
              <FieldDescription>
                Edits only the content you have selected. If you want to exapnd
                the correction you need to reselect.
              </FieldDescription>
            </Field>

            <div className="mt-2 flex justify-end gap-2">
              <Button variant="outline" onClick={handlePopupCancel}>
                Cancel
              </Button>
              <Button onClick={handlePopupSubmit}>Done</Button>
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
