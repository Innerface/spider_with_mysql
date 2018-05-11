from aip import AipNlp

APP_ID = "10595165"
API_KEY = "BiYK5tGajcbqwtT531XXcLwH"
SECRET_KEY = "2mXX5eiinHKHILBuE4FEAe9VstaDCRD6"
client = AipNlp(APP_ID,API_KEY,SECRET_KEY)

#词法分析
text = "百度是一家高科技公司"
lexer_ = client.lexer(text)
print(lexer_)

#词义相似度
word1 = "上海"
word2 = "北京"
wordSim_ = client.wordSimEmbedding(word1, word2)
print(wordSim_)