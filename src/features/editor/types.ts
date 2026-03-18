export interface EditorProps {
  text?: string
  onChange?: (text: string) => void
}

export interface SelectionInfo {
  range: Range
  selection: Selection
  text: string
  start: number
  end: number
  rect: DOMRect
}

export type Segment =
  | { type: "text"; content: string; selected?: boolean }
  | { type: "edit"; content: string; replacement: string }
