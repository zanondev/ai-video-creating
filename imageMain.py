from services import openaiService, tempService

INITIAL_TEXT =  "Crie uma imagem sobre a seguinte descrição: "
SPLITED_TEXT = '"Em uma noite de lua cheia, encontrou uma porta misteriosa no sótão de uma casa abandonada.."'
DETAIL_TEXT = 'Faça a imagem em um tom escuro, de terror, um tanto quanto realista, que traga estranheza. Certifique-se que a imagem nunca possuirá textos ou números escritos.'

def main():
    imageText = INITIAL_TEXT + SPLITED_TEXT + ' ' + DETAIL_TEXT
    imageUrl = openaiService.generate_image(imageText)
    tempService.export_image_url(imageUrl)

if __name__ == "__main__":
    main()