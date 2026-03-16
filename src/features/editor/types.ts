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
