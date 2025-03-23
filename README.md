# chatgpt-conversations-export

## Manage and save your exported ChatGPT conversations
When exporting all ChatGPT data. It generates a conversations.json file.

### Chat Viewer
Chat Viewer (and Chat Viewer ES in Spanish) is a simple way to display your exported JSON data and make it readable to print or export as PDF.
![chat-viewer](https://github.com/user-attachments/assets/45ee14fe-2ef2-4031-817e-89db28476bc6)
This excludes files, it is just for the text chat.

### Conversation Splitter
The conversations.json file can be too big. This is just a simple Python script (no modules required) to split that into multiple files:

Basic usage (`conversations.json` or any other file):

`python conversation_splitter.py conversations.json`

Defaults to splitting all conversations in .json files into an 'output' dir.

Options:

`python conversation_splitter.py conversations.json -o my_folder -m`

-o, --output-dir: Output directory (default: "output")

-m, --markdown: Export in markdown format

Example output file name: "2024-31-12 Title.json" (or md).
