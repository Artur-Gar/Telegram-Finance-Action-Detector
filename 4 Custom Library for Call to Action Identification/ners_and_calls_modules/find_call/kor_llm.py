from kor.extraction import create_extraction_chain
from kor import from_pydantic
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate

# Setting up structured extraction in Kor using a schema and few-shot learning
class Text(BaseModel):
    firm_NER: str = Field(default=None, description="Тикер компании")
    call_to_action: int = Field(default=None, description="Призыв к действию")

schema, validator = from_pydantic(
    Text,
    description="Призывы к покупке тикера",  
    examples=[  
        ("Пользователь: \
         Ценная бумага: 'Лукойл', \
         Тикер: 'LKOH', \
         Текст: 'Лукойл - переоценен! Эксперты прогнозируют снижение цены до 6000 руб. Рекомендуем вставать в шорт !'", 
         [{"firm_NER": "LKOH", "call_to_action": 1}]),

        ("Пользователь: \
         Ценная бумага: 'TCS Group Holding', \
         Тикер: 'TCGS', \
         Текст: 'Что думаете о перспективах TCS Group Holding?  Стоит ли покупать акции?'", 
         [{"firm_NER": "TCGS", "call_to_action": 0}]),

        ("Пользователь: \
         Ценная бумага: 'Астры', \
         Тикер: 'ASTR', \
         Текст: 'Фин результаты Астры в смотрятся намного лучше Росбанка, пора скупать.'",
         [{"firm_NER": "ASTR", "call_to_action": 1}]),

        ("Пользователь: \
         Ценная бумага: 'Росбанка', \
         Тикер: 'ROSB', \
         Текст: 'Фин результаты Астры в смотрятся намного лучше Росбанка, пора скупать.'",
         [{"firm_NER": "ROSB", "call_to_action": 0}]),
        
        ("Пользователь: \
         Ценная бумага: 'Аэрофлота', \
         Тикер: 'AFLT', \
         Текст: 'Будьте осторожны!  Акция 'Аэрофлота' может резко упасть. Проведите собственный анализ перед принятием решения.'",
         [{"firm_NER": "AFLT", "call_to_action": 0}]),

        ("Пользователь: \
         Ценная бумага: 'Северсталь', \
         Тикер: 'GMKN', \
         Текст: 'Северсталь расскрывает отчетность. Завтра утром - массированная продажа акций 'Норникеля'! В 9:00 все на борт!'",
         [{"firm_NER": "GMKN", "call_to_action": 1}]),

        ("Пользователь: \
         Ценная бумага: 'Норникеля', \
         Тикер: 'CHMF', \
         Текст: 'Северсталь расскрывает отчетность. Завтра утром - массированная продажа акций 'Норникеля'! В 9:00 все на борт!'",
         [{"firm_NER": "CHMF", "call_to_action": 0}]),

        ("Пользователь: \
         Ценная бумага: 'Роснефти', \
         Тикер: 'ROSN', \
         Текст: 'Не дадим врагам развалить российскую экономику!  Покупаем акции Роснефти, поддержим отечественную нефтянку!'",
         [{"firm_NER": "ROSN", "call_to_action": 1}]),

        ("Пользователь: \
         Ценная бумага: 'Газпром', \
         Тикер: 'GAZP', \
         Текст: 'Ребята, кто с нами забирает Газпром? 100к акций на 160 руб.'",
         [{"firm_NER": "GAZP", "call_to_action": 1}]),

        ("Пользователь: \
         Ценная бумага: 'русгидро', \
         Тикер: 'HYDR', \
         Текст: 'Народ, ставлю на команду русгидро в этом матче'",
         [{"firm_NER": "HYDR", "call_to_action": 0}]),

        ("Пользователь: \
         Ценная бумага: 'афк', \
         Тикер: 'AFKS', \
         Текст: 'Так и знал, что не надо было держать афк, ни дивов, ничего'",
         [{"firm_NER": "AFKS", "call_to_action": 0}]),

        ("Пользователь: \
         Ценная бумага: 'ВТБ', \
         Тикер: 'VTBR', \
         Текст: 'США разрешили операции с российскими банками для расчетов в сфере энергетики, включая ВТБ и Альфа-банк. Сбербанк остается под санкциями. Ну что, лонг первых?'", 
         [{"firm_NER": "VTBR", "call_to_action": 1}]),

        ("Пользователь: \
         Ценная бумага: 'Сбербанк', \
         Тикер: 'SBER', \
         Текст: 'США разрешили операции с российскими банками для расчетов в сфере энергетики, включая ВТБ и Альфа-банк. Сбербанк остается под санкциями. Ну что, лонг первых?'", 
         [{"firm_NER": "SBER", "call_to_action": 0}]),
    ],
    many=True,  # Returns a list of all company names mentioned in the text
)

# translated the default prompt for Kor into Russian
instruction_template = PromptTemplate(
    input_variables=["type_description", "format_instructions"], 
    template=(
        " Твоя задача - определить, есть ли призыв к скоординированной деятельности по покупке или продаже ценных бумаг компании в тексте. Текст, название ценной бумаги и ее тикер тебе отправляет пользователь."
        " Извлекай структурированную информацию из пользовательского ввода, которая"
        " соответствует форме, описанной ниже. При извлечении информации, пожалуйста, убедитесь, что"
        " точно соответствует информации о типе. Не добавляйте никаких атрибутов, которые "
        " не отображаются в схеме, показанной ниже.\n\n"
        "{type_description}\n\n"
        "{format_instructions}\n\n"
    ),
)

## Returns a DataFrame indicating the presence of calls to action
input_message = "Пользователь: Ценная бумага: '{NER}', Тикер: '{ticker}', Текст: '{text}"

## Confidence threshold for ticker selection
filter_value = 0.8

def call_determination(text, ner, ticker, llm) -> int:
    """
    The function uses an LLM to determine whether there is a call for collective action involving a security.
    
    It returns a number:
    1 – if a call to action is present,
    0 – if not.

    Args:
    text – the text to analyze
    ner – the named entity
    ticker – the corresponding ticker
    llm – the language model used for analysis
    """
    ## Define the prompt and chain for interacting with the LLM (initialized in the main script)
    chain = create_extraction_chain(llm, schema, validator=validator, instruction_template=instruction_template) 
    user_message = input_message.format(NER=ner, ticker=ticker, text=text)
    ## Structured request using Pydantic schema is sent to the LLM, and the response is parsed accordingly
    return chain.invoke(user_message)['validated_data'][0].call_to_action