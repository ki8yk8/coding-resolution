import Editor from "./features/editor/editor"

export function App() {
  return (
    <div>
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

      <footer></footer>
    </div>
  )
}

export default App
