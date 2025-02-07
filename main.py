import os
from params import text
from services import textService, processService

def main():
    initialText: str = text.get_initial_text()
    promptToSplit: str = textService.get_splited_text(initialText)
    splitedText: list[str] = textService.split_prompt(promptToSplit)
    rootPath = os.path.dirname(os.path.abspath(__file__))
    processService.process_text(splitedText, initialText, rootPath)

if __name__ == "__main__":
    main()