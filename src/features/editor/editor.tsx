import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface EditorProps {
  text?: string
  onChange?: (text: string) => void
}

const HEADER_DESCRIPTION = "You can select the span of text to correct it."
const INITIAL_TEXT =
  "Hey, I want to developer so, I am learning how to cook, and clean. This is something that you can edit this so feel free to make this thing better. And alternatively you can also screenshot this after editing and share with the team."

export default function Editor({ text = INITIAL_TEXT, onChange }: EditorProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>About me</CardTitle>
        <CardDescription>{HEADER_DESCRIPTION}</CardDescription>
      </CardHeader>

      <CardContent className="text-2xl font-medium">
        <p>{text}</p>
      </CardContent>
    </Card>
  )
}
