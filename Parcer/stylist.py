from googletrans import Translator
import openai

from config import API_KEY


class Stylist:
    translator = Translator()

    def minimizate_post(self, post):
        model_engine = "text-davinci-003"
        prompt = post + '\nI want you to write a short abstract of this article.'\
                        'Your answer should be divided into paragraphs, explain in plain language. Should be indented between paragraphs. Before each paragraph put a emoji '\
                        'which reflects the essence of the paragraph.'
        openai.api_key = API_KEY

        # задаем макс кол-во слов
        max_tokens = 130

        # генерируем ответ
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(completion.choices[0].text)
        return completion.choices[0].text

    def give_hashtags(self, post):
        model_engine = "text-davinci-003"
        prompt = post + '\ngive me to 5 hashtags for this news, understandable for crypto investors. Use names of cryptocurrences too.'
        openai.api_key = API_KEY

        # задаем макс кол-во слов
        max_tokens = 7

        # генерируем ответ
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print(completion.choices[0].text)
        #translator.translate(post_text, dest='ru').text
        return completion.choices[0].text

    def translate(self, post_text):
        return self.translator.translate(post_text, dest='ru').text

    def style(self, post):
        post_text= ''
        post[0] = self.translator.translate(post[0], dest='ru').text
        header = "🚨<b>" + post[0] + "</b>"
        link = post[-1]
        post.pop(-1)
        post.pop(0)
        for paragraph in post:
            paragraph += "\n\n"
            post_text+= paragraph
        post_text = self.translate(self.minimizate_post(post_text))
        tags = self.give_hashtags(post_text)
        awesome_post = header + '\n\n' + post_text + '\n' + link + '\n' + tags
        return awesome_post