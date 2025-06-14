# PROJECT.md

technical documentation links:
- nextjs: https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder
- pydantic: https://docs.pydantic.dev/latest/concepts/models
- drizzleorm: ???
- radix-ui: https://www.radix-ui.com/primitives/docs/components/form
- tailwindcss: https://tailwindcss.com/docs/flex-wrap
- markedjs: https://marked.js.org

this document is used for project task management and feature development

things to fix:
[x] user auth login does not persist when refresh or navigation to another admin view (fixed by using localhost:3000)
[x] make `/creator` route to upload 'text blocks' from admin client
[] create POC to create audio output from text block using 3rd party api service (11Labs, AssemblyAI)
[] learners can upload audio files and get back text in target language Chinese/English (OAI Whisper, 11Labs, AssemblyAI)

### Feat: Create POC to create audio output from text block using 3rd party api service (11Labs, AssemblyAI)

- the creator can input valid markdown into a simple, clean textbox. after submitting the markdown input, the system will generate a booklet with multiple textboxes from the markdown input. if the markdown is not valid, then there will be an error return from the backend system with some hints on how to fix the input.
- Q: why use markdown and not other formats?
    - A: markdown is a simple, easy to learn format that can be used for articles, books, and all kinds of content
    - A: MD is an open sourced standard that have many open sourced parsers
    - A: no need for rich text editor features that are complex to build and store, more people should learn MD
    - A: can be sent in emails
- Technical details of the Feat implemenation:
    - marked (https://github.com/markedjs/marked) can be used to processed MD in the backend
    - client text input should be sent to backend service `POST: /booklet`, validated, and stored raw markdown in DB, then background job will process raw markdown into TextBlocks with enriched data such as translations and pinyin.
        - create data models for `RawMarkdownText`, `Booklet`, `TextBlock`
        1. `POST: /booklet` api to store raw input
        2. `func processTextBlocksFromMarkdown()` background process creates TextBlocks and stores in DB, changes status for RawMarkdownText to `processed`


**Built by: Fuzhou Tairan Smart Learning (福州泰然智学有限公司), powered by Singapore ABQuest (AB寻求人工智能应用有限公司)**

Partners:
- **Xiamen 23Maoyi Network (厦门二十三网络科技有限公司)**
