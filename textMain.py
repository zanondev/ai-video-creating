from params import text
from services import textService, tempService

def main():
    initialText: str = text.get_initial_text()
    promptToSplit: str = textService.get_splited_text(initialText)
    splitedText: str = textService.split_prompt(promptToSplit)

    tempService.export_text(splitedText)

if __name__ == "__main__":
    main()