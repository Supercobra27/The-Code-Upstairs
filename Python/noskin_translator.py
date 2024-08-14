encoded_alphabet = "!#$%&@()*+`-/0123456789<=>"
decoded_alphabet = "abcdefghijklmnopqrstuvwxyz"

def create_dict(encoded_alphabet, decoded_alphabet):
    code_dict = dict()
    for i, char in enumerate(encoded_alphabet):
        code_dict[char] = decoded_alphabet[i]
    return code_dict


def decode(coded_text, encoded_alphabet=encoded_alphabet, decoded_alphabet=decoded_alphabet):
    decode_dict = create_dict(encoded_alphabet, decoded_alphabet)
    for (key, value) in decode_dict.items():
        coded_text = coded_text.replace(key, value)
    return coded_text

def encode(text, encoded_alphabet=encoded_alphabet, decoded_alphabet=decoded_alphabet):
    encode_dict = create_dict(encoded_alphabet, decoded_alphabet)
    for (key, value) in encode_dict.items():
        text = text.replace(value, key)
    return text

coded_text = [")&4& =17 !4& !6 -!56", 
              "-*66-& 5*56&4", 
              "!4& =17 56*-- $108*0$&% =17 !4& /&", 
              "57$) ! @!*-74& %1&506 %&5&48& 61 -*8&",
              "%*&",
              "=174& +756 ! 2*6*@7- $12=",
              "*/ 6)& 14*(*0!-"
              ]
for code in coded_text:
    print(decode(code))

encode_txt = "hehe stinky"
print(encode(encode_txt))
