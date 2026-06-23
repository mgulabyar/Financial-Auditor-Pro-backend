# import os
# from openai import AsyncOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# class AIService:
#     @staticmethod
#     async def get_audit_summary(stats_report, raw_data):
#         client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         system_prompt = (
#             "You are an Elite Financial Auditor. Analyze the findings and give a professional executive summary. "
#             "STRICT RULES: \n"
#             "1. Use CLEAR CAPITALIZED HEADINGS for each section.\n"
#             "2. DO NOT use any markdown symbols like asterisks (**) or hashes (#).\n"
#             "3. Use plain text only. Use simple dashes (-) for bullet points.\n"
#             "4. Keep the tone formal and executive."
#         )

#         user_prompt = f"Statistics: {stats_report}\nData Preview: {raw_data[:500]}"

#         try:
#             # --- MODEL NAME UPDATED HERE ---
#             response = await client.chat.completions.create(
#                 model="gpt-4o",  # gpt-4-turbo-preview ko badal kar gpt-4o kar diya
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt},
#                 ],
#             )

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AIService:
    @staticmethod
    async def get_audit_summary(stats_report, raw_data):
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        system_prompt = (
            "You are an Elite Financial Auditor. Analyze the findings and give a professional executive summary. "
            "STRICT RULES: \n"
            "1. Use CLEAR CAPITALIZED HEADINGS for each section.\n"
            "2. DO NOT use any markdown symbols like asterisks (**) or hashes (#).\n"
            "3. Use plain text only. Use simple dashes (-) for bullet points.\n"
            "4. Keep the tone formal and executive."
        )

        user_prompt = f"Statistics: {stats_report}\nData Preview: {raw_data[:500]}"

        try:
            # --- MODEL NAME UPDATED HERE ---
            response = await client.chat.completions.create(
                model="gpt-4o",  # gpt-4-turbo-preview ko badal kar gpt-4o kar diya
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            # Agar phir bhi fail ho toh error log karein
            print(f"Detailed Error: {str(e)}")
            return f"AI Summary generation failed: {str(e)}"