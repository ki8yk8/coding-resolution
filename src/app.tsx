import Editor from "./features/editor/editor"

export function App() {
  return (
    <div className="flex h-screen flex-col gap-4">
      <main className="flex items-center justify-between gap-14 px-10 py-5">
        <div>
          <h1 className="text-2xl font-bold text-green-400">
            Hey, It's me KI8YK8
          </h1>
          <p className="mt-4 text-xl">
            This is my personal portfolio. In this portfolio I am trying to test
            my JS skill to see if I am able to design what I am thinking or not.
            This is interactive portfolio where you can interact with the
            paragraphs written on the sides and kind of editor pops up.
          </p>
        </div>
        <div className="max-w-1/2">
          <Editor />
        </div>
      </main>

      <div className="flex justify-center pt-9">
        <div className="relative w-2/3">
          <p className="absolute -top-4 left-4 text-8xl font-extrabold opacity-10">
            "
          </p>
          <p className="px-10 text-center text-4xl font-extralight">
            Once a wise man said, A quick brown fox quickly jumped over the lazy
            dog.
          </p>
        </div>
      </div>

      <footer className="flex grow items-end justify-center py-4">
        <p className="text-center text-sm">
          Made by KI8YK8. Thanks to resolution coding.
        </p>
      </footer>
    </div>
  )
}

export default App
