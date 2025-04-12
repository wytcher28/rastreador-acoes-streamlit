# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 14:21:30 2025

@author: a840760
"""
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Defina suas credenciais da API do Twitter
consumer_key = 'kBAUkSg2ZfrkW8Jh6taHFzlsY'
consumer_secret = 'pEU75fknXAaHyVM3DMEZqx2TnPDJVyQxj4CoXdAENTXPdso5Ct'
access_token = '118052766-h7R84w25G0nTJPs1xVu4zHBnQJlqbP9ICJFL9JAD'
access_token_secret = 'iPs5i6cAi3SLkVLeO5AiSvEccCwLCIdnjC8MvHUkcfq6u'

# Autenticação na API do Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Inicialização do analisador de sentimentos
analisador_sentimentos = SentimentIntensityAnalyzer()

# Função para buscar tweets por hashtag, calcular métricas de engajamento e análise de sentimento
def analisar_hashtag(hashtag, count=100):
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=f"#{hashtag}", tweet_mode='extended', lang='pt').items(count)
        
        total_curtidas = 0
        total_retweets = 0
        total_seguidores = 0
        total_respostas = 0
        total_cliques_links = 0
        total_tweets = 0
        total_sentimento_positivo = 0
        total_sentimento_neutro = 0
        total_sentimento_negativo = 0
        
        for tweet in tweets:
            total_tweets += 1
            total_curtidas += tweet.favorite_count
            total_retweets += tweet.retweet_count
            total_seguidores += tweet.user.followers_count
            total_respostas += tweet.reply_count
            total_cliques_links += len(tweet.entities.get('urls', []))

            # Realizar análise de sentimento no texto do tweet
            texto_tweet = tweet.full_text
            sentimentos = analisador_sentimentos.polarity_scores(texto_tweet)

            # Classificar o sentimento do tweet
            if sentimentos['compound'] >= 0.05:
                total_sentimento_positivo += 1
            elif sentimentos['compound'] <= -0.05:
                total_sentimento_negativo += 1
            else:
                total_sentimento_neutro += 1

        # Calcular métricas médias se houver tweets analisados
        if total_tweets > 0:
            media_curtidas = total_curtidas / total_tweets
            media_retweets = total_retweets / total_tweets
            media_seguidores = total_seguidores / total_tweets
            media_respostas = total_respostas / total_tweets
            media_cliques_links = total_cliques_links / total_tweets
            percentual_positivo = (total_sentimento_positivo / total_tweets) * 100
            percentual_neutro = (total_sentimento_neutro / total_tweets) * 100
            percentual_negativo = (total_sentimento_negativo / total_tweets) * 100
        else:
            media_curtidas = media_retweets = media_seguidores = media_respostas = media_cliques_links = 0
            percentual_positivo = percentual_neutro = percentual_negativo = 0

        return {
            'total_tweets': total_tweets,
            'media_curtidas': media_curtidas,
            'media_retweets': media_retweets,
            'media_seguidores': media_seguidores,
            'media_respostas': media_respostas,
            'media_cliques_links': media_cliques_links,
            'percentual_positivo': percentual_positivo,
            'percentual_neutro': percentual_neutro,
            'percentual_negativo': percentual_negativo
        }
    
    except tweepy.TweepyException as e:
        print(f"Erro ao buscar tweets: {e}")
        return None

# Exemplo de uso
hashtag = input("Digite a hashtag que deseja analisar: ")
resultados = analisar_hashtag(hashtag)

if resultados:
    print(f"Análise da hashtag #{hashtag}:")
    print(f"Total de tweets analisados: {resultados['total_tweets']}")
    print(f"Média de curtidas por tweet: {resultados['media_curtidas']:.2f}")
    print(f"Média de retweets por tweet: {resultados['media_retweets']:.2f}")
    print(f"Média de seguidores dos autores: {resultados['media_seguidores']:.2f}")
    print(f"Média de respostas por tweet: {resultados['media_respostas']:.2f}")
    print(f"Média de cliques em links por tweet: {resultados['media_cliques_links']:.2f}")
    print(f"Percentual de tweets positivos: {resultados['percentual_positivo']:.2f}%")
    print(f"Percentual de tweets neutros: {resultados['percentual_neutro']:.2f}%")
    print(f"Percentual de tweets negativos: {resultados['percentual_negativo']:.2f}%")