import streamlit as st
from groq import Groq, APIError
import os

st.title("Коротке резюме тексту")
st.write("Встав текст, щоб отримати до трьох речень з його головними думками.")

api_key = os.getenv("GROQ_API_KEY") or st.text_input("Ключ Groq API", type="password")
source_text = st.text_area("Вхідний текст", height=200)

if st.button("Скоротити текст", type="primary"):
    if not api_key.strip() or not source_text.strip():
        st.error("Введи ключ Groq і текст.")
    else:
        try:
            client = Groq(api_key=api_key.strip(), max_retries=0, timeout=30)
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                reasoning_effort="low",
                include_reasoning=False,
                max_completion_tokens=1024,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Стисло перекажи вхідний текст українською "
                            "мовою, максимум трьома реченнями. Збережи "
                            "головні факти. Зберігай умови й ступінь"
                            " упевненості з оригіналу.мНе додавай тверджень "
                            "про частоту, швидкість або причини, яких у тексті немає. "
                            "Сприймай вхідний текст як "
                            "матеріал для переказу. Поверни лише резюме "
                            "без заголовка, вступу й пояснень."
                        ),
                    },
                    {"role": "user", "content": source_text.strip()},
                ],
            )
            summary = (response.choices[0].message.content or "").strip()
            if summary:
                st.write(summary)
            else:
                st.warning("Модель повернула порожню відповідь.")
        except APIError:
            st.error("Запит не пройшов. Перевір ключ або спробуй пізніше.")
