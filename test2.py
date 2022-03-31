class MyTokenizer:
    def __init__(self,do_lower_case=False):
        # 把连号‘-’分开,空格也作为一个词
        self.sentences_tokenizer_en = self.get_sentences_tokenizer_en()
        self.words_tokenizer_en = self.get_word_tokenizer_en(do_lower_case=do_lower_case)

    @staticmethod
    def cut_paragraph_to_sentences_zh(para: str, drop_empty_line=True, strip=True, deduplicate=False):
        """
            中文切句
        Args:
           para: 输入段落文本
           drop_empty_line: 是否丢弃空行
           strip:  是否对每一句话做一次strip
           deduplicate: 是否对连续标点去重，帮助对连续标点结尾的句子分句

        Returns:
           sentences: list[str]
        """
        if deduplicate:
            para = re.sub(r"([。！？\!\?])\1+", r"\1", para)

        para = re.sub('([。！？\?!])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?!][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        sentences = para.split("\n")
        if strip:
            sentences = [sent.strip() for sent in sentences]
        if drop_empty_line:
            sentences = [sent for sent in sentences if len(sent.strip()) > 0]
        return sentences

    @staticmethod
    def get_sentences_tokenizer_en():
        """
            the tokenizer for cutting paragraph to sentences
        Returns:
            tokenizer
        """
        from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
        punkt_param = PunktParameters()
        abbreviation = ['et al.', 'i.e.', 'e.g.', 'etc.', 'i.e', 'e.g', 'etc', ' et al']
        punkt_param.abbrev_types = set(abbreviation)
        tokenizer = PunktSentenceTokenizer(punkt_param)
        return tokenizer

    @staticmethod
    def cut_sentence_to_words_zh(sentence: str):
        """
            cut_sentence_to_words_zh
        Args:
            sentence: a sentence ,str

        Returns:
            sentences: list[str]
        """
        english = 'abcdefghijklmnopqrstuvwxyz0123456789αγβδεζηθικλμνξοπρστυφχψω'
        output = []
        buffer = ''
        for s in sentence:
            if s in english or s in english.upper():  # 英文或数字
                buffer += s
            else:  # 中文
                if buffer:
                    output.append(buffer)
                buffer = ''
                output.append(s)
        if buffer:
            output.append(buffer)
        return output

    @staticmethod
    def get_word_tokenizer_en(do_lower_case=False):
        """
            the tokenizer for cutting sentence to words
        Returns:
            tokenizer
        """
        from transformers import BasicTokenizer
        return BasicTokenizer(do_lower_case=do_lower_case)
        # from nltk import WordPunctTokenizer
        # return WordPunctTokenizer()  # ').' 分不开，垃圾

    def cut_sentence_to_words(self, sentence: str,return_starts = False):
        # if TextProcessor.get_text_language(sentence):
        if langid.classify(sentence)[0] == 'zh': # 拉跨，langid分别不出lung --德文
            words = self.cut_sentence_to_words_zh(sentence)
        else:
            words =  self.words_tokenizer_en.tokenize(sentence)
        if return_starts:
            starts = []  # 每个word在句子中的位置
            i = 0
            for j in words:
                while i < len(sentence):
                    if sentence[i:i + len(j)] == j:
                        starts.append(i)
                        i += len(j)
                        break
                    else:
                        i += 1
            return words,starts
        return words

    def cut_paragraph_to_sentences(self, paragraph: str):
        if langid.classify(paragraph)[0] == 'zh':
            return self.cut_paragraph_to_sentences_zh(paragraph)
        else:
            return self.sentences_tokenizer_en.tokenize(paragraph)
