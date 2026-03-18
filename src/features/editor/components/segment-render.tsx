import type { Segment } from "../types"

export default function Segments({
  segments,
  refs,
  onMouseUp,
  showEdited = false,
}: {
  segments: Array<Segment>
  refs: React.RefObject<(HTMLSpanElement | null)[]>
  onMouseUp?: (index: number) => void
  showEdited?: boolean
}) {
  const editedSpanStyle = showEdited ? "" : "line-through"

  const handleMouseUp = (index: number) => onMouseUp?.(index)

  return (
    <p className="text-2xl font-medium">
      {segments.map((segment, index) =>
        segment["type"] === "text" ? (
          <span
            key={index}
            ref={(e) => {
              refs.current[index] = e
            }}
            onMouseUp={handleMouseUp.bind(null, index)}
            className={segment.selected ? "bg-red-400 text-white" : ""}
          >
            {segment["content"]}
          </span>
        ) : (
          <span
            key={index}
            className={`bg-blue-400 italic ${editedSpanStyle}`}
            ref={(e) => {
              refs.current[index] = e
            }}
            onMouseUp={handleMouseUp.bind(null, index)}
          >
            {showEdited ? segment["replacement"] : segment["content"]}
          </span>
        )
      )}
    </p>
  )
}
