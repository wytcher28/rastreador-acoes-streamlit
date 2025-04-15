# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 21:16:49 2025

@author: a840760
"""

# main.py - Aplicação de aprendizado com blockchain

import os
import speech_recognition as sr
import pyperclip
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration
from web3 import Web3
import json
import torch
from dotenv import load_dotenv

# === CARREGAR VARIÁVEIS DE AMBIENTE ===
load_dotenv()
INFURA_URL = os.getenv("https://mainnet.infura.io/v3/230be4e09dcf40cfa5dfe0e7f2e70011")
PRIVATE_KEY = os.getenv("a2288ffb94fbdde2ade66e13ec0b9d0df860419e6c3ee2b6653016cccc51e941")
CONTRACT_ADDRESS = os.getenv("6080604052348015600e575f80fd5b5061088b8061001c5f395ff3fe608060405234801561000f575f80fd5b506004361061004a575f3560e01c80631e15ac771461004e57806338138ede1461007e57806389b8a5521461009c578063fd869838146100cc575b5f80fd5b61006860048036038101906100639190610309565b6100e8565b60405161007591906103a4565b60405180910390f35b610086610193565b60405161009391906103d3565b60405180910390f35b6100b660048036038101906100b19190610309565b61019e565b6040516100c391906103a4565b60405180910390f35b6100e660048036038101906100e19190610518565b610243565b005b60605f82815481106100fd576100fc61055f565b5b905f5260205f20018054610110906105b9565b80601f016020809104026020016040519081016040528092919081815260200182805461013c906105b9565b80156101875780601f1061015e57610100808354040283529160200191610187565b820191905f5260205f20905b81548152906001019060200180831161016a57829003601f168201915b50505050509050919050565b5f8080549050905090565b5f81815481106101ac575f80fd5b905f5260205f20015f9150905080546101c4906105b9565b80601f01602080910402602001604051908101604052809291908181526020018280546101f0906105b9565b801561023b5780601f106102125761010080835404028352916020019161023b565b820191905f5260205f20905b81548152906001019060200180831161021e57829003601f168201915b505050505081565b5f81908060018154018082558091505060019003905f5260205f20015f9091909190915090816102739190610786565b503373ffffffffffffffffffffffffffffffffffffffff167f7e937b9c5d2947df3d5f9731a5d1b62d6aca66ec7e3b70bf36793e9daf0b7e08826040516102ba91906103a4565b60405180910390a250565b5f604051905090565b5f80fd5b5f80fd5b5f819050919050565b6102e8816102d6565b81146102f2575f80fd5b50565b5f81359050610303816102df565b92915050565b5f6020828403121561031e5761031d6102ce565b5b5f61032b848285016102f5565b91505092915050565b5f81519050919050565b5f82825260208201905092915050565b8281835e5f83830152505050565b5f601f19601f8301169050919050565b5f61037682610334565b610380818561033e565b935061039081856020860161034e565b6103998161035c565b840191505092915050565b5f6020820190508181035f8301526103bc818461036c565b905092915050565b6103cd816102d6565b82525050565b5f6020820190506103e65f8301846103c4565b92915050565b5f80fd5b5f80fd5b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b61042a8261035c565b810181811067ffffffffffffffff82111715610449576104486103f4565b5b80604052505050565b5f61045b6102c5565b90506104678282610421565b919050565b5f67ffffffffffffffff821115610486576104856103f4565b5b61048f8261035c565b9050602081019050919050565b828183375f83830152505050565b5f6104bc6104b78461046c565b610452565b9050828152602081018484840111156104d8576104d76103f0565b5b6104e384828561049c565b509392505050565b5f82601f8301126104ff576104fe6103ec565b5b813561050f8482602086016104aa565b91505092915050565b5f6020828403121561052d5761052c6102ce565b5b5f82013567ffffffffffffffff81111561054a576105496102d2565b5b610556848285016104eb565b91505092915050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52603260045260245ffd5b7f4e487b71000000000000000000000000000000000000000000000000000000005f52602260045260245ffd5b5f60028204905060018216806105d057607f821691505b6020821081036105e3576105e261058c565b5b50919050565b5f819050815f5260205f209050919050565b5f6020601f8301049050919050565b5f82821b905092915050565b5f600883026106457fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8261060a565b61064f868361060a565b95508019841693508086168417925050509392505050565b5f819050919050565b5f61068a610685610680846102d6565b610667565b6102d6565b9050919050565b5f819050919050565b6106a383610670565b6106b76106af82610691565b848454610616565b825550505050565b5f90565b6106cb6106bf565b6106d681848461069a565b505050565b5b818110156106f9576106ee5f826106c3565b6001810190506106dc565b5050565b601f82111561073e5761070f816105e9565b610718846105fb565b81016020851015610727578190505b61073b610733856105fb565b8301826106db565b50505b505050565b5f82821c905092915050565b5f61075e5f1984600802610743565b1980831691505092915050565b5f610776838361074f565b9150826002028217905092915050565b61078f82610334565b67ffffffffffffffff8111156107a8576107a76103f4565b5b6107b282546105b9565b6107bd8282856106fd565b5f60209050601f8311600181146107ee575f84156107dc578287015190505b6107e6858261076b565b86555061084d565b601f1984166107fc866105e9565b5f5b82811015610823578489015182556001820191506020850194506020810190506107fe565b86831015610840578489015161083c601f89168261074f565b8355505b6001600288020188555050505b50505050505056fea26469706673582212205648ec177479a6211b8ac916a852aae5d22baa7ebcac7da456cc7d6793daf52d64736f6c634300081a0033")

# === EXEMPLO DE ABI DO CONTRATO (atualize com o real) ===
CONTRACT_ABI = '0x642c4bd0c4fef7276a018261b4941f84a35861709e211f7006e0c608f17383bd'[
  {
    "inputs": [
      {"internalType": "string", "name": "content", "type": "string"}
    ],
    "name": "storeLearning",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalLearnings",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
    "name": "getLearning",
    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
    "stateMutability": "view",
    "type": "function"
  }
]

# === CONEXÃO COM BLOCKCHAIN ===
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    raise Exception("Falha ao conectar na blockchain")

account_address = web3.eth.account.from_key(PRIVATE_KEY).address
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# === MODELOS DE IA ===
engine_blip = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
processor_blip = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

# === FUNÇÕES DE ANÁLISE ===
def ouvir_reuniao():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        audio = recognizer.listen(source)
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print("Transcrição:", texto)
        return texto
    except:
        print("Não entendi.")
        return ""

def ler_clipboard():
    texto = pyperclip.paste()
    print("Clipboard:", texto)
    return texto

def ocr_em_imagem(caminho):
    img = Image.open(caminho)
    texto = pytesseract.image_to_string(img, lang='por')
    print("OCR:", texto)
    return texto

def descrever_imagem(caminho):
    image = Image.open(caminho).convert('RGB')
    inputs = processor_blip(images=image, return_tensors="pt")
    out = engine_blip.generate(**inputs)
    descricao = processor_blip.decode(out[0], skip_special_tokens=True)
    print("Descrição:", descricao)
    return descricao

def registrar_na_blockchain(texto):
    nonce = web3.eth.get_transaction_count(account_address)
    tx = contract.functions.storeLearning(texto).build_transaction({
        'chainId': 11155111,  # Sepolia
        'gas': 200000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Registrado na blockchain! Hash: {tx_hash.hex()}")

# === INTERFACE DE TERMINAL ===
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1 - Ouvir Reunião")
        print("2 - Ler Texto do Clipboard")
        print("3 - OCR de Imagem")
        print("4 - Descrever Imagem")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            conteudo = ouvir_reuniao()
        elif opcao == "2":
            conteudo = ler_clipboard()
        elif opcao == "3":
            caminho = input("Caminho da imagem: ")
            conteudo = ocr_em_imagem(caminho)
        elif opcao == "4":
            caminho = input("Caminho da imagem: ")
            conteudo = descrever_imagem(caminho)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            continue

        if conteudo:
            registrar_na_blockchain(conteudo)
